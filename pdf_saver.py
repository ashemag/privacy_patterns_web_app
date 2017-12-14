import sys
import os 
import urllib2
import time 
from collections import defaultdict, Counter 
import csv 
from bs4 import BeautifulSoup
import shutil 

PATH = 'pdfminer-20140328/_pdfs/'
BOUND = 1 

def download_file(_path, url): 
	arr = url.split('/')
	filename = arr[len(arr) - 1]
	response = urllib2.urlopen(url)
	file = open(_path + filename, 'wb') #need wb because pdfs are binary files 
	file.write(response.read())
	file.close()
	return filename 

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

def crawl(filename): 
	# delete evrything in folder to start 
	delete_folder_contents(PATH)
	# iterate through pdf with relevant URLs 
	with open(filename) as csvfile:
		reader = csv.DictReader(csvfile)
		for i, row in enumerate(reader):
			if i >= BOUND: 
				break 

			print "On case " + str(i + 1)
			folder = "case_" + str(i + 1) + "/"
			_path = PATH + folder
			organize_into_case_folder(_path, folder)
			links = find_pdfs(row['Case URL'])
			for link in links: 
				filename = download_file(_path, link)
				pdf_to_text(_path, filename)


#Downloads all pdfs from cases in data.csv and creates .txt version 
if __name__ == "__main__":
	tic = time.clock()
	crawl("data.csv")
	toc = time.clock()
	print "TOTAL TIME: " + str(round((toc - tic) * 100 / float(60), 2)) + " minutes"
