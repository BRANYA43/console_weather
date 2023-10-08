import json
from dataclasses import dataclass
from json import JSONDecodeError
from subprocess import Popen, PIPE

import config
from exceptions import CantGetCoordinates


@dataclass(slots=True, frozen=True)
class Coordinates:
    latitude: float
    longitude: float


def get_gps_coordinates() -> Coordinates:
    coordinates = _get_ipinfo_coordinate()
    return _round_coordinates(coordinates)


def _get_ipinfo_coordinate() -> Coordinates:
    response = _get_ipinfo_response()
    response = _decode_ipinfo_response_to_dict(response)
    return _parse_ipinfo_response(response)


def _parse_ipinfo_response(response: dict) -> Coordinates:
    try:
        latitude, longitude = map(_convert_str_to_float, response['loc'].split(','))
        return Coordinates(latitude=latitude, longitude=longitude)
    except KeyError:
        raise CantGetCoordinates


def _convert_str_to_float(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise CantGetCoordinates


def _round_coordinates(coordinates: Coordinates) -> Coordinates:
    if not config.USE_ROUNDED_COORDS:
        return coordinates
    return Coordinates(*map(lambda c: round(c, 1), [coordinates.latitude, coordinates.longitude]))


def _get_ipinfo_response() -> bytes:
    process = Popen(['curl', 'ipinfo.io'], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if err is not None or exit_code != 0:
        raise CantGetCoordinates
    return output


def _decode_ipinfo_response_to_dict(response: bytes) -> dict:
    try:
        return json.loads(response)
    except JSONDecodeError:
        raise CantGetCoordinates


if __name__ == '__main__':
    print(get_gps_coordinates())
