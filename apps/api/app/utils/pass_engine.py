import numpy as np
from datetime import datetime, timedelta, timezone

from shapely.geometry import LineString, mapping, shape
from skyfield.api import EarthSatellite, load, wgs84

from app.schemas.orbital_pass import PassComputeResult


def create_satellite_from_tle(tle) -> EarthSatellite:
    return EarthSatellite(tle.line1, tle.line2, tle.name or "SAT", load.timescale())


def get_observer_from_aoi_geometry(aoi_geometry) -> tuple:
    """Returns AOI centroid as (lat, lon) and Skyfield Topos"""
    geojson = shape(aoi_geometry)
    centroid = geojson.centroid
    lat, lon = centroid.y, centroid.x
    topos = wgs84.latlon(latitude_degrees=lat, longitude_degrees=lon)
    return (lat, lon), topos


def generate_times(start: datetime, end: datetime, step_seconds: int = 10):
    ts = load.timescale()
    num_steps = int((end - start).total_seconds() / step_seconds) + 1
    return ts.utc(
        [start + timedelta(seconds=i * step_seconds) for i in range(num_steps)]
    )


def compute_elevation_series(sat: EarthSatellite, topos, times):
    difference = sat - topos
    topocentric = difference.at(times)
    altitudes = topocentric.altaz()[0].degrees  # shape: [N]
    return altitudes


def find_pass_windows(times, elevations, threshold_deg=10.0):
    """Returns list of (start_idx, end_idx) for intervals above threshold"""
    above = elevations >= threshold_deg
    intervals = []
    start = None
    for i, is_above in enumerate(above):
        if is_above and start is None:
            start = i
        elif not is_above and start is not None:
            if i > start + 1:  # must be >1 point long
                intervals.append((start, i - 1))
            start = None
    # catch last
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
    subpoint_objs = sat.at(times).subpoint()
    subpoints = list(
        zip(subpoint_objs.latitude.degrees, subpoint_objs.longitude.degrees)
    )  # [(lat, lon)]

    intervals = find_pass_windows(times, elevations, threshold_deg=min_elevation_deg)

    passes = [
        extract_pass_data(times, subpoints, elevations, interval)
        for interval in intervals
    ]
    return passes
