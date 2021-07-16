from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import datetime


__version__ = '0.2.2'
__author__ = 'Mikyas Tesfamichael'
__email__ = 'mickyastesfamichael@gmail.com'


ppd_arg_parser = ArgumentParser(
    prog='ppd',
    description='''
    Short for "Periodic Publication Downloader", ppd is a script written using Python 3.8 that downloads the
    "periodic" Jehovah's Witness publication specified. You can download Awakes, Watchtowers (Public and Study)
    or Meeting Workbooks in any format from the command line.''',
    formatter_class=RawTextHelpFormatter,
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
    {__author__} ({__email__})''')

ppd_arg_parser.version = __version__
# The options in the following argument group apply only to periodic publications
ppd_arg_parser.add_argument('pub', metavar='pub', type=str, choices=('w', 'wp', 'g', 'mwb'),
                            help='The type of publication to download (w | wp | g | mwb)')
today = datetime.today()
ppd_arg_parser.add_argument('-m', '--month', type=int,
                            help='The month of the issue (defaults to the current month)',
                            default=str(today.month))
ppd_arg_parser.add_argument('-y', '--year', type=int,
                            help='The year of the issue (defaults to the current year)',
                            default=str(today.year))
# The options in the following argument group apply only to books
'''Implement the code for book downloading arguments and options'''
# The following options either apply to all kinds of publications ppd can download or to none at all
ppd_arg_parser.add_argument('-l', '--lang', type=str, default='AM',
                            help='''The short language code of the target language
(ex: AM for Amharic, E for English, etc. Defaults to AM)''')
ppd_arg_parser.add_argument('-f', '--format', type=str, default='JWPUB',
                            help='The file format of the download. PDF, JWPUB, EPUB, BRL or RTF (defaults to '
                             'JWPUB)')
ppd_arg_parser.add_argument('-o', '--link-only', action='store_true',
                            help='''Only show download links (publications will not be downloaded)''')
ppd_arg_parser.add_argument('-r', '--hierarchy', action='store_true',
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
ppd_arg_parser.add_argument('-c', '--cont', action='store_true',
                            help='''Continue fetching links for releases of the specified publication
until the end of the year (see the last example below)''')
ppd_arg_parser.add_argument('-v', '--version', action='version')
