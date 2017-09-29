import random
import re
import json
import sys


LEARNED_RESPONSES = ("Thanks. This is helpful.", "I am learning something new every day.", "Cheers! Buddy.")


class Eliza():
	def __init__(self):
		self.load_reflection_rules("Database/reflection_rules.json")
		self.load_reflections("Database/reflections.json")

	def load_reflections(self, file_name):
		with open(file_name) as file:
			self.reflections = json.load(file)

	def load_reflection_rules(self, file_name):
		with open(file_name) as file:
			self.reflection_rules = json.load(file)

	# Reflect the tokens in the response
	def reflect(self, response):
		tokens = response.lower().split()

		for i in range(0, len(tokens)):
			if tokens[i] in self.reflections:
				tokens[i] = self.reflections[tokens[i]] 

		return " ".join(tokens)		


	# Generate a response if a pattern matches and learn from the user
	def generate_response(self, user_input, retriever):
		for sentence_pattern, responses in self.reflection_rules:
			pattern_matched = re.match(sentence_pattern, user_input.rstrip(".!?"))

			if pattern_matched:
				response = random.choice(responses)

				# Try to learn from the user
				print ("->" + response.format(*[self.reflect(g) for g in pattern_matched.groups()]))

				user_response = input()

				# Store response to the database
				retriever.add_response_to_database(user_input, user_response)

				return random.choice(LEARNED_RESPONSES)
		
		return ""	
