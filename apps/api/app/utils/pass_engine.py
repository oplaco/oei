import numpy as np
from datetime import datetime, timedelta, timezone

from shapely.geometry import LineString, mapping, shape
from skyfield.api import EarthSatellite, load, wgs84

from app.schemas.orbital_pass import PassComputeResult


def create_satellite_from_tle(tle) -> EarthSatellite:
    return EarthSatellite(tle.line1, tle.line2, tle.name or "SAT", load.timescale())


def get_observer_from_aoi_geometry(aoi_geometry) -> tuple:
    """
    Converts AOI geometry to Skyfield observer at its centroid.

    Note:
        Uses only the centroid of the AOI as the observation point as simplification.
    """
    geojson = shape(aoi_geometry)
    centroid = geojson.centroid
    lat, lon = centroid.y, centroid.x
    topos = wgs84.latlon(
        latitude_degrees=lat, longitude_degrees=lon
    )  # short for Topocentric observer in Skyfield
    return (lat, lon), topos


def generate_times(start: datetime, end: datetime, step_seconds: int = 10):
    """
    Generates a Skyfield Time array with uniform time steps between start and end.

    Args:
        start (datetime): UTC start time.
        end (datetime): UTC end time.
        step_seconds (int): Time step in seconds between samples.

    Returns:
        skyfield.timelib.Time: Skyfield Time array covering the interval [start, end].
    """
    ts = load.timescale()
    num_steps = int((end - start).total_seconds() / step_seconds) + 1
    return ts.utc(
        [start + timedelta(seconds=i * step_seconds) for i in range(num_steps)]
    )


def compute_elevation_series(sat: EarthSatellite, topos, times):
    """
    Computes the elevation angle of the satellite as seen from a fixed observer location
    over a sequence of times.

    Args:
        sat (EarthSatellite): Skyfield satellite object.
        topos: Skyfield observer location (e.g., AOI centroid as a wgs84.latlon).
        times: Skyfield Time array for sampling.

    Returns:
        np.ndarray: Array of elevation angles (in degrees) for each time step.
    """
    difference = sat - topos  # get satellite relative to AOI
    topocentric = difference.at(
        times
    )  # vector from AOI to satellite over time. Check https://rhodesmill.org/skyfield/api-vectors.html#skyfield.vectorlib.VectorFunction
    altitudes = topocentric.altaz()[0].degrees  # altaz() returns (alt, az, distance)
    return altitudes  # array of elevation angles


def find_pass_windows(elevations: np.ndarray, threshold_deg: float = 10.0):
    """
    Detects visibility intervals based on elevation threshold.

    Args:
        elevations (np.ndarray): Array of elevation angles (degrees) over time.
        threshold_deg (float): Minimum elevation (deg) to consider a valid pass.

    Returns:
        list[tuple[int, int]]: List of index ranges (start_idx, end_idx) where
        elevation stays above the threshold for at least two consecutive points.
    """
    above = elevations >= threshold_deg
    intervals = []
    start = None

    for i, is_above in enumerate(above):
        if is_above and start is None:
            start = i
        elif not is_above and start is not None:
            if i > start + 1:  # at least 2 points long
                intervals.append((start, i - 1))
            start = None

    # Handle case where the last point is still "above"
    if start is not None and len(above) > start + 1:
        intervals.append((start, len(above) - 1))

    return intervals


def extract_pass_data(times, subpoints, elevations, interval) -> PassComputeResult:
    start_idx, end_idx = interval
    start_time = times[start_idx].utc_datetime().replace(tzinfo=timezone.utc)
    end_time = times[end_idx].utc_datetime().replace(tzinfo=timezone.utc)

    max_idx = np.argmax(elevations[start_idx : end_idx + 1]) + start_idx
    max_elevation = elevations[max_idx]
    max_time = times[max_idx].utc_datetime().replace(tzinfo=timezone.utc)

    track = [
        (subpoints[i][1], subpoints[i][0])  # (lon, lat)
        for i in range(start_idx, end_idx + 1)
    ]
    track_geojson = mapping(LineString(track))

    return PassComputeResult(
        start_time=start_time,
        end_time=end_time,
        max_elevation_deg=max_elevation,
        max_elevation_time=max_time,
        track_geojson=track_geojson,
    )


def compute_passes_over_aoi(tle, aoi_geometry, window, min_elevation_deg=10.0):
    sat = create_satellite_from_tle(tle)
    (lat, lon), topos = get_observer_from_aoi_geometry(aoi_geometry)
    times = generate_times(window.start, window.end)

    # compute elevations and sub-satellite points
    elevations = compute_elevation_series(sat, topos, times)
    subpoint_objs = sat.at(
        times
    ).subpoint()  # Get the sub-satellite points or ground track
    subpoints = list(
        zip(subpoint_objs.latitude.degrees, subpoint_objs.longitude.degrees)
    )  # Turn into simple list of float tuples [(lat, lon)]

    intervals = find_pass_windows(
        elevations, threshold_deg=min_elevation_deg
    )  # Detect intervals where the elevation is greater than the threshold

    passes = [
        extract_pass_data(times, subpoints, elevations, interval)
        for interval in intervals
    ]  # Create a list of PassComputeResult objects
    return passes
