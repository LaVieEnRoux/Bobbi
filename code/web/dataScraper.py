from webTools import PitchforkLoader


def save_by_artist(artistList, saveLocation, debug=False):

    loader = PitchforkLoader("/home/jon/Bobbi/data/reviews", debug=debug)

    for artistName in artistList:
        ret = loader.save_reviews_from_search(artistName)

        if ret and debug:
            print "Loading failed for reviews for: {}".format(artistName)


def artist_list():

    # version 1
    artistList = ["kanye west", "taylor swift", "frank ocean", "rihanna",
                  "mac demarco", "daft punk", "tyler the creator",
                  "gregory porter", "bryson tiller", "stevie wonder",
                  "action bronson", "the 1975", "allen stone",
                  "ariana grande", "bon iver", "bruno mars",
                  "breakbot", "chance the rapper", "childish gambino",
                  "corinne bailey rae", "d angelo", "danny brown",
                  "dj khaled", "dwele", "the internet",
                  "isaiah rashad", "joey bada$$", "justin timberlake",
                  "kendrick lamar", "mayer hawthorne", "mick jenkins",
                  "noname", "anderson paak", "run the jewels", "st vincent",
                  "vince staples", "vulfpeck"]

    return artistList


def main():

    artistList = artist_list()
    saveLocation = "/home/jon/Bobbi/data/reviews/"
    debug = True

    save_by_artist(artistList, saveLocation, debug=debug)


if __name__ == "__main__":
    main()
