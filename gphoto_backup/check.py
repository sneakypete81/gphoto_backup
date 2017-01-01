import os
from report import Report

def check_photos(albums, output_folder):
    print "\nChecking photos..."
    check_count = 0
    reports = []

    for album in albums:
        print "Album '%s':" % album
        album_path = os.path.join(output_folder, album)
        if not os.path.exists(album_path):
            print "Album folder not found: %s" % album_path
            reports.append(Report(Report.MISSING_FOLDER, album_path=album_path))
            continue

        for photo in albums[album]:
            photo_path = os.path.join(album_path, photo.filename)
            if not os.path.exists(photo_path):
                print "Photo not found: %s" % photo_path
                reports.append(Report(Report.MISSING_FILE,
                                      album=album, photo_path=photo_path))
                continue

            report = _check_size(photo, photo_path)
            if report:
                reports.append(report)

            report = _check_duplicate_filename(photo)
            if report:
                reports.append(report)

            check_count += 1

    print "%d photos checked." % check_count
    return reports

def _check_size(photo, photo_path):
    report = None
    local_size = os.path.getsize(photo_path)
    remote_size = int(photo.size.text)
    if local_size != remote_size:
        print("Remote size of %s (%d) doesn't match local size (%d)" %
              (photo_path, remote_size, local_size))
        report = Report(Report.SIZE_MISMATCH, photo=photo,
                        local_size=local_size, remote_size=remote_size)
    return report

def _check_duplicate_filename(photo):
    report = None
    if photo.filename != photo.title.text:
        print "Duplicate photo '%s' de-duplicated to '%s'" % (photo.title.text,
                                                              photo.filename)
        report = Report(Report.DUPLICATE_FILENAME, photo=photo)
    return report
