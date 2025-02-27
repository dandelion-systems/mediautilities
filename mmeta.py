'''
	This file is a demonstrator of mediameta Python package functionality.

	Copyright 2022 Dandelion Systems <dandelion.systems at gmail.com>

	mmeta parses all metadata it finds in a JPEG, HEIC, TIFF or MOV file and
	either creates a file with the same name and .metadata extension or 
	displays its findings in a standard output. Should it find GPS coordinates,
	in an image file, a link to Google Maps will be generated too.

	See the command line options for details.

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
from optparse import OptionParser
from mediameta import ImageMetadata
from mediameta import VideoMetadata
from mediameta import UnsupportedMediaFile
from mediameta import GPS_link

def get_gps_link(i:ImageMetadata) -> str:
	try:
		return GPS_link(
			lat     = i['GPSLatitude'],
			lat_ref = i['GPSLatitudeRef'],
			lng     = i['GPSLongitude'],
			lng_ref = i['GPSLongitudeRef']
		)
	except:
		return 'No GPS data.'

def main():
	opt_parser = OptionParser('Usage: %prog media_file_or_directory' + os.linesep + 'Only jpeg, heic, tiff and mov files will be processed.')
	opt_parser.add_option('-f', '--folder', help='Save metadata for all files in a folder.', action='store_true', dest='folder')
	opt_parser.add_option('-d', '--display', help='Only display metadata, do not create a file.', action='store_true', dest='display')
	opt_parser.add_option('-e', '--encoding', help='Set the code page for string values, default = utf_8.', action='store', type='string', dest='encoding', default='utf_8')
		
	try:
		(options,args) = opt_parser.parse_args(sys.argv)
		do_search_folder = options.folder
		do_display = options.display
		encoding = options.encoding
		file_or_folder_name = args[1]
	except IndexError:				# handle unknown options as OptionParser does not
		opt_parser.print_help()		# print help by default in this case
		return
	except:							# if --help is specified, OptionParser prints help 
		return						# and throws an exception. Handle it gracefully here

	if do_search_folder:
		work_range = []
		for f in os.scandir(file_or_folder_name):
			if f.is_file(follow_symlinks=False):
				work_range.append(f.path)
	else:
		work_range = [file_or_folder_name,]

	for file_name in work_range:
		try:
			# JPEG or HEIC or TIFF
			meta_data = ImageMetadata(file_name, encoding)
		except UnsupportedMediaFile:
			try:
				# MOV
				meta_data = VideoMetadata(file_name, encoding)
			except UnsupportedMediaFile:
				print('File ' + file_name + ' cannot be processed. \
					No metadata or this format is not supported.')
				continue
		
		meta_data.interpret()

		if do_display:
			print(file_name)
			print(meta_data)
			print('Maps: ' + get_gps_link(meta_data))
			print(''.ljust(10,'-'))
		else:
			file_name_no_ext, _ = os.path.splitext(file_name)
			fm = open(file_name_no_ext + '.metadata', 'w')
			fm.write(str(meta_data))
			fm.write('Maps: ' + get_gps_link(meta_data))
			fm.close()

	return

if __name__ == '__main__':
	try:
		main()
	except:
		print (sys.exc_info())
