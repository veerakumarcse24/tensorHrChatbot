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
from chatbot.serializers import (BookSerializer, PublisherSerializer)

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

from chatbot.tensorneuro import tensortrain, tensorresponse

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

#tz = pytz.timezone('UTC')

@csrf_exempt
def updateUser(request, format=None):
    if request.method == "POST":
        try:
            data = request.POST
            model = Publisher()
            model.name = data.get('name')
            model.address = data.get('address')
            model.city = data.get('city')
            model.state_province = data.get('state_province')
            model.country = data.get('country')
            model.website = data.get('website')
            model.save()
            result = {'Status': 200, 'message': 'Saved successfully.'}
            return JSONResponse(result)
        except Exception as e:
            return HttpResponse(status=404)
    else:
        data = {'Status': 'failed', 'message': 'Invalid'}
        return JSONResponse(data)

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
        if(len(inputMSG) > 2):
            translateSource = textblobmethods.getSourceLanguage(inputMSG)
            inputLanguage = str(translateSource)
            if(inputLanguage != 'en'):
                inputMSG = str(textblobmethods.translateLanguage(inputMSG, 'en'))
        else:
            inputLanguage = 'en'

        responseMsg = []
        chatResponse = tensorresponse.response(inputMSG)
        if(chatResponse and inputLanguage != 'en'):
            chatResponse = str(textblobmethods.translateLanguage(chatResponse, inputLanguage))
        responseMsg.append(chatResponse)
        responseData = {"speechResponse":responseMsg}
        return JSONResponse(responseData)
    else:
        data = "this is post"
    return JSONResponse(data)


@csrf_exempt
def getAuthor(request, u_id):
    if request.method == "GET":
        model = Publisher.objects.filter(id=u_id)
        serializer = PublisherSerializer(model, many=True)
        #print (serializer)
        data = serializer.data
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


