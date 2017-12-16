import sys
import os 
import urllib2
import time 
from collections import defaultdict, Counter 
import csv 
from bs4 import BeautifulSoup
import shutil 

'''
1. Downloads all pdfs from cases in data.csv and creates .txt version 
2. Finds following features in text: 
	-Complaint types: If COMPLAINT is written in first X characters, extract VIOLATIONS AGAINST Y ACT 
	-Decision: If DECISION Is written in first X characters, extract it is ordered, it is further ordered 
	 
'''

PATH = 'pdfminer-20140328/_pdfs/'

#downloads pdf files from ftc site 
def download_file(_path, url): 
	arr = url.split('/')
	filename = arr[len(arr) - 1]
	response = urllib2.urlopen(url)
	file = open(_path + filename, 'wb') #need wb because pdfs are binary files 
	file.write(response.read())
	file.close()
	return filename 

#finds all links that are pdfs on ftc page 
def find_pdfs(url): 
	html_doc = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html_doc, 'html.parser')
	links = set() 
	for link in soup.find_all('a'):
		_link = link.get('href')
		end = str(_link)[-4:]
		if end == '.pdf': 
			links.add(_link)
	return links

# pdfminer command 
def pdf_to_text(_path, filename): 
	filename_txt = filename[:-4] + ".txt"
	os.system("pdf2txt.py -o" + _path + filename_txt + " " + _path + filename)

#HELPER: deletes all items in foler
def delete_folder_contents(folder): 
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path): shutil.rmtree(file_path)
		except Exception as e:
			print(e)

# creates case_X folders 
def organize_into_case_folder(_path, folder): 
	if not os.path.exists(PATH + folder):
		os.makedirs(_path)
	else: 
		delete_folder_contents(_path)

def extract_complaint(data, filename, feature_data): 
	if "COMPLAINT" in data: 
		print "Complaint doc found: " + filename
		arr = data.split("\n")
		for line in arr: 
			if "violations" in line.lower() or "violation" in line.lower(): 
				if feature_data == None: 
					feature_data = {} #unclear why case 5 has feature_data = NONETYPE 
				if 'complaint' in feature_data: 
					entry = feature_data['complaint']
					feature_data = entry.append(line)
				else: 
					feature_data['complaint'] = [line]

def extract_decisions(data, filename, feature_data): 
	if "DECISION AND ORDER" in data: 
		print "Decisions doc found: " + filename 
		arr = data.split("IT IS")
		decision_data = []
		for elem in arr:
			if "ORDERED" in elem: 
				decision_data.append(elem.strip())
		feature_data['decisions'] = '\nDELIM\n'.join(decision_data)

def extract_features(_path): 
	arr = os.listdir(_path) 
	f = []
	for filename in arr: 
		if filename[-4:] == ".txt": 
			f.append(filename)
	
	feature_data = {}
	for filename in f: 
		with open(_path + filename, 'r') as file:
			data = file.read() 
			extract_complaint(data, filename, feature_data)
			extract_decisions(data, filename, feature_data) 
	
	return feature_data 

def create_sheet(filename = "feature_data.csv"): 
	print "Creating sheet..."
	with open(filename, 'wb') as csvfile: 
		writer = csv.writer(csvfile)
		fieldnames = ['Case URL', 'Complaint', 'Decisions']
		writer.writerow(fieldnames)
		# for entry in data: 
		# 	writer.writerow([entry['case_url'], ', '.join(entry['complaint']), entry['decisions']])
			
# main 
def crawl(filename): 
	# delete everything in folder to start 
	delete_folder_contents(PATH)
	create_sheet()
	data = []

	# iterate through pdf with relevant URLs 
	with open(filename) as csvfile:
		reader = csv.DictReader(csvfile)
		for i, row in enumerate(reader):
			# if i < 5: 
			# 	continue 
			# if i >= BOUND: 
			# 	break 

			print "On case " + str(i + 1)
			folder = "case_" + str(i + 1) + "/"
			_path = PATH + folder
			organize_into_case_folder(_path, folder)
			case_url = row['Case URL']
			links = find_pdfs(case_url)
			
			print "Starting pdf download..."
			for link in links: 
				arr = link.split('/')
				name = arr[len(arr) - 1]
				if "cmpt" in name or "cmplt" in name or "do" in name or "decision" in name or "complaint" in name or "order" in name.lower(): 
					print name 
					filename = download_file(_path, link)
					pdf_to_text(_path, filename)
			
			print "Beginning data mining..."
			# search through all .txts to extra data 
			feature_data = extract_features(_path)
			
			if 'complaint' not in feature_data: 
				feature_data['complaint'] = ['N/A']
			if 'decisions' not in feature_data: 
				feature_data['decisions'] = 'N/A'
			
			feature_data['case_url'] = case_url 
			print feature_data 

			#append to csv 
			with open('feature_data.csv', 'ab') as csvfile: 
				writer = csv.writer(csvfile, lineterminator='\n')
				print "Writing row..."
				text = str(feature_data['decisions'])
				text = text.replace("\n", " ")
				text = text.replace("\r", " ")
				text = text.replace(",", " ")
				writer.writerow([feature_data['case_url'], ', '.join(feature_data['complaint']), text])

#driver 
if __name__ == "__main__":
	tic = time.clock()
	crawl("data.csv")
	toc = time.clock()
	print "TOTAL TIME: " + str(round((toc - tic) * 100 / float(60), 2)) + " minutes"
