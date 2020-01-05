#import asyncio
#import asyncpg
import psycopg2
import os
import boto3

rds_host = os.environ['MAIN_RDS_HOST']
db_name = os.environ['MAIN_RDS_DBNAME']
user = os.environ['MAIN_RDS_USER']
password = os.environ['MAIN_RDS_PASS']

def connect(rds_host, db_name, user, password):
    conn = psycopg2.connect(host=rds_host,
                        database=db_name,
                        user=user,
                        password=password)
                        cur = conn.cursor()
    conn.close()


#async def run(rds_host, db_name, user, password):
    #conn = await asyncpg.connect(user=user, password=password, database=db_name, host=rds_host)
    #await conn.close()

if __name__ == '__main__':
    rds_host = os.environ['MAIN_RDS_HOST']
    db_name = os.environ['MAIN_RDS_DBNAME']
    user = os.environ['MAIN_RDS_USER']
    password = os.environ['MAIN_RDS_PASS']

    #asyncio.get_event_loop().run_until_complete(run(rds_host, db_name, user, password))
    connect(rds_host, db_name, user, password)

    print('Success')
