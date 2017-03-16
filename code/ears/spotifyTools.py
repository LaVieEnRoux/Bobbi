import spotipy
import cPickle as pickle
import os
import math

TRACKS_PER_CALL = 10


class SpotifySearches(object):
    '''Object with a set of methods for searching Spotify for
    music stuff.

    Ability to serialize and load all previous searches for a
    given user.'''

    def __init__(self, userID="", cachePath="", debug=False):
        self.api = spotipy.Spotify()
        self.cachePath = cachePath
        self.debug = debug

        # load prior searches if userID is given. Otherwise initialize
        # empty search cache
        if userID == "":
            self.searchCache = {}
        else:
            searchPath = os.path.join(self.cachePath, userID)
            self.searchCache = pickle.load(open(searchPath, 'rb'))

    def artist_search(self, artistName, numAlbums=10):
        '''Search for an artist, get all albums'''

        # get top search result for artist
        searchRes = self.api.search(q="artist:{}".format(artistName),
                                    type="artist")
        items = searchRes['artists']['items']

        if len(items) == 0:
            if self.debug:
                print "Found no results for search {}".format(artistName)
                return None
        artist = items[0]

        # iterate through albums and add non-duplicates to list
        allAlbums = []
        albumRes = self.api.artist_albums(artist['id'])
        allAlbums.extend(albumRes['items'])
        while albumRes['next']:
            albumRes = self.api.next(albumRes)
            allAlbums.extend(albumRes['items'])

        if self.debug:
            print "Found {} albums from search {}".format(len(allAlbums),
                                                          artistName)

        uniqueAlbumNames = set()
        uniqueAlbums = []
        for album in allAlbums:
            name = album['name'].lower()
            if name not in uniqueAlbumNames:
                uniqueAlbumNames.add(name)
                uniqueAlbums.append(album)

        return uniqueAlbums[:numAlbums]

    def album_tracks(self, albumID):
        tracks = []
        res = self.api.album_tracks(albumID)
        tracks.extend(res['items'])
        while res['next']:
            res = self.api.next(res)
            tracks.extend(res['items'])
        return tracks

    def artist_tracks(self, artistName, sortBy="popularity",
                      numAlbums=10):
        '''Return a sorted list of all tracks for a given artist
        search string. Can specify the sorting method, defaults
        to popularity.'''

        albums = self.artist_search(artistName, numAlbums=numAlbums)

        tracks = []
        for album in albums:
            tracks.extend(self.album_tracks(album['id']))

        # since album track call doesn't return track popularity, must
        # make another API call for multiple tracks to get pop numbers!
        # Also we'll limit the amount of tracks we request per call
        # to 10 so the API doesn't complain
        trackIDs = [x['id'] for x in tracks]
        numCalls = int(math.ceil(len(trackIDs) / float(TRACKS_PER_CALL)))
        fullTrackList = []
        for call in xrange(numCalls):
            lower = call * TRACKS_PER_CALL
            upper = min(len(trackIDs), (call + 1) * TRACKS_PER_CALL)
            IDsForCall = trackIDs[lower:upper]
            fullTrackList.extend(self.api.tracks(IDsForCall)['tracks'])

        if sortBy == "popularity":
            # negative sorting for decreasing order
            sortedTracks = sorted(fullTrackList, key=lambda x: -x["popularity"])
            return sortedTracks

        if self.debug:
            print "Sorting type {} is not supported!".format(sortBy)
        return tracks


if __name__ == "__main__":

    searches = SpotifySearches(debug=True)
    res = searches.artist_search("kanye west", numAlbums=2)
    for r in res:
        tracks = searches.album_tracks(r['id'])
        for t in tracks:
            print t["name"]

    print

    sortTracks = searches.artist_tracks("kanye west", numAlbums=10)
    for t in sortTracks:
        print t["name"]
