#!/usr/bin/env python2
"""A set of tools for downloading and managing Google Photos"""
import os
import sys
import argparse
import json
from datetime import datetime
from collections import OrderedDict

import requests
from progressbar import ProgressBar, FormatLabel, Bar

from login import login
from gdata.photos import AnyEntryFromString

METADATA_FILENAME = "photo_metadata_{timestamp}.json"
COMMANDS = ["download", "check", "metadata"]

PBAR_WIDGETS = [FormatLabel("|%(value)d/%(max)d Albums"), Bar()]

def clear_progressbar(pbar):
    pbar.fd.write('\r' + (' ' * pbar.term_width) + '\r')

def download_metadata(gd_client):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = METADATA_FILENAME.format(timestamp=timestamp)

    print "\nDownloading metadata..."
    user_feed = gd_client.GetUserFeed().entry
    albums = OrderedDict()

    pbar = ProgressBar(widgets=PBAR_WIDGETS, maxval=len(user_feed)).start()
    for i, album in enumerate(reversed(user_feed)):
        pbar.update(i)
        album_title = album.title.text
        if album_title in albums:
            raise ValueError("Repeated album title: %s" % album_title)

        photos = gd_client.GetFeed("/data/feed/api/user/default/albumid/%s?kind=photo&imgmax=d"
                                   % album.gphoto_id.text).entry
        albums[album_title] = photos
        clear_progressbar(pbar)
        print "%s (%d photos)" % (album_title, len(albums[album_title]))
    pbar.finish()

    print "\nSaving metadata to %s..." % filename
    albums_xml = OrderedDict()
    for album in albums:
        albums_xml[album] = [photo.ToString() for photo in albums[album]]

    json.dump(albums_xml, open(filename, "w"), indent=2)
    return albums

def read_metadata(filename):
    print "\nReading metadata from %s..." % filename
    albums = json.load(open(filename), object_pairs_hook=OrderedDict)

    pbar = ProgressBar(widgets=PBAR_WIDGETS, maxval=len(albums)).start()
    for i, album in enumerate(albums):
        pbar.update(i)
        albums[album] = [AnyEntryFromString(xml) for xml in albums[album]]
        clear_progressbar(pbar)
        print "%s (%d photos)" % (album, len(albums[album]))
    pbar.finish()
    return albums

def download_photos(albums, output_folder):
    print "\nDownloading albums..."
    mkdir_if_needed(output_folder)
    download_count = 0

    pbar = ProgressBar(widgets=PBAR_WIDGETS, maxval=len(albums)).start()
    for i, album in enumerate(albums):
        clear_progressbar(pbar)
        print "%s" % album
        pbar.update(i)
        mkdir_if_needed(os.path.join(output_folder, album))
        for photo in albums[album]:
            filename = photo.title.text
            filepath = os.path.join(output_folder, album, filename)
            if os.path.exists(filepath):
                continue

            response = requests.get(photo.content.src)
            response.raise_for_status()
            with open(filepath, 'wb') as image_file:
                image_file.write(response.content)

            download_count += 1
    pbar.finish()

    print "%d photos downloaded." % download_count

def check_photos(albums, output_folder):
    print "\nChecking photos..."
    check_count = 0

    for album in albums:
        album_path = os.path.join(output_folder, album)
        if not os.path.exists(album_path):
            print "Album folder not found: %s" % album_path
            continue

        for photo in albums[album]:
            filename = photo.title.text
            photo_path = os.path.join(album_path, filename)
            if not os.path.exists(photo_path):
                print "Photo not found: %s" % photo_path
                continue

            check_size(photo, photo_path)
            check_count += 1

    print "%d photos checked." % check_count

def check_size(photo, photo_path):
    local_size = os.path.getsize(photo_path)
    remote_size = int(photo.size.text)
    if local_size != remote_size:
        print("Remote size of %s (%d) doesn't match local size (%d)" %
              (photo_path, remote_size, local_size))

def mkdir_if_needed(path):
    try:
        os.mkdir(path)
    except OSError:
        pass

def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", nargs="?", default="download",
                        help="What to do (default: 'download').")
    parser.add_argument("source", help="Either a Google email address or a previously " +
                        "downloaded metadata.json file")
    parser.add_argument("--output-folder", "-o", default=".",
                        help="Folder to store downloaded photos (default: '.').")

    options = parser.parse_args(sys.argv[1:])
    if options.command not in COMMANDS:
        parser.error("Command '%s' not recognised." % options.command)

    # Detect if an email address has been supplied
    options.is_email = ("@" in options.source)
    return options

def main():
    options = parse_arguments()
    output_folder = os.path.expanduser(options.output_folder)
    if not os.path.exists(output_folder):
        raise OSError("Output folder not found:" % output_folder)

    if options.is_email:
        gd_client = login(options.source)
        albums = download_metadata(gd_client)
    else:
        albums = read_metadata(options.source)

    if options.command == "download":
        download_photos(albums, output_folder)
    elif options.command == "check":
        check_photos(albums, output_folder)
    elif options.command == "metadata":
        pass


#############################################

if __name__ == '__main__':
    main()
