'''
 * @author raj
 * @create date 2019-08-13 11:36:12
 * @modify date 2019-08-13 11:36:12
 * @desc [description]
 */
'''

import os
from os import walk
import numpy as np
import json
from numpy import array


def writeJSON(outputFileName, dictionary):
	with open(outputFileName, 'w') as outputFile:
		json.dump(dictionary, outputFile, sort_keys = True, indent = 4)


def writeCSV(matrix, rowHeaders, columnHeaders):
	firstLine = 'filename,'
	for columnHeader in columnHeaders:
		firstLine += columnHeader+','
	firstLine = firstLine[:-1]
	# print(firstLine)

def __main__():

	fileDictList = []
	fileWiseDict = {}

	for (root, dirs, files) in os.walk('../processed-nltk'):
		fileDict = {}
		cnt = 0
		wordCount = 0
		uniqueWordCount = 0
		allUniqueWordDict = {}
		files.sort()

		for fileName in files:

			wordDict = {}
			fileDict = {}

			with open('../processed-nltk/'+fileName,'r') as file:
				data = file.read().lower()
				wordList = data.split(' ')
				for word in wordList:
					wordCount += 1
					if word == '':
						continue
					if word not in wordDict:
						wordDict[word] = 1
					else:
						wordDict[word] += 1

					if word not in allUniqueWordDict:
						allUniqueWordDict[word] = 1
					else:
						allUniqueWordDict[word] += 1

			fileDict['filename'] = fileName.replace('-processed.txt','')
			fileDict['data'] = wordDict
			fileWiseDict[fileName] = wordDict
			fileDictList.append(fileDict)
			uniqueWordCount = len(allUniqueWordDict)

		wordVector = []
		columnHeaders = [0]*uniqueWordCount
		rowHeaders = ['']*124

		rowCount = 0

		for fileName in files:
		
			wordss = [0]*uniqueWordCount
			rowHeaders[rowCount] = fileName.replace('-processed.txt','')
			rowCount += 1

			cnt = 0
			for word in sorted(allUniqueWordDict.keys()):
				columnHeaders[cnt] = word
				if word in fileWiseDict[fileName]:
					wordss[cnt] = fileWiseDict[fileName][word]
				wordss[cnt] = 0
				cnt += 1
			wordVector.append(wordss)


		print(rowHeaders)
		print(len(wordVector))
		writeCSV(wordVector, rowHeaders, columnHeaders)

__main__()