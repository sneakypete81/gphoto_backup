import os

def check_photos(albums, output_folder):
    print "\nChecking photos..."
    check_count = 0

    for album in albums:
        print "Album '%s':" % album
        album_path = os.path.join(output_folder, album)
        if not os.path.exists(album_path):
            print "Album folder not found: %s" % album_path
            continue

        for photo in albums[album]:
            photo_path = os.path.join(album_path, photo.filename)
            if not os.path.exists(photo_path):
                print "Photo not found: %s" % photo_path
                continue

            _check_size(photo, photo_path)
            _check_duplicate_filename(photo)
            check_count += 1

    print "%d photos checked." % check_count

def _check_size(photo, photo_path):
    local_size = os.path.getsize(photo_path)
    remote_size = int(photo.size.text)
    if local_size != remote_size:
        print("Remote size of %s (%d) doesn't match local size (%d)" %
              (photo_path, remote_size, local_size))

def _check_duplicate_filename(photo):
    if photo.filename != photo.title.text:
        print "Duplicate photo '%s' de-duplicated to '%s'" % (photo.title.text,
                                                              photo.filename)
