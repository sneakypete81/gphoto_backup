import os

from progressbar import FormatLabel, Bar

PBAR_WIDGETS = [FormatLabel("|%(value)d/%(max)d Albums"), Bar()]

def clear_progressbar(pbar):
    pbar.fd.write('\r' + (' ' * pbar.term_width) + '\r')

def mkdir_if_needed(path):
    try:
        os.mkdir(path)
    except OSError:
        pass
