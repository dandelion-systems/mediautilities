# Demonstrators of `mediameta` Python package

These Python scripts are demonstrators of mediameta Python package functionality.

Copyright 2022 Dandelion Systems <dandelion.systems at gmail.com>

See https://github.com/dandelion-systems/mediameta for the source code of
the package and installation tips.

`sample_mm_cli.py` is the minimalistic sample. It scans the local folder '.img' for JPEG, HEIC or TIFF impages and prints out their metadata into standard output. The other two Python scripts are a bit more sophisticated, see below.

## mmeta

`mmeta` parses all metadata it finds in a JPEG, HEIC, TIFF or MOV file and either creates a file with the same name and _.metadata_ extension or displays its findings in a standard output. It operates on folders or on individual files. Should it find GPS coordinates in an image file, a link to Google Maps will be generated too.

Kindly mind that there are certain metadata tags that are considered non-printable. They parsed from files anyway and you can still access them in your own code, but `mmeta` will not show them.

See the command line options for details.

Usage samples:

Print all metadata for all files in a folder into standard output:

	mmeta --display --folder ~/img

Create a _.metadata_ file for a specific image:

	mmeta ~/img/IMG005.HEIC

Display metadata for a specific image using an alternative encoding:

	mmeta --display --encoding=cp1251 ~/img/img1.jpeg

## mrename

`mrename` uses the date and time when an image or video was taken to rename the file. It operates on a folder which can contain a mixture of JPEG, HEIC, TIFF and MOV files. In case of images it looks either at _DateTimeOriginal_ EXIF tag or _DateTime_ TIFF tag. Should it encounter a MOV file, it tries to use _com.apple.quicktime.creationdate_ metadata field. 

Control the prefix, postfix and time stamp format through the command line options. Dry runs are possible too.

> Should two or more files happen to have the same name after renaming, an index will be appended at the end of the name.

Usage samples:

Rename all image and video files in a folder, use _YYYY-MM-DD HH-mm-ss_ as a new file name template:

	mrename ~/img

Do the same but with custom prefix:

	mrename --prefix="Souvenir de" ~/img

And again the same but keeping only the date, not the time in a file name:

	mrename --prefix="Souvenir de" --time-stamp=%Y-%m-%d  ~/img

