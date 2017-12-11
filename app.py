# coding: utf-8

from flask import Flask
from flask import g, session, request, url_for, flash
from flask import redirect, render_template, json
from flask_oauthlib.client import OAuth
from flask_mysqldb import MySQL
from werkzeug import generate_password_hash, check_password_hash
import requests
import oauth2
import config
import movies

app = Flask(__name__)
app.debug = True
app.secret_key = config.flask_key

mysql = MySQL()

app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'MovieSearcher'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)

oauth = OAuth(app)

twitter = oauth.remote_app(
    'twitter',
    consumer_key=config.consumer_key,
    consumer_secret=config.consumer_secret,
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate'
)

#single user authentication (when twitter handle already in database)
def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=config.consumer_key, secret=config.consumer_secret)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=bytes(post_body, "utf-8"), headers=http_headers )
    return content


@twitter.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']


@app.before_request
def before_request():
    g.user = None
    if 'twitter_oauth' in session:
        g.user = session['twitter_oauth']


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showLogin')
def showLogin():
    return render_template('login.html', message=request.args.get('message'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':

        # authorize Twitter to access your account if the "Login via Twitter" button is pressed
        if request.form['login'] == "Login via Twitter":
            callback_url = url_for('oauthorized', next=request.args.get('next'))
            flash('You accept the request to sign in.')
            return twitter.authorize(callback=callback_url or request.referrer or None)

        elif request.form['login'] == "Login":
            try:
                username = request.form['inputUsername']
                password = request.form['inputPassword']

                conn = mysql.connect
                cursor = conn.cursor()
                cursor.callproc('sp_validateUser', [username])
                data = cursor.fetchall()

                if len(data) > 0:

                    # check credentials in database and see if they match
                    if check_password_hash(str(data[0][2]), password):
                        session['user'] = username
                        twit_un = str(data[0][3])

                        # check if twitter username is in database, and run request with it if it is
                        if data[0][3] is not None:
                            tweets = oauth_req("https://api.twitter.com/1.1/statuses/user_timeline.json?include_rts=false&screen_name="+twit_un, config.access_token, config.access_token_secret)
                            tweets = json.loads(tweets)
                            tweets = [t['text'] for t in tweets]

                            # get the top words used (number based on the top variable)
                            # NOTE: VALUE OF TOP CANNOT EXCEED 40; only 40 requests are allowed per 15 seconds
                            top_num = 5
                            top_words = movies.get_top_words(tweets, top_num)
                            movie_dict = movies.create_movie_dictionary(top_words)

                            return render_template('movies.html', movies=movie_dict, message="Welcome, %s" % twit_un)

                        else: # username is not in database, authenticate as if logging in with twitter
                            callback_url = url_for('oauthorized', next=request.args.get('next'))
                            flash('You accept the request to sign in.')
                            return twitter.authorize(callback=callback_url or request.referrer or None)

                    else: # credentials didn't match
                        return redirect(url_for('showLogin', message="Username/password is incorrect"))

                else: # username didn't match
                    return redirect(url_for('showLogin', message="Username/password is incorrect"))

            except Exception as e:
                return redirect(url_for('showLogin', message="An error has occurred"))

            finally:
                cursor.close()
                conn.close()

@app.route('/showSignup')
def showSignup():
    return render_template('signup.html', message=request.args.get('message'))

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['inputName']
    username = request.form['inputUsername']
    password = request.form['inputPassword']

    try:
        conn = mysql.connect
        cursor = conn.cursor()
        hashed_password = generate_password_hash(password)
        cursor.callproc('sp_createUser', [name, username, hashed_password])
        data = cursor.fetchall()

        if name and username and password and request.method == 'POST':
            if len(data) is 0:
                conn.commit()
                return redirect(url_for('showLogin', message="Successfully signed up! Login in to link your Twitter account"))

            else:
                return redirect(url_for('showSignup', message="Username already exists! Enter a valid username"))

    except Exception as e:
        return redirect(url_for('showSignup'))

    finally:
        cursor.close()
        conn.close()

@app.route('/logout')
def logout():
    session.pop('twitter_oauth', None)
    return render_template('index.html',message = 'You have logged out.')


@app.route('/oauthorized')
def oauthorized():
    resp = twitter.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.')
    else:
        session['twitter_oauth'] = resp
    return redirect(url_for('home'))
    
@app.route('/home')
def home():

    tweets = None
    if g.user is not None:
        resp = twitter.request('statuses/user_timeline.json?include_rts=false')
        if resp.status == 200:
            tweets = resp.data
        else:
            flash('Unable to load tweets from Twitter.')

    # updates database with the twitter username used to authenticate
    try:
        conn = mysql.connect 
        cursor = conn.cursor()

        # add twitter username into database to access later
        twit_un = tweets[0]["user"]["screen_name"]
        username = session.get('user')
        cursor.callproc('sp_addTwitterUser', [username, twit_un])
        conn.commit()

        # get the top words used (number based on the top variable)
        # NOTE: VALUE OF TOP CANNOT EXCEED 40; only 40 requests are allowed per 15 seconds
        tweets = [t['text'] for t in tweets]
        top_num = 5
        top_words = movies.get_top_words(tweets, top_num)
        movie_dict = movies.create_movie_dictionary(top_words)

        return render_template('movies.html',movies=movie_dict, message = 'Welcome, %s' % session['twitter_oauth']['screen_name'],tweets=tweets)

    except Exception as e:
        return (redirect(url_for('index')))

    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run()
