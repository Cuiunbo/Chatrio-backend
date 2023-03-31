import mysql.connector

# 连接数据库
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345677',
    database='library'
)

print(conn.info_query)

