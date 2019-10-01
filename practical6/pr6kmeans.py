"""
 * @author raj
 * @create date 2019-09-24 12:40:38
 * @modify date 2019-10-01 11:25:24
 * @desc tf-idf, SVD, kmeans to cluster text documents
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

mergedCorpus = []
vectorizer = TfidfVectorizer()
finalContent = ''
labeledData = []

def processForDir(directoryPath):
	
	vectorizerList = []

	for (root, dirs, files) in os.walk(directoryPath):
		for file in files:
			with open(directoryPath+'/'+file, 'rb') as fileInput:
				corpus = []
				content = fileInput.read().decode(errors='replace')
				content = preProcessData(content.lower())
				corpus.append(content)

				mergedCorpus.append(content)

				global finalContent
				finalContent += content

				# now labeling with filename
				labeledData.append(directoryPath.replace('../bbcsport/',''))

				X = vectorizer.fit_transform(corpus)
				vectorizerList.append(X)

	return vectorizerList

athleticsVectorizerList = processForDir('../bbcsport/athletics')
cricketVectorizerList = processForDir('../bbcsport/cricket')
rugbyVectorizerList = processForDir('../bbcsport/rugby')
tennisVectorizerList = processForDir('../bbcsport/tennis')
footballVectorizerList = processForDir('../bbcsport/football')

finalContent = preProcessData(finalContent)
final_vectorizer = vectorizer.fit_transform(mergedCorpus)
final_vectorizer_array = final_vectorizer.toarray() 
print(final_vectorizer_array.shape)

X_train, X_test, Y_train, Y_test = train_test_split(final_vectorizer_array, labeledData, test_size = 0.2, random_state = 5)


u,s,v = np.linalg.svd(X_train.T, full_matrices=True, compute_uv=True)
print(u.shape)
print(s.shape)
print(v.shape)
q,w = v.shape

number = 100

U = u[:,:number]
V = v[:number, :]
print(U.shape)
print(V.shape)

X_train_svd = V.T
Y_train_svd = Y_train


from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters = 5, random_state=0).fit(X_train_svd)

X_test_svd = np.matmul(X_test, U)
Y_test_svd = Y_test
Y_predict = kmeans.predict(X_test_svd)


# print('\n\nusing TruncatedSVD()')
# print(confusion_matrix(Y_test_svd, Y_predict))
