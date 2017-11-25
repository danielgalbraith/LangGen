from lxml import html
import requests

with open("data.txt", "w") as f:

	chnames = []
	with open('qnames.txt') as infile:
		for line in infile:
			chnames.append(line.strip('\n'))
	for i in range(0,144):
		chnum = str(i+1)
		page = requests.get('http://wals.info/chapter/' + chnum)
		tree = html.fromstring(page.content)
		values = tree.xpath('//*[@class="table table-hover values"]/tbody/tr[*]/td[2]/text()')
		values = [x for x in values if not (x.isdigit() 
                                         or x[0] == '-' and x[1:].isdigit())]
		freqs = tree.xpath('//*[@class="table table-hover values"]/tbody/tr[*]/td[3]/text()')
		valuesPlusFreqs = ''
		for j in range(0,len(values)):
			valuesPlusFreqs += values[j] + '|' + freqs[j] + '|'
		f.write(chnum.encode('utf-8') + '|' + chnames[i].encode('utf-8') + '|' + valuesPlusFreqs.encode('utf-8') + '\n')