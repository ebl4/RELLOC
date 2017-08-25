import pymysql


def database_connection():
	conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='extractor')

	cur = conn.cursor()

	cur.execute("SELECT id, subject_type FROM triple")

	print()

	for row in cur:
	    print(row)

	cur.close()
	conn.close()