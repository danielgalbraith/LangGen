import numpy as np
import random
import pickle
import argparse


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


def load_data(in_dir):
	with open(in_dir + 'wals_data.txt', 'r') as f:
		lines = f.readlines()
		lines = [line.strip('\n') for line in lines]
		return lines


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
	What to do for Q144 (dealing with crazy negation word order tables)
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
			if choice_b:
				choice_string = str(choice_a[0] + '; ' + choice_b[0] + '; ' + choice_d[0])
			if choice_c:
				choice_string = str(choice_a[0] + '; ' + choice_c[0] + '; ' + choice_d[0])
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
	What to do for Q90 (get rid of various subtypes of relative clauses tables)
	What to do for Q130 (get rid of cultural categories table)
	What to do for Q136 (get rid of M in First Person Singular table)
	What to do for Q137 (get rid of M in Second Person Singular table)
	What to do for Q143 (get rid of Preverbal/Postverbal/Minor morpheme tables)
	'''
	for i in range(0, chnum_to_end_dict[chnum]):
		data.pop()
	return data


def get_setting(data):
	values = []
	freqs = []
	weights = []
	for i in range(2,len(data)):
		if i % 2 == 0:
			values.append(data[i])
		else:
			freqs.append(data[i])
	for j in range(0,len(freqs)):
		weights.append(float(freqs[j]))
	for k in range(0,len(values)-1):
		normw = [w/sum(weights) for w in weights]
		feature = np.random.choice(values, 1, p=normw)
	return str(feature[0])


def remove_contradictions(choice_dict, data_dict):
	# Phonology:
	# Consonant-vowel ratio:
	# Consonant inventory:
	if choice_dict['4'] in ["No voicing contrast", "Voicing contrast in fricatives alone"]:
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
	# Pronouns
	if choice_dict['35'] == "No independent subject pronouns":
		choice_dict['39'] = "No grammaticalised marking at all"
		choice_dict['43'] = "Third person pronouns and demonstratives are unrelated to demonstratives"
		choice_dict['44'] = "No gender distinctions"
		choice_dict['45'] = "Second person pronouns encode no politeness distinction"
		choice_dict['99'] = "None"
		choice_dict['101'] = random_choice(['Pronominal subjects are expressed by affixes on verbs', '437', 'Pronominal subjects are expressed by clitics with variable host', '32', 'More than one of the above types with none dominant', '32'], 0, 6)[0]
		choice_dict['136'] = "No M-T pronouns"
		choice_dict['137'] = "No N-M pronouns"
	# Articles:
	if choice_dict['37'] in ["Definite word distinct from demonstrative", "Demonstrative word used as marker of definiteness", "Definite affix on noun"]:
		choice_dict['38'] = random_choice(data_dict['38'], 2, 10)[0]
	elif choice_dict['37'] == "No definite article but indefinite article":
		choice_dict['38'] = random_choice(data_dict['38'], 2, 8)[0]
	else:
		choice_dict['38'] = "Neither indefinite nor definite"
	# Adpositions:
	if choice_dict['48'] == "No adpositions":
		choice_dict['85'] = "No adpositions"
	else:
		choice_dict['85'] = random_choice(data_dict['85'], 2, 10)[0]
	# Tense-Aspect:
	if choice_dict['69'] == "No tense-aspect inflection":
		choice_dict['67'] == "No inflectional marking of future/non-future distinction"
	# Imperatives:
	if choice_dict['70'] == "The language has morphologically dedicated second plural imperatives but no morphologically dedicated second singular imperatives":
		choice_dict['71'] = random_choice(data_dict['71'], 6, 10)[0]
		choice_dict['72'] = random_choice(['The language has a maximal system, but not a minimal one', '133', 'The language has neither a maximal nor a minimal system', '201'], 0, 4)[0]
	elif choice_dict['70'] == "The language has no morphologically dedicated second-person imperatives at all":
		choice_dict['71'] = random_choice(data_dict['71'], 6, 10)[0]
		choice_dict['72'] = "The language has neither a maximal nor a minimal system"		
	# Evidentials:
	if choice_dict['77'] == "No grammatical evidentials":
		choice_dict['78'] = "No grammatical evidentials"
	# Word order:
	if choice_dict['81'] == "Subject-object-verb (SOV)":
		choice_dict['82'] = "Subject precedes verb (SV)"
		choice_dict['83'] = "Object precedes verb (OV)"
		choice_dict['84'] = random_choice(['Oblique-object-verb (XOV)', '48', 'Object-oblique-verb (OXV)', '27', 'Object-verb-oblique (OVX)', '45', 'More than one order with none dominant', '167'], 0, 8)[0]
		choice_dict['95'] = random_choice(['Object-verb and postpositional (OV&Postp)', '472', 'Object-verb and prepositional (OV&Prep)', '14', 'Languages not falling into one of the preceding four types', '158'], 0, 6)[0]
		choice_dict['96'] = random_choice(['Object-verb and relative clause-noun (OV&RelN)', '132', 'Object-verb and noun-relative clause (OV&NRel)', '113', 'Languages not falling into one of the preceding four types', '213'], 0, 6)[0]
		if choice_dict['96'] == "Object-verb and relative clause-noun (OV&RelN)":
			choice_dict['90'] = "Relative clause precedes noun (RelN)"
		elif choice_dict['96'] == "Object-verb and noun-relative clause (OV&NRel)":
			choice_dict['90'] = "Relative clause follows noun (NRel)"
		else:
			choice_dict['90'] = random_choice(['Internally-headed relative clause', '24', 'Correlative relative clause', '7', 'Adjoined relative clause', '8', 'Double-headed relative clause', '1', 'Mixed types of relative clause with none dominant', '64'], 0, 10)[0]
		choice_dict['97'] = random_choice(['Object-verb and adjective-noun (OV&AdjN)', '216', 'Object-verb and noun-adjective (OV&NAdj)', '332', 'Languages not falling into one of the preceding four types', '198'], 0, 6)[0]
		if choice_dict['97'] == "Object-verb and adjective-noun (OV&AdjN)":
			choice_dict['87'] = "Modifying adjective precedes noun (AdjN)"
		elif choice_dict['97'] == "Object-verb and noun-adjective (OV&NAdj)":
			choice_dict['87'] = "Modifying adjective follows noun (NAdj)"
		else:
			choice_dict['87'] = random_choice(['Both orders of noun and modifying adjective occur, with neither dominant', '110', 'Adjectives do not modify nouns, occurring as predicates in internally headed relative clauses', '5'], 0, 4)[0]
		choice_dict['144'] = random_choice(['NegSOV', '11', 'SNegOV', '15', 'SONegV', '65', 'SOVNeg', '49', 'More than one position for negative morpheme, with none dominant', '91',
			'Optional single negation', '1', 'Obligatory double negation', '101', 'Optional double negation', '67', 'Morphological negation only (but not double negation)', '333',
			'Other languages', '168'], 0, 20)[0]
	elif choice_dict['81'] == "Subject-verb-object (SVO)":
		choice_dict['82'] = "Subject precedes verb (SV)"
		choice_dict['83'] = "Object follows verb (VO)"
		choice_dict['84'] = random_choice(['Verb-object-oblique (VOX)', '210', 'Oblique-verb-object (XVO)', '3', 'More than one order with none dominant', '167'], 0, 6)[0]
		# HERE
		choice_dict['95'] = random_choice(['Object-verb and postpositional (OV&Postp)', '472', 'Object-verb and prepositional (OV&Prep)', '14', 'Languages not falling into one of the preceding four types', '158'], 0, 6)[0]
		choice_dict['96'] = random_choice(['Object-verb and relative clause-noun (OV&RelN)', '132', 'Object-verb and noun-relative clause (OV&NRel)', '113', 'Languages not falling into one of the preceding four types', '213'], 0, 6)[0]
		if choice_dict['96'] == "Object-verb and relative clause-noun (OV&RelN)":
			choice_dict['90'] = "Relative clause precedes noun (RelN)"
		elif choice_dict['96'] == "Object-verb and noun-relative clause (OV&NRel)":
			choice_dict['90'] = "Relative clause follows noun (NRel)"
		else:
			choice_dict['90'] = random_choice(['Internally-headed relative clause', '24', 'Correlative relative clause', '7', 'Adjoined relative clause', '8', 'Double-headed relative clause', '1', 'Mixed types of relative clause with none dominant', '64'], 0, 10)[0]
		choice_dict['97'] = random_choice(['Object-verb and adjective-noun (OV&AdjN)', '216', 'Object-verb and noun-adjective (OV&NAdj)', '332', 'Languages not falling into one of the preceding four types', '198'], 0, 6)[0]
		if choice_dict['97'] == "Object-verb and adjective-noun (OV&AdjN)":
			choice_dict['87'] = "Modifying adjective precedes noun (AdjN)"
		elif choice_dict['97'] == "Object-verb and noun-adjective (OV&NAdj)":
			choice_dict['87'] = "Modifying adjective follows noun (NAdj)"
		else:
			choice_dict['87'] = random_choice(['Both orders of noun and modifying adjective occur, with neither dominant', '110', 'Adjectives do not modify nouns, occurring as predicates in internally headed relative clauses', '5'], 0, 4)[0]
		choice_dict['144'] = random_choice(['NegSOV', '11', 'SNegOV', '15', 'SONegV', '65', 'SOVNeg', '49', 'More than one position for negative morpheme, with none dominant', '91',
			'Optional single negation', '1', 'Obligatory double negation', '101', 'Optional double negation', '67', 'Morphological negation only (but not double negation)', '333',
			'Other languages', '168'], 0, 20)[0]
	elif choice_dict['81'] == "Verb-subject-object (VSO)":
		...
	elif choice_dict['81'] == "Verb-object-subject (VOS)":
		...
	elif choice_dict['81'] == "Object-verb-subject (OVS)":
		...
	elif choice_dict['81'] == "Object-subject-verb (OSV)":
		...
	elif choice_dict['81'] == "Lacking a dominant word order":
		...
	elif choice_dict['81'] == "SOV or SVO":
		...
	elif choice_dict['81'] == "VSO or VOS":
		...
	elif choice_dict['81'] == "SVO or VSO":
		...
	elif choice_dict['81'] == "SVO or VOS":
		...
	else: # SOV or OVS


def write_to_file(out_dir, chnames, chnums, choice_dict, run_idx):
	with open(out_dir + ('lang_%s.txt' % run_idx), "w") as f:
		for i in range(0,len(chnames)):
			print(chnums[i] + '. ' + chnames[i] + ': ' + '\033[1m' + choice_dict[chnums[i]] + '\033[0m')
			f.write(str(chnums[i]) + '. ' + str(chnames[i]) + ': ' + str(choice_dict[chnums[i]]) + '\n')


def dump_lang_dict(out_dir, choice_dict, run_idx):
	with open(out_dir + ("lang_dict_%s.bin" % run_idx), "wb") as f:
		pickle.dump(choice_dict, f)


def generate_lang(in_dir, out_dir, run_idx, dump_dict):
	choice_dict = {}
	data_dict = {}
	chnames = []
	chnums = []
	lines = load_data(in_dir)
	for j in range(0,len(lines)):
		data = lines[j].split('|')
		data.pop() # get rid of newline
		chnum = data[0]
		chname = data[1]
		data_dict[chnum] = data
		# Get rid of data from irrelevant tables:
		if chnum in chnum_to_end_dict.keys():
			data = clean_up_tables(data, chnum, chnum_to_end_dict)
		# Get setting for current question:
		setting = get_setting(data)
		# Special choice logic for certain features:
		if chnum in special_choice_dict.keys():
			setting = special_choice(data, chnum, special_choice_dict)
		# Add settings to dictionary, add to lists of chapter numbers and names
		choice_dict[chnum] = setting
		chnames.append(chname)
		chnums.append(chnum)
	# Deal with logical contradictions here:
	remove_contradictions(choice_dict, data_dict)
	write_to_file(out_dir, chnames, chnums, choice_dict, run_idx)
	if dump_dict:
		dump_lang_dict(out_dir, choice_dict, run_idx)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input_dir", help="Directory containing input file with WALS grammar features.", default="data/")
	parser.add_argument("-o", "--output_dir", help="Output directory for language text file and dict dump.", default="output/")
	parser.add_argument("-n", "--n_runs", help="Number of times to run LangGen (default=1).", default=1)
	parser.add_argument("-d", "--dump_dict", help="Option to dump Python dictionary of language settings.", action='store_true', default=False)
	args = parser.parse_args()
	
	in_dir = args.input_dir
	out_dir = args.output_dir
	n_runs = int(args.n_runs)
	dump_dict = args.dump_dict

	for i in range(0, n_runs):
		generate_lang(in_dir, out_dir, i, dump_dict)


if __name__ == '__main__':
	main()
