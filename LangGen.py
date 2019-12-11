import numpy as np
import random
import pickle
import argparse

def random_choice(data, start, end):
	sub_data = data[start:end]
	freqs = []
	values = []
	weights = []
	for i in range(0,len(sub_data)):
		if i % 2 == 0:
			values.append(sub_data[i])
		else:
			freqs.append(sub_data[i])
	for k in range(0,len(freqs)):
		weights.append(float(freqs[k]))
	normw = [w/sum(weights) for w in weights]
	feature = np.random.choice(values, 1, p=normw)
	return feature

def q21_func(data):
	# Isolate case exponence table & do random choice
	feature21a = random_choice(data, 2, 12)
	# Isolate TAM exponence table & do random choice
	feature21b = random_choice(data, 12, 24)
	# Make feature[0] a string combining choice for case & TAM tables
	feature21string = feature21a[0] + '; ' + feature21b[0]
	return(feature21string)


def q25_func(data):
	# Isolate Locus of marking table & do random choice
	feature25a = random_choice(data, 2, 12)
	# Isolate Zero marking table & do random choice
	feature25b = random_choice(data, 12, 16)
	# Make feature[0] a string combining choice for Locus of marking & Zero marking tables
	feature25string = feature25a[0] + '; ' + feature25b[0]
	return(feature25string)

def q79_func(data):
	# Isolate Suppletion in Tense and Aspect table & do random choice
	feature79a = random_choice(data, 2, 10)
	# Isolate Suppletion in Imperatives and Hortatives table & do random choice
	feature79b = random_choice(data, 10, 18)
	# Make feature[0] a string combining choice for Suppletion tables
	feature79string = feature79a[0] + '; ' + feature79b[0]
	return(feature79string)

def q81_func(data):
	# Isolate main word orders table and do random choice
	feature81a = random_choice(data, 2, 16)
	# If lacking dominant word order, do the "languages with 2 dominant orders" table 67/189 of the time:
	feature81b = []
	if feature81a[0] == 'Lacking a dominant word order':
		rand = np.random.randint(0,189)
		if rand < 68:
			feature81b = random_choice(data, 16, 26)
	# Make feature[0] a string combining choice for dominant word order tables
	feature81string = feature81a[0]
	if len(feature81b) > 0:
		feature81string = feature81a[0] + '; ' + feature81b[0]
	return(feature81string)

def q108_func(data):
	# Isolate Antipassive table & do random choice
	feature108a = random_choice(data, 2, 8)
	# If not lacking antipassive, do Productivity of Antipassive table:
	feature108b = []
	if feature108a[0] != 'No antipassive':
		feature108b = random_choice(data, 8, 14)
	# Make feature[0] a string combining choice for Antipassive tables
	feature108string = feature108a[0]
	if len(feature108b) > 0:
		feature108string = feature108a[0] + '; ' + feature108b[0]
	return(feature108string)

def q109_func(data):
	# Isolate Applicatives table & do random choice
	feature109a = random_choice(data, 2, 18)
	# If not lacking applicative, do Other Roles of Applied Objects table:
	feature109b = []
	if feature109a[0] != 'No applicative construction':
		feature109b = random_choice(data, 18, 26)
	# Make feature[0] a string combining choice for Applicative tables
	feature109string = feature109a[0]
	if len(feature109b) > 0:
		feature109string = feature109a[0] + '; ' + feature109b[0]
	return(feature109string)

def q143_func(data):
	# Isolate main negation types table & do random choice
	feature143a = random_choice(data, 2, 36)
	# If obligatory double negation, do following:
	feature143b = []
	if feature143a[0] == 'Obligatory Double Negation':
		feature143b = random_choice(data, 36, 68)
	# If optional double negation, do following:
	feature143c = []
	if feature143a[0] == 'Optional Double Negation':
		feature143c = random_choice(data, 68, 114)
	# If optional triple negation, do following:
	feature143d = []
	if feature143a[0] in ('Optional Triple Negation with Obligatory Double Negation','Optional Triple Negation with Optional Double Negation'):
		feature143d = random_choice(data, 114, 126)
	# Make feature[0] a string combining choice for all tables in Ch 143:
	feature143string = feature143a[0]
	if len(feature143b) > 0:
		feature143string = feature143a[0] + '; ' + feature143b[0]
	if len(feature143c) > 0:
		feature143string = feature143a[0] + '; ' + feature143c[0]
	if len(feature143d) > 0:
		if len(feature143b) > 0:
			feature143string = feature143a[0] + '; ' + feature143b[0] + '; ' + feature143d[0]
		if len(feature143c) > 0:
			feature143string = feature143a[0] + '; ' + feature143c[0] + '; ' + feature143d[0]
	return(feature143string)

def q144_func(data):
	# Isolate main negation types table & do random choice
	feature144 = random_choice(data, 2, 44)
	feature144string = feature144[0]
	return(feature144string)

def run_langgen(in_dir, out_dir):
	with open(out_dir + 'lang.txt', "w") as f:
		chnum = ''
		chname = ''
		choice_dict = {}
		data_dict = {}
		chnames = []
		chnums = []
		with open(in_dir + 'wals_data.txt') as dfile:
			# Put each line of data.txt into a list of lines:
			lines = dfile.readlines()
			lines = [line.strip('\n') for line in lines]
		dfile.close()
		# Do this for each line of data:
		for j in range(0,len(lines)):
			# Split up line into list of items:
			data = lines[j].split('|')
			data.pop()
			chnum = data[0]
			chname = data[1]
			# Add line to data dict:
			data_dict[chnum] = data
			# What to do for Q10 (get rid of Nasal Vowels in West Africa):
			if chnum == '10':
				for y in range(0,10):
					data.pop()
			# What to do for Q39 (get rid of table for Pama-Nyungan):
			if chnum == '39':
				for z in range(0,4):
					data.pop()
			# What to do for Q58 (get rid of Number of Possessive Nouns table):
			if chnum == '58':
				for q in range(0,8):
					data.pop()
			# What to do for Q90 (get rid of various subtypes of relative clauses tables): NEED TO FIX!
			if chnum == '90':
				for q in range(0,58):
					data.pop()
			# What to do for Q130 (get rid of cultural categories table):
			if chnum == '130':
				for q in range(0,6):
					data.pop()
			# What to do for Q136 (get rid of M in First Person Singular table):
			if chnum == '136':
				for q in range(0,4):
					data.pop()
			# What to do for Q137 (get rid of M in Second Person Singular table):
			if chnum == '137':
				for q in range(0,4):
					data.pop()
			# What to do for Q143 (get rid of Preverbal/Postverbal/Minor morpheme tables):
			if chnum == '143':
				for q in range(0,24):
					data.pop()
			# Get setting for current question:
			values = []
			freqs = []
			weights = []
			for i in range(2,len(data)):
				if i % 2 == 0:
					values.append(data[i])
				if i % 2 != 0:
					freqs.append(data[i])
			for k in range(0,len(freqs)):
				weights.append(float(freqs[k]))
			for x in range(0,len(values)-1):
				normw = [w/sum(weights) for w in weights]
				feature = np.random.choice(values, 1, p=normw)
			setting = ''
			setting += feature[0]
			# What to do for Q21 (dealing with Case exponence + TAM exponence tables):
			if chnum == '21':
				setting = q21_func(data)
			# What to do for Q25 (dealing with Locus of marking + Zero marking of A and P tables):
			if chnum == '25':
				setting = q25_func(data)
			# What to do for Q79 (dealing with Suppletion according to Tense and Aspect + Suppletion in Imperatives and Hortatives):
			if chnum == '79':
				setting = q79_func(data)
			# What to do for Q81 (dealing with languages lacking a dominant word order):
			if chnum == '81':
				setting = q81_func(data)
			# What to do for Q108 (dealing with Antipassive):
			if chnum == '108':
				setting = q108_func(data)
			# What to do for Q109 (dealing with Applicative):
			if chnum == '109':
				setting = q109_func(data)
			# What to do for Q143 (dealing with crazy negation tables):
			if chnum == '143':
				setting = q143_func(data)
			# What to do for Q144 (dealing with crazy negation word order tables): NEED TO FIX!
			if chnum == '144':
				setting = q144_func(data)
			# Add settings to dictionary, add to lists of chapter numbers and names
			choice_dict[chnum] = setting
			chnames.append(chname)
			chnums.append(chnum)
		# Deal with logical contradictions here:
		# Phonology:
		# Consonant-vowel ratio:
		# Consonant inventory:
		if choice_dict['4'] == "No voicing contrast" or choice_dict['4'] == "Voicing contrast in fricatives alone":
			choice_dict['5'] = random_choice(['Other', '242', 'Missing /p/', '33'], 0, 4)[0]
			choice_dict['7'] = random_choice(['No glottalized consonants', '409', 'Ejectives only', '58', 'Glottalized resonants only', '4', 'Ejectives and glottalized resonants', '20'], 0, 8)[0]
		# Case-marking:
		if choice_dict['49'] == "No morphological case-marking":
			choice_dict['28'] = "Inflectional case marking is absent or minimal"
			choice_dict['50'] = "No morphological case-marking"
			choice_dict['51'] = "Neither case affixes nor adpositional clitics"
			choice_dict['98'] = "Neutral"
			choice_dict['99'] = random_choice(data_dict['99'], 2, 6)[0]
		# Genders:
		if choice_dict['30'] == "None":
			choice_dict['31'] = "No gender system"
			choice_dict['32'] = "No gender system"
		# Plurals:
		if choice_dict['33'] == "No plural":
			choice_dict['34'] = "No nominal plural"
			choice_dict['36'] = random_choice(data_dict['36'], 4, 10)[0]
		# Output to terminal and file
		for i in range(0,len(chnames)):
			print(chnums[i] + '. ' + chnames[i] + ': ' + '\033[1m' + choice_dict[chnums[i]] + '\033[0m')
			f.write(str(chnums[i]) + '. ' + str(chnames[i]) + ': ' + str(choice_dict[chnums[i]]) + '\n')

	with open(out_dir + "lang_dict.bin", "wb") as f:
		pickle.dump(choice_dict, f)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input_dir", help="Directory containing input file with WALS grammar features.", default="data/")
	parser.add_argument("-o", "--output_dir", help="Output directory for language text file and dict dump.", default="output/")
	args = parser.parse_args()
	
	in_dir = args.input_dir
	out_dir = args.output_dir

	run_langgen(in_dir, out_dir)


if __name__ == '__main__':
	main()
