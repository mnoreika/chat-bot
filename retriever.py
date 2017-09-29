import pickle
import math
import random
import glob
import re

primary_database = "Database/main.txt"

class Retriever():
	def __init__(self):
		self.database = []

	def tokenise_text(self, input):
		tokens = re.findall("[a-zA-Z'`]+", input)

		tokens = [token.lower() for token in tokens]

		return tokens

	def store_dialogues_to_database(self, file_name):
		
		with open(file_name) as file:
			sentence, response = file.readline(), file.readline()

			while response != "":
				if sentence != "\n" and response != "\n":
					self.database.append((self.tokenise_text(sentence), response.strip(), file_name))

				sentence, response = response, file.readline()

	def train_on_data(self):
		for file_name in glob.glob('Database/*.txt'):
			self.store_dialogues_to_database(file_name)

	def add_response_to_database(self, input, response):
		self.database.append((self.tokenise_text(input), response.strip()))
		
		with open("Database/main.txt", "a") as file:
			file.write("\n\n" + input + "\n" + response.strip())

	def generate_vector(self, input_sentence, db_sentence):
		vector = []

		for word in db_sentence:
			word_found = False

			for i in range(0, len(input_sentence)):
				if word == input_sentence[i]:
					vector.append(i + 1)
					word_found = True

			if not word_found:
				vector.append(0)	
	
		return vector		

	def vector_intersection(self, vector1, vector2):
		result = []

		for i in range(0, len(vector1)):
			if i == len(vector2):
				break

			if vector1[i] == vector2[i]:
				result.append(vector1[i])

		return result

	def vector_length(self, input_vector):
		length = 0

		for element in input_vector:
			length += element * element



		return 	math.sqrt(length)

	def caculalate_similarity_ratio(self, input_vector, db_vector):
		intersection = self.vector_intersection(db_vector, input_vector)
		union = list(set(db_vector) | set(input_vector))

		if (self.vector_length(union) == 0):
			return 1


		s_ratio = 1 - (self.vector_length(intersection) / self.vector_length(union))

		return s_ratio


	def retrieve_response(self, input_text):
		input_vector = self.generate_vector(input_text, input_text)

		similarity_ratios = []

		for entry in self.database:
			entry_vector = self.generate_vector(input_text, entry[0])
			similarity_ratios.append((self.caculalate_similarity_ratio(input_vector, entry_vector), entry[1], entry[2]))

		similarity_ratios = sorted(similarity_ratios)	

		responses = []
		primary_responses = []

		for i in range(0, len(similarity_ratios)):
			if similarity_ratios[i][0] == similarity_ratios[0][0]:
				if (similarity_ratios[i][2] == primary_database):
					primary_responses.append(similarity_ratios[i][1])
				else:
					responses.append(similarity_ratios[i][1])

		if (similarity_ratios[0][0] < 0.35):
			if (len(primary_responses) != 0):
				return random.choice(primary_responses)
			else:
				return random.choice(responses)	
		else:	
			return ""