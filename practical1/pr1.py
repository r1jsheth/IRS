"""
 * @author raj
 * @desc simply searches a phrase from a file
"""
import os

print("Enter content to search:")
searchString = input()


def searchInFiles(keywordList):
	resultList = []
	for filename in os.listdir("./cricket"):
		with open('./cricket/' + filename) as file:
			data = file.read().lower()
			for searchString in keywordList:
				flag = 1
				if searchString.lower() not in data:
					flag = 0
					break
			if flag == 1:
				resultList.append(filename)
	return resultList


# searchString = searchString.replace('\"', '\'')
# keywordList = searchString.split('\'')

# for keyword in keywordList:
# 	keyword = keyword.replace('\'','')
# 	keyword = keyword.replace('\"','')

# while("" in keywordList):
# 	keywordList.remove("")


if (searchString[0] == '\'' or searchString[0] == '\"') and (searchString[-1] == '\'' or searchString[-1] == '\"'):
	keywordList = []
	searchString = searchString.replace('\'','')
	searchString = searchString.replace('\"','')
	keywordList.append(searchString)
	print(keywordList)
	resultList = searchInFiles(keywordList)
else:
	keywordList = searchString.split(' ')
	print(keywordList)
	resultList = searchInFiles(keywordList)

print("Content was found in following list of files:")
print(resultList)