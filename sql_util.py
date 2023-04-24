import apsw
import os
import sys

DB_FILE = os.environ.get("IMPREZZA_REPORTING_DB", "imprezza-report.db")
REQUIRED_TABLES = {
    'cpc_event',
    'pixel_event',
    'order_transaction',       
    'product_line_item_sale',
    }

def assert_db(filename=DB_FILE):
    print("testing database")
    if not os.path.isfile(filename) or not os.path.getsize(filename) > 0:
        print(f"Database file '{filename}' is not present or is empty") 
        sys.exit(1)
    try:
        with apsw.Connection(filename) as conn:
            assert_tables(conn) 
    except apsw.SQLError:
        print(f"Database file '{filename}' is present but is not a sqlite file") 
        sys.exit(1)


def assert_tables(conn,required_tables=REQUIRED_TABLES):
    result =  conn.cursor().execute("select name from sqlite_master where type='table'")
    tables_in_db = set([ name for name, in result])

    missing = False
    for required_table in required_tables:
        if required_table not in tables_in_db:
            missing = True
            print(f"Table {required_table} required but not in database.")
    if missing:
        print("Missing tables. Exiting")
        sys.exit(1)


def execute_sql(sql,filename=DB_FILE,bound_data=()):
    with apsw.Connection(filename) as conn:
        result = conn.cursor().execute(sql,bound_data)
        for tup in result:
            yield tup

def execute_sql_one(sql,filename=DB_FILE):
    return next(execute_sql(sql))



