'''
	This file is a demonstrator of mediameta Python package functionality.

	Copyright 2022 Dandelion Systems <dandelion.systems at gmail.com>

    mrename uses the date and time when an image or video was taken to rename 
    the file. It operates on a folder which can contain a mixture of 
    JPEG, HEIC, TIFF and MOV files. Control the prefix, postfix and time stamp
    format through the command line options. Dry runs are possible too.

	See https://github.com/dandelion-systems/mediameta for the source code of
	the package and installation tips.
	
	mediameta is free software; you can redistribute it and/or modify
	it under the terms of the MIT License.

	mediameta is distributed in the hope that it will be useful, but
	WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	See the MIT License for more details.

	SPDX-License-Identifier: MIT
'''

import os
import sys
import shutil
import time
import uuid
from optparse import OptionParser
import mediameta as mm

def main():
    opt_parser = OptionParser('Usage: %prog [options] directory_with_images' + os.linesep + 'Only jpeg, heic, tiff and mov files will be processed.')
    opt_parser.add_option('-p', '--prefix', help='New file name prefix.', action='store', type='string', dest='prefix', default='')
    opt_parser.add_option('-f', '--postfix', help='New file name postfix.', action='store', type='string', dest='postfix', default='')
    opt_parser.add_option('-s', '--time-stamp', help='Date format for the new file name.', action='store', type='string', dest='date_format', default='%Y-%m-%d %H-%M-%S')
    opt_parser.add_option('-d', '--dry', help='Only simulate renaming.', action='store_true', dest='dry')
        
    try:
        (options,args) = opt_parser.parse_args(sys.argv)

        prefix = options.prefix
        if prefix != '':
            prefix = prefix + ' '

        postfix = options.postfix
        if postfix != '':
            postfix = ' ' + postfix

        date_format = options.date_format
        dry = options.dry
        img_dir = args[1]
    except IndexError:				# handle unknown options as OptionParser does not
        opt_parser.print_help()		# print help by default in this case
        return
    except:							# if --help is specified, OptionParser prints help 
        return						# and throws an exception. Handle it gracefully here

    file_count = 0

    for f in os.scandir(img_dir):
        if not f.is_file(follow_symlinks=False):
            continue

        current_file_path = f.path
        file_name, file_extension = os.path.splitext(current_file_path)

        if file_extension == '.metadata': # this file was generated by us on one of the previous runs, skip it
            continue

        try:
            meta_data = mm.ImageMetadata(current_file_path)              # JPEG or HEIC or TIFF
        except mm.UnsupportedMediaFile:
            try:
                meta_data = mm.VideoMetadata(current_file_path)          # MOV
            except mm.UnsupportedMediaFile:
                print('File ' + current_file_path + ' cannot be processed. No metadata or this format is not supported.')
                continue

        date_fmt = '%Y:%m:%d %H:%M:%S'
        if (date_str := meta_data['DateTimeOriginal']) is None:          # JPEG or HEIC
            if (date_str := meta_data['DateTime']) is None:              # TIFF
                date_str = meta_data['com.apple.quicktime.creationdate'] # MOV
                date_fmt = '%Y-%m-%dT%H:%M:%S%z'

        if date_str is None:
            print('File ' + current_file_path + ' cannot be processed. No date and time information found.')
            continue

        image_date = time.strptime(date_str,date_fmt)
        new_file_name = prefix + time.strftime(date_format,image_date) + postfix
        new_file_path = os.path.dirname(current_file_path) + os.sep + new_file_name
        tmp_file_path = os.path.dirname(current_file_path) + os.sep + str(uuid.uuid4())

        if dry:
            print(current_file_path + '\t' + new_file_path + file_extension)
        else:
            shutil.move(current_file_path, tmp_file_path)
            file_index = 1
            new_file_path1 = new_file_path
            while os.path.exists(new_file_path1 + file_extension):
                new_file_path1 = new_file_path + '_' + str(file_index)
                file_index += 1
            shutil.move(tmp_file_path, new_file_path1 + file_extension)
            file_count += 1

    if dry:
        print()
        print('Note: an index will be appended to the resulting file names if they are the same.')
    else:
        print('Done. ' + str(file_count) + ' files processed.')
        
if __name__ == '__main__':
    try:
        main()
    except:
        print (sys.exc_info())

            