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


def special_choice(data, chnum, scd):
	'''
	What to do for Q21 (dealing with Case exponence + TAM exponence tables)
	What to do for Q25 (dealing with Locus of marking + Zero marking of A and P tables)
	What to do for Q79 (dealing with Suppletion according to Tense and Aspect + Suppletion in Imperatives and Hortatives)
	What to do for Q81 (dealing with languages lacking a dominant word order)
	What to do for Q108 (dealing with Antipassive)
	What to do for Q109 (dealing with Applicative)
	What to do for Q143 (dealing with crazy negation tables)
	What to do for Q144 (dealing with crazy negation word order tables): NEED TO FIX!
	'''
	start_a = scd[chnum][0]
	end_a = scd[chnum][1]
	choice_a = random_choice(data, start_a, end_a)
	choice_string = choice_a[0]
	
	if chnum == '81':
		end_b = scd[chnum][2]
		# If lacking dominant word order, do the "languages with 2 dominant orders" table 67/189 of the time:
		if choice_a[0] == 'Lacking a dominant word order':
			rand = np.random.randint(0,189)
			if rand < 68:
				choice_b = random_choice(data, end_a, end_b)
				choice_string = str(choice_a[0] + '; ' + choice_b[0])
		return choice_string
	elif chnum == '108':
		end_b = scd[chnum][2]
		# If not lacking antipassive, do Productivity of Antipassive table:
		if choice_a[0] != 'No antipassive':
			choice_b = random_choice(data, end_a, end_b)
			choice_string = str(choice_a[0] + '; ' + choice_b[0])
		return choice_string 
	elif chnum == '109':
		end_b = scd[chnum][2]
		# If not lacking applicative, do Other Roles of Applied Objects table:
		if choice_a[0] != 'No applicative construction':
			choice_b = random_choice(data, end_a, end_b)
			choice_string = str(choice_a[0] + '; ' + choice_b[0])
		return choice_string
	elif chnum == '143':
		end_b = scd[chnum][2]
		end_c = scd[chnum][3]
		end_d = scd[chnum][4]
		choice_b = []
		choice_c = []
		# Logic for special negation settings:
		if choice_a[0] == 'Obligatory Double Negation':
			choice_b = random_choice(data, end_a, end_b)
			choice_string = str(choice_a[0] + '; ' + choice_b[0])
		elif choice_a[0] == 'Optional Double Negation':
			choice_c = random_choice(data, end_b, end_c)
			choice_string = str(choice_a[0] + '; ' + choice_c[0])
		elif choice_a[0] in ('Optional Triple Negation with Obligatory Double Negation','Optional Triple Negation with Optional Double Negation'):
			choice_d = random_choice(data, end_c, end_d)
			if len(choice_b) > 0:
				choice_string = choice_a[0] + '; ' + choice_b[0] + '; ' + choice_d[0]
			if len(choice_c) > 0:
				choice_string = choice_a[0] + '; ' + choice_c[0] + '; ' + choice_d[0]
		return choice_string
	elif chnum == '144':
		return choice_string
	else:
		end_b = scd[chnum][2]
		choice_a = random_choice(data, start_a, end_a)
		choice_b = random_choice(data, end_a, end_b)
		choice_string = str(choice_a[0] + '; ' + choice_b[0])
	return choice_string


def clean_up_tables(data, chnum, chnum_to_end_dict):
	'''
	What to do for Q10 (get rid of Nasal Vowels in West Africa)
	What to do for Q39 (get rid of table for Pama-Nyungan)
	What to do for Q58 (get rid of Number of Possessive Nouns table)
	What to do for Q90 (get rid of various subtypes of relative clauses tables): NEED TO FIX!
	What to do for Q130 (get rid of cultural categories table)
	What to do for Q136 (get rid of M in First Person Singular table)
	What to do for Q137 (get rid of M in Second Person Singular table)
	What to do for Q143 (get rid of Preverbal/Postverbal/Minor morpheme tables)
	'''
	for i in range(0, chnum_to_end_dict[chnum]):
		data.pop()
	return data


def run_langgen(in_dir, out_dir):
	with open(out_dir + 'lang.txt', "w") as f:
		chnum = ''
		chname = ''
		choice_dict = {}
		data_dict = {}
		chnames = []
		chnums = []
		chnum_to_end_dict = { 
								'10': 10,
								'39': 4,
								'58': 8,
								'90': 58,
								'130': 6,
								'136': 4,
								'137': 4,
								'143': 24
							}
		special_choice_dict = 	{ 
									'21': [2, 12, 24],
									'25': [2, 12, 16],
									'79': [2, 10, 18],
									'81': [2, 16, 26],
									'108': [2, 8, 14],
									'109': [2, 18, 26],
									'143': [2, 36, 68, 114, 126],
									'144': [2, 44]
								}
		with open(in_dir + 'wals_data.txt') as dfile:
			# Put each line of data.txt into a list of lines:
			lines = dfile.readlines()
			lines = [line.strip('\n') for line in lines]
		dfile.close()
		# Do this for each line of data:
		for j in range(0,len(lines)):
			# Split up line into list of items:
			data = lines[j].split('|')
			data.pop() # get rid of newline
			chnum = data[0]
			chname = data[1]
			# Add line to data dict:
			data_dict[chnum] = data
			# Get rid of data from irrelevant tables:
			if chnum in chnum_to_end_dict.keys():
				data = clean_up_tables(data, chnum, chnum_to_end_dict)
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
			# Special choice logic for certain features:
			if chnum in special_choice_dict.keys():
				setting = special_choice(data, chnum, special_choice_dict)
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
