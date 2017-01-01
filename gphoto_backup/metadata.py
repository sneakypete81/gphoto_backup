import os
import json
from collections import OrderedDict
from datetime import datetime

from progressbar import ProgressBar
from gdata.photos import AnyEntryFromString

from util import PBAR_WIDGETS, clear_progressbar

METADATA_FILENAME = "photo_metadata_{timestamp}.json"

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
        _create_unique_filename(photos)
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

def _create_unique_filename(photos):
    filenames = []
    for photo in photos:
        filename = photo.title.text
        while filename in filenames:
            root, ext = os.path.splitext(filename)
            filename = "%s_%s" % (root, ext)

        filenames.append(filename)
        photo.filename = filename

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
