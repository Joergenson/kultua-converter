import m3u8
import requests


def setup_m3u8(url):
    request = requests.get(url)
    m3u8_data = m3u8.loads(request.text)
    return m3u8_data


def resolutions(url):
    m3u8_data = setup_m3u8(url)
    video_resolutions = []
    for playlist in m3u8_data.playlists:
        video_resolutions.append(playlist.stream_info.resolution)
    return video_resolutions


def get_uri(resolution, url):
    uri = []
    m3u8_data = setup_m3u8(url)

    for playlist in m3u8_data.playlists:
        if playlist.stream_info.resolution == resolution:
            uri.append(playlist.uri)
    return uri
