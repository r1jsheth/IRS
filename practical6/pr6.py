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
# print(len(athleticsVectorizerList))
cricketVectorizerList = processForDir('../bbcsport/cricket')
# print(len(cricketVectorizerList))
rugbyVectorizerList = processForDir('../bbcsport/rugby')
# print(len(rugbyVectorizerList))
tennisVectorizerList = processForDir('../bbcsport/tennis')
# print(len(tennisVectorizerList))
footballVectorizerList = processForDir('../bbcsport/football')




finalContent = preProcessData(finalContent)
final_vectorizer = vectorizer.fit_transform(mergedCorpus)
final_vectorizer_array = final_vectorizer.toarray() 
print(final_vectorizer_array.shape)



# applying SVD to reduce dimensionality
u, s, vh = np.linalg.svd(final_vectorizer_array, full_matrices=False, compute_uv=True)

number = 100

print("Enter size")
number = int(input())

# Option 1 will create N X N matrix
# reducted_data = np.dot(u, np.diag(s))
truncatedManually = np.dot(u[:, :number], np.diag(s[:number]))
print(truncatedManually.shape)

# Option 2
from sklearn.decomposition import TruncatedSVD

truncatedSVD = TruncatedSVD(n_components = number)
truncatedSVD_data = truncatedSVD.fit_transform(final_vectorizer.toarray())
print(truncatedSVD_data.shape)


# Predict on data truncated manually
X_train, X_test, Y_train, Y_test = train_test_split(truncatedManually, labeledData, test_size = 0.2)

classifier = GaussianNB()

classifier.fit(X_train, Y_train)
Y_predict = classifier.predict(X_test)

print('manually')
print(confusion_matrix(Y_test, Y_predict))
print(accuracy_score(Y_test, Y_predict))

# Predict on truncated by library
X_train, X_test, Y_train, Y_test = train_test_split(truncatedSVD_data, labeledData, test_size = 0.2)

classifier.fit(X_train, Y_train)
Y_predict = classifier.predict(X_test)

print('library')
print(confusion_matrix(Y_test, Y_predict))
print(accuracy_score(Y_test, Y_predict))