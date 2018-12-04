# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from django.shortcuts import render

#from hrmsv2.settings import FRONT_URL

from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core.signing import Signer
from django.core.mail import send_mail
# from rest_framework.test import APIRequestFactory
from django.core.files import uploadedfile
from django.core.files import uploadhandler
from rest_framework import generics
from datetime import datetime
#from hrmsv2.settings import MEDIA_URL
from django.db.models import Q
from django.db.models import Sum
import dateutil.parser
import os
# import datetime
import json
import base64

#from chatbot.models import Publisher
from chatbot.models import StarRatings
from chatbot.serializers import (StarRatingSerializer)

# import chats functions
import nltk
#nltk.download()
#from nltk.corpus import names
#from nltk.book import *
import random
from chatbot.controller import chats
from chatbot.controller import textblobmethods
from chatbot.traindata import hrtrain
from nltk.chat.util import Chat, reflections

from django.utils.crypto import get_random_string

from bs4 import BeautifulSoup

#tensorflow trainingset

from chatbot.tensorneuro import tensortrain, tensorresponse, processingData

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

#tz = pytz.timezone('UTC')

# @csrf_exempt
# def chat(request, format=None):   #http://localhost:8000/test1?name=veera
#     if request.method == "GET":
#         data = request.GET
#         inputMSG = data.get('inputmsg')
#         if(len(inputMSG) > 2):
#             translateSource = textblobmethods.getSourceLanguage(inputMSG)
#             inputLanguage = str(translateSource)
#             if(inputLanguage != 'en'):
#                 inputMSG = str(textblobmethods.translateLanguage(inputMSG, 'en'))
#         else:
#             inputLanguage = 'en'

#         chat = Chat(hrtrain.pairs, reflections)
#         responseMsg = []
#         chatResponse = chat.respond(inputMSG)
#         if(chatResponse and inputLanguage != 'en'):
#             chatResponse = str(textblobmethods.translateLanguage(chatResponse, inputLanguage))
#         responseMsg.append(chatResponse)
#         responseData = {"speechResponse":responseMsg}
#         return JSONResponse(responseData)
#     else:
#         data = "this is post"
#     return JSONResponse(data)


@csrf_exempt
def chat(request, format=None):
    if request.method == "GET":
        data = request.GET
        inputMSG = data.get('inputmsg')
        # if(len(inputMSG) > 2):
        #     translateSource = textblobmethods.getSourceLanguage(inputMSG)
        #     inputLanguage = str(translateSource)
        #     if(inputLanguage != 'en'):
        #         inputMSG = str(textblobmethods.translateLanguage(inputMSG, 'en'))
        # else:
        #     inputLanguage = 'en'

        responseMsg = []
        if(not inputMSG or inputMSG == ''):
            chatResponse = 'Thanks for visiting, Enter some message here.'
        else:
            chatResponse = tensorresponse.response(inputMSG)
        if(not chatResponse):
            chatResponse = 'Can you please explain further'
        # if(chatResponse and inputLanguage != 'en'):
        #     chatResponse = str(textblobmethods.translateLanguage(chatResponse, inputLanguage))
        responseMsg.append(chatResponse)
        responseData = {"speechResponse":responseMsg}
        return JSONResponse(responseData)
    else:
        data = "this is post"
    return JSONResponse(data)


@csrf_exempt
def traininputdata(request): #train data using tensorflow
    if request.method == "GET":
        tensortrain.trainInputData()
        data = {'Status': 'success', 'message': 'Input data was trained successfully.'}
    else:
        data = {'Status': 'failed', 'message': 'Invalid'}
    return JSONResponse(data)

@csrf_exempt
def processingdata(request): #train data using tensorflow
    if request.method == "GET":
        processingData.convertToJson()
        data = {'Status': 'success', 'message': 'Raw data was formatted successfully.'}
    else:
        data = {'Status': 'failed', 'message': 'Invalid'}
    return JSONResponse(data)

@csrf_exempt
def saveRatings(request): #save users ratings
    if request.method == "POST":
        data=json.loads(request.body)
        try:
            model = StarRatings.objects.get(username = data.get('username'))
        except StarRatings.DoesNotExist:
            model = StarRatings()
            model.username = data.get('username')
        model.comments = data.get('comments')
        model.rating = data.get('rating')
        model.save()
        data = {'Status': 'success', 'message': 'Thank you for your ratings.'}
    else:
        data = {'Status': 'failed', 'message': 'Invalid'}
    return JSONResponse(data)

@csrf_exempt
def getRatings(request): #save users ratings
    if request.method == "GET":
        getAllRatings = StarRatings.objects.all()
        serializer = StarRatingSerializer(getAllRatings, many=True)
        data = {'Status': 'success', 'data': serializer.data}
    else:
        data = {'Status': 'failed', 'message': 'Invalid'}
    return JSONResponse(data)

@csrf_exempt
def chatDownload(request): #download chat
    if request.method == "GET":
        BASE = os.path.dirname(os.path.abspath(__file__))
        file_path = open(os.path.join(BASE + '/tensorneuro/trainingData', "rawData.txt"), "rb")
        content = file_path
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=chatlog.txt'
        response['Status'] = "success"
        data = response
    else:
        data = ''
    return data

@csrf_exempt
def logsDownload(request): #download chat
    if request.method == "GET":
        BASE = os.path.dirname(os.path.abspath(__file__))
        file_path = open(os.path.join(BASE + '/tensorneuro/trainingData', "users_queries.txt"), "rb")
        content = file_path
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=untrackLogs.txt'
        response['Status'] = "success"
        data = response
    else:
        data = ''
    return data

@csrf_exempt
def trainDataDownload(request): #download trainingdata
    if request.method == "GET":
        BASE = os.path.dirname(os.path.abspath(__file__))
        file_path = open(os.path.join(BASE + '/tensorneuro/trainingData', "formattedData.json"), "rb")
        content = file_path
        response = HttpResponse(content, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=trainData.json'
        response['Status'] = "success"
        data = response
    else:
        data = ''
    return data
