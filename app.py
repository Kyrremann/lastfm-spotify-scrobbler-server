import os

from flask import Flask, redirect, render_template, request, session
import spotify_connect_scrobbler as scrobbler
from database import Database

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'no so secret' # TODO: Pass key with env variable.

SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']

LASTFM_API_KEY = os.environ['LASTFM_API_KEY']
LASTFM_API_SECRET = os.environ['LASTFM_API_SECRET']

spotify_client = scrobbler.spotify.SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
lastfm_client = scrobbler.lastfm.LastfmClient(LASTFM_API_KEY, LASTFM_API_SECRET)

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
    # return "<a href='{}'>Authenticate Last.fm</a>".format(auth_url)
    return render_template("step.html", auth_url=auth_url, step=2)

@app.route("/steps/3")
def capture_lastfm_token():
    # Retrieve Last.fm credentials.
    token = request.args.get('token', '')
    lastfm_credentials = lastfm_client.request_access_token(token)

    # TODO: Deserialize Spotify credentials
    spotify_credentials = session['spotify_credentials']

    # TODO: Save credentials to MongoDB
    # lastfm_credentials.todict()
    # spotify_credentials
    return render_template("step.html", auth_url='', step=3)

if __name__ == "__main__":
    app.run()
