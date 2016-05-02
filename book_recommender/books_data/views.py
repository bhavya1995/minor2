from django.shortcuts import render
from django.http import HttpResponse,Http404
import json
from books_data.models import *
# Create your views here.

def home(request):
	return render(request,'minor.html')

def submitUserId (request):
	userID = request.GET.get('userid')
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
			temp['img'] = bookObj[0].img2
			temp['author'] = bookObj[0].bookAuthor
			bookdata_arr.append(temp)
		except:
			pass
	print(bookdata_arr)
	return render(request, 'page2minor.html', {"data": bookdata_arr})