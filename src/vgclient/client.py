from typing import Union, Dict, List
import requests

from bs4 import BeautifulSoup
from langdetect import detect


from .types import VGMAlbumInfo, ReleaseInfo, AlbumTitles
from .mapping import VGMTOCLIENT

class VGMdbPageParserWithFixMixin:
    def advanced_parse_album_title(self, title_content_list: List[BeautifulSoup]) -> AlbumTitles:
        """
        Need to include other names
        :param title_content_list:
        :return:
        """
        display = None
        original = None
        temp_dict = {}
        for result in title_content_list:
            vgm_lang = result["lang"]
            vgm_text = result.contents[1]
            if vgm_lang in VGMTOCLIENT:
                temp_dict.update({VGMTOCLIENT[vgm_lang]: vgm_text})
            display = display or vgm_text
            if (display!=vgm_text) and (display==original):
                original = vgm_text
            else:
                original = original or display

        # VERIFY LANGUAGE (since title language is not clean)
        if detect(temp_dict["english"]) != "en":
            del temp_dict["english"]
        if detect(temp_dict["japanese"]) != "ja":
            del temp_dict["japanese"]

        return AlbumTitles(
            display=display,
            original=original,
            **temp_dict
        )

    def parse_release_info_from_soup(self, soup: BeautifulSoup) -> ReleaseInfo:
        """
        Notes:
        There are issues that have to solved:
        - the displayed title is always assumed to be english, which is not always true
        - if there are missing language version of the title, then they are filled using the display title
        :param soup:
        :return:
        """
        # Release info is found under the innermain div
        innermain = soup.find("div", {"id": "innermain"})
        first_header = innermain.findNext("h1")
        album_titles_soup = first_header.findAll("span", {"class": "albumtitle"})
        album_title = self.advanced_parse_album_title(album_titles_soup)

        return ReleaseInfo(

        )


class VGMdbClient(VGMdbPageParserWithFixMixin):
    DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0"
    BASE_URL = "https://vgmdb.net"
    ALBUM_URL = BASE_URL+"/album/"
    SEARCH_URL = BASE_URL+"/search?do=results"

    def __init__(self):
        self.session = requests.Session()

    def login(self):
        """"""

    def get_page(self, url: str) -> Dict:
        """"""

    def get_album(self, album_id: Union[int, str]) -> VGMAlbumInfo:
        """"""
        response = self.session.get(self.ALBUM_URL+str(album_id))
        album_soup = BeautifulSoup(response.text, "lxml")
        release = self.parse_release_info_from_soup(album_soup)

        return VGMAlbumInfo(
            album_id,

        )

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

class AsyncVGMdbClient(VGMdbPageParserWithFixMixin):
    DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0"
    BASE_URL = "https://vgmdb.net"
    SEARCH_URL = BASE_URL+"/search?do=results"

    def __init__(self):
        pass

    async def login(self):
        """"""

    async def get_page(self, url: str) -> Dict:
        pass

    async def get_album(self, album_id: Union[int, str]) -> Dict:
        """"""

    async def get_artist(self, artist_id: Union[int, str]) -> Dict:
        """"""

    async def get_labels(self, labels_id: Union[int, str]) -> Dict:
        pass

    async def get_products(self, p):
        pass

    async def get_events(self):
        pass

    async def simple_search(self):
        pass

    async def advanced_search(self):
        pass
