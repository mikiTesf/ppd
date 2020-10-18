
## PD (Publication Downloader)
```
usage: pd [-h] [-m MONTH] [-y YEAR] [-l LANG] [-f FORMAT] [-c] [-v] {w,wp,g,mwb}

    Short for "Publication Downloader", pd.py is a script written using Python 3.8 that downloads
    the publication specified. You can download any "periodic" JW publication - Awake, Watchtower,
    Watchtower - Public or Meeting Workbook in any format from the command line.

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
                        The file format of the download. PDF, JWPUB, EPUB, BRL or RTF
                        (defaults to JWPUB)
  -c, --cont            Decides weather the script should continue downloading releases of the
                        specified publication until the end of the year (See the last example below)
  -v, --version         show program's version number and exit

examples:
    Executing the command below will not download any publication as the publication is not supplied.
    % python3.8 pd.py --year 2010 --month 2 --format pdf --lang e

    This will download the Awake of September 2010 in the PDF format and the English language.
    % python3.8 pd.py g --year 2010 --month 9 --format pdf --lang e

    This will download the Public Watchtower of the current year and month in the EPUB
    format and the Arabic language.
    % python3.8 pd.py wp --format epub --lang a

    This will download all Meeting Workbook issues from January 2018 up to December 2018
    in the JWPUB format and the Amharic language (note that `--cont` is passed).
    % python3.8 pd.py mwb --year 2018 --month 1 --format jwpub --lang am --cont
```

It was written using Python 3.8 and the minimum version of Python 3 its compatible with is uncertain.

#### Installation
PD is available on [PyPi](https://pypi.org/project/pub_downloader/). You can install it with: `pip3 install pub_downloader`.
