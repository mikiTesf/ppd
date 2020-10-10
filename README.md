
## PD (Publication Downloader)
```
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
```

It was written using Python 3.8 and the minimum version of Python 3 its compatible with is uncertain.
