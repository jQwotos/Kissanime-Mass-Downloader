'''
Dependencies: Python 3.x, cfscrape, requests, Nodejs or PyV8, PyExecJS, BeautifulSoup4, wget, kivy
You only need kivy if you are using the UI rather than command line. To specify that you want to use command line add a -c to your command
Download them using:
    pip3 install cfscrape requests pyexecjs bs4 wget
- If your running any distro that has the debian repository (debian, ubuntu ...) you can install NodeJS and kivy
    sudo su
    apt-get install nodejs software-properties-common
    apt-get update
    apt-get install python3-kivy

- If your on windows or mac visit
    https://nodejs.org/en/download/

Author: Jason Le
Email: le.kent.jason@gmail.com
Github: jQwotos
'''
import requests, cfscrape, wget, os, re, glob, sys, argparse, threading
from bs4 import BeautifulSoup

class CFScrapeLogin:
    def __init__(self):
        output.send("Initializing Scraper, this may take 5 - 10 seconds")
        self.scraper = cfscrape.create_scraper()
        self.URL = "https://kissanime.to/"
        self.downloaded = []
        self.undownlodable = []
        LoginURL = self.URL + "Login"
        USR = "Naal1933"
        PASSWD = "Naal1933"

        login_data = dict(username=USR, password=PASSWD, next='/')
        self.scraper.get(LoginURL)
        output.send("Logging in with bot credentials")
        self.scraper.post(LoginURL, data=login_data, headers={"Referer": "https://google.com"})
        output.send("Logged in")

class Parse:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-l", "--link", help="Link to series (https://kissanime.to/Anime/Sword-Art-Online-Dub)", type=str, nargs="?", default="null")
        parser.add_argument("-d", "--delete", help="After scanning, the program will ask you to remove extras found such as intros.", action="store_true")
        parser.add_argument("-f", "--file", help="Import shows from file", type=str, nargs="?", default="null")
        self.args = parser.parse_args()

class Thread_Handler:
    def __init__(self):
        self.toBeDownloaded = []
        if parser.args.file != "null":
            if os.path.isfile(parser.args.file):
                with open(str(parser.args.file)) as f:
                    for line in f:
                        self.toBeDownloaded.append(line.replace("\n", ""))
                self.send()
            else:
                output.send("Unable to find your input file")
        elif parser.args.link != "null":
            self.send(parser.args.link)
        else:
            output.send("No link found, please specify using -l (--help for help menu) or input now")
            self.send(input())

        self.start()


    def send(self, showLink = "null"):
        if showLink != "null": self.toBeDownloaded.append(showLink)

    def start(self):
        while len(self.toBeDownloaded) >= 1:
            print("Starting to download: " + self.toBeDownloaded[0])
            downloader.start(self.toBeDownloaded[0])
            print("Finished downloading: " + self.toBeDownloaded[0])
            for x in range(2): os.chdir('..')
            del self.toBeDownloaded[0]

class Downloader:
    def __init__(self, showLink = "https://kissanime.to/Anime/Sword-Art-Online-Dub"):
        self.acceptableQualities = ["1920x1080.mp4", "1280x720.mp4", "854x480.mp4", "640x360.mp4"]

    def start(self, showLink = "https://kissanime.to/Anime/Sword-Art-Online-Dub"):
        self.seriesLink = showLink
        self.findEpisodes()

    def findEpisodes(self):
        showPage = scrape.scraper.get(self.seriesLink).content
        soupShowPage = BeautifulSoup(showPage)

        self.showLinks = []
        for link in soupShowPage.findAll(attrs={'title' : re.compile("^Watch anime")}):
            output.send(link.get("href"))
            self.showLinks.append(link.get("href"))
        if parser.args.delete:
            tobeDeleted = []
            while True:
                output.send("Paste the link that you want to remove, leave blank when your done")
                removal = input()
                if removal == "": break
                try:
                    for link in self.showLinks:
                        if removal in link:
                            tobeDeleted.append(link)
                            output.send("Deleting:" + str(link))
                except:
                    output.send("Unable to find that link")

            for link in tobeDeleted:
                del self.showLinks[self.showLinks.index(link)]
            output.send("Updated list:")
        for link in self.showLinks:
            output.send(link)
        self.totalEpisodes = len(self.showLinks)
        output.send(str(self.totalEpisodes) + " episodes found")

        if self.totalEpisodes > 0:
            output.send("Starting up downloader")
            self.showLinks.reverse()
            self.findPrev()
        else:
            output.send("Unable to find episodes, is kissanime.to down or maybe your network")

    def findPrev(self):
        try:
            title = str(re.findall(r'https://kissanime.to/Anime/(.*)', self.seriesLink)[0]) + "/"
        except:
            output.send("Error with link")
            exit()
        self.downloadedEp = []
        self.convertedDownloads = []
        if not os.path.exists("Downloads"): os.makedirs("Downloads")
        os.chdir("Downloads")
        if not os.path.exists(title):
            os.makedirs(title)
            os.chdir(title)
        else:
            output.send(str(os.getcwd()))
            os.chdir(title)
            output.send(str(os.getcwd()))
            output.send("Found a previously downloaded episodes")
            self.downloadedEp = glob.glob("*")
            for ep in range(len(self.downloadedEp)):
                if not self.downloadedEp[ep].endswith(".mp4"):
                    os.remove(self.downloadedEp[ep])
                else:
                    self.convertedDownloads.append(int(self.downloadedEp[ep].replace(".mp4", "")))
            output.send("Downloaded episodes detected:" + str(self.downloadedEp))
        self.download()

    def download(self):
        for currentEp in range(1, self.totalEpisodes + 1):
            if currentEp not in self.convertedDownloads:
                # Initialization
                currentEpStr = str(currentEp)
                doubleBreak = False

                page = scrape.scraper.get(scrape.URL + self.showLinks[currentEp - 1]).content
                soupedUp = BeautifulSoup(page)

                for link in soupedUp.find_all("a"):
                    # Only take the highest quality and do a double break
                    for quality in self.acceptableQualities:
                        if str(link.text) == quality:
                            output.send("Found one!")
                            doubleBreak = True
                            break
                    hyperLink = link.get("href")
                    if doubleBreak: break
                if doubleBreak:
                    output.send("Found download for episode: " + currentEpStr + " on " + str(hyperLink))
                    output.send("Quality:" + link.text)
                    wget.download(hyperLink, currentEpStr + ".mp4")
                    print('\n')
                    output.send("Finished downloading episode:" + currentEpStr)
                    scrape.downloaded.append(currentEpStr)
                else:
                    output.send("Unable to find a link for episode: " + currentEpStr)
                    scrape.undownlodable.append(currentEpStr)

class Out:
    def send(self, msg):
        print(str(msg))

downloader = Downloader()
output = Out()
scrape = CFScrapeLogin()
parser = Parse()
handler = Thread_Handler()
