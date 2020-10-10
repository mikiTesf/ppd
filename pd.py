import requests
from datetime import datetime
import re
from sys import argv
from os import makedirs
from os.path import join, abspath, exists

import wget


options = dict()

HELP = """
NAME
       pd (short for "publication downloader") - Download any "periodic" JW publication(s). Awake,
       Watchtower, Watchtower - Public or Meeting Workbook in any format from the command line

SYNOPSIS
       python3.8 pd.py [--year=YEAR; default=current] [--month=MONTH; default=current]
                       [--ftype={jwpub | pdf | epub | rtf | brl}; default=jwpub]
                       [--lang=LANGUAGE_CODE; default=AM] [--cont]
                       --pub={g | w | wp | mwb}
       python3.8 pd.py [-h | --help]

DESCRIPTION
       pd.py is a script written using Python 3.8 that downloads the publication(s) specified
       by the options shown above. The `pub` option is mandatory and must always be supplied.
       All other options will be set to their default values if they are not provided explicitly
       or if the ones provided are faulty.

OPTIONS
       A summary of the available options is included below.

       --year        The year of the issue (defaults to the current year)

       --month       The month of the issue (defaults to the current month)

       --ftype       The file format of the download. PDF, JWPUB, EPUB, BRL or RTF (defaults to JWPUB)

       --lang        The short language code of the target language (ex: AM for Amharic,
                     E for English, etc. Defaults to AM)

       --cont        Decides weather the script should continue downloading releases of the
                     specified publication until the end of the year (See the last example below)

       --pub         The type of the publication to download. w, wp, g or mwb. It must always be supplied.
                     If this option is not supplied this help will be shown instead

       -h, --help    Display this help and exit

EXAMPLES
       Executing the command below will not download any publication as `pub` is not supplied.
       % python3.8 pd.py --year=2010 --month=2 --ftype=pdf --lang=e

       This will download the Awake of February 2010 in the PDF format and the English language.
       % python3.8 pd.py --pub=g --year=2010 --month=2 --ftype=pdf --lang=e

       This will download the Public Watchtower of the current year and month in the EPUB
       format and the Arabic language.
       % python3.8 pd.py --pub=wp --lang=a --ftype=epub

       This will download all Meeting Workbook issues from January 2018 up to December 2018
       in the JWPUB format and the Amharic language (note that `--cont` is passed).
       % python3.8 pd.py --pub=mwb --year=2018 --month=1 --ftype=jwpub --lang=am --cont
"""


def zero_pad_month(month: str):
    if len(month) == 1:
        month = '0' + month
    return month


def collect_options(args_list):
    for arg in args_list:
        match = re.match('--year=(\\d{4})', arg)
        if match:
            options['year'] = match.group(1)
            continue

        match = re.match('--month=(\\d{1,2})', arg)
        if match:
            options['month'] = zero_pad_month(match.group(1))
            continue

        match = re.match('--ftype=([a-z]+)', arg, re.IGNORECASE)
        if match:
            ftype = match.group(1).upper()
            options['ftype'] = ftype
            continue

        match = re.match('--lang=([a-z]+)', arg, re.IGNORECASE)
        if match:
            options['lang'] = match.group(1).upper()
            continue

        match = re.match('--cont', arg, re.IGNORECASE)
        if match:
            options['cont'] = True
            continue

        match = re.match('--pub=([a-z]+)', arg, re.IGNORECASE)
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


def get_download_links():
    download_links = []
    months = [options['month']]

    if options['cont']:
        months.extend(get_subsequent_months(months[0]))

    print('Getting download links...')

    for month in months:
        publication_identifier = f"{options['pub']} {options['year']}/{month}"
        request_url = f"https://pubmedia.jw-api.org/GETPUBMEDIALINKS?issue={options['year']}{month}&output=json" \
                      f"&pub={options['pub']}&fileformat={options['ftype']}%2CEPUB%2CJWPUB%2CRTF%2CTXT%2CBRL%2CBES%2CDAISY" \
                      f"&alllangs=0&langwritten={options['lang']}&txtCMSLang={options['lang']}"
        try:
            response = requests.get(request_url).json()
        except KeyboardInterrupt:
            print('Download interrupted. Exiting...')
            exit(0)
        except requests.exceptions.Timeout:
            print(f'There was a request timeout. \033[93m{publication_identifier} not downloaded\033[0m. '
                  'Attempting to download the next publication...')
            continue
        except requests.exceptions.ConnectionError:
            print('Could not connect to the internet. Exiting...')
            exit(0)
        else:
            if type(response) == list:
                # [{"id": "some-uuid", "title": "Not found", "status": 404}]
                print(f"{publication_identifier} {options['lang']} does not exist.")
            else:
                available_formats = list(response['files'][options['lang']].keys())

                if options['ftype'] in available_formats:
                    pub_link = response['files'][options['lang']][options['ftype']][0]['file']['url']
                    print(f"{publication_identifier} download link: {pub_link}")
                    download_links.append(pub_link)
                else:
                    print(f"{publication_identifier} available format(s): {available_formats}")

    return download_links


def download_publications(download_links: list):
    if len(download_links) == 0:
        print('No download links found. Exiting...')
        exit(0)

    download_path = join('downloads', options['pub'], options['lang'], options['year'])
    makedirs(download_path, exist_ok=True)

    print('###################################################################################################')

    for link in download_links:
        file_name = link[link.rindex('/') + 1:]

        if exists(join(download_path, file_name)):
            print(f"'{file_name}' already exists. Skipping...")
            continue

        print(f"downloading: {file_name}")

        try:
            wget.download(link, out=download_path)
        except KeyboardInterrupt:
            print('\nDownload interrupted. Exiting...')
            exit(0)
        print()  # An empty line inserted to prevent progress bars from overlapping over one another

    print('done...', f"all downloads saved to '{abspath(download_path)}'")


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
options['cont'] = False

# On the following line, the default options will be replaced with those passed by the user. If any of the options
# supplied by the user are faulty, the default values set before `collect_options(...)` is called are used
options = collect_options(args)

# The following check is important because even though options were supplied, the `pub` option may still not be
# supplied (ex. invoking `python pd.py year=2017 month=7 lang=am`)
if options['pub'] is None:
    print(HELP)
    exit(0)

download_publications(get_download_links())
