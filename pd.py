from requests import get
from datetime import datetime
import re
from sys import argv


options = dict()
FILE_TYPES = ['PDF', 'EPUB', 'JWPUB', 'RTF']


def zero_pad_month(month: str):
    if len(month) == 1:
        month = '0' + month
    return month


def collect_options(args_list):
    for arg in args_list:
        match = re.match('year=(\\d{4})', arg)
        if match:
            options['year'] = match.group(1)
            continue

        match = re.match('month=(\\d{1,2})', arg)
        if match:
            options['month'] = zero_pad_month(match.group(1))
            continue

        match = re.match('ftype=([a-z]+)', arg, re.IGNORECASE)
        if match:
            ftype = match.group(1)
            if ftype.upper() in FILE_TYPES:
                options['ftype'] = ftype
            continue

        match = re.match('lang=([a-z]+)', arg, re.IGNORECASE)
        if match:
            options['lang'] = match.group(1)
            continue

        match = re.match('cont=(true|false)', arg, re.IGNORECASE)
        if match:
            options['cont'] = match.group(1)
            continue

        match = re.match('pub=([a-z]+)', arg, re.IGNORECASE)
        if match:
            options['pub'] = match.group(1)
            continue

    return options


def get_resource_link(url: str):
    response = get(url)
    pass


def download_publication(url: str):
    pass


args = argv[1:]

# The first thing to check is if the user is trying to get help on how to use `pd`
if (len(args) == 0) or ('-h' in args) or ('--help' in args):
    # print(HELP)
    exit(0)

# If the execution made it this far, then start parsing for arguments, The following will be the defaults
today = datetime.today()
options['year'] = str(today.year)
options['month'] = zero_pad_month(str(today.month))
options['pub'] = None
options['ftype'] = 'JWPUB'
options['lang'] = 'AM'
options['cont'] = 'false'

options = collect_options(args)

request_url = f"https://pubmedia.jw-api.org/GETPUBMEDIALINKS?issue={options['year']}{options['month']}&output=json" \
              f"&pub={options['pub']}&fileformat={options['ftype']}%2CEPUB%2CJWPUB%2CRTF%2CTXT%2CBRL%2CBES%2CDAISY" \
              f"&alllangs=0&langwritten={options['lang']}&txtCMSLang={options['lang']}"


def download_publication(url: str):
    pass


request_url = f'https://pubmedia.jw-api.org/GETPUBMEDIALINKS?issue={year}{month}&output=json'\
               f'&pub={pub}&fileformat={ftype}%2CEPUB%2CJWPUB%2CRTF%2CTXT%2CBRL%2CBES%2CDAISY'\
               f'&alllangs=0&langwritten={lang}&txtCMSLang={lang}'

response = get(request_url)
print(response.json())
