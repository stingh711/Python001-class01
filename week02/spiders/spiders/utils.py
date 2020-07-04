import pymysql.cursors


def insert_movie(name, time, category):
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="v2mprt",
        db="movies",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
    with conn:
        sql = "insert into `movies` (`name`, `time`, `category`) values (%s, %s, %s)"
        cur = conn.cursor()
        cur.execute(sql, (name, time, category,))
        conn.commit()

