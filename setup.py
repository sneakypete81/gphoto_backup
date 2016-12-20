#!/usr/bin/python2
from distutils.core import setup

setup(name="gphoto_backup",
      version="0.1.0",
      description="Maintain a local backup of your Google Photos.",
      url='https://github.com/sneakypete81/gphoto_backup',
      author='Pete Burgers',
      author_email='sneakypete81@gmail.com',
      license='GPL',
      packages=["gphoto_backup"],
      data_files=[],
      scripts=["bin/gphoto_backup"]
)
