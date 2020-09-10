from urllib.parse import urlparse
from os.path import basename, splitext


def get_url_filename(link: str) -> str:
    return basename(urlparse(link).path)


def is_image(path: str) -> bool:
    if path is None:
        return False
    return splitext(path)[-1].strip('.').split('?')[0].lower() in [
        'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'svg', 'gif'
    ]

