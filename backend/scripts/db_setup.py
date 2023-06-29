import mysql.connector
import os

cnx = mysql.connector.connect( host='db', user='root', password='password' )

cursor = cnx.cursor()

cursor.execute('CREATE DATABASE IF NOT EXISTS sdcs')
cursor.execute('USE sdcs')

################
### DATABASE Schema Setup
################

with open('data/schema.sql') as f:
    sql_dump = f.read()

for command in sql_dump.split(';'):
    try:
        cursor.execute(command)
    except mysql.connector.Error as err:
        print('Failed to execute command:', err)

################
### Seed Database
################
cnx.start_transaction()

discord_id = os.getenv('TEST_DISCORD_USER_ID')
print(f"Seeding database with test discord user {discord_id}...")

cursor.execute(f"""
  INSERT IGNORE INTO campaign (theatre, start)
  VALUES ('Syria', '2021-01-01 00:00:00')
""")

cursor.execute(f"""
  INSERT IGNORE INTO user (discord_id)
  VALUES ("{discord_id}")
""")

cursor.execute(f"""
  INSERT IGNORE INTO userside (user_id, campaign_id, coalition)
  VALUES (
    (SELECT id FROM user WHERE discord_id = "{discord_id}"),
    (SELECT id FROM campaign ORDER BY id DESC LIMIT 1),
    "blue"
  )
""")

cnx.commit()

cursor.close()
cnx.close()
