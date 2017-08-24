from spotify_connect_scrobbler import scrobbler, spotify, lastfm
from database import Database

from spotify_connect_scrobbler.credentials import Credentials

import sys, os, json

def start_scrobbling():
    spotify_client = spotify.SpotifyClient(
        os.environ['SPOTIFY_CLIENT_ID'],
        os.environ['SPOTIFY_CLIENT_SECRET'])
    lastfm_client = lastfm.LastfmClient(
        os.environ['LASTFM_API_KEY'],
        os.environ['LASTFM_API_SECRET'])

    db = Database(os.environ['MONGODB_URI'],
                  os.environ['MONGODB_DATABASE'],
                  os.environ['MONGODB_COLLECTION'])

    document_id = os.environ['MONGODB_DOCUMENT']
    users = db.find_credentials(document_id)['users']
    for user_id in users:
        print('Scrobble music for {}'.format(user_id))
        credentials = scrobbler.scrobble(users[user_id], spotify_client, lastfm_client)
        users[user_id] = credentials.todict()

    db.update_credentials(document_id, {'users': users})


if __name__ == "__main__":
    start_scrobbling()
