#!/usr/bin/env python

import requests
from datetime import datetime
import argparse
from os import makedirs
from os.path import join, abspath, exists, basename
from urllib.parse import urlparse

import wget

from ppd import __version__, __author__


class PPD:

    def __init__(self):
        # noinspection PyTypeChecker
        self.arg_parser = argparse.ArgumentParser(
            prog='ppd',
            description='''
    Short for "Periodic Publication Downloader", ppd is a script written using Python 3.8 that downloads the
    "periodic" Jehovah's Witness publication specified. You can download Awakes, Watchtowers (Public and Study)
    or Meeting Workbooks in any format from the command line.''',
            formatter_class=argparse.RawTextHelpFormatter,
            allow_abbrev=False,
            epilog=f'''
examples:
    Executing the command below will not download any publication as the publication is not specified.
    % ppd --year=2010 --month=2 --format=pdf --lang=e

    This will download the Awake of September 2010 in the PDF format and the English language.
    % ppd g --year=2010 --month=9 --format=pdf --lang=e

    This will download the Public Watchtower of the current year and month in the EPUB format
    and the Arabic language.
    % ppd wp --format=epub --lang=a

    This will download all Meeting Workbook issues from January 2018 up to December 2018
    in the JWPUB format and the Amharic language (note that `--cont` is passed).
    % ppd mwb --year=2018 --month=1 --format=jwpub --lang=am --cont

more on options:
    Short options can be used in place of long ones. Here is the short option equivalent of the
    last example above:
    % ppd mwb -y 2018 -m 1 -f jwpub -l am -c

author:
    {__author__} (mickyastesfamichael@gmail.com)''')

        self.arg_parser.version = __version__
        # The options in the following argument group apply only to periodic publications
        self.arg_parser.add_argument('pub', metavar='pub', type=str, choices=('w', 'wp', 'g', 'mwb'),
                                     help='The type of publication to download (w | wp | g | mwb)')
        today = datetime.today()
        self.arg_parser.add_argument('-m', '--month', type=int,
                                     help='The month of the issue (defaults to the current month)',
                                     default=str(today.month))
        self.arg_parser.add_argument('-y', '--year', type=int,
                                     help='The year of the issue (defaults to the current year)',
                                     default=str(today.year))
        # The options in the following argument group apply only to books
        '''Implement the code for book downloading arguments and options'''
        # The following options either apply to all kinds of publications ppd can download or to none at all
        self.arg_parser.add_argument('-l', '--lang', type=str, default='AM',
                                     help='''The short language code of the target language
(ex: AM for Amharic, E for English, etc. Defaults to AM)''')
        self.arg_parser.add_argument('-f', '--format', type=str, default='JWPUB',
                                     help='The file format of the download. PDF, JWPUB, EPUB, BRL or RTF (defaults to '
                                          'JWPUB)')
        self.arg_parser.add_argument('-o', '--link-only', action='store_true',
                                     help='''Only show download links (publications will not be downloaded)''')
        self.arg_parser.add_argument('-r', '--hierarchy', action='store_true',
                                     help='''Create a directory hierarchy in the current working directory in which downloaded
publications will be saved. The hierarchy follows the following pattern:
        <publication-type>/<publication-language>/<publication-year>/

For example if you download all public Watchtowers of 2020 in the Amharic language,
this is what the file tree for the downloads will look like:
                wp/
                └── AM
                    └── 2020
                        ├── wp_AM_202001.extn
                        ├── wp_AM_202005.extn
                        └── wp_AM_202009.extn''')
        self.arg_parser.add_argument('-c', '--cont', action='store_true',
                                     help='''Continue fetching links for releases of the specified publication
until the end of the year (see the last example below)''')
        self.arg_parser.add_argument('-v', '--version', action='version')

        parsed_args = self.arg_parser.parse_args()

        self.pub = parsed_args.pub
        self.month = self.zero_pad_month(str(parsed_args.month))
        self.year = str(parsed_args.year).zfill(4)
        self.lang = parsed_args.lang.upper()
        self.format = parsed_args.format.upper()
        self.cont = parsed_args.cont
        self.hierarchy = parsed_args.hierarchy
        self.link_only = parsed_args.link_only

    @staticmethod
    def zero_pad_month(month: str):
        return month.zfill(2)

    def get_subsequent_months(self, current_month: str):
        current_month = int(current_month)
        subsequent_months = []

        if (current_month < 1) or (current_month > 12):
            return subsequent_months  # which will be empty at this point

        while (current_month + 1) < 13:
            current_month += 1
            subsequent_months.append(self.zero_pad_month(str(current_month)))

        return subsequent_months

    def get_download_links(self):
        download_links = []
        months = [self.month]

        if self.cont:
            months.extend(self.get_subsequent_months(months[0]))

        print('Getting download links...')

        for month in months:
            publication_identifier = f"{self.pub} {month}/{self.year} ({self.lang})"
            request_url = f"https://pubmedia.jw-api.org/GETPUBMEDIALINKS?issue={self.year}{month}&output=json" \
                          f"&pub={self.pub}&fileformat={self.format}%2CEPUB%2CJWPUB%2CRTF%2CTXT%2CBRL%2CBES%2CDAISY" \
                          f"&alllangs=0&langwritten={self.lang}&txtCMSLang={self.lang}"
            try:
                response = requests.get(request_url).json()
            except KeyboardInterrupt:
                exit('\nDownload interrupted. Exiting...')
            except requests.exceptions.Timeout:
                print(
                    f"There was a request timeout. \033[93mDownload link for '{publication_identifier}' "
                    f"not fetched\033[0m.", 'Attempting to download the next publication...')
                continue
            except requests.exceptions.ConnectionError:
                exit('Could not connect to the internet. Exiting...')
            else:
                if type(response) == list:
                    # [{"id": "some-uuid", "title": "Not found", "status": 404}]
                    print(f"{publication_identifier} does not exist.")
                else:
                    available_formats = list(response['files'][self.lang].keys())

                    if self.format in available_formats:
                        pub_link = response['files'][self.lang][self.format][0]['file']['url']
                        print(f"{publication_identifier} download link: {pub_link}")
                        download_links.append(pub_link)
                    else:
                        print(f"{publication_identifier} available format(s): {available_formats}")

        return download_links

    def download_publications(self, download_links: list):
        if self.link_only:
            exit(0)

        if len(download_links) == 0:
            exit('No download links found. Exiting...')

        if self.hierarchy:
            download_path = join(self.pub, self.lang, str(self.year))
            makedirs(download_path, exist_ok=True)
        else:
            download_path = '.'

        print('###################################################################################################')

        for link in download_links:
            file_name = basename(urlparse(link).path)

            if exists(join(download_path, file_name)):
                print(f"'{file_name}' already exists. Skipping...")
                continue

            print(f"downloading: {file_name}")

            try:
                wget.download(link, out=download_path)
            except KeyboardInterrupt:
                exit(
                    f"\nDownload interrupted. Check '{abspath(download_path)}' for downloaded publications. Exiting...")
            except ConnectionResetError:
                print(
                    f"The connection was reset by the remote server. \033[93m'{file_name}' not downloaded\033[0m. "
                    f"Skipping...")
                continue
            print()  # An empty line inserted to prevent progress bars from overlapping over one another

        print('done...', f"download(s) saved to '{abspath(download_path)}'")


def main():
    ppd = PPD()
    ppd.download_publications(ppd.get_download_links())


if __name__ == '__main__':
    main()
