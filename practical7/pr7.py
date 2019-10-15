"""
 * @author raj
 * @create date 2019-10-15 11:53:27
 * @modify date 
 * @description Genetic Algorithms
"""



from sklearn.feature_extraction.text import TfidfVectorizer
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split



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

def removeDigits(inputString):
	resultString = ''.join([i for i in inputString if not i.isdigit()])
	return resultString


def removePunctuations(content):
	tokenizer = RegexpTokenizer(r'\w+')
	tokenizedContent = tokenizer.tokenize(content)
	finalContent = ""
	for word in tokenizedContent:
		finalContent += word + " "
	return finalContent




def preProcessData(content):
	content = removeStopWords(content)
	content = removeStemming(content)
	content = removeDigits(content)
	content = removePunctuations(content)
	return content

corups = []
labeledData = []

def processForDir(directoryPath):
	
	for (root, dirs, files) in os.walk(directoryPath):
		for file in files:

			with open(directoryPath+'/'+file, 'rb') as fileInput:

				content = fileInput.read().decode(errors='replace')
				content = preProcessData(content.lower())

				corups.append(content)

				# now labeling with filename
				labeledData.append(directoryPath.replace('../bbcsport/',''))


processForDir('../bbcsport/athletics')
processForDir('../bbcsport/cricket')
processForDir('../bbcsport/rugby')
processForDir('../bbcsport/tennis')
processForDir('../bbcsport/football')

vectorizer = TfidfVectorizer()
final_vectorizer = vectorizer.fit_transform(corups)
final_vectorizer_array = final_vectorizer.toarray() 
print(final_vectorizer_array.shape)

X_train, X_test, Y_train, Y_test = train_test_split(final_vectorizer_array, labeledData, test_size = 0.2, random_state = 5)