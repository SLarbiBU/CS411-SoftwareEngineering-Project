from flask import Flask, render_template, json, request
import requests
import oauth2
import config
app = Flask(__name__)

# Twitter authorization
def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=config.consumer_key, secret=config.consumer_secret)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=bytes(post_body, "utf-8"), headers=http_headers )
    return content

@app.route('/')
def search():
	return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def show_result():
	text = request.form['searchValue']
	url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name='
	url += text + '&include_rts=false&count=200'
	r = oauth_req(url, config.access_token, config.access_token_secret)
	tweets = json.loads(r)
	return render_template('results.html', tweets=tweets)

if __name__ == "__main__":
	app.run()

#@app.route('/results'):
#def showPost():
