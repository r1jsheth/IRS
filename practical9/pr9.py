"""
 *	@author raj
 *	@create date 2019-11-05 11:34:58
 *	@modify date 2019-11-05 13:03:48
 *	@description: Meta search engine methods
 *				1) Borda ranking
 *
 *
 *	@input:
 *	csv file
"""

import csv
import numpy as np
import math

csv_fname = 'input.csv'

ratingMatrix = np.genfromtxt(csv_fname, delimiter=',')

print(ratingMatrix)

for x in ratingMatrix:
	for number in x:
		if math.isnan(number):
			print(number, end = ' ')
	print()



# remainingItems = []

# cnt = 0
# for item in ratingMatrix[userIdx-1]:
# 	if math.isnan(item):
# 		remainingItems.append(cnt)
# 	cnt += 1

# print(remainingItems)



'''
 *	method a) r(c,s) = 1/N * (Σ r(c',s))
 *	0-based indexing
'''
def predictRatingMethodA(ratingMatrix, userIdx, itemIdx):
	result = 0
	n,m = len(ratingMatrix), len(ratingMatrix[0])

	userCount = 0
	for i in range(0,n):
		if i == userIdx:
			continue
		if not math.isnan(ratingMatrix[i][itemIdx]):
			result += float(ratingMatrix[i][itemIdx])
			userCount += 1

	return result/userCount


# print(predictRating(ratingMatrix, 3, 2))


'''
 *	method c) 
'''
def predictRatingMethodC(ratingMatrix, userIdx, itemIdx):
	r_avg = 0
	count = 0
	n,m = len(ratingMatrix), len(ratingMatrix[0])


	for item in ratingMatrix[userIdx]:
		if not math.isnan(item):
			r_avg += item
			count += 1

	r_avg /= count

	# print(r_avg)

	userWhoHaveSeenItemList = []

	for i in range(0,n):
		if i == userIdx:
			continue
		if not math.isnan(ratingMatrix[i][itemIdx]):
			userWhoHaveSeenItemList.append(i)

	# print(userWhoHaveSeenItemList)


	weight_map = {}
	avg_map = {}
	for i in userWhoHaveSeenItemList:

		r_avg_i = 0
		r_avg_i_cnt = 0

		for j in range(0,m):

			if j == itemIdx or math.isnan(ratingMatrix[i][j]):
				continue
			r_avg_i += ratingMatrix[i][j]
			r_avg_i_cnt += 1


		avg_map[i] = r_avg_i/r_avg_i_cnt

	# print(avg_map)

	for i in userWhoHaveSeenItemList:

		numerator = 0
		modeA = 0
		modeB = 0
		
		for j in range(0,m):
			if not math.isnan(ratingMatrix[i][j]) and not math.isnan(ratingMatrix[userIdx][j]):
				numerator += ratingMatrix[i][j]*ratingMatrix[userIdx][j]
				modeA += ratingMatrix[i][j]**2
				modeB += ratingMatrix[userIdx][j]**2

		denom = math.sqrt(modeA)*math.sqrt(modeB)

		w_ij = numerator/denom
		weight_map[i] = w_ij

	# print(weight_map)


	interRes = 0
	weightSum = 0
	for i in userWhoHaveSeenItemList:
		interRes += (ratingMatrix[i][itemIdx]-avg_map[i])*weight_map[i]
		weightSum += weight_map[i]

	result = r_avg + interRes/weightSum
	# print(result)
	return result

print('For which user you want to recommend movie?')
userIdx = int(input())

for j in range(0, len(ratingMatrix[0])):
	if math.isnan(ratingMatrix[userIdx][j]):
		rating = predictRatingMethodC(ratingMatrix, userIdx, j)
		print('Movie',j,'predicated rating is:',rating)