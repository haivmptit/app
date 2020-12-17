import psycopg2
def connection():
    conn = psycopg2.connect(
        database="demo1",
        user="postgres",
        password="songuyento",
        # host="localhost",
        host="postgres",
        port="5432")
    return conn