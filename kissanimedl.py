'''
Name: Jason Le
Email: le.kent.jason@gmail.com
Github: jQwotos
'''

import cfscrape, os, re, logging
import constants
from bs4 import BeautifulSoup

class Scraper:
    '''
    The Kiss anime scraper.
    '''
    def __init__(self):
        # Creates a cfscraper scraper object that will be used later on
        self.scraper = cfscrape.create_scraper()
        logging.debug("Scraper has been initialized.")
        self.loggedIn = False

    def login(self, username = "", password = ""):
        if username == "" or password == "":
            logging.debug("No username or password was found when calling this function.")
            try:
                from secrets import username, password
            except ImportError:
                logging.error("Unable to find credentials, did you update secrets.py file?")

        loginData = dict(username=username, password=password, next="/")
        logging.debug("Attempted to login with credentials %s" % (loginData))
        self.scraper.post(constants.LOGIN_URL, data=login_data, headers={"Referer": "https://google.com"})
        logging.debug("Succcesfully logged in using credentials.")
        self.loggedIn = True

    # Currently not working (WIP)
    def Search(self, query = "Sword art online"):
        data = dict(keyword=query)
        resultPage = BeautifulSoup(self.scraper.post(constants.SEARCH_URL, data=data, headers={"Referer": constants.BASE_URL}).content, 'html.parser')
        return resultPage
        table = resultPage.findAll('table', {"class": "listing"})
        data = []
        for row in table.findAll("tr"):
            if 'head' not in row.get('class') and 'height: 10px' not in row.get("style"):
                link = row.get("href")
                title = row.text()

                data.append({"title": title,
                             "link": link})
        return data

    # Retrieves the individual episodes from a show link
    # requires a link as a string
    # returns a list of dictionaries [{"name": title, "link": link}]
    def get_episodes(self, link):
        resultPage = BeautifulSoup(self.scraper.get(link).content, 'html.parser')
        vids = []

        for row in resultPage.findAll(attrs={'title' : re.compile("^Watch anime")}):
            link = row.get("href")
            title = (row.text).replace('\r\n                                        ', '')
            vids.append({'name': title, 'link': link})
            logging.info("Found | %s at %s" % (title, link))
        return vids

    # takes in link for a specific episode as string
    # returns a direct link to MP4 as string
    def get_mp4(self, link):
        if not self.loggedIn:
            self.login()
        episodePage = BeautifulSoup(self.scraper.get(constants.BASE_URL + link).content, 'html.parser')
        for l in episodePage.find_all("a"):
            print(str(l.text))
            if str(l.text) in constants.ACCEPTABLE_QUALITIES:
                mp4Link = l.get("href")
                logging.info("Found quality %s" % (str(l.text)))
                return mp4Link

    def get_all_details(self, link):
        if not self.loggedIn:
            self.login()
        vids = self.get_episodes(link)
        for vid in vids:
            vid['mp4'] = self.get_mp4(vid['link'])
            logging.info("Video Details: %s" % (str(vid['mp4'])))

        return vids

    # downloads an MP4 link
    # takes in link to MP4, name of file, destination all as string
    def download(self, link, name, destination="Downloads"):
        # check to see if the path already exists, if not create it
        if not os.exists(destionation):
            os.mkdir(destination)
        # move to path
        os.chdir(destination)
        # create a get request
        download_request = self.scraper.get(link, timeout=30, stream=True)
        # write to file
        with open(name + ".tmp", 'wb') as f:
            logging.info("Downloading %s" % (name))
            for chunk in download_request.iter_content(1024 * 1024):
                f.write(chunk)
            os.rename(name + ".tmp", name + ".mp4")
