import sqlalchemy
import psycopg2

try:
    conn = psycopg2.connect("dbname='gdp' user='main' host='localhost' password='{}'".format(os.environ['MAIN_PG_PASS']))
except:
    print "I am unable to connect to the database"

cur = conn.cursor()

def insert_into_table (name, data):
    # Name is the table name.
    # Data is a list of tuples to be inserted.
    count = 0
    for tup in data:
        cur.execute("INSERT INTO {} VALUES {}".format (name, tup))
        count += 1
    print('Insert completed. {} rows added.'.format(count))

if __name__ == '__main__':
    pass
