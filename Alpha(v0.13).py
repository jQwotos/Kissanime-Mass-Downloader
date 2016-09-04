'''
Author: Jason Le
Email: le.kent.jason@gmail.com
Github: jQwotos
'''
import requests, cfscrape, os, re, glob, sys, argparse, threading, wget, time
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
        parser.add_argument("-f", "--file", help="Import shows from file", type=str, nargs="?", default="null")
        parser.add_argument("-d", "--delete", help="After scanning, the program will ask you to remove extras found such as intros.", action="store_true")
        parser.add_argument("-n", "--fancyname", help="Auto name the folder without - or dub or sub", action="store_true")
        parser.add_argument("-w", "--wget", help="Use the wget module rather than requests to download", action="store_true")
        parser.add_argument("-c", "--directory", help="Specify a custom directory where the anime will be downloaded", type=str, nargs="?", default="Downloads")
        parser.add_argument("-a", "--continous", help="For series that are still airing, continue to keep folder updated", action="store_true")
        self.args = parser.parse_args()

class Thread_Handler:
    def __init__(self):
        self.toBeDownloaded = []

        # Read from input file
        if parser.args.file != "null":
            if os.path.isfile(parser.args.file):
                with open(str(parser.args.file)) as f:
                    for line in f:
                        self.toBeDownloaded.append(line.replace("\n", ""))
            else:
                output.send("Unable to find your input file")

        # Read from in-line link
        if parser.args.link != "null":
            self.toBeDownloaded.append(parser.args.link)

        if parser.args.link == "null" and parser.args.file == "null":
            self.toBeDownloaded.append(input("Please input link: "))

        # Fixes links
        for link in range(len(self.toBeDownloaded)):
            if "kissanime.to" not in self.toBeDownloaded[link]:
                self.toBeDownloaded[link] = "https://kissanime.to/Anime/" + self.toBeDownloaded[link]

        if parser.args.continous:
            while True:
                print("Running on continous update mode, press Ctrl + C to quit.")
                self.start()
                print("Waiting another hour before updating")
                time.sleep(3600) #3600
        else:
            self.start()

    def start(self):
        for dld in self.toBeDownloaded:
            print("Starting to Download: ", dld)
            downloader.start(dld)
            os.chdir("../..")
            print("Finished downloading: ", dld)

class Downloader:
    def __init__(self, showLink = "https://kissanime.to/Anime/Sword-Art-Online-Dub"):
        self.acceptableQualities = ["1920x1080.mp4", "1280x720.mp4", "854x480.mp4", "640x360.mp4", "960x720.mp4", "480x360.mp4"]

    def start(self, showLink = "https://kissanime.to/Anime/Sword-Art-Online-Dub"):
        self.seriesLink = showLink
        self.findEpisodes()

    # Find all episode links
    def findEpisodes(self):
        showPage = scrape.scraper.get(self.seriesLink).content
        soupShowPage = BeautifulSoup(showPage, "html.parser")

        # Find links to episodes and compile into self.showLinks
        self.showLinks = []
        for link in soupShowPage.findAll(attrs={'title' : re.compile("^Watch anime")}):
            output.send(link.get("href"))
            self.showLinks.append(link.get("href"))

        # Start of deletion menu
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
        # End of deletion menu

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
            title = str(re.findall(r'kissanime.to/Anime/(.*)', self.seriesLink)[0]) + "/"
            if parser.args.fancyname:
                title = title.replace("-Dub", "").replace("-Sub", "").replace("-", " ")
        except:
            output.send("Error with link")
            exit()
        self.downloadedEp = []
        self.convertedDownloads = []
        if parser.args.directory:
            print("Searching for: ", parser.args.directory)
            if not os.path.exists(parser.args.directory):
                print("Directory non existant, i'll make it for you.")
                os.makedirs(parser.args.directory)
            os.chdir(parser.args.directory)
            print("Found the directory, navigating into it.")
        else:
            print("No directory was supplied, I will be using default.")
            if not os.path.exists("Downloads"):
                os.makedirs("Downloads")
            os.chdir("Downloads")
        if not os.path.exists(title):
            os.makedirs(title)
            os.chdir(title)
        else:
            output.send(str(os.getcwd()))
            os.chdir(title)
            output.send(str(os.getcwd()))
            output.send("Found a previously downloaded episodes")
            print("I will be scanning the directory for the episodes now.")
            self.downloadedEp = glob.glob("*")
            for ep in range(len(self.downloadedEp)):
                if not self.downloadedEp[ep].endswith(".mp4"):
                    print("Deleting: ", self.downloadedEp[ep])
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
                soupedUp = BeautifulSoup(page, "html.parser")

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
                    trials = 0
                    while trials <= 3:
                        try:
                            if parser.args.wget:
                                wget.download(hyperLink, currentEpStr + ".mp4")
                            else:
                                print("Downloading using requests")
                                epiLink = currentEpStr + ".tmp"
                                request = requests.get(hyperLink, timeout=30, stream=True)
                                with open(epiLink, 'wb') as f:
                                    for chunk in request.iter_content(1024 * 1024):
                                        f.write(chunk)
                                os.rename(epiLink, currentEpStr + ".mp4")
                            break
                        except Exception as exp:
                            output.send(exp)
                            trials += 1
                            output.send("Failed to download, retrying")
                            os.remove(epiLink)


                    output.send("Finished downloading episode:" + currentEpStr)
                else:
                    output.send("Unable to find a link for episode: " + currentEpStr)

class Out:
    def send(self, msg):
        print(str(msg))

parser = Parse()
downloader = Downloader()
output = Out()
scrape = CFScrapeLogin()
handler = Thread_Handler()
