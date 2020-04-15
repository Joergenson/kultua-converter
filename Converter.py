from PlaylistGrapper import get_uri
from PlaylistGrapper import resolutions
from PlaylistParser import get_playlist_uris
from PlaylistParser import get_base_url
from PlaylistConverter import fetch_url
from PlaylistConverter import fetch_all_urls
from PlaylistConverter import generate_list_of_files
import subprocess
import shutil



def convert_to_mp4_best_quality(url, name):
    res = resolutions(url)
    for resultion in res:
        print(resultion)
    uri = get_uri(res[-1],url)
    playlist_uri = get_playlist_uris(uri[0])
    fetch_all_urls(playlist_uri, get_base_url(uri[0]))
    generate_list_of_files()
    name = "%s.mp4" % (name)
    subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "parts.txt", "-c", "copy", name])
    shutil.rmtree("video_parts")