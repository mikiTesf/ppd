from requests import get
from datetime import datetime


def zero_pad_month(month: str):
    if len(month) == 1:
        month = '0' + month
    return month


today = datetime.today()

year = str(today.year)
month = zero_pad_month(str(today.month))
pub = 'mwb'
ftype = 'JWPUB'
lang = 'AM'


request_url = f'https://pubmedia.jw-api.org/GETPUBMEDIALINKS?issue={year}{month}&output=json'\
               f'&pub={pub}&fileformat={ftype}%2CEPUB%2CJWPUB%2CRTF%2CTXT%2CBRL%2CBES%2CDAISY'\
               f'&alllangs=0&langwritten={lang}&txtCMSLang={lang}'

response = get(request_url)
print(response.json())
