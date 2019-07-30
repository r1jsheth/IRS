import os
from os import listdir
from os.path import isfile, join

def getStopWords():
	stopWordsList = []
	with open('stopWordsList') as stopWordsFile:
		data = stopWordsFile.read().lower()
		stopWordsList = data.split('\n')
		return stopWordsList


def removePunctuations(inputString):
	punctuationList = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
	resultString = ''
	for char in inputString:
		if char not in punctuationList:
			resultString = resultString + char
	return resultString


def removeDigits(inputString):
	resultString = ''.join([i for i in inputString if not i.isdigit()])
	return resultString


def removeStopWords(inputString, stopWordsList):
	inputString = inputString.replace('\n',' ')
	inputString = inputString.split(' ')
	inputString  = [word for word in inputString if word.lower() not in stopWordsList]
	resultString = ' '.join(inputString)
	return resultString


def writeFile(data, fileName):
	preProcessedFile = open('../preprocessed/'+fileName, 'w')
	preProcessedFile.write(data)
	preProcessedFile.close()

def preProcess(fileName):
	with open('../cricket/'+fileName) as inputFile:
		data = inputFile.read().lower()
		stopWordsList = getStopWords()
		data = removeStopWords(data, stopWordsList)
		data = removeDigits(data)
		finalResult = removePunctuations(data)
		preProcessedFileName = fileName.replace('.txt','')
		writeFile(finalResult, preProcessedFileName+'-preprocessed.txt')
		print("Done! Saved Successfully!")


def fileExists(fileName):
	if(os.path.exists('../cricket/'+fileName)):
		return True
	else:
		return False

inputFile = input("Enter filename:")
print(inputFile)

if(fileExists(inputFile)):
	preProcess(inputFile)
else:
	print("File doesn't exist!")
	exit(-1)



# directoryPath = './cricket'
# allFiles = [file for file in listdir(directoryPath) if isfile(join(directoryPath, file))]

# for file in allFiles:
# 	print(file,end=' ')
# 	preProcess(file)