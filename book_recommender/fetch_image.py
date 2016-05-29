import urllib.request
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='bhavya', db='minor2',autocommit=True)
cur = conn.cursor()
conn.autocommit(True)
cur.execute("SELECT DISTINCT bookid FROM results;")
user_details_data = cur.fetchall()
for u in user_details_data:
	strin = "SELECT img2 FROM books_name WHERE bookid = '%s';" % (str(u[0]))
	cur.execute(strin) 
	books_data = cur.fetchall()
	print(books_data[0][0])
	strin = "static/images/%s.jpg" % (str(u[0]))
	urllib.request.urlretrieve(books_data[0][0], strin) 
	print(strin)