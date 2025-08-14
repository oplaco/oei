from skyfield.api import EarthSatellite
from skyfield.api import wgs84
from skyfield.api import load


def parse_tle_block(name: str, line1: str, line2: str) -> dict:
    """Parses a TLE block into a skyfield.api.EarthSatellite object"""
    satellite = EarthSatellite(line1, line2, name)
    sat_id = int(line1[2:7])
    epoch = satellite.epoch.utc_datetime()

    return {
        "name": name.strip(),
        "line1": line1.strip(),
        "line2": line2.strip(),
        "epoch_utc": epoch,
        "satnum": sat_id,
        "intl_desg": line1[9:17].strip(),
        "inclination_deg": float(satellite.model.inclo),
        "raan_deg": float(satellite.model.nodeo),
        "eccentricity": float(satellite.model.ecco),
        "arg_perigee_deg": float(satellite.model.argpo),
        "mean_anomaly_deg": float(satellite.model.mo),
        "mean_motion_rev_per_day": float(satellite.model.no_kozai),
        "bstar": float(satellite.model.bstar),
        "rev_number": int(line2[63:68].strip()),
    }


def validate_tle_checksum(tle_line: str) -> bool:
    if len(tle_line) < 69:
        return False
    checksum_char = tle_line[68]
    try:
        expected = int(checksum_char)
    except ValueError:
        return False

    total = 0
    for ch in tle_line[:68]:
        if ch.isdigit():
            total += int(ch)
        elif ch == "-":
            total += 1
    return total % 10 == expected
