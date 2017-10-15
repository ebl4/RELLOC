import pymysql


def database_connection():
	conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='extractor')

	cur = conn.cursor()

	cur.execute("SELECT id, subject_type, subject_value, object_type, object_value FROM triple WHERE subject_type = 'LOCATION' AND object_type != 'LOCATION' OR subject_type != 'LOCATION' AND object_type = 'LOCATION'")

	# for row in cur:
	#     print(row)

	cur.close()
	conn.close()

	return cur

def database_write(e, l, p, gPoint, dPoint, geof):
	conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='extractor')

	cur = conn.cursor()

	print("writing to db")

	try:
		cur.execute("""INSERT INTO corresp(entity_name,location_name,pid,gnPoint,dbPoint,geo_feature) VALUES (%s,%s,%s,%s,%s,%s)""", (e,l,p,gPoint,dPoint,geof))
		print("wrote to db")
		conn.commit()
	except:
		print("deu rollback")
		conn.rollback()

	cur.close()
	conn.close()

