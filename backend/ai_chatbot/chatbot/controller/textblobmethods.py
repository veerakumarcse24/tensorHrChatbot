# -*- coding: utf-8 -*-

from textblob import TextBlob

def getSourceLanguage(inputData):
    source_language = TextBlob(inputData)
    return (source_language.detect_language())

def translateLanguage(inputData, lang):
    source_language = TextBlob(inputData)
    return (source_language.translate(to=lang))
