import urllib2
import os
from bs4 import BeautifulSoup
import time

WAIT_SECONDS = 2


class ReviewLoader(object):
    '''
    Parent class for review loaders for specific websites. Performs the
    saving and loading for reviews

    Args:    reviewsPath - absolute path to directory containing all reviews
                           in .txt files
    '''
    def __init__(self, reviewsPath):
        self.reviewsPath = reviewsPath

    def load_review(self, reviewName):
        '''Loads review from database'''
        try:
            with open(os.path.join(self.reviewsPath, reviewName), 'r') as f:
                reviewText = f.read()
            return reviewText
        except:
            return None

    def save_review(self, reviewText, reviewName):
        '''Saves review to database'''
        try:
            with open(os.path.join(self.reviewsPath, reviewName), 'w') as f:
                f.write(reviewText)
            return 0
        except:
            return 1  # error code of 1

    def review_exists(self, reviewName):
        '''Checks if review is already saved'''
        return os.path.isfile(os.path.join(self.reviewsPath, reviewName))


class PitchforkLoader(ReviewLoader):
    '''
    Class for loading in text from Pitchfork reviews. Able to add all
    reviews to a common serialized database of reviews, and load each
    review for a given artist.
    '''
    def __init__(self, reviewsPath, debug=False):
        ReviewLoader.__init__(self, reviewsPath)
        self.URLbase = "http://pitchfork.com"
        self.searchURL = self.URLbase + "/search/?query={}"
        self.debug = debug

    def search(self, searchString):
        '''Searches website for album reviews. Returns a list of URLs for
        all albums that result from the search'''

        if self.debug:
            print "Searching Pitchfork for: {}".format(searchString)

        searchURL = self.searchURL.format(urllib2.quote(searchString))
        request = urllib2.Request(searchURL,
                                  headers={'User-Agent': 'Magic Browser'})
        albumLinks = []
        try:
            webpage = urllib2.urlopen(request)
        except:
            if self.debug:
                print "Loading from URL {} failed!".format(searchURL)
            return None

        # parse album review URLs from search result HTML
        pageHTML = webpage.read()
        soup = BeautifulSoup(pageHTML, 'lxml')
        albums = soup.find("section", id="result-albumreviews")

        # check if page load worked
        if albums is None:
            if self.debug:
                print "search for {} yielded no albums!".format(searchString)
            return None  # loaded page has no albumreviews

        albumList = albums.find("ul")
        for album in albumList.findAll("li"):
            albumData = album.find("a", class_="album-link")
            if albumData is not None:
                albumLinks.append(self.URLbase + albumData.get("href"))

        webpage.close()

        return albumLinks

    def review_text(self, reviewURL):
        '''Returns the text for a review given the URL for the review,
        as a byte string.'''

        # set up parser
        request = urllib2.Request(reviewURL,
                                  headers={'User-Agent': 'Magic Browser'})
        webpage = urllib2.urlopen(request)
        html = webpage.read()
        soup = BeautifulSoup(html, 'lxml')

        # parse review text from html
        article = soup.find("div", class_="article-content")

        # check if load worked
        if article is None:
            return None

        articleWords = article.find("div", class_="contents dropcap")
        allParagraphs = articleWords.findAll("p")
        paragraphList = map(lambda x: x.getText(), allParagraphs)
        reviewText = " ".join(paragraphList).encode('utf-8')

        return reviewText

    def get_reviews_from_search(self, searchString):
        '''Returns a dict of all review strings for albums resulting
        from a search string. Keys are review IDs.'''

        allReviews = {}
        albumLinks = self.search(searchString)

        if albumLinks is None:
            return None

        # iterate over each album and load reviews (wait though!)
        for link in albumLinks:

            if self.debug:
                print "Loading album from URL: {}".format(link)

            reviewID = link.split("/")[-2]
            reviewText = self.review_text(link)

            if reviewText is not None:
                allReviews[reviewID] = reviewText
            elif self.debug:
                print "Loading review {} didn't work!".format(reviewID)

            # wait!! Don't request too fast!
            time.sleep(WAIT_SECONDS)

        return allReviews

    def save_reviews_from_search(self, searchString):
        '''Saves all reviews from a given search string'''

        reviewDict = self.get_reviews_from_search(searchString)

        if reviewDict is None:
            if self.debug:
                print "No reviews, skipping save section"
            return 0

        # iterate through returns reviewDicts
        success = 0
        for reviewID in reviewDict.iterkeys():
            reviewText = reviewDict[reviewID]
            ret = self.save_review(reviewText, reviewID)
            success = max(success, ret)  # success is 1 if any return fails

            if ret and self.debug:
                print "Saving review {} failed!".format(reviewID)

        return success


if __name__ == "__main__":

    loader = PitchforkLoader("/home/jon/Bobbi/data/reviews", debug=True)
    loader.save_rev
    iews_from_search("Frank Ocean")
