"""Stadium Finder."""


import requests
from bs4 import BeautifulSoup


def get_stadium_coordinates(stadium_name):
    """Return the coordinates of a stadium.

    Parameters
    ----------
    name : string
        Name of stadium (must match Wikipedia)

    Returns
    -------
    latitude, longitude : float, float
        Latitude and longitude in decimal degrees.

    Examples
    --------
    >>> get_stadium_coordinates("CenturyLink Field")
    (47.5952, -122.3316)
    """
    WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/"
    stadium_name = stadium_name.replace(" ", "_")

    r = requests.get(WIKIPEDIA_URL + stadium_name)
    stadium_soup = BeautifulSoup(r.content, "lxml")
    location_html = stadium_soup.select_one("span.geo-dec")
    location = location_html.get_text().encode('ascii', 'ignore')
    latitude, longitude = location.split()

    # North and east are positive, south and west are negative
    sign_dict = {'N': 1, 'E': 1, 'S': -1, 'W': -1}

    def decimalize(l):
        """Convert text lat or long to decimal."""
        return float(l[:-1]) * sign_dict[l[-1]]
    latitude = decimalize(latitude)
    longitude = decimalize(longitude)

    return (latitude, longitude)
