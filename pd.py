from requests import get
from datetime import datetime
import re
from sys import argv


options = dict()
FILE_TYPES = ['PDF', 'EPUB', 'JWPUB', 'RTF']

HELP = """
NAME
       pd (short for "pub downloader") - Download any periodic JW publication(s) (g, wp, w, mwb) in any format from the
       command line

SYNOPSIS
       python3.x pd.py [year=YEAR; default=current] [month=MONTH; default=current]
                       [ftype={jwpub | pdf | epub | rtf}; default=jwpub] [lang=LANGUAGE_CODE; default=AM]
                       [cont={true | false}; default=false] pub={g | w | wp | mwb}
       python3.x pd.py [-h|--help]

DESCRIPTION
       pd.py is a script written using Python 3.8 that downloads the publication(s) specified by the options shown above.
       The `pub` option is mandatory and must always be supplied. All other options will be set to their default values
       if they are not provided explicitly.

OPTIONS
       A summary of the available options is included below.

       year        The year of the issue (default to the current year)

       month       The month of the issue (defaults to the current month)

       ftype       The file format of the download (PDF, JWPUB, EPUB or RTF; it defaults to JWPUB)

       lang        The short language code of the target language (ex: AM for Amharic, E for English, etc.)

       cont        Decides weather the script should continue downloading releases of the specified publication
                   until the end of the year (can be set to true or false; defaults to false). See examples below.

       pub         The type of the "periodic" publication to download (w, wp, g, mwb; must always be supplied). If
                   this option is not supplied this help will be shown instead.

       -h, --help  Display this help and exit

EXAMPLES
       Executing the command below will not download any publication as `pub` is not supplied.
       % python3.x pd.py year=2010 month=2 ftype=pdf lang=e

       This will download the Awake of February 2010 in the PDF format and the English language
       % python3.x pd.py year=2010 month=2 ftype=pdf lang=e pub=g

       This will download the Public Watchtower of the current year and month in the EPUB format and the Arabic language
       % python3.x pd.py ftype=epub lang=a pub=wp

       This will download all Meeting Workbook issues from January 2018 up to December 2018 in the JWPUB format
       and the Amharic language (note that `cont` is set to true)
       % python3.x pd.py year=2018 month=1 ftype=jwpub lang=am pub=mwb cont=true
"""


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
            ftype = match.group(1).upper()
            if ftype in FILE_TYPES:
                options['ftype'] = ftype
            continue

        match = re.match('lang=([a-z]+)', arg, re.IGNORECASE)
        if match:
            options['lang'] = match.group(1).upper()
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


def get_subsequent_months(current_month: str):
    current_month = int(current_month)
    subsequent_months = []

    if (current_month > 12) or (current_month < 1):
        return subsequent_months  # which will be empty at this point

    while (current_month + 1) < 13:
        current_month += 1
        subsequent_months.append(zero_pad_month(str(current_month)))

    return subsequent_months


def get_resource_links():
    download_links = []
    months = [options['month']]

    if options['cont'] == 'true':
        months.extend(get_subsequent_months(months[0]))

    for month in months:
        request_url = f"https://pubmedia.jw-api.org/GETPUBMEDIALINKS?issue={options['year']}{month}&output=json" \
                      f"&pub={options['pub']}&fileformat={options['ftype']}%2CEPUB%2CJWPUB%2CRTF%2CTXT%2CBRL%2CBES%2CDAISY" \
                      f"&alllangs=0&langwritten={options['lang']}&txtCMSLang={options['lang']}"
        response = get(request_url).json()

        if type(response) == list:
            # [{"id": "some-uuid", "title": "Not found", "status": 404}]
            print(f"{options['pub']} {options['year']}/{options['month']} in the language {options['lang']} and "
                  f"file format {options['ftype']} does not exist.")
        else:
            download_links.append(response['files'][options['lang']][options['ftype']][0]['file']['url'])

    return download_links


def download_publications(download_links: list):
    pass


args = argv[1:]

# The first thing to check is if the user is trying to get help on how to use `pd`
if (len(args) == 0) or ('-h' in args) or ('--help' in args):
    print(HELP)
    exit(0)

# If the execution made it this far, then start parsing for arguments, The following will be the defaults
today = datetime.today()
options['year'] = str(today.year)
options['month'] = zero_pad_month(str(today.month))
options['pub'] = None
options['ftype'] = 'JWPUB'
options['lang'] = 'AM'
options['cont'] = 'false'
# On the following line, the default options will be replaced with those passed by the user. If any of the options
# supplied by the user are faulty, the default values set before `collect_options(...)` is called are used
options = collect_options(args)

download_links = get_resource_links()
