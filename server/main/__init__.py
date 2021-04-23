import os
from flask import Flask, request, jsonify
import tweepy
from monkeylearn import MonkeyLearn

# --------------------------------------
# BASIC APP SETUP
# --------------------------------------
app = Flask(__name__, instance_relative_config=True)

# Config
app_settings = os.getenv(
    'APP_SETTINGS',
    'main.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

# Extensions
from flask_cors import CORS
CORS(app)

# Keras stuff
# global graph
# graph = get_default_graph()
# model = load_model('main/Sentiment_CNN_model.h5')
MAX_SEQUENCE_LENGTH = 300

# Twitter
auth = tweepy.OAuthHandler(app.config.get('CONSUMER_KEY'), app.config.get('CONSUMER_SECRET'))
auth.set_access_token(app.config.get('ACCESS_TOKEN'), app.config.get('ACCESS_TOKEN_SECRET'))
api = tweepy.API(auth,wait_on_rate_limit=True)
ml = MonkeyLearn(app.config.get('MONKEY_LEARN_SENTIMENT_TOKEN'))
model_id = app.config.get('MODEL_ID')
key_words_model_id = app.config.get('KEY_WORDS_MODEL_ID')


# loading tokenizer
# with open('main/tokenizer.pickle', 'rb') as handle:
#     tokenizer = pickle.load(handle)

def predict(text, include_neutral=True):
    data = []
    data.append(text)

    result = ml.classifiers.classify(model_id, data)
    label = result.body[0]['classifications'][0]['tag_name']
    score = result.body[0]['classifications'][0]['confidence']
    return {"label" : label, "score": float(score)} 


def extractKeyWords(data):
    result = ml.extractors.extract(key_words_model_id, data)
    keywords = [ extract['parsed_value'] for extract in result.body[0]['extractions'] ]
    freq = [ extract['count'] for extract in result.body[0]['extractions'] ]
    return {"keywords": keywords, "freq": freq}

@app.route('/')
def index():
    return 'Hello'

@app.route('/getsentiment', methods=['GET'])
def getsentiment():
    data = {"success": False}
    # if parameters are found, echo the msg parameter 
    if (request.args != None):
        data["predictions"] = predict(request.args.get("text"))
        data["success"] = True
    return jsonify(data)

@app.route('/analyzehashtag', methods=['GET'])
def analyzehashtag():
    positive = 0
    neutral = 0
    negative = 0
    data = []
    for tweet in tweepy.Cursor(api.search,q="#" + request.args.get("text") + " -filter:retweets",rpp=5,lang="en", tweet_mode='extended').items(100):
        prediction = predict(tweet.full_text)
        if(prediction["label"] == "Positive"):
            positive += 1
        if(prediction["label"] == "Neutral"):
            neutral += 1
        if(prediction["label"] == "Negative"):
            negative += 1
            data.append(tweet.full_text)
    key_words = extractKeyWords(data)
    print(key_words)
    return jsonify({"positive": positive, "neutral": neutral, "negative": negative})

@app.route('/gettweets', methods=['GET'])
def gettweets():
    tweets = []
    for tweet in tweepy.Cursor(api.search,q="#" + request.args.get("text") + " -filter:retweets",rpp=5,lang="en", tweet_mode='extended').items(50):
        temp = {}
        temp["text"] = tweet.full_text
        temp["username"] = tweet.user.screen_name
        # with graph.as_default():
        prediction = predict(tweet.full_text)
        temp["label"] = prediction["label"]
        temp["score"] = prediction["score"]
        tweets.append(temp)
    return jsonify({"results": tweets})
    