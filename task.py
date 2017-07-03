from spotify_connect_scrobbler import scrobbler
import sys, os, json

def start_scrobbling():
    scrobbler.main()

if __name__ == "__main__":
    start_scrobbling()
