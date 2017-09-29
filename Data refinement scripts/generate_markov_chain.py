import sys

from markov import MarkovModel


markov = MarkovModel()

markov.build_chains(sys.argv[1])

markov.save_chains(sys.argv[1])

print ("Markov model was succesfully generated.")