from __future__ import print_function

import sys
import random

from fuzzywuzzy import process

from spotifyTools import SpotifySearches
from spCommands import send_command

# Python 2/3 compatibility
try:
    import Queue as q
except:
    import queue as q


RANDOM_SONGS = 10


class SpotifyController(object):
    ''' Controls Spotify using searches and the SP command line
    interface '''

    def __init__(self):

        self.search = SpotifySearches()
        self.songQueue = q.Queue()


    def _command(self, commandType, arg=""):
        ''' Wrapper for the sp command function '''

        try:
            ret = send_command(commandType, arg=arg)

        except ValueError:
            print("Invalid command type!")
            return 1

        if ret:
            print("Command failed!")
        return ret


    def play_next(self):
        ''' Play next song in the queue '''

        if not self.songQueue.empty():
            nextURI = self.songQueue.get()["uri"]
            self._command("open", arg=nextURI)


    def play_artist(self, artist_name, play_type="track", play_name="",
                    sortBy="popularity"):
        ''' Given an artist, play either an album or a track
        by them. Album name or track name can be provided, but if
        not, then first or highest ranked result will be played. '''

        if play_type == "track":

            allTracks = self.search.artist_tracks(artist_name)

            # just play a random one for now
            if play_name == "":
                randIndex = random.randint(0, RANDOM_SONGS - 1)
                playURI = allTracks[randIndex]["uri"]
                while self._command("open", arg=playURI):
                    continue

            else:
                # use fuzzy string distance
                allNames = [t["name"] for t in allTracks]
                topTrackMatch, _ = process.extractOne(play_name, allNames)
                topTrackURI = allTracks[allNames.index(topTrackMatch)]["uri"]
                while self._command("open", arg=topTrackURI):
                    continue


        elif play_type == "album":

            pass

        else:
            print("Play type {} is not supported yet!".format(play_type))


    def play_album(self, album_name, shuffle=False):

        pass


if __name__ == "__main__":

    if len(sys.argv) == 1:
        artist = "Kanye West"
    elif len(sys.argv) == 2:
        artist = sys.argv[1]
        song = ""
    elif len(sys.argv) == 3:
        artist = sys.argv[1]
        song = sys.argv[2]

    testController = SpotifyController()
    testController.play_artist(artist, play_name=song)
