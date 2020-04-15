import requests
import m3u8


def playlist_to_m3u8(playlist_url):
    request = requests.get(playlist_url)
    playlist = m3u8.loads(request.text)
    return playlist


def get_playlist_uris(playlist_url):
    playlist_uri = []
    playlist = playlist_to_m3u8(playlist_url)
    base_url = get_base_url(playlist_url)
    for segment in playlist.segments:
        uri = segment.uri
        whole_uri = "%s%s" % (base_url, uri)
        playlist_uri.append(whole_uri)
    return playlist_uri


def get_base_url(playlist_url):
    url = str(playlist_url)
    return url.replace("index.m3u8", "")
