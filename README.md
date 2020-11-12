
## PPD (Periodic Publication Downloader)
```
usage: ppd [-h] [-m MONTH] [-y YEAR] [-l LANG] [-f FORMAT] [-c] [-o] [-v] {w,wp,g,mwb}

    Short for "Periodic Publication Downloader", ppd is a script written using Python 3.8 that downloads the
    "periodic" Jehovah's Witness publication specified. You can download Awakes, Watchtowers (Public and Study)
    or Meeting Workbooks in any format from the command line.

positional arguments:
  {w,wp,g,mwb}          The type of the publication to download

optional arguments:
  -h, --help            show this help message and exit
  -m MONTH, --month MONTH
                        The month of the issue (defaults to the current month)
  -y YEAR, --year YEAR  The year of the issue (defaults to the current year)
  -l LANG, --lang LANG  The short language code of the target language
                        (ex: AM for Amharic, E for English, etc. Defaults to AM)
  -f FORMAT, --format FORMAT
                        The file format of the download. PDF, JWPUB, EPUB, BRL or RTF (defaults to JWPUB)
  -c, --cont            Continue downloading releases of the specified publication until
                        the end of the year (See the last example below)
  -o, --links-only      Only show download links (publications will not be downloaded)
  -v, --version         show program's version number and exit

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
    % ppd mwb --year 2018 --month 1 --format jwpub --lang am --cont

more on options:
    Long options can have an equal sign between them and their values (--format=pdf). Also, short options can
    be used inplace of long ones. Here is the short option equivalent of the last example above:
    % ppd mwb -y 2018 -m 1 -f jwpub -l am -c

downloads:
    ppd will create a directory hierarchy in the current working directory in which downloaded publications
    will be saved. The hierarchy follows the following pattern:
                        <publication-type>/<publication-language>/<publication-year>

    For example if you download all public Watchtowers of 2020 in the Amharic language, this is what the file
    tree for the downloads will look like:
                        wp/
                        └── AM
                            └── 2020
                                ├── wp_AM_202001.extn
                                ├── wp_AM_202005.extn
                                └── wp_AM_202009.extn
```

It was written using Python 3.8 and the minimum version of Python 3 its compatible with is uncertain.

#### Installation
`ppd` is available on [PyPI](https://pypi.org/project/ppd/). You can install it with: `pip install ppd`.
