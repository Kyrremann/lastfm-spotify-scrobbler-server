import os

from flask import Flask, redirect, render_template, request, session
from spotify_connect_scrobbler import scrobbler, spotify, lastfm, credentials
from database import Database

app = Flask(__name__)
app.config['DEBUG'] = os.environ['DEBUG_MODE'] if 'DEBUG_MODE' in os.environ else False
app.secret_key = os.environ['APP_SECRET_KEY'] if 'APP_SECRET_KEY' in os.environ else 'no so secret'

SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']

LASTFM_API_KEY = os.environ['LASTFM_API_KEY']
LASTFM_API_SECRET = os.environ['LASTFM_API_SECRET']

spotify_client = spotify.SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
lastfm_client = lastfm.LastfmClient(LASTFM_API_KEY, LASTFM_API_SECRET)

@app.route("/")
def front_page():
    return render_template("index.html")

@app.route("/steps/1")
def enter_email():
    # Direct user to authentication Spotify URL.
    redirect_uri = "{}steps/2".format(request.url_root)
    app.logger.debug(redirect_uri)
    auth_url = spotify_client.request_authorization(redirect_uri)
    return render_template("step.html", auth_url=auth_url, step=1)

@app.route("/steps/2")
def capture_spotify_token():
    # Retrieve Spotify credentials.
    code = request.args.get('code', '')
    original_redirect_uri = "{}steps/2".format(request.url_root)
    spotify_credentials = spotify_client.request_access_token(
            code, original_redirect_uri)
    session['spotify_credentials'] = spotify_credentials.todict()

    # Direct user to authentication Last.fm URL.
    redirect_uri = "{}steps/3".format(request.url_root)
    auth_url = lastfm_client.request_authorization(redirect_uri)
    return render_template("step.html", auth_url=auth_url, step=2)

@app.route("/steps/3")
def capture_lastfm_token():
    # Retrieve Last.fm credentials.
    token = request.args.get('token', '')
    lastfm_credentials = lastfm_client.request_access_token(token)

    # TODO: Deserialize Spotify credentials
    spotify_credentials = session['spotify_credentials']

    user_credentials = credentials.Credentials.load_from_dict({'lastfm': lastfm_credentials.todict(), 'spotify': spotify_credentials})
    user_id = spotify_client.get_user_id(user_credentials.spotify)

    db = Database(os.environ['MONGODB_URI'],
                  os.environ['MONGODB_DATABASE'],
                  os.environ['MONGODB_COLLECTION'])

    document_id = os.environ['MONGODB_DOCUMENT']
    users = db.find_credentials(document_id)['users']
    users[user_id] = user_credentials.todict()
    db.update_credentials(document_id, {'users': users})
    app.logger.info('Added user {} to our scrobble list'.format(user_id))

    return render_template("step.html", auth_url='', step=3)

if __name__ == "__main__":
    app.run()
