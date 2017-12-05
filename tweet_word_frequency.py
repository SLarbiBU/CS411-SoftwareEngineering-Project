from nltk.corpus import stopwords
from collections import Counter
import re

stoplist = stopwords.words('english')
STOPWORDS = """im aint arent cant couldve couldnt couldve doesnt dont gonna gotta hadnt hasnt havent hed hes howd howll im ive isnt itd itll its lets mightve shes thatll thats theyre theyve wasnt were weve werent whats whose whos wholl whyd wouldve wouldnt youll did youre youve with some your just have from"""
stoplist += STOPWORDS.split()
'''tweet_word_frequency'''

def combine_list(text_list):
	''' Combines list of tweets into 1 string
	'''
	return ' '.join(text_list)

def clean_text(text):
	''' Clean any non-alphanumeric characters and remove stop words
	'''
	alpha_text = re.split('[?.,!]', text)
	#print(alpha_text)
	alpha_text = [re.sub(r'[^a-zA-Z ]', '', t) for t in alpha_text]
	alpha_text = ' '.join(alpha_text).split()
	return [w.lower() for w in alpha_text]

class Word_Frequency:
	''' DONT FORGET TO ADD DATABASE COMPATIBILITY'''

	screen_name = ''
	words = []
	search_terms = []

	def __init__(self, text_list):
		# maybe add other language compatibility?
		self.words = [w for w in clean_text(combine_list(text_list)) if w not in stoplist]

	def find_frequency(self):
		counts = Counter(self.words)
		return counts

	def set_search_term(self):
		freq = self.find_frequency()
		self.search_terms = list(freq.keys())

	def get_most_common(self, num_words):
		freq = self.find_frequency()
		return [k for k,v in freq.most_common(num_words)]
