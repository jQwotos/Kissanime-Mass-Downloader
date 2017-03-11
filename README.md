### [Check status](https://reddit.com/r/kissanime)
# Seems like Kissanime bot tolerance has gone down.
I found that I have to use a browser to do a recaptcha a lot more now than before.
It seems that Kissanime will set your IP to temporarily disabled from watching / downloading episodes until a captcha is completed.
A 9anime.to downloader is currently in the works as a replacement.
# Kiss anime downloader
A CLI program designed for servers to download full seasons of anime from Kissanime.
I suggest using this on a Plex server, but it can also be used in any environment.
### Quick Usage
```
python3 Alpha(v0.13).py -l Log-Horizon-Dub
```

### Help and Usage
```
usage: python3 Alpha(v0.13).py [-h] [-l [LINK]] [-f [FILE]] [-d] [-n] [-w]
                       [-c [DIRECTORY]] [-a]

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
  -a, --continous       For series that are still airing, continue to keep
                        folder updated
```
### Installation on Linux
#### Automated
```
wget https://raw.githubusercontent.com/jQwotos/Kissanime-Mass-Downloader/master/install.sh && sudo chmod +x install.sh && sudo ./install.sh
```
#### Manual
```
git clone https://github.com/jQwotos/Kissanime-Mass-Downloader
cd Kissanime-Mass-Downloader/
pip install -r requirements.txt
apt-get install nodejs
```

### Installation on Mac
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install python3 git nodejs
cd Kissanime-Mass-Downloader/
pip3 install -r requirements.txt
```
### Example input file
```
https://kissanime.to/Anime/Sword-Art-Online-Dub
https://kissanime.to/Anime/Log-Horizon-Dub
Charlotte-Sub
```

## Bugs with Kissanime
This script isn't yet able to handle crashes on Kissanime's end. For now you can just restart the script after 10 - 30 seconds and unless Kissanime is under maintnance it should fix itself. (I'm still working on V2, however Kissanime keeps updating their site to block it). Here are some errors that we can't handle and what they will say.
* 500 Error on per Episode page ("Unable to find a link for episode: *")
* This service is not available ("Unable to find episodes, is kissanime.to down or maybe your network")

## Desc
A quick script written in python that will auto download all episodes found within a series. Simply boot up the program with Python3 and give it the link to the show when it ask.

Version >= Alpha(v0.13).py
- Added continous mode
- Allowed for part links, instead of https://kissanime.to/Anime/Rewrite, it now accepts Rewrite

Version >= Alpha(v0.11).py
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
