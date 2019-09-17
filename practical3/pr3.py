"""
 * @author raj
 * @create date 2019-08-06 12:16:04
 * @modify date 2019-08-06 12:16:04
 * @desc removes stopwords and punctuations from a file using nltk
"""

import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer

def fileExists(fileName):
	if(os.path.exists('../cricket/'+fileName)):
		return True
	else:
		return False

def getFileContent(fileName):
	with open('../cricket/'+fileName) as inputFile:
		fileContent = inputFile.read().lower()
		return fileContent

def removeStopWords(content):
	stopWords = set(stopwords.words('english'))
	wordTokens = word_tokenize(content)
	filteredContent = [word for word in wordTokens if not word in stopWords]
	filteredContent = []
	for word in wordTokens:
		if word not in stopWords:
			filteredContent.append(word)
	finalContent = ""
	for word in filteredContent:
		finalContent += word + " "
	return finalContent

def removeStemming(content):
	posterStemmer = PorterStemmer()
	wordList = word_tokenize(content)
	resultContent = ""
	for word in wordList:
		resultContent += posterStemmer.stem(word) + " "
	
	return resultContent


def removePunctuations(content):
	tokenizer = RegexpTokenizer(r'\w+')
	tokenizedContent = tokenizer.tokenize(content)
	finalContent = ""
	for word in tokenizedContent:
		finalContent += word + " "
	return finalContent


def writeFile(data, fileName):
	preProcessedFile = open(fileName, 'w')
	preProcessedFile.write(data)
	preProcessedFile.close()

def removeDigits(inputString):
	resultString = ''.join([i for i in inputString if not i.isdigit()])
	return resultString

def processFile(fileName):
	fileContent = getFileContent(fileName)
	tokenizedContent = removePunctuations(fileContent)
	removedDigitsContent = removeDigits(tokenizedContent)
	unstemmedContent = removeStemming(removedDigitsContent)
	finalContent = removeStopWords(unstemmedContent)
	processedFileName = fileName.replace('.txt','')
	writeFile(finalContent, '../processed-nltk/'+ processedFileName + '-processed.txt')

# import os 
# from os import walk
# def processFile(fileName):
# 	fileContent = getFileContent(fileName)
# 	fileContent = removeStopWords(fileContent)
# 	# fileContent = removeStemming(fileContent)
# 	fileContent = removeDigits(fileContent)
# 	fileContent = removePunctuations(fileContent)
# 	processedFileName = fileName.replace('.txt','')
# 	writeFile(fileContent, '../processed-nltk/'+ processedFileName + '-processed.txt')

# for (root, dirs, files) in os.walk('../cricket'):
# 	for fileName in files:
# 		processFile(fileName)
# 		print(fileName)
# exit(0)

fileName = input("Enter file name:")
# fileName = '001.txt'
if(fileExists(fileName)):
	processFile(fileName)
	print("Done processing and saved successfully!")
else:
	print("Error file doesn't exist")