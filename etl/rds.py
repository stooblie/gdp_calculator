import psycopg2
import os
import boto3

rds_host = os.environ['MAIN_RDS_HOST']
db_name = os.environ['MAIN_RDS_DBNAME']
user = os.environ['MAIN_RDS_USER']
password = os.environ['MAIN_RDS_PASS']

conn = psycopg2.connect(host=rds_host,
                        database=db_name,
                        user=user,
                        password=password)

cur = conn.cursor()

conn.close()

if __name__ == '__main__':
    print('Success')
