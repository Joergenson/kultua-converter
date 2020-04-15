import os
import requests


def fetch_url(uri, part_name):
    if not os.path.exists("video_parts"):
        os.makedirs("video_parts")
    request = requests.get(uri)
    video_name = str(uri).replace(part_name, "")
    filename = "%s.ts" % video_name
    with open(os.path.join("video_parts", filename), 'wb') as file:
        file.write(request.content)


def fetch_all_urls(uris, part_name):
    if not os.path.exists("video_parts"):
        os.makedirs("video_parts")

    for uri in uris:
        request = requests.get(uri)
        video_name = str(uri).replace(part_name, "")
        filename = "%s" % video_name
        if not os.path.isfile(filename):
            with open(os.path.join("video_parts", filename), 'wb') as file:
                file.write(request.content)


def generate_list_of_files():
    f = []
    for (dirpath, dirnames, filenames) in os.walk(os.path.join("video_parts")):
        f.extend(filenames)
        break
    with open("parts.txt", 'w') as file:
        for text in f:
            path = os.path.join("video_parts", text)
            temp_text = "file '%s'\n" % path
            file.write(temp_text)
