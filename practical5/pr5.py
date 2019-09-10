"""
 * @author raj
 * @create date 2019-09-10 11:45:56
 * @modify date /
 * @desc tf-idf and naive bayes to classify text documents
"""



from sklearn.feature_extraction.text import TfidfVectorizer
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer



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

mergedCorpus = []
vectorizer = TfidfVectorizer()
finalContent = ''
labeledData = []

def processForDir(directoryPath):
	
	vectorizerList = []

	for (root, dirs, files) in os.walk(directoryPath):
		for file in files:
			with open(directoryPath+'/'+file, 'r') as fileInput:
				corpus = []
				content = preProcessData(fileInput.read().lower())
				corpus.append(content)
				
				mergedCorpus.append(content)
				
				global finalContent
				finalContent += content
				
				# now labeling with filename
				labeledData.append([directoryPath.replace('../bbcsport/','') + '/' + file,directoryPath.replace('../bbcsport/','')])
				X = vectorizer.fit_transform(corpus)
				
				
				vectorizerList.append(X)

	return vectorizerList

athleticsVectorizerList = processForDir('../bbcsport/athletics')
cricketVectorizerList = processForDir('../bbcsport/cricket')
rugbyVectorizerList = processForDir('../bbcsport/rugby')
tennisVectorizerList = processForDir('../bbcsport/tennis')

print(len(labeledData))

finalContent = preProcessData(finalContent)
finalX = vectorizer.fit_transform(mergedCorpus)