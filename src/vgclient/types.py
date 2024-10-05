from enum import StrEnum
from typing import TypedDict, NamedTuple, Optional, List, Union, Dict, Tuple


class AlbumTitles(TypedDict, total=False):
    """
    From vgmdb:
    There is support for multiple titles, separated by carriage returns (Enter key). Only the first line is absolutely required.
    line 1: Display Name
    This is the name that will appear as the title when the album is displayed.
    Generally, the name for an album comes from the title on the Front or the Spine.
    If a game does not have an official English language release, don't submit a literal or fan translation of the game's name. Other common terms in the album title should be translated (e.g. 音楽集 -> Music Collection). See this thread for a list of these terms and the respective translation.
    Never abbreviate to OST (unless the title really does include it, but this is rare).
    All monospace characters should be mapped to the Latin charset equivalent, thus ～ＪＡＳＣＩＩ should be ~JASCII. Decorative symbols like ☆ are still permitted.
    line 2: Original
    Use this when the official name differs from the display name.
    For Eastern releases, this will often require Unicode characters.
    line 3: Romanized
    Direct romanization of the original title. Note, don't include this if it's essentially the same as the Display title.
    In particular, please do not literally transcribe loan words (i.e., no Orijinaru Saundotorakku)
    line 4+: Alternatives
    Any alternate titles can be added here. For albums whose titles and franchise names are typically rendered in English, Japanese titles may be included here to aid in searches.
    If a game does not have an official English language release, don't submit a literal or fan translation of the game's name.
    Unless the front or obi indicates otherwise, a main title and a sub title should be separated by a colon (:), and two titles of equal standing should be separated by a slash (/). A slash (/) may also be used at the submitter's discretion to include the artist's name on an artist album, as Title / Artist.
    """
    display: str
    original: str
    romanized: Optional[str]
    japanese: Optional[str]
    english: Optional[str] # should be official

class VGMDBCatalog:
    """Split multi catalog when needed."""
    def __init__(self, catalog_formated:str):
        self._catalog = catalog_formated

    def __repr__(self):
        return self._catalog

    def __str__(self):
        return self._catalog

    def __iter__(self):
        if "~" in self._catalog:
            start, end = self._catalog.split("~")
            for i in range(int(start[-len(end):]), int(end)+1):
                yield start[:len(end)]+str(i)
        else:
            return [self._catalog]

class VGMPublisher:
    """Comma separated list of publishers."""
    def __init__(self, publisher_formatted: str):
        self._publishers = publisher_formatted

    def __repr__(self):
        return self._publishers

    def __str__(self):
        return self._publishers

    def __iter__(self):
        for publisher in self._publishers.split(","):
            yield publisher.rstrip(" ").lstrip(" ")

class Products:
    """Comma separated list of products represented on the album.
    TODO: add a product name parsing (parenthesis parsing)
    e.g.: Drakengard (Drag-on Dragoon)
    """
    def __init__(self, product_formatted: str):
        self._products = product_formatted

    def __repr__(self):
        return self._products

    def __str__(self):
        return self._products

    def __iter__(self):
        for product in self._products.split(","):
            yield product.rstrip(" ").lstrip(" ")

class VGMTrackString:
    def __init__(self, track_string: str):
        self.track_string = track_string
        (self.track_index,
         self.track_name,
         self.track_duration) = self.parse_track_string(track_string)

    def __repr__(self):
        return self.track_string

    def __str__(self):
        return self.track_string

    @classmethod
    def parse_track_string(cls, track_string)->Tuple:
        """Return track index, track name, track duration"""
        parts = track_string.rsplit(" ", 1)
        if len(parts[-1].split(":")) == 2:
            duration = parts[-1]
            track_string = parts[0]
        else:
            duration = None
        first_space_index = track_string.find(' ')
        track_index = None
        track_name = track_string
        if first_space_index is not None:
            if track_string[:first_space_index].isdigit():
                track_index = track_string[:first_space_index]
                track_name = track_string[(first_space_index+1):]
        return track_index, track_name, duration

class VGMDiskTrackListString:
    def __init__(self, track_string):
        self.track_string = track_string

    def __repr__(self):
        return self.track_string

    def __str__(self):
        return self.track_string



class ReleaseType(StrEnum):
    COMMERCIAL = 'Commercial'
    DOUJIN = "Doujin/Indie"
    BOOTLEG = "Bootleg"


class ReleaseSubType(StrEnum):
    GENERAL = "General"
    LIMITED = "Limited Edition"


class DateTuple(NamedTuple):
    """"""
    day: Optional[int]
    month: Optional[int]
    year: Optional[int]

class Price(TypedDict):
    value: float
    currency: str


class MediaFormat(StrEnum):
    CD = "CD"
    CASSETTE = "Cassette"
    VINYL = "Vinyl"
    DVD = "DVD"
    VHS = "VHS"
    DIGITAL = "Digital"
    CD_VIDEO = "CD Video"
    SA_CD = "SA-CD"
    BLU_RAY = "Blu-ray"
    LASER_DISC = "Laser Disc"
    FLOPPY_DISC = "Floppy Disc"
    FLEXI_DISC = "Flexi Disc"
    UHQCD = "UHQCD"
    BLU_SPEC_CD = "Blu-spec CD"
    BLU_SPEC_CD_2 = "Blu-spec CD2"
    HQCD = "HQCD"
    SHM_CD = "SHM-CD"
    PLAYBUTTON = "PLAYBUTTON"
    MINI_DISC = "Mini Disc"
    HDCD = "HDCD"
    BETAMAX = "Betamax"
    USB = "USB"
    DOWNLOAD_CODE = "Download Code"
    OTHER = "Other"
    CD_DVD = "CD + DVD"
    CD_BLU_RAY = "CD + Blu-ray"


class VGMCategory(StrEnum):
    """
    Game - Music from or related to any game: console, computer, handheld, cabinet, slot, tabletop.
    Animation - Music related to animation, whether Japanese (anime), Western, or nontraditional.
    Publication - Music related to print publications such as manga or light novels.
    Radio/Audio Drama - Music related to radio shows or audio dramas that contain illustrated characters.
    Tokusatsu/Puppetry - Music from live action visual arts with stylized characters, in particular Tokusatsu, puppetry, and other costumed programming.
    Live Action - Music from all other live action products.
    Multimedia Franchise - Music from Idol-based multimedia franchises that span genres.
    Game-adjacent - Music related to gaming/gaming systems, but not referencing a specific game. Includes notional game soundtracks, rhythm game simulators, chiptunes, demoscene, and system music or sounds.
    Event - Music produced for an event by the organizers, such as themed goods for conferences, performances and tournaments.
    Albums with no category defined will be treated as "Composer Discography" albums, i.e. original albums, unassociated with a product franchise, that are used to fill discographies of composers or arrangers.
    """
    OST = "Original Soundtrack"
    ARRANGEMENT = "Arrangement"
    VOCAL = "Vocal"
    DRAMA = "Drama"
    LIVE_EVENT = "Live Event"
    REMIX = "Remix"
    ORIGINAL_WORK = "Original Work"
    TALK = "Talk"
    REMASTER = "Remaster"
    PROTOTYPE = "Prototype/Unused"
    SOUND_EFFECT = "Sound Effect"
    DATA = "Data"
    VIDEO = "Video"


class SourceClassification(StrEnum):
    """
    You can select or de-select multiple classifications and categories with control-click.
    If the album contains at least 1 arrange, drama, remix, or original track, then include it in the classifications.
    Use the Vocal classification if the album contains vocal tracks.
    Original Soundtrack
    Music that accompanies some audio, visual, or printed work
    Arrangement
    Arrangement of music that accompanied some audio, visual, or printed work
    Vocal
    Music that includes vocals
    Drama
    Stories, monologues, and radio shows where everyone is in character
    Live Event
    Music recorded at a live event
    Remix
    A derived work that uses samples of the original work. Only use for valid VGMdb categories
    Original Work
    Music that has no connection to any of VGMdb's categories
    Talk
    Dialogues where the actors or composers are speaking, but are not in character
    Remaster
    A modified or improved work that overcomes limitations in the original recording or hardware. Only use for valid VGMdb categories.
    Prototype/Unused
    Music that is related to any of VGMdb's categories, but was not used in it. Image albums and image songs qualify
    Sound Effect
    Sound effects and voice samples
    Data
    A data track that appears on the media
    Video
    Any video work
    """
    GAME = "Game"
    ANIMATION = "Animation"
    PUBLICATION = "Publication"
    RADIO_AUDIO_DRAMA = "Radio/Audio Drama"
    GAME_ADJACENT = "Game-Adjacent"
    EVENT = "Event"
    TOKUSATSU = "Tokusatsu/Puppetry"
    LIVE_ACTION = "Live Action"
    MULTIMEDIA_FRANCHISE = "Multimedia/Franchise"


class VGMMediaInfo(TypedDict):
    disc_id: Optional[str]
    catalog_number: Optional[str]
    format: MediaFormat
    category: List[VGMCategory]


class ReleaseInfo(TypedDict):
    album_titles: AlbumTitles
    catalog: VGMDBCatalog
    barcode: str
    release_type: ReleaseType
    release_sub_type: ReleaseSubType
    release_date: DateTuple
    price: Optional[Price]
    publisher: Optional[VGMPublisher]


class VGMSupplementaryInfo(TypedDict):
    category: List[VGMCategory]
    classification: SourceClassification
    products: Products
    platforms: List[str] # should be an enum but too lazy
    notes: str

class VGMAlbumInfo(TypedDict):
    """"""
    vgm_album_id: str
    release: ReleaseInfo
    media_info: List[VGMMediaInfo]
    supplementary_info: VGMSupplementaryInfo
    links: List[str] # External link TODO: parse this
    related_albums: List[str] # LIST OF VGM_ALBUM_ID
    covers: List[str] # path to cover TODO: parse this

class TracklistLanguageEnum(StrEnum):
    ENGLISH = "English"
    JAPANESE = "Japanese"
    ROMAJI = "Romaji"
    GERMAN = "German"
    FRENCH = "French"



class VGMTracklist:
    language: Union[TracklistLanguageEnum, str]
    translator_name: str
    translation_web_source: str
    disks_tracklist: Dict[int, VGMDiskTrackListString] # disk index, tracklist
