"""
 *	@author raj
 *	@create date 2019-10-15 11:53:27
 *	@modify date 
 *	@description: Meta search engine methods
 *				1) Borda ranking
 *
 *
 *	@input:
 *	5 4
	1 2 3 4
	2 1 4 3
	3 2 1 4
	-1 2 1 3
	-1 2 1 -1
"""

import os

no_search_engines = int(input("Enter no of component search engines: "))
no_web_pages = int(input("Enter no of total web pages: "))


rankMapList = []

for i in range(0, no_search_engines):
	os.system('clear')
	currentRankMap = {}
	for j in range(0, no_web_pages):
		
		flag_correct_input = False
		while flag_correct_input == False:
			print("For search engine", i+1)
			print("What is rank for page", chr(j+97), "?")
			print("Enter -1 if it doesn't exist in the results:")
			rank = int(input())

			# Validate for correct ranking
			if rank == -1:
				flag_correct_input = True
			elif rank <= 0 or rank > no_web_pages:
				print("rank >= 1 and rank <=", no_web_pages)
				print("Error in input, try again")
			else:
				flag_seen = False
				for page,rank2 in currentRankMap.items():
					if rank2 == rank:
						print("\nRank can not be repeated!!")
						flag_seen = True

				if flag_seen == False:
					flag_correct_input = True

			if flag_correct_input == True:
				currentRankMap[chr(j+97)] = rank
	
	rankMapList.append(currentRankMap)

scoreMap = {}

for search_engine_result in rankMapList:

	minus_one_list = []


	for page,rank in search_engine_result.items():
		if rank == -1:
			minus_one_list.append(page)
	
	for page in minus_one_list:
		if page in scoreMap:
			scoreMap[page] += float(len(minus_one_list) * float(len(minus_one_list) + 1)/(2*len(minus_one_list)))
		else:
			scoreMap[page] = float(len(minus_one_list) * float(len(minus_one_list) + 1)/(2*len(minus_one_list)))


	for page,rank in search_engine_result.items():
		if rank == -1:
			continue
		if page in scoreMap:
			scoreMap[page] += float(no_web_pages - rank + 1)
		else:
			scoreMap[page] = float(no_web_pages - rank + 1)


# print(scoreMap)
pageRankList = []

for page,rank in scoreMap.items():
	pageRankList.append((rank,page))

pageRankList.sort(reverse = True)
print(pageRankList)