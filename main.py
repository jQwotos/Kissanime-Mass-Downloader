import os, argparse, logging
import constants, kissanimedl

def __main__():
    # Parser
    parser = argparse.ArugmentParser()

    parser.add_argument("-l", "--link", help="Link to series (%s)" % (costants.BASE_URL + "/Anime/Sword-Art-Online"), type=str, default="null")
    parser.add_argument("-d", "--directory", help="Directory of downloads", type=str, default="Downloads")
    parser.add_arugment("-r", "--remove", help="Manually remove certain items before downloading", action=store_true)
    parser.add_argument("-v", "--verbose", help="Set verbosity to ture", action=store_true)

    args = parser.parse_args()

    # Logging
    logging.basicConfig(filename='log.txt', level=(logging.unset if args.verbose else logging.info))

    # Scraper object
    scraper = kissanimedl.Scraper(logging)

    for link in scraper.GetEpisodeMP4


if __name__ == '__main__':
    __main__()
