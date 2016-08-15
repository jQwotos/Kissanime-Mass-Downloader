### Please update your version of cfscrape https://github.com/Anorov/cloudflare-scrape

# Kiss anime downloader
## Help and Usage
```
usage: Alpha(v0.12).py [-h] [-l [LINK]] [-f [FILE]] [-d] [-n] [-w]
                       [-c [DIRECTORY]]

optional arguments:
  -h, --help            show this help message and exit
  -l [LINK], --link [LINK]
                        Link to series (https://kissanime.to/Anime/Sword-Art-
                        Online-Dub)
  -f [FILE], --file [FILE]
                        Import shows from file
  -d, --delete          After scanning, the program will ask you to remove
                        extras found such as intros.
  -n, --fancyname       Auto name the folder without - or dub or sub
  -w, --wget            Use the wget module rather than requests to download
  -c [DIRECTORY], --directory [DIRECTORY]
                        Specify a custom directory where the anime will be
                        downloaded
```
### Example file
```
https://kissanime.to/Anime/Sword-Art-Online-Dub
https://kissanime.to/Anime/Log-Horizon-Dub
```

## Desc
A quick script written in python that will auto download all episodes found within a series. Simply boot up the program with Python3 and give it the link to the show when it ask.

## Requirements
Requires Python 3.x, cfscrape, requests, Nodejs or PyV8, PyExecJS, re, BeautifulSoup4, wget, and kivy

Download them using: 
```
    pip3 install cfscrape requests pyexecjs bs4 wget
```
- If your running any distro that has the debian repository (debian, ubuntu ...) you can install NodeJS
```
    sudo su
    apt-get install nodejs
 ```

- If your on windows or mac visit
    https://nodejs.org/en/download/

Version> >= Alpha(v0.11).py
- Updated args with new forces

Version >= Alpha(v0.07)
- Improved previous download search
- Added -d arg

Verson >= Alpha(v0.06)
- Command line Utility

Version >= Alpha(v0.04)
- Implemented fake resuming, which deletes unfinished downloads are continues downloading non-downloaded episodes

## Testing
You may find yourself wanting some new features that havn't been fully tested yet, you can find these in the TESTING folder.

WARNING! I have not fully run complete test to make sure that the versions within the TESTING folder are working!
