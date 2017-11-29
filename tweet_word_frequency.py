from nltk.corpus import stopwords
from collections import Counter
import re
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
	print(alpha_text)
	return ' '.join(alpha_text).split()

class Word_Frequency:
	''' DONT FORGET TO ADD DATABASE COMPATIBILITY'''

	screen_name = ''
	words = []

	def __init__(self, screen_name, text_list):
		self.screen_name = screen_name
		# maybe add other language compatibility?
		self.words = [w for w in clean_text(combine_list(text_list)) if w not in stopwords.words('english')]

	def find_frequency(self):
		counts = Counter(self.words)
		return counts
