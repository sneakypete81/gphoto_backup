import os

import requests
from progressbar import ProgressBar

from util import mkdir_if_needed, PBAR_WIDGETS, clear_progressbar


def download_photos(albums, output_folder):
    print "\nDownloading albums to '%s'..." % output_folder
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
