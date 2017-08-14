from spotify_connect_scrobbler import scrobbler
import sys, os, json

def start_scrobbling():
    spotify_client = scrobbler.spotify.SpotifyClient(
        os.environ['SPOTIFY_CLIENT_ID'],
        os.environ['SPOTIFY_CLIENT_SECRET'])
    lastfm_client = scrobbler.lastfm.LastfmClient(
        os.environ['LASTFM_API_KEY'],
        os.environ['LASTFM_API_SECRET'])

    db = Database(os.environ['MONGODB_URI'],
                  os.environ['MONGODB_DATABASE'],
                  os.environ['MONGODB_COLLECTION'])

    document_id = '599205a1734d1d2227f7b033'
    users = db.find_credentials(document_id)
    for user in users:
        credentials = scrobbler.scrobbler.scrobble(document)
        user = credentials.todict()

    db.update_credentials(document_id, users)


if __name__ == "__main__":
    start_scrobbling()
