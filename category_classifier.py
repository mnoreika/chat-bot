import re
import operator
import pickle
import glob
import sys
from collections import OrderedDict

max_profile_size = 500

# Split text into tokens
def tokenise(text):
	tokens = re.findall("[a-zA-Z'`]+", text)
	tokens = [" " + token + " " for token in tokens]

	return tokens

# Find ngrams for a particu;ar token
def find_ngrams(ngrams, token, n):
	characters = list(token)

	for i in range(len(token) - n + 1):
		ngram = "".join(characters[i : i + n])
		ngrams.setdefault(ngram, 0)
		ngrams[ngram] += 1

# Generate a text profile of ngrams
def generate_text_profile(text):
	tokens = tokenise(text)

	ngrams = OrderedDict()

	for token in tokens:
		for i in range(1, 6):
			find_ngrams(ngrams, token, i)

	profile = sorted(ngrams.items(), key = operator.itemgetter(1), reverse = True)

	return profile[:max_profile_size]

# Save profile to file
def save_text_profile(file_name, text):
	with open(file_name + ".profile", 'wb') as file:
		profile = generate_text_profile(text)

		pickle.dump(profile, file)

# Load profile from file
def load_text_profile(file_name):
	with open(file_name, 'rb') as file:
		profile = pickle.load(file)		

	return profile	

# Determine the distance measure between two profiles
def calculate_profile_difference(input_profile, loaded_profile):
	difference = 0

	for i in range(len(input_profile)):
		for z in range(len(loaded_profile)):
			if (input_profile[i][0] == loaded_profile[z][0]):
				difference += abs(i - z)

	return difference

# Determine text category
def determine_text_category(text):
	input_profile = generate_text_profile(text)

	profile_scores = []

	for file_name in glob.glob('Categories/*.profile'):
		database_profile = load_text_profile(file_name)

		profile_scores.append((calculate_profile_difference(input_profile, database_profile), 
			file_name.replace("Categories/", "").replace(".profile", "")))

	profile_scores = sorted(profile_scores)

	return profile_scores[0][1]



	



