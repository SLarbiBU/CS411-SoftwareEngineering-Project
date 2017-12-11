import config
import tweet_word_frequency
import oauth2
import requests
import json
from random import sample

def get_movies(search_term):
	''' Returns movies resulting from querying search term in json format
	'''
	url = "https://api.themoviedb.org/3/search/movie?api_key="+config.tmdb_key+"&language=en-US&query="+search_term
	payload = "{}"
	response = requests.request("GET", url, data=payload)
	result = json.loads(response.text)
	movie_list = result['results']
	return movie_list

def get_top_words(tweet_list, top_num):
	''' Returns list of top 'top_num' words
	'''
	tweet_freq = tweet_word_frequency.Word_Frequency(tweet_list)
	tweet_freq.set_search_term()
	most_common = tweet_freq.get_most_common(top_num)
	return most_common

def create_movie_dictionary(word_list):
	''' Returns dictionary of user's recommended movies based on results of
		querying the list of top words
	'''
	movie_dict = []
	for i in range(len(word_list)):
		# make API call using get_movies
		movie_list = get_movies(word_list[i])
		if movie_list != []:
			selected_movies = sample(range(len(movie_list)), 2 if len(movie_list) > 2 else len(movie_list))

			for j in selected_movies:
				if movie_list[j]['title'] and movie_list[j]['overview'] and movie_list[j]['vote_average'] and movie_list[j]['poster_path']:
					movie = {}
					movie['title'] = movie_list[j]['title']
					movie['description'] = movie_list[j]['overview']
					movie['vote_average'] = movie_list[j]['vote_average']
					movie['poster_path'] = "https://image.tmdb.org/t/p/w500" + movie_list[j]['poster_path']
					movie_dict.append(movie)
	return movie_dict


	