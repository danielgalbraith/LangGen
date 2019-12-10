import sys
import time
import requests
from tqdm import tqdm
from lxml import html

print('Getting data from WALS...')

with open("data/wals_data.txt", "w") as f:
	chnames = []
	with open('data/qnames.txt') as infile:
		for line in infile:
			chnames.append(line.strip('\n'))
	for i in tqdm(range(0,144)):
		chnum = str(i+1)
		try:
			page = requests.get('http://wals.info/chapter/' + chnum)
		except requests.exceptions.RequestException as e:
    		print e
    		sys.exit(1)
		tree = html.fromstring(page.content)
		values = tree.xpath('//*[@class="table table-hover values"]/tbody/tr[*]/td[2]/text()')
		values = [x for x in values if not (x.isdigit() 
                                         or x[0] == '-' and x[1:].isdigit())]
		freqs = tree.xpath('//*[@class="table table-hover values"]/tbody/tr[*]/td[3]/text()')
		valuesPlusFreqs = ''
		for j in range(0,len(values)):
			valuesPlusFreqs += values[j] + '|' + freqs[j] + '|'
		f.write(str(chnum) + '|' + str(chnames[i]) + '|' + str(valuesPlusFreqs) + '\n')
		time.sleep(3)

print('Done!')