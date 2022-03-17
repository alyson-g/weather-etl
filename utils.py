"""
A collection of utility functions
"""


def build_api_url(latitude: str, longitude: str) -> str:
    """
    Build a URL to send to the API
    :param latitude: A string representing the latitude
    :param longitude: A string representing the longitude
    :return: A formatted URL string
    """
    url = "https://api.open-meteo.com/v1/forecast?"
    url += f"latitude={latitude}"
    url += f"&longitude={longitude}"
    url += "&hourly="

    # These are the parameters pulled from the API
    params = [
        "temperature_2m", "relativehumidity_2m", "dewpoint_2m",
        "pressure_msl", "cloudcover", "precipitation",
        "weathercode"
    ]

    url += ",".join(params)

    return url
