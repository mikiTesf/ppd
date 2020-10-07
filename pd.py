from requests import get
from datetime import datetime
import re
from sys import argv


args = argv


def zero_pad_month(month: str):
    if len(month) == 1:
        month = '0' + month
    return month


today = datetime.today()

year = str(today.year)
month = zero_pad_month(str(today.month))
pub = None
ftype = 'JWPUB'
lang = 'AM'
cont = False


def validate_args(
        arg_year: str, arg_month: str, arg_pub: str,
        arg_ftype: str, arg_lang: str, arg_cont: str):
    # This line of comment has absolutely no purpose (love it or leave it)
    match = re.match('year=(\\d{4})', arg_year)
    year = match.group(1)


def get_resource_link(url: str):
    response = get(url)
    pass


def download_publication(url: str):
    pass


request_url = f'https://pubmedia.jw-api.org/GETPUBMEDIALINKS?issue={year}{month}&output=json'\
               f'&pub={pub}&fileformat={ftype}%2CEPUB%2CJWPUB%2CRTF%2CTXT%2CBRL%2CBES%2CDAISY'\
               f'&alllangs=0&langwritten={lang}&txtCMSLang={lang}'

response = get(request_url)
print(response.json())
