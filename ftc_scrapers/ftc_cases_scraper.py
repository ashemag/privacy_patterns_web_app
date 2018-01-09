import os 
import urllib2
from bs4 import BeautifulSoup
import time 
from collections import defaultdict, Counter 
#charting 
import matplotlib.pyplot as plt
#sheet 
import csv 

NO_PAGES_TO_SEARCH = 141
KEY_TAGS = ['data security', 'consumer privacy', 'privacy', 'security', 'privacy and security', 'privacy shield']
DELIM = "KEY"

# add pair count to tag network 
def count_pairs(tags, tag_network): 
	for i, elemA in enumerate(tags): 
		for j, elemB in enumerate(tags): 
			if i != j:
				tag_network[elemA + DELIM + elemB] += 1

def extract_tags(soup, analysis, tag_network): 
	divs = soup.find_all('div', class_ = 'field-name-field-tags-view')
	tags = [] 
	for div in divs: 
		for link in div.find_all('a'): 
			tag = link.contents[0].lower().strip()
			tags.append(tag) 
			analysis[tag] += 1

	count_pairs(tags, tag_network)
	return tags

#helper method to detect valid tags 
def valid_tags(tags):
	for tag in tags: 
		if tag in KEY_TAGS: 
			return True 
	return False 

#helper method to extract text from html given key 
def extract_text(soup, key): 
	text = soup.get_text().encode('utf-8')
	if key in text: 
		text = text.split(key)[1].strip().split('\n')[0].strip()
		return text 
	print key + " not available"
	return 'N/A'

def extract_case_data(case_url, data, analysis, tag_network):
	html_doc = urllib2.urlopen(case_url).read()
	soup = BeautifulSoup(html_doc, 'html.parser')
	tags = extract_tags(soup, analysis, tag_network)
	update_time = extract_text(soup, 'Last Updated:')
	case_number = extract_text(soup, 'FTC Matter/File Number:')
	if valid_tags(tags): 
		title = soup.head.title.string
		processed_title = title.split("|")[0].strip()
		data[processed_title.encode('utf-8')] = [case_url, case_number, update_time,', '.join(tags).encode('utf-8')] 	
	
#find all cases on page 
def extract_cases(url): 
	html_doc = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html_doc, 'html.parser')

	links = set()
	for link in soup.find_all('a'):
		links.add(link.get('href'))

	key = 'https://www.ftc.gov/enforcement/cases-proceedings'
	processed_links = set()
	for link in links:
		if link == None: 
			continue 
		link = link.encode("utf-8") #convert unicode -> string 
		if key in link: 
			processed_links.add(link)
	return processed_links

#helper method to get next page url in sequence 
def get_next_url(url, page_count): 
	if "?" not in url: 
		url = "https://www.ftc.gov/enforcement/cases-proceedings?page=1"
	else: 
		url = "https://www.ftc.gov/enforcement/cases-proceedings?page=" + str(page_count) 
	return url 

#extract data from page 
#move on to next page (cap exploration to 10 pages)
#print all titles of pages 1-10 
def crawl(url, tag_network): 
	data = {}
	analysis = Counter() 
	page_count = 0
	total_cases = 0 
	print "Beginning crawl..."

	while(page_count < NO_PAGES_TO_SEARCH): 
		#get cases on page 
		cases_url = extract_cases(url)	
		
		#extract data from each case page 
		for i, case_url in enumerate(cases_url):
			total_cases += 1
			print "On case " + str(i + 1) 
			extract_case_data(case_url, data, analysis, tag_network)

		print "Completed page " + str(page_count + 1)
		page_count += 1

		# get next page url 
		url = get_next_url(url, page_count)

	return data, analysis, total_cases

# to chart tag data 
def create_chart(analysis):
	print "Creating chart..."
	labels = []
	values = []
	total = 0 
	for key, value in analysis.most_common(): 
		labels.append(key.decode("utf-8"))
		values.append(value)
		total += value 
	values = [x / float(total) * 100 for x in values]
	plt.pie(values)
	plt.axis('equal')
	plt.title('FTC Case Tag Distribution', y=1.05, fontsize=15) #distance from plot and size
	plt.legend(loc="upper left", bbox_to_anchor=(0, 1.15), prop={'size': 6}, labels=['%s, %1.1f %%' % (l, s) for l, s in zip(labels, values)])
	plt.tight_layout()
	plt.show()

def create_sheet(data, filename): 
	print "Creating sheet..."
	with open(filename, 'wb') as csvfile: 
		writer = csv.writer(csvfile)
		fieldnames = ['Case Name', 'Case URL', 'Case Number', 'Last Updated', 'Tags']
		writer.writerow(fieldnames)
		for key in data: 
			entry = data[key]
			entry.insert(0, key)
			writer.writerow(entry)
		
def process_tag_network(tag_network): 
	processed_tag_network = []
	skip = set() 
	for keyA in tag_network: 
		if keyA in skip: 
			continue 

		count = tag_network[keyA]
		#extract tags from key 
		tags = keyA.split(DELIM)
		
		# form new key 
		keyB = tags[1] + DELIM + tags[0]
		
		if keyB in tag_network: 
			count += tag_network[keyB]
			skip.add(keyB)

		processed_tag_network.append([keyA, count])
	
	return processed_tag_network

def gephi_helper(network, filename): 
	with open(filename, 'wb') as csvfile: 
		writer = csv.writer(csvfile)
		fieldnames = ['Source', 'Target', 'count', 'Type']
		writer.writerow(fieldnames)
		for key, value in network: 
			arr = key.split(DELIM)
			print key 
			source, target = arr 
			writer.writerow([source, target, value, 'Undirected'])
		
if __name__ == "__main__":
	start = time.clock() 
	url = 'https://www.ftc.gov/enforcement/cases-proceedings'
	tag_network = Counter() 
	data, analysis, total_cases = crawl(url, tag_network)
	
	print "\n"
	print data 
	print "\n"
	print analysis 
	print "\n"
	print "===="
	print "\n"
	print "Total cases searched: " + str(total_cases)
	print "Number of cases involving privacy: " + str(len(data))
	
	processed_tag_network = process_tag_network(tag_network) #list of [tag1DELIMtag2, count]
	print processed_tag_network

	end = time.clock() 
	print "TOTAL TIME: " + str(end - start) #TOTAL TIME: 214.645653
	
	gephi_helper(processed_tag_network, 'network.csv')
	create_sheet(data, 'data.csv')
	create_chart(analysis)
	print "\n"
	print "==="

	