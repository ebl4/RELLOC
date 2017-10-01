import pymysql


def database_connection():
	conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='extractor')

	cur = conn.cursor()

	cur.execute("SELECT id, subject_type, subject_value, object_type, object_value FROM triple WHERE subject_type = 'LOCATION' OR object_type = 'LOCATION' LIMIT 100")

	# for row in cur:
	#     print(row)

	cur.close()
	conn.close()

	return cur