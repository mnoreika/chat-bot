import random
import re
import pickle

class MarkovModel():

	# Build markov chains from the text corpus given
	def build_chains(self, file_name):
		input_text = ""

		with open(file_name, 'r') as file:
			line = file.readline()

			while line != "":
				input_text += line
				line = file.readline()


		tokens = re.findall("[a-zA-Z'`,.!;]+", input_text)

		tokens =  [token.lower() for token in tokens]

		chains = dict()

		# Link a pair of words in a sentence with the next word in a sequence
		for i in range(len(tokens) - 2):
			chain_key = tokens[i] + " " + tokens[i + 1]

			if chain_key in chains:
				word_exists = False

				for entry in chains[chain_key]:
					if entry[1] == tokens[i + 2]:
						entry[0] += 1

						# Sort the chains according to the frequency, highest first
						chains[chain_key].sort(key = lambda x: x[0], reverse = True)
						word_exists = True

				if not word_exists:
					chains[chain_key].append([1, tokens[i + 2]])
			else:	
				chains.setdefault(chain_key, [])
				chains[chain_key].append([1, tokens[i + 2]])
		
		# Save the chain dictionary
		self.chains = chains

	def save_chains(self, file_name):
		with open(file_name + ".ch", 'wb') as file:
			pickle.dump(self.chains, file)	


	def load_chains(self, file_name):
		with open(file_name, 'rb') as file:
			self.chains = pickle.load(file)			

	# Generate text using Markov chains
	def generate_text(self, input_words):
		# Choose response lenght at random
		length = random.randint(0, len(input_words) * 3)

		# Check if input is not too small for a seed
		if (len(input_words) > 2):
			seed = random.randint(0, len(input_words) - 2)
			word1, word2 = input_words[seed], input_words[seed + 1]
		else:
			word1, word2 = "", ""

		# If seed cannot start the chain choose a random starting point
		if (word1 + " " + word2) not in self.chains:
			key, value = random.choice(list(self.chains.items())) 
			words = key.split(" ")
			word1 = words[0]
			word2 = words[1]

		gen_text = []

		# Generate text response
		for i in range(0, length):
			gen_text.append(word1)

			if word1 + " " + word2 in self.chains:
				word1, word2 = word2, self.chains[word1 + " " + word2][0][1] 

			else:	
				return "I don't think I understand."
				
		if (len(gen_text) != 0):
			gen_text[0] = gen_text[0].title()
		else:
			return "I am sorry, what are you talking about?"	
				
		return ' '.join(gen_text) + "."	
