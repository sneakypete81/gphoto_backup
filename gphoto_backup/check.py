import os
from report import Report, url_from_path

def check_photos(albums, output_folder):
    print "\nChecking photos..."
    check_count = 0
    reports = []

    for album in albums:
        print "Album '%s':" % album
        album_path = os.path.abspath(os.path.join(output_folder, album))
        if not os.path.exists(album_path):
            print "Album folder not found: %s" % album_path
            reports.append(Report(Report.MISSING_FOLDER, album=album,
                                  album_path=album_path))
            continue

        for photo in albums[album]:
            photo_path = os.path.abspath(os.path.join(album_path, photo.filename))
            if not os.path.exists(photo_path):
                print "Photo not found: %s" % photo_path
                reports.append(Report(Report.MISSING_FILE, album=album,
                                      photo_path=photo_path))
                continue

            report = _check_size(album, photo, photo_path)
            if report:
                reports.append(report)

            report = _check_duplicate_filename(album, photo)
            if report:
                reports.append(report)

            check_count += 1

    print "%d photos checked." % check_count
    return reports

def _check_size(album, photo, photo_path):
    report = None
    local_size = os.path.getsize(photo_path)
    remote_size = int(photo.size.text)
    if local_size != remote_size:
        print("Remote size of %s (%d) doesn't match local size (%d)" %
              (photo_path, remote_size, local_size))
        local_url = url_from_path(photo_path)
        remote_url = photo.content.src
        report = Report(Report.SIZE_MISMATCH, album=album, photo=photo,
                        local_size=local_size, local_url=local_url,
                        remote_size=remote_size, remote_url=remote_url)
    return report

def _check_duplicate_filename(album, photo):
    report = None
    if photo.filename != photo.title.text:
        print "Duplicate photo '%s' de-duplicated to '%s'" % (photo.title.text,
                                                              photo.filename)
        report = Report(Report.DUPLICATE_FILENAME, album=album, photo=photo)
    return report
