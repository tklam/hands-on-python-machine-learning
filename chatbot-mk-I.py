import random
import os
import re
import nltk

# hey this chatbot is painfully slow, so slow...
# why? please try to improve it

# download pre-built model data (need to run this only once)
#os.environ['NLTK_DATA'] = os.getcwd() + './nltk_data/'
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('twitter_samples')

from nltk.corpus import twitter_samples
from textblob import TextBlob

TWEETS = twitter_samples.strings('positive_tweets.json')

def preprocess_text(sentence):
    cleaned = []
    words = sentence.split(' ')
    for w in words:
        if w == 'i':
            w = 'I'
        if w == "i'm":
            w = "I'm"
        cleaned.append(w)
    return ' '.join(cleaned)

def compose_response(pronouns, nouns, adjectives, verbs):
    about_me = False
    about_user = False
    if 'You' in pronouns or 'you' in pronouns or 'Jarvis' in nouns or 'jarvis' in nouns:
        # The user has just talked about me
        about_me = True
    if 'I' in pronouns or 'i' in pronouns:
        # The user has just talked about itself
        about_user = True

    # find replies about 'You' or 'I' or 'both'
    reply_candidates = set([])
    reply_candidates_add = reply_candidates.add
    for t in TWEETS:
        reply_pronouns, reply_nouns, reply_adjectives, reply_verbs = tag_part_of_speech(TextBlob(t))
        if about_user and about_me:
            if ('I' in reply_pronouns or 'i' in reply_pronouns) and ('You' in reply_pronouns or 'you' in reply_pronouns) :
                reply_candidates_add(t)
        elif about_me:
            if 'I' in reply_pronouns or 'i' in reply_pronouns :
                reply_candidates_add(t)
        elif about_user:
            if 'You' in reply_pronouns or 'you' in reply_pronouns :
                reply_candidates_add(t)

    # find replies about the noun
    noun_reply_candidates = set([])
    noun_reply_candidates_add = noun_reply_candidates.add
    for t in TWEETS:
        reply_pronouns, reply_nouns, reply_adjectives, reply_verbs = tag_part_of_speech(TextBlob(t))
        for noun in reply_nouns:
            if noun in nouns :
                noun_reply_candidates_add(t)

    # find replies about the adjective
    adj_reply_candidates = set([])
    adj_reply_candidates_add = adj_reply_candidates.add
    for t in TWEETS:
        reply_pronouns, reply_nouns, reply_adjectives, reply_verbs = tag_part_of_speech(TextBlob(t))
        for noun in reply_nouns:
            if noun in nouns :
                adj_reply_candidates_add(t)

    if not reply_candidates and not noun_reply_candidates and not adj_reply_candidates:
        reply_candidates = TWEETS
    elif not reply_candidates and not noun_reply_candidates and adj_reply_candidates:
        reply_candidates = adj_reply_candidates
    elif not reply_candidates and noun_reply_candidates and not adj_reply_candidates:
        reply_candidates = noun_reply_candidates
    elif not reply_candidates and noun_reply_candidates and adj_reply_candidates:
        reply_candidates = noun_reply_candidates & adj_reply_candidates
    elif reply_candidates and not noun_reply_candidates and not adj_reply_candidates:
        reply_candidates = reply_candidates
    elif reply_candidates and noun_reply_candidates and not adj_reply_candidates:
        reply_candidates = reply_candidates & noun_reply_candidates 
    elif reply_candidates and noun_reply_candidates and adj_reply_candidates:
        reply_candidates = reply_candidates & noun_reply_candidates & adj_reply_candidates

    reply_candidates = list(reply_candidates)

    raw_reply = reply_candidates[int(random.random() * len(reply_candidates))]

    reply = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",raw_reply).split())
    return reply
    

def tag_part_of_speech(blob):
    pronouns = []
    nouns = []
    adjectives = []
    verbs = []
    for word, part_of_speech in blob.pos_tags:
        #print(word + ' ' + part_of_speech)
        if part_of_speech == 'PRP': # This is a pronoun
            pronouns.append(word)
        elif part_of_speech == 'NN':  # This is a noun
            nouns.append(word)
        elif part_of_speech == 'JJ':  # This is an adjective
            adjectives.append(word)
        elif part_of_speech.startswith('VB'):  # This is a verb
            verbs.append(word)
    return (pronouns, nouns, adjectives, verbs)

def jarvis_reply(user_intput):
    cleaned_text = preprocess_text(user_input)
    blob = TextBlob(cleaned_text)
    pronouns, nouns, adjectives, verbs = tag_part_of_speech(blob)
    return compose_response(pronouns, nouns, adjectives, verbs)

greeting = 'Hey dude! My name is Jarvis!\n'
while (True):
    user_input = input(greeting)
    if (user_input == 'quit'):
        print('Have a nice day!')
        break
    print(jarvis_reply(user_input))
    greeting = '\n'
