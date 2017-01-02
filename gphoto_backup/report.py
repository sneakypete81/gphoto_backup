import urlparse
import urllib

from jinja2 import Environment, PackageLoader

class Report(object):
    MISSING_FOLDER = "missing_folder"
    MISSING_FILE = "missing_file"
    SIZE_MISMATCH = "size_mismatch"
    DUPLICATE_FILENAME = "duplicate_filename"

    def __init__(self, report_type, album, **kwds):
        self.report_type = report_type
        self.album = album
        for key in kwds:
            setattr(self, key, kwds[key])

    def __repr__(self):
        return "<Report '%s'>" % self.report_type

def generate_html(reports, filename):
    env = Environment(loader=PackageLoader("gphoto_backup", "templates"),
                      trim_blocks=True, lstrip_blocks=True, autoescape=True)
    template = env.get_template("report.html")

    # pylint: disable=no-member
    # (https://github.com/PyCQA/pylint/issues/490)
    with open(filename, "w") as output:
        output.write(template.render(reports=reports))

def url_from_path(path):
    return urlparse.urljoin("file:", urllib.pathname2url(path))
