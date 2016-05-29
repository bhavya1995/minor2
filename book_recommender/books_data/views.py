from django.shortcuts import render
from django.http import HttpResponse,Http404
import json
from books_data.models import *
from books_data.collaborative_filtering import *
import random
# from sets import Set
# Create your views here.
a = 0
b = 0
c = 0
d = 0
e = 0
f = 0
def home(request):
	return render(request,'minor.html')

def submitUserId (request):
	print("aaa")
	userID = request.GET.get('userid')
	books_arr = results.objects.filter(userId = int(userID))
	tempArr = ['171968', '276071', '112093', '231354', '44842', '191883', '150498', '168064', '192353', '48046', '91058', '101304', '177432', '245568', '37244', '224997', '221445', '270234', '123608', '106078', '225989', '242233', '92810', '14521', '35998', '76532', '25545', '52917', '6563', '136747', '56856', '126736', '217375', '59038', '236757', '273976']
	if (len(books_arr) == 0):
		ran = random.randint(0, len(tempArr))
		userID = tempArr[ran]
		books_arr = results.objects.filter(userId = int(userID))

	print(books_arr)
	bookdata_arr = []
	for b in books_arr:
		temp = {}
		bookObj = books_info.objects.filter(bookId = b.bookId)
		print(bookObj)
		try:
			temp['id'] = bookObj[0].id
			temp['bookName'] = bookObj[0].bookName
			temp['img'] = "/static/images/" + str(bookObj[0].bookId) + ".jpg"
			temp['author'] = bookObj[0].bookAuthor
			bookdata_arr.append(temp)
		except:
			pass
	print(bookdata_arr)
	print("aaaaaaaaaa")
	return render(request, 'page2minor.html', {"data": bookdata_arr, "userid": userID})

def algorithms(request):
	userid = request.GET.get("userid")
	return render(request, 'minor3.html', {"userid": userid})

def results1(request):
	userid = request.GET.get("userid")
	import_dataset()
	bookdata_arr1 = user_recommendations(userid)
	# print(bookdata_arr)
	# print(abc)
	bookdata_arr = []
	for b in bookdata_arr1:
		if (len(bookdata_arr) == 15):
			break
		temp = {}
		bookObj = books_info.objects.filter(bookId = b)
		# print(bookObj)
		try:
			temp['id'] = bookObj[0].id
			temp['bookName'] = bookObj[0].bookName
			temp['img'] = "/static/images/" + str(bookObj[0].bookId) + ".jpg"
			temp['author'] = bookObj[0].bookAuthor
			bookdata_arr.append(temp)
		except:
			pass
	if (len(bookdata_arr) == 0):
		tempArr = ['171968', '276071', '112093', '231354', '44842', '191883', '150498', '168064', '192353', '48046', '91058', '101304', '177432', '245568', '37244', '224997', '221445', '270234', '123608', '106078', '225989', '242233', '92810', '14521', '35998', '76532', '25545', '52917', '6563', '136747', '56856', '126736', '217375', '59038', '236757', '273976']
		bookdata_arr1 = user_recommendations(tempArr[random.randint(0, len(tempArr))])
		bookdata_arr = []
		for b in bookdata_arr1:
			if (len(bookdata_arr) == 15):
				break
			temp = {}
			bookObj = books_info.objects.filter(bookId = b)
			# print(bookObj)
			try:
				temp['id'] = bookObj[0].id
				temp['bookName'] = bookObj[0].bookName
				temp['img'] = "/static/images/" + str(bookObj[0].bookId) + ".jpg"
				temp['author'] = bookObj[0].bookAuthor
				bookdata_arr.append(temp)
			except:
				pass

	finalObj = {
		'pearson': bookdata_arr
	}
	bookdata_arr = []
	nn = ['138954', '123203', '28216', '177386', '106614', '12348', '120797', '190809', '20982', '14049', '275808', '19725', '85653', '57913', '264029', '259006', '92593', '78236', '160346', '167894', '112881', '44920', '18309', '139574', '135673', '25606', '113339', '123801', '105974', '200365', '46099', '256603', '705', '71009', '140337', '84135', '45471', '192158', '17058', '262467', '100452', '76483', '6022', '200993', '182403', '20032', '33535', '246375', '64775', '92547', '67415', '278552', '86959', '189151', '128241', '144107', '626', '76942', '41721', '29702', '190885', '137620', '275967', '203370', '161936', '131602', '214213', '64968']

	bookdata_arr1 = cosineSimilarity(userid)
	if (len(bookdata_arr1) == 0):
		bookdata_arr1 = cosineSimilarity(nn[random.randint(1,20)])

	# print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	# print(bookdata_arr)
	counter = 1
	for b in bookdata_arr1:
		if (counter == 15):
			break
		temp = {}
		bookObj = books_info.objects.filter(bookId = b)
		# print(bookObj)
		try:
			temp['id'] = bookObj[0].id
			temp['bookName'] = bookObj[0].bookName
			temp['img'] = "/static/images/" + str(bookObj[0].bookId) + ".jpg"
			temp['author'] = bookObj[0].bookAuthor
			bookdata_arr.append(temp)
		except:
			pass
		counter += 1
	finalObj['cosine'] = bookdata_arr
	
	numOfBooks = random.randint(1, 15)
	counter = 1
	aa = results.objects.filter(rating__gte = 8)
	print(aa)
	bookdata_arr = set()
	ada = []
	while (counter <= numOfBooks):
		temp = {}
		bookObj = books_info.objects.filter(bookId = aa[counter - 1].bookId)
		print(bookObj)
		try:
			temp['id'] = bookObj[0].id
			temp['bookName'] = bookObj[0].bookName
			temp['img'] = "/static/images/" + str(bookObj[0].bookId) + ".jpg"
			temp['author'] = bookObj[0].bookAuthor
			print(temp)
			prev = len(bookdata_arr)
			bookdata_arr.add(bookObj[0].id)
			if (prev != len(bookdata_arr)):
				ada.append(temp)
		except:
			pass
		counter += 1
	# print(ada)
	finalObj['matrix'] = ada
	pp.pprint(finalObj)
	a = len(finalObj['pearson'])
	b = len(finalObj['cosine'])
	c = len(finalObj['matrix'])
	return render(request, 'minor4.html', {'data': finalObj, 'userid': userid, 'a': a, 'b': b, 'c': c})

def coockoo(request):
	a = request.GET.get('a')
	b = request.GET.get('b')
	c = request.GET.get('c')
	aa = results.objects.filter(rating__gte = 9)
	print(len(aa))
	rr = random.randint(1,4)
	ada = []
	counter = 1
	while (counter <= rr):
		temp = {}
		abc = random.randint(1, 7000)
		bookObj = books_info.objects.filter(bookId = aa[abc].bookId)
		print(bookObj)
		try:
			temp['id'] = bookObj[0].id
			temp['bookName'] = bookObj[0].bookName
			temp['img'] = "/static/images/" + str(bookObj[0].bookId) + ".jpg"
			temp['author'] = bookObj[0].bookAuthor
			print(temp)
			# prev = len(bookdata_arr)
			# bookdata_arr.add(bookObj[0].id)
			# if (prev != len(bookdata_arr)):
			ada.append(temp)
		except:
			pass
		counter += 1
	finalObj = {
		'pearson': ada
	}
	rr = random.randint(1,4)
	ada = []
	counter = 1
	while (counter <= rr):
		temp = {}
		abc = random.randint(1, 7000)
		bookObj = books_info.objects.filter(bookId = aa[abc].bookId)
		print(bookObj)
		try:
			temp['id'] = bookObj[0].id
			temp['bookName'] = bookObj[0].bookName
			temp['img'] = "/static/images/" + str(bookObj[0].bookId) + ".jpg"
			temp['author'] = bookObj[0].bookAuthor
			print(temp)
			# prev = len(bookdata_arr)
			# bookdata_arr.add(bookObj[0].id)
			# if (prev != len(bookdata_arr)):
			ada.append(temp)
		except:
			pass
		counter += 1
	finalObj['cosine'] = ada
	rr = random.randint(1,4)
	ada = []
	counter = 1
	while (counter <= rr):
		temp = {}
		abc = random.randint(1, 7000)
		bookObj = books_info.objects.filter(bookId = aa[abc].bookId)
		print(bookObj)
		try:
			temp['id'] = bookObj[0].id
			temp['bookName'] = bookObj[0].bookName
			temp['img'] = "/static/images/" + str(bookObj[0].bookId) + ".jpg"
			temp['author'] = bookObj[0].bookAuthor
			print(temp)
			# prev = len(bookdata_arr)
			# bookdata_arr.add(bookObj[0].id)
			# if (prev != len(bookdata_arr)):
			ada.append(temp)
		except:
			pass
		counter += 1
	finalObj['matrix'] = ada
	print(finalObj)
	d = len(finalObj['pearson'])
	e = len(finalObj['cosine'])
	f = len(finalObj['matrix'])

	return render(request, 'cuckoorec.html', {'data': finalObj, 'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f})

def minorcharts(request):
	a = request.GET.get('a')
	b = request.GET.get('b')
	c = request.GET.get('c')
	d = request.GET.get('d')
	e = request.GET.get('e')
	f = request.GET.get('f')
	return render(request, 'minorcharts.html', {'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f})

def finalcharts(request):
	a = request.GET.get('a')
	b = request.GET.get('b')
	c = request.GET.get('c')
	d = request.GET.get('d')
	e = request.GET.get('e')
	f = request.GET.get('f')
	return render(request, 'finalcharts.html', {'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f})
