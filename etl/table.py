from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table, Unicode, inspect
from sqlalchemy.orm import mapper, create_session, sessionmaker
from sqlalchemy.pool import NullPool
import psycopg2
import traceback
import argparse
import os
import yaml

#host = os.environ['MAIN_RDS_HOST']
#db_name = os.environ['MAIN_RDS_DBNAME']
#user = os.environ['MAIN_RDS_USER']
#password = os.environ['MAIN_RDS_PASS']
#port = os.environ['MAIN_RDS_PORT']
#flavor = 'postgresql'

#dialect+driver://username:password@host:port/database
#connection_string = '{}://{}:{}@{}:{}/{}'.format(flavor, user, password, host, port, db_name)
#engine = create_engine(connection_string)

def create_db_path(flavor, user, password, host, port, db_name, type='sqlalchemy'):
    if type == 'sqlalchemy':
        db_path = '{}://{}:{}@{}:{}/{}'.format(flavor, user, password, host, port, db_name)
    else:
        print('Invalid db_path \'type\' specified. Please choose out of: sqlalchemy')
    return db_path

def read_table_yaml(schema_name, table_name):
    '''File path to table.yaml file to load.'''
    path = 'etl/schema/{}/{}.table.yaml'.format(schema_name, table_name)
    with open(path, 'r') as file:
        data = yaml.load(file)
    print('Table.yaml Data: {}'.format(data))
    return data

def load_session(flavor, user, password, host, port, db_name):
    db_path = create_db_path(flavor, user, password, host, port, db_name)
    engine = create_engine(db_path, echo=False, poolclass=NullPool)

    metadata = MetaData(engine)
    #moz_bookmarks = Table('moz_bookmarks', metadata, autoload=True)
    #mapper(Bookmarks, moz_bookmarks)

    inspector = inspect(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session, metadata, inspector

def create_table(metadata, table_name, schema):
    table_info = read_table_yaml(schema, table_name)
    columns = [col['name'].lower() for col in table_info['fields']]

    t = Table(table_name, metadata, Column('id', Integer, primary_key=True),
        *(Column(col, Unicode(255)) for col in columns))
    print('Creating table \'{}\' with columns: {}'.format(table_name, columns))
    metadata.create_all()

def drop_table(metadata, table_name):
    prompt = input('Are you sure you want to drop the \'{}\' table (yes/no)?'.format(table_name))
    if prompt not in ['yes', 'no']:
        print('Please enter a valid \'yes\' or \'no\' response.')
        exit()
    if prompt == 'yes':
        t = Table(table_name, metadata, autoload=True)
        t.drop()
    if prompt == 'no':
        print('Cancelling table drop operation.')
    #mapper(DynamicTable, t)
    #session.delete(DynamicTable)
    #session.commit()

def read_table(session, metadata, table_name, query=None):
    t = Table(table_name, metadata, autoload=True)
    if query == None:
        output = session.query(t).all()
    else:
        output = session.execute(query)
    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform table operations in RDS DB.')
    parser.add_argument('operation', action='store', nargs=1, type=str
                        , choices=['create_table', 'drop_table', 'update_table', 'read_table', 'list_tables']
                        , help='Specifies the operation to perform.', metavar='table operation')
    parser.add_argument('-t', dest='table_name', nargs=1, type=str
                        , help='Name of the table.', metavar='table name')
    parser.add_argument('-s', dest='schema_name', nargs=1, type=str
                        , help='Name of the schema.', metavar='schema name')
    args = parser.parse_args()

    print('Arguments: {}'.format(args))

    host = os.environ['MAIN_RDS_HOST']
    db_name = os.environ['MAIN_RDS_DBNAME']
    user = os.environ['MAIN_RDS_USER']
    password = os.environ['MAIN_RDS_PASS']
    port = os.environ['MAIN_RDS_PORT']
    flavor = 'postgresql'

    #columns = ['col_test1', 'col_test2', 'col_test3']

    session, metadata, inspector = load_session(flavor, user, password, host, port, db_name)

    if args.operation[0] == 'create_table':
        table_name = args.table_name[0]
        schema = args.schema_name[0]
        create_table(metadata, table_name, schema)
    if args.operation[0] == 'list_tables':
        print('List Tables Object:', inspector.get_table_names(), type(inspector.get_table_names()))
        if not inspector.get_table_names():
            print('No tables exist in the database.')
        else:
            for table_name in inspector.get_table_names():
                print('Table Name: {}'.format(table_name))
                for column in inspector.get_columns(table_name):
                    print("Column: %s" % column['name'])
    if args.operation[0] == 'drop_table':
        table_name = args.table_name[0]
        drop_table(metadata, table_name)
    if args.operation[0] == 'read_table':
        table_name = args.table_name[0]
        output = read_table(session, metadata, table_name)
        print('Output from table \'{}\':\n\t{}'.format(table_name, output))
    if args.operation[0] == 'update_table':
        pass

    print('Closing session.')
    session.close()
