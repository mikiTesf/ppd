#!/usr/bin/env python

import requests
from datetime import datetime
import argparse
from os import makedirs
from os.path import join, abspath, exists, basename
from urllib.parse import urlparse

import wget


class PPD:

    def __init__(self, pub: str, month: int, year: int, lang: str, file_format: str, cont: bool):
        self.pub = pub
        self.month = self.zero_pad_month(str(month))
        self.year = year
        self.lang = lang.upper()
        self.format = file_format.upper()
        self.cont = cont

    @staticmethod
    def zero_pad_month(month: str):
        if len(month) == 1:
            month = '0' + month
        return month

    def get_subsequent_months(self, current_month: str):
        current_month = int(current_month)
        subsequent_months = []

        if (current_month > 12) or (current_month < 1):
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
            publication_identifier = f"{self.pub} {month}/{self.year}"
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
                    print(f"{publication_identifier} ({self.lang}) does not exist.")
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
        if len(download_links) == 0:
            exit('No download links found. Exiting...')

        download_path = join('downloads', self.pub, self.lang, str(self.year))
        makedirs(download_path, exist_ok=True)

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
            print()  # An empty line inserted to prevent progress bars from overlapping over one another

        print('done...', f"all downloads saved to '{abspath(download_path)}'")


def main():
    # noinspection PyTypeChecker
    arg_parser = argparse.ArgumentParser(
        prog='ppd',
        description='''
    Short for "Periodic Publication Downloader", ppd is a script written using Python 3.8 that downloads the "periodic"
    Jehovah's Witness publication specified. You can download Awakes, Watchtowers (Public and Study) or Meeting Workbooks
    in any format from the command line.''',
        formatter_class=argparse.RawTextHelpFormatter,
        allow_abbrev=False,
        epilog='''
examples:
    Executing the command below will not download any publication as the publication is not specified.
    % ppd --year 2010 --month 2 --format pdf --lang e

    This will download the Awake of September 2010 in the PDF format and the English language.
    % ppd g --year 2010 --month 9 --format pdf --lang e

    This will download the Public Watchtower of the current year and month in the EPUB
    format and the Arabic language.
    % ppd wp --format epub --lang a

    This will download all Meeting Workbook issues from January 2018 up to December 2018
    in the JWPUB format and the Amharic language (note that `--cont` is passed).
    % ppd mwb --year 2018 --month 1 --format jwpub --lang am --cont''')

    arg_parser.version = 'version 0.2'
    arg_parser.add_argument('pub', type=str, choices=['w', 'wp', 'g', 'mwb'],
                            help='The type of the publication to download')
    today = datetime.today()
    arg_parser.add_argument('-m', '--month', type=int, help='The month of the issue (defaults to the current month)',
                            default=str(today.month))
    arg_parser.add_argument('-y', '--year', type=int, help='The year of the issue (defaults to the current year)',
                            default=str(today.year))
    arg_parser.add_argument('-l', '--lang', type=str, default='AM',
                            help='''The short language code of the target language
(ex: AM for Amharic, E for English, etc. Defaults to AM)''')
    arg_parser.add_argument('-f', '--format', type=str, default='JWPUB',
                            help='The file format of the download. PDF, JWPUB, EPUB, BRL or RTF (defaults to JWPUB)')
    arg_parser.add_argument('-c', '--cont', action='store_true',
                            help='''Decides weather the script should continue downloading releases of the
specified publication until the end of the year (See the last example below)''')
    arg_parser.add_argument('-v', '--version', action='version')

    parsed_args = arg_parser.parse_args()

    ppd = PPD(
        parsed_args.pub, parsed_args.month, parsed_args.year,
        parsed_args.lang, parsed_args.format, parsed_args.cont)
    links = ppd.get_download_links()
    ppd.download_publications(links)


if __name__ == '__main__':
    main()
