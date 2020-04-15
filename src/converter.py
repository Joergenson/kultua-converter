from src.playlist_grapper import get_uri
from src.playlist_grapper import resolutions
from src.playlist_parser import get_playlist_uris
from src.playlist_parser import get_base_url
from src.playlist_converter import fetch_all_urls
from src.playlist_converter import generate_list_of_files
import subprocess
import shutil


def convert_to_mp4_best_quality(url, name):
    res = resolutions(url)
    for resolution in res:
        print(resolution)
    uri = get_uri(res[-1], url)
    playlist_uri = get_playlist_uris(uri[0])
    fetch_all_urls(playlist_uri, get_base_url(uri[0]))
    generate_list_of_files()
    name = f"{name}.mp4"
    subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "parts.txt", "-c", "copy", name])
    shutil.rmtree("video_parts")
