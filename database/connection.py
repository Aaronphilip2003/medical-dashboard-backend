import clickhouse_connect

def get_db_client():
    return clickhouse_connect.get_client(
        host='localhost',
        port=8123,
        username='default',
        password='',
        database='default'
    )

client = get_db_client() 