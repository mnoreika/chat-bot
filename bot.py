import random
import sys

from category_classifier import determine_text_category
from markov import *
from retriever import *
from eliza import *

GREETING_KEYWORDS = ("hello", "hi", "hey", "good day", "greetings")

GREETING_RESPONSE = ("Hello!", "Hi!", "Hi there!", "Hey!", "Greetings!")


FAREWELL_KEYWORDS = ("bye", "good bye", "farewell", "talk to you later", "see you")

FAREWELL_RESPONSE = ("Bye!", "See you soon.", "Good bye.", "Take care.")

# Load different modules
markov = MarkovModel()
retriever = Retriever()
eliza = Eliza()

markov.load_chains("Database/zero.ch")

retriever.train_on_data()

# Check if input contains greeting keyword
def contains_greeting(input_words):

	for word in input_words:
		if word in GREETING_KEYWORDS:
			return True

	return False	

# Check if input contains farewell keyword
def contains_farewell(input_words):

	for word in input_words:
		if word in FAREWELL_KEYWORDS:
			return True

	return False		


# Generate a response to the user
def generate_response(input):
	global end_of_conversation

	# Split the input into tokens
	input_words = re.findall("[a-zA-Z'`]+", input)

	# Make tokens lowercase
	input_words = [word.lower() for word in input_words]

	response = ""

	# Check for a greeting
	if (contains_greeting(input_words)):
		response += random.choice(GREETING_RESPONSE)

	# Check for a farewell
	elif (contains_farewell(input_words)):
		response += random.choice(FAREWELL_RESPONSE)
		end_of_conversation = True

	else:
		# Look for response in retrieval database
		retrieved_response = retriever.retrieve_response(input_words)	

		if (retrieved_response != ""):
			response += retrieved_response
		else:
			# Try to learn from the user
			reflected_response = eliza.generate_response(input, retriever)

			if (reflected_response != ""):
				response += reflected_response
			else:	
				# Generate Markov chain
				response += markov.generate_text(input_words) 

	return response




end_of_conversation = False

while not end_of_conversation:

	user_input = input()

	# If -c flag is given print out category of input
	if (len(sys.argv) > 1 and sys.argv[1] == "-c"):
		print("Category: " + determine_text_category(user_input))	


	delimiters = [',', '.', '!', '?', ';', '\n']
	sentences = []

	# Split input in to individual sentences
	sentence_start = 0
	for i in range(0, len(user_input)):

		# Add the last sentence even if delimeter is missing
		if i + 1 == len(user_input):
			sentences.append(user_input[sentence_start : len(user_input)])
			break

		# Add sentence to the list
		if user_input[i] in delimiters:
			sentences.append(user_input[sentence_start : i + 1])

			sentence_start = i + 1	

	# Generate response
	response = "-> "
	
	for sentence in sentences:
		if (sentence != ""):
			response += generate_response(sentence) + " "

	print (response)	

