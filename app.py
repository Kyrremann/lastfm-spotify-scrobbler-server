from flask import Flask, redirect, render_template, request, session
import os
from spotify_connect_scrobbler.lastfm import LastfmClient
from spotify_connect_scrobbler.spotify import SpotifyClient

app = Flask(__name__)
app.secret_key = 'no so secret' # TODO: Pass key with env variable.

SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
spotify_client = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

LASTFM_API_KEY = os.environ['LASTFM_API_KEY']
LASTFM_API_SECRET = os.environ['LASTFM_API_SECRET']
lastfm_client = LastfmClient(LASTFM_API_KEY, LASTFM_API_SECRET)

import task

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/steps/1")
def enter_email():
    # Direct user to authentication Spotify URL.
    redirect_uri = "{}steps/2".format(request.url_root)
    print(redirect_uri)
    auth_url = spotify_client.request_authorization(redirect_uri)
    return render_template("step.html", auth_url=auth_url)

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
    return "<a href='{}'>Authenticate Last.fm</a>".format(auth_url)

@app.route("/steps/3")
def capture_lastfm_token():
    # Retrieve Last.fm credentials.
    token = request.args.get('token', '')
    lastfm_credentials = lastfm_client.request_access_token(token)

    # TODO: Deserialize Spotify credentials
    spotify_credentials = session['spotify_credentials']
    # TODO: Save credentials to MongoDB
    return "Last.fm credentials: {}\nSpotify credentials: {}".format(lastfm_credentials.todict(), spotify_credentials)

@app.route("/scrobble")
def manual_scrobbling():
    task.start_scrobbling()
    return redirect("/")

if __name__ == "__main__":
    app.run()