from django.db import models

# Create your models here.

class results(models.Model):
	userId = models.IntegerField()
	bookId = models.CharField(max_length = 255)
	rating = models.IntegerField()

	def __str__(self):
		return str(self.userId) + " " + self.bookId + " " + str(self.rating)

class books_info(models.Model):
	bookId = models.CharField(max_length = 255)
	bookName = models.CharField(max_length = 255)
	bookAuthor = models.CharField(max_length = 255)
	year = models.IntegerField()
	publisher = models.CharField(max_length = 255)
	img1 = models.CharField(max_length = 255)
	img2 = models.CharField(max_length = 255)
	img3 = models.CharField(max_length = 255)

	def __str__(self):
		return self.bookName