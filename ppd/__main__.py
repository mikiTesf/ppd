#!/usr/bin/env python

import requests
from os import makedirs
from os.path import join, abspath, exists, basename
from urllib.parse import urlparse

import wget

from ppd import ppd_arg_parser


class PPD:

    def __init__(self):
        parsed_args = ppd_arg_parser.parse_args()

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
