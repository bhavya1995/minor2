
#!/usr/bin/env python
# Implementation of collaborative filtering recommendation engine

import csv
# from recommendation_data import dataset
from math import sqrt
import pymysql
import pprint
from scipy import spatial

pp = pprint.PrettyPrinter(indent=4)

dataset = {}


def similarity_score(person1,person2):
	
	# Returns ratio Euclidean distance score of person1 and person2 

	both_viewed = {}		# To get both rated items by person1 and person2

	for item in dataset[person1]:
		if item in dataset[person2]:
			both_viewed[item] = 1

		# Conditions to check they both have an common rating items	
		if len(both_viewed) == 0:
			return 0

		# Finding Euclidean distance 
		sum_of_eclidean_distance = []	

		for item in dataset[person1]:
			if item in dataset[person2]:
				sum_of_eclidean_distance.append(pow(dataset[person1][item] - dataset[person2][item],2))
		sum_of_eclidean_distance = sum(sum_of_eclidean_distance)

		return 1/(1+sqrt(sum_of_eclidean_distance))



def pearson_correlation(person1,person2):

	# To get both rated items
	both_rated = {}
	for item in dataset[person1]:
		if item in dataset[person2]:
			both_rated[item] = 1

	number_of_ratings = len(both_rated)
	# if (number_of_ratings > 1):
	# 	print (person1 + " " + person2)		
	
	# Checking for number of ratings in common
	if number_of_ratings == 0:
		return 0

	# Add up all the preferences of each user
	person1_preferences_sum = sum([dataset[person1][item] for item in both_rated])
	person2_preferences_sum = sum([dataset[person2][item] for item in both_rated])

	# Sum up the squares of preferences of each user
	person1_square_preferences_sum = sum([pow(dataset[person1][item],2) for item in both_rated])
	person2_square_preferences_sum = sum([pow(dataset[person2][item],2) for item in both_rated])

	# Sum up the product value of both preferences for each item
	product_sum_of_both_users = sum([dataset[person1][item] * dataset[person2][item] for item in both_rated])

	# Calculate the pearson score
	numerator_value = product_sum_of_both_users - (person1_preferences_sum*person2_preferences_sum/number_of_ratings)
	denominator_value = sqrt((person1_square_preferences_sum - pow(person1_preferences_sum,2)/number_of_ratings) * (person2_square_preferences_sum -pow(person2_preferences_sum,2)/number_of_ratings))
	# if (str(person1) == "8" and str(person2) == "11676"):
		# print ("aajfkfbkwffkakfkjbka,dfbkffnakfnfankf")
		# pp.pprint(both_rated)
		# print (str(numerator_value) + "adad" + str(denominator_value))
	if denominator_value == 0:
		return 0
	else:
		r = numerator_value/denominator_value
		return r 

def most_similar_users(person,number_of_users):
	# returns the number_of_users (similar persons) for a given specific person.
	scores = [(pearson_correlation(person,other_person),other_person) for other_person in dataset if  other_person != person ]
	
	# Sort the similar persons so that highest scores person will appear at the first
	scores.sort()
	scores.reverse()
	return scores[0:100]

def user_recommendations(person):

	# Gets recommendations for a person by using a weighted average of every other user's rankings
	totals = {}
	simSums = {}
	rankings_list =[]
	for other in dataset:
		# print(other)
		# don't compare me to myself
		if other == person:
			continue
		sim = pearson_correlation(person,other)
		# print (sim)
		#print ">>>>>>>",sim

		# ignore scores of zero or lower
		if sim <=0: 
			continue
		for item in dataset[other]:

			# only score movies i haven't seen yet
			if item not in dataset[person] or dataset[person][item] == 0:

			# Similrity * score
				totals.setdefault(item,0)
				totals[item] += dataset[other][item]* sim
				# sum of similarities
				simSums.setdefault(item,0)
				simSums[item]+= sim

		# Create the normalized list

	rankings = [(total/simSums[item],item) for item,total in totals.items()]
	rankings.sort()
	rankings.reverse()
	# returns the recommended items
	recommendataions_list = [recommend_item for score,recommend_item in rankings]
	return recommendataions_list

def cosineSimilarity(person):
	finalArray = set()
	for d in dataset:
		if (d == person):
			continue
		dataset1 = []
		dataset2 = []
		for myself in dataset[person]:
			dataset1.append(dataset[person][myself])
		for otherRating in dataset[d]:
			dataset2.append(dataset[d][otherRating])
		# print (dataset1)
		# print (dataset2)
		if (len(dataset1) < len(dataset2)):
			counter = len(dataset2) - len(dataset1)
			while (counter > 0):
				dataset1.append(0)
				counter -= 1
		if (len(dataset1) > len(dataset2)):
			counter = len(dataset1) - len(dataset2)
			while (counter > 0):
				dataset2.append(0)
				counter -= 1

		result = 1 - spatial.distance.cosine(dataset1, dataset2)
		if (result >= 0.995):
			for otherRating in dataset[d]:
				finalArray.add(otherRating)
		resultArray = []
		for setItem in finalArray:
			for myself in dataset[person]:
				flag = 0
				if (setItem == dataset[person]):
					flag = 1
					break
				if (flag == 1):
					break
			if (flag == 0):
				resultArray.append(setItem)

 
	# print(resultArray)
	# print ("\n\n\n")
	# print (len(resultArray))
	return resultArray

# def createMatrix():
# 	#Matrix rows users and columns that are books
# 	# Cell is ranking user Vs Book and 0 if not present
	

def import_dataset():
	conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='bhavya', db='minor2',autocommit=True)
	cur = conn.cursor()
	conn.autocommit(True)

	# booksRating = list(csv.reader(open("BX-Book-Ratings.csv",newline='', encoding="latin1"), delimiter = ';'))
	# print (booksRating[1])
	# counter = 0
	# for b in booksRating:
	# 	if (counter == 0):
	# 		pass
	# 	else :
	# 		cur.execute("INSERT INTO books_rating VALUES (" + b[0] +",'" + b[1] +"'," + b[2] +");")
	# 	counter += 1

	# booksName = list(csv.reader(open("BX-Books.csv",newline='', encoding="latin1"), delimiter = ';'))
	# counter = 0
	# for b in booksName:
	# 	if (counter == 0):
	# 		pass
	# 	else :
	# 		cur.execute("INSERT INTO books_name VALUES ('%s', '%s', '%s', '%d', '%s')" % (b[0], b[1], b[2], b[3], b[4]))
	# 		print (b[1])
	# 	counter += 1
	# print ("THE END *****************************************************************************")
	
	# usersData = list(csv.reader(open("BX-Users.csv",newline='', encoding="latin1"), delimiter = ';'))
	# counter = 0
	# str = ''
	# for b in usersData:
	# 	if (counter == 0):
	# 		pass
	# 	elif (counter == 100000):
	# 		break
	# 	else :
	# 		str +=  "INSERT INTO user_details VALUES ('%d', '%s', '%s');" % (int(b[0]), b[1], b[2])
	# 		print (b[0])
	# 	counter += 1
	# cur.execute(str)




	cur.execute("SELECT * FROM results ORDER BY userid ASC;")
	user_details_data = cur.fetchall()
	userid = 0
	for u in user_details_data:
		if (u[0] != userid):
			dataset[str(u[0])] = {}
			dataset[str(u[0])][u[1]] = u[2]
			userid = u[0]
		else:
			dataset[str(u[0])][u[1]] = u[2]
			userid = u[0]
	# cur.execute("SELECT * FROM user_details LIMIT 100")
	# user_details_data = cur.fetchall()
	# # print(cur.fetchone())
	# for u in user_details_data:
	# 	userId = u[0]
	# 	dataset[str(userId)] = {}
	# 	# print (type(userId))
	# 	cur.execute("SELECT * FROM books_rating WHERE userid = %s LIMIT 20000", userId)
	# 	books_details_data = cur.fetchall()
	# 	for bdd in books_details_data:
	# 		dataset[str(userId)][bdd[1]] = bdd[2]
	# 	print (u)
	# pp.pprint (dataset)
	conn.close()

	# print (booksName)
	# mycsv = list(mycsv)

# pp.pprint (dataset)
import_dataset()
nn = []
for other in dataset:	
	# print(other)
	aa = cosineSimilarity(other)
	if (len(aa) != 0):
		nn.append(other)
	print(nn)

# # 	temp = similarity_score("201641", other)
# # 	if (temp != 0):
# # 		print (other + " " + str(temp))
# # pp.pprint (most_similar_users("201641", 11962))
# 	abc = user_recommendations(other)
# 	print (abc)
# 	if (len(abc) == 0):
# 		pass
# 	else:
# 		print (other + "\n")
# 		print(user_recommendations(other))
