from jinja2 import Environment, PackageLoader

class Report(object):
    MISSING_FOLDER = "missing_folder"
    MISSING_FILE = "missing_file"
    SIZE_MISMATCH = "size_mismatch"
    DUPLICATE_FILENAME = "duplicate_filename"

    def __init__(self, type_, **kwds):
        self.type_ = type_
        for key in kwds:
            setattr(self, key, kwds[key])

    def __repr__(self):
        return "<Report '%s'>" % self.type_

def generate_html(reports):
    env = Environment(loader=PackageLoader("gphoto_backup", "templates"))
    template = env.get_template("report.html")
    # pylint: disable=no-member
    # (https://github.com/PyCQA/pylint/issues/490)
    return template.render(reports=reports)
