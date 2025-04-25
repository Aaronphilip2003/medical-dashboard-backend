# import clickhouse_connect

# def get_db_client():
#     return clickhouse_connect.get_client(
#         host='localhost',
#         port=8123,
#         username='default',
#         password='',
#         database='default'
#     )

# client = get_db_client() 
# # nvYid9.YcRPRU
import clickhouse_connect

def get_db_client():
    return clickhouse_connect.get_client(
        host='wu44ehj45r.asia-southeast1.gcp.clickhouse.cloud',
        port=8443,
        username='default',
        password='nvYid9.YcRPRU',
        database='default',
        secure=True
    )

client = get_db_client()