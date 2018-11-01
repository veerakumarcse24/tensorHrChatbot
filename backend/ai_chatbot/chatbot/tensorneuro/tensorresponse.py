import os.path
BASE = os.path.dirname(os.path.abspath(__file__))
# things we need for NLP
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = nltk.stem.SnowballStemmer('english')

# things we need for Tensorflow
import numpy as np
import tflearn
import tensorflow as tf
import random
import sys

# restore all of our data structures
import pickle
data = pickle.load( open( "training_data", "rb" ) )
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

# print(words)

# print(classes)


# import our chat-bot intents file
import json
with open(os.path.join(BASE + '/trainingData', "formattedData.json")) as json_data:
    intents = json.load(json_data)

# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')

def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))

# load our saved model
model.load('./model.tflearn')
# p = bow("is your shop open today?", words)
# print (p)
# print (classes)

# create a data structure to hold user context
context = {}

ERROR_THRESHOLD = 0.25
def classify(sentence):
    print('----')
    print(sentence)
    print(words)
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    print(results)
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    print(results)
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    print('********************')
    print(return_list)
    print('**********************')
    return return_list

def response(sentence, userID='123', show_details=True):
    results = classify(sentence)
    # if we have a classification then find the matching intent tag
    #print('came here')
    #print(results)
    if results:
        # loop as long as there are matches to process
        while results:
            #print("came 1")
            for i in intents['intents']:
                #print("came 2")
                # find a tag matching the first result
                if i['tag'] == results[0][0]:
                    # set context for this intent if necessary
                    if 'context_set' in i:
                        if show_details: print ('context:', i['context_set'])
                        context[userID] = i['context_set']
                        print(context)

                    # check if this intent is contextual and applies to this user's conversation
                    if not 'context_filter' in i or \
                        (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        if show_details: print ('tag:', i['tag'])
                        # a random response from the intent
                        print(i)
                        return (random.choice(i['responses']))

            results.pop(0)

