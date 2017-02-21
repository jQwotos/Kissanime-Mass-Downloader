import kissanimedl, logging, datetime

today = datetime.datetime.now()

logging.basicConfig(filename="%s.log" % (str(today)), level=logging.DEBUG)

s = kissanimedl.Scraper()
s.login("Naal1933", "Naal1933")

print(s.get_all_details("http://kissanime.ru/Anime/Sword-Art-Online-Dub"))
