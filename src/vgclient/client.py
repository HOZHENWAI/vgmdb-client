from typing import Union, Dict

import requests



class VGMdbClient:
    DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0"
    BASE_URL = "https://vgmdb.net"
    SEARCH_URL = BASE_URL+"/search?do=results"

    def __init__(self):
        self.session = requests.Session()

    def login(self):
        """"""

    def get_page(self, url: str) -> Dict:
        """"""

    def get_album(self, album_id: Union[int, str]) -> Dict:
        """"""

    def get_artist(self, artist_id: Union[int, str]) -> Dict:
        """"""

    def get_labels(self, labels_id: Union[int, str]) -> Dict:
        """"""

    def get_products(self, p):
        """"""

    def get_events(self):
        """"""

    def simple_search(self):
        """"""

    # ADVANCED FEATURES
    def advanced_search(self):
        """"""

