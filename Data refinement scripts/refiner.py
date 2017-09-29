import glob

text = ""	
counter = 0
for file_name in glob.glob('output_dial/*'):
	print(file_name)

	if (counter == 10):
		break;

	counter += 1	
	with open(file_name, "r", encoding = "ISO-8859-1") as file:

		line = file.readline()
		while line != "":
			tokens = line.split(": ")
			text += (" ".join(tokens[1:]))
			line = file.readline()
	

with open("Database/movies.txt", "w") as file2:
	file2.write(text)