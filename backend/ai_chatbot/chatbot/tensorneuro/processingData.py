import json
import sys
import os.path
BASE = os.path.dirname(os.path.abspath(__file__))

def convertToJson():
    intentJson = {}
    sentenceJson = []
    for line in open(os.path.join(BASE + '/trainingData', "rawData.txt")):
        if 'User:' in line:
            temp = {}
            arrayIndex = len(sentenceJson)
            temp['tag'] = 'question_' + str(arrayIndex)
            temp['patterns'] = []
            question_data = line.replace('User:', '')
            filtered_data = question_data.rstrip()
            temp['patterns'].append(filtered_data.strip())
            temp['context_set'] = ''

        if 'Santa:' in line:
            temp['responses'] = []
            answer_data = line.replace('Santa:', '')
            filtered_data = answer_data.rstrip()
            temp['responses'].append(filtered_data.strip())
            sentenceJson.append(temp)

    intentJson['intents'] = sentenceJson

    with open(os.path.join(BASE + '/trainingData', "formattedData.json"), 'w') as outfile:
        json.dump(intentJson, outfile)

    print("suceess...")
