import mediameta as mm
import os

# Iterate through files in a given directory
for f in os.scandir('./img'):
	# Skip subdirectories and links
	if not f.is_file(follow_symlinks=False):
		continue

	# Try and load the metadata
	try:
		meta_data = mm.ImageMetadata(f.path)
		meta_data.interpret()
	except mm.UnsupportedMediaFile:
		print(f.path + ' - format is not supported.')
		continue

	# If success show it
	print('Metadata in ' + f.path)
	print(meta_data)