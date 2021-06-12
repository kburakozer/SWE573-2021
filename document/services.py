import requests
import xml.etree.ElementTree as ET
from document.models import Document
import string
import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import xmltodict
from Bio import Entrez


spacy_nlp = spacy.load('en_core_web_sm')
punctuations = string.punctuation
stop_words = spacy.lang.en.stop_words.STOP_WORDS

def search(term, num_article):
	Entrez.api_key = 'f949f78d21fff30c490ba1c886fd214ae708'
	Entrez.email = 'kburakozer@yahoo.com'

	search_term = Entrez.esearch(db="pubmed", term=term, retmax=num_article)
	result = Entrez.read(search_term)
	search_term.close()
	id_list = result["IdList"]

	return id_list


	# for ids in range(0, len(id_list), 100):
	# 	details_handle = Entrez.efetch(db="pubmed",id=id_list2[ids:ids+100], retmode="xml", rettype="abstract",retmax=100)
	# 	details_xml = details_handle.read()
	# 	details = xmltodict.parse(details_xml)
	# 	article_list = details.get('PubmedArticleSet').get('PubmedArticle')
	# 	details_handle.close()
	# 	return article_list
		
def get_details(id_list):
		Entrez.api_key = 'f949f78d21fff30c490ba1c886fd214ae708'
		Entrez.email = 'kburakozer@yahoo.com'
		details_handle = Entrez.efetch(db="pubmed",id=id_list, retmode="xml", rettype="abstract",retmax=100)
		details_xml = details_handle.read()
		details = xmltodict.parse(details_xml)
		article_list = details.get('PubmedArticleSet').get('PubmedArticle')
		details_handle.close()
		return article_list


def get_pmid(article):
	id = article.get('MedlineCitation').get('PMID').get('#text')
	if id:
		return id
	else:
		return ""

def get_title(article):
	title = article.get('MedlineCitation').get('Article').get('ArticleTitle')
	if title:
		return title
	else:
		return ""


def get_date(article):
	year = article.get('MedlineCitation').get('DateRevised').get('Year')
	month = article.get('MedlineCitation').get('DateRevised').get('Month')
	day = article.get('MedlineCitation').get('DateRevised').get('Day')
	data = ""
	try:
		date = day+"."+month+"."+year
	except:
		pass
	return date


def get_author(article):
	author_list = article.get('MedlineCitation').get('Article').get('AuthorList')

	author_name = ""
	if author_list:
		for author in author_list.get('Author'):

			try:
				first_name = author.get('ForeName')
				last_name = author.get('LastName')
				full_name = first_name + " " + last_name+ ", "
				author_name += full_name
			except:
				#print("no name")
				pass
	return author_name


def get_doi(article):
	doi = ""
	try:
		doi = article.get('MedlineCitation').get('Article').get('ELocationID').get('#text')

	except:
		pass
	return doi


def get_abstract(article):

	abstract = ""
	try:
		abstract_dict = article.get('MedlineCitation').get('Article').get('Abstract').get('AbstractText')

		if type(abstract_dict) is str:
			return abstract_dict
		elif type(abstract_dict) is list:
			for item in abstract_dict:
				abstract += item.get('#text')
	except:
		pass
	return abstract


def get_keyword(article):
	keyword_list = []

	try:
		keywords = article.get('MedlineCitation').get('KeywordList').get('Keyword')
		if keywords:
			if type(keywords) is list:
			
				for item in keywords:
					keyword_list.append(item.get('#text'))
			else:

				keyword_list = keywords.get('#text').split(',')
	except:
		pass


	return keyword_list


def tokenize(abstract):
	new_s = ""
	for i in string.punctuation:
		if i != '.':
			new_s += i

	abstract = re.sub(r"[0-9]", '', abstract)
	abstract = re.sub(r'#\S+', '', abstract)
	abstract = re.sub(r'\S@\S+', '', abstract)
	abstract = re.sub(r'\S+com', '', abstract)
	table = abstract.maketrans("", "", new_s)
	abstract2 = abstract.translate(table)
	#creating token object
	tokens = spacy_nlp(abstract)

    

    #lower, strip and lemmatize
	tokens = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in tokens]
    
    #remove stopwords, and exclude words less than 2 characters
	tokens = [word for word in tokens if word not in stop_words and word not in punctuations and len(word) > 2]
	return tokens





def create_db():
    id_list = search("emotional intelligence", 60000)
    start = 0
    stop = 100
    total = int(60000/100)
    for j in range(total):
        ids = id_list[start:stop]
        start +=100
        stop += 100
        articles = get_details(ids)
        for i in (articles):
            abstract2 = get_abstract(i)
            Document.objects.create(doc_id = get_pmid(i),
            title = get_title(i),
            author = get_author(i),
            year = get_date(i),
            abstract = get_abstract(i),
            doi = get_doi(i),
            keywords = get_keyword(i),
            tokens = tokenize(abstract2))
    query_result = Document.objects.all()

    return query_result



create_db()