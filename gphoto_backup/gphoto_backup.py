#!/usr/bin/env python2
"""A set of tools for downloading and managing Google Photos"""
import os
import sys
import argparse

from progressbar import ProgressBar

from login import login
from metadata import download_metadata, read_metadata
from download import download_photos
from check import check_photos

COMMANDS = ["download", "check", "metadata"]
EPILOG = """
Commands:
    download : Download metadata and any missing photos (default).
    check    : Run some checks on the downloaded photos.
    metadata : Download metadata only.
"""

def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__, epilog=EPILOG,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("command", nargs="?", default="download",
                        help="what to do (default: 'download')")
    parser.add_argument("source", help="either a Google email address or a previously " +
                        "downloaded metadata.json file")
    parser.add_argument("--output-folder", "-o", default=".",
                        help="folder to store downloaded photos (default: '.')")

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
