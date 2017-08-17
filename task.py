from spotify_connect_scrobbler import scrobbler
from database import Database

import sys, os, json

def start_scrobbling():
    spotify_client = scrobbler.SpotifyClient(
        os.environ['SPOTIFY_CLIENT_ID'],
        os.environ['SPOTIFY_CLIENT_SECRET'])
    lastfm_client = scrobbler.LastfmClient(
        os.environ['LASTFM_API_KEY'],
        os.environ['LASTFM_API_SECRET'])

    db = Database(os.environ['MONGODB_URI'],
                  os.environ['MONGODB_DATABASE'],
                  os.environ['MONGODB_COLLECTION'])

    document_id = os.environ['MONGODB_DOCUMENT']
    users = db.find_credentials(document_id)['users']
    for index, user_document in enumerate(users):
        credentials = scrobbler.scrobble(user_document, spotify_client, lastfm_client)
        user = credentials.todict()
        users[index] = user

    db.update_credentials(document_id, {'users': users})


if __name__ == "__main__":
    start_scrobbling()
