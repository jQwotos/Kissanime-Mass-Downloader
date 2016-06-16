py'''
Dependencies: Python 3.x, requests, Nodejs or PyV8, PyExecJS, BeautifulSoup4 and wget
You only need if you are using the UI rather than command line. To specify that you want to use command line add a -c to your command
Download them using:
    pip3 install requests bs4 wget

Author: Jason Le
Email: le.kent.jason@gmail.com
Github: jQwotos
'''
import requests, cfscrape, wget, os, re, glob, sys, argparse, glob
from bs4 import BeautifulSoup


class Standard:
    def __init__(self, infoDict = dict()):
        self.infoDict = infoDict
        self.infoDict['title'] = self.infoDict['title'].replace("-", " ")

        self.FindPrev()
        self.Download()

    def singleD(self, link, filename):
        name = "[Isolated Downloader]"

        if filename not in self.downloaded:
            print(name, "Downloading:", filename)
            with open(filename, 'wb') as f:
                response = requests.get(link, stream=True)

            for block in response.iter_content(1024):
                f.write(block)


    def Download(self):
        name = "[Downloader] "
        maxTrials = 3
        trials = 0
        for link, filename in self.fullDictionary['links'].items():
            while trials <= maxTrials:
                try:
                    self.singleD(link, filename)
                    break
                except:
                    trials += 1
                    print(name, "I couldn't download ", filename, " at ", link)
                    print(name, "Trial: ", trials)
        os.chdir("..")

    def FindPrev(self):
        name = "[FindPrev] "

        self.downloaded = []

        title = self.infoDict['title']
        if os.path.exists(title):
            print(name, "I found previously downloaded episodes")
            os.chdir(title)
            downloadedEp = glob.glob("*")
            for fither in downloadedEp:
                if not fither.endswith(".mp4"):
                    os.remove(fither)
                else:
                    self.downloaded.append(fither.replace(".mp4", ""))
        else:
            print(name, "I can't find previously downloaded episodes, therefor I will make a folder")
            os.mkdir(title)

# Start of link specific programs
class Primewire:
    def __init__(self):
        name = "[Primewire]"
        print(name, "I started!")
        link = input()
        self.baseLink = "http://primewire.ag"
        self.r = BeautifulSoup(requests.get(link).content)

        links = self.r.findAll("div", {"class" : "tv_episode_item"})
        for link in links:
            self.singlePage(link.a['href'])

    def singlePage(self, link):
        print(link)
        page = BeautifulSoup(requests.get(baseLink + link).content)

        links = page.findAll("table", {"class" : "movie_version"})

# End of link specific programs

class Kissanime:
    def __init__(self):
        name = "[Kissanime]"
        print(name, "I started!"
        link = input()
        self.baseLink = "https://kissanime.to"

        releaseDict = {'title': link.replace(self.baseLink, "").replace("/", "").replace("-", " ")}

        print(name, "initializing scraper")
        print(name, "this might take 5 - 10 seconds")
        self.scraper = cfscrape.create_scraper()
        USR = "Naal1933"
        PASSWD = "Naal1933"
        LoginURL = self.baseLink + "/Login"

        login_data = dict(username=USR, password=PASSWD, next='/')
        self.scraper.get(LoginURL)

        self.scraper.post(LoginURL, data=login_data, headers={"Referer": "https://google.com"})
        output.send("Logged in")

        self.r = BeautifulSoup(scraper.get(link).content)

        self.acceptableQualities = ["1920x1080.mp4", "1280x720.mp4", "854x480.mp4", "640x360.mp4"]
        for link in self.r.findAll(attrs={'title' : re.compile("^Watch anime")}):
            releaseDict['episodes'].append({link.replace(self.baseLink, "")})
