import requests
from redditgtk.confManager import ConfManager
from hashlib import sha256
from urllib.parse import urlparse
from os.path import isfile
from redditgtk.path_utils import get_url_filename

confman = ConfManager()
GET_HEADERS = {
    'User-Agent': 'redditgtk/1.0',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate'
}
TIMEOUT = 30


def __error_out(link: str, code: int):
    raise requests.HTTPError(
        f'response code {code} for url `{link}`'
    )


def shasum(txt: str) -> str:
    return sha256(txt.encode()).hexdigest()


def download_img(link: str) -> str:
    dest = f'{confman.cache_path}/{get_url_filename(link)}'
    if not isfile(dest):
        res = requests.get(link, headers=GET_HEADERS, timeout=TIMEOUT)
        if 200 <= res.status_code <= 299:
            with open(dest, 'wb') as fd:
                for chunk in res.iter_content(1024):
                    fd.write(chunk)
        else:
            # __error_out(link, res.status_code)
            return None
    return dest
