import sys
from text_parser import save_text_profile
from text_parser import load_text_profile
import glob

for file_name in glob.glob('Categories/*'):
	print (file_name)
	with open(file_name, 'r') as file:
		text = file.read()

		save_text_profile(file_name, text)


