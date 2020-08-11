import os
import sqlite3
import pandas as pd



# Clear example.db if it exists
if not os.path.exists('accounts.db'):

# Create a database
    conn = sqlite3.connect('accounts.db')

# Add the data to our database
    data_url = [['test','tester','Utest','testing','test','1929','Test Agency','Tester','test123','test@gmail.test','test','Anywhere-US']]
    headers = ['first_name','last_name','school','degree','field','year','current_employer','job_title','user_name','contact','password','location']
    data_table = pd.DataFrame(data=data_url, columns=headers)
    data_table.to_sql('data_table', conn, dtype={
    'first_name':'VARCHAR(256)',
    'last_name':'VARCHAR(256)',
    'scool':'VARCHAR(256)',
    'degree':'VARCHAR(256)',
	'field':'VARCHAR(256)',
	'year':'VARCHAR(4)',
	'current_employer':'VARCHAR(256)',
	'job_title':'VARCHAR(256)',
	'user_name':'VARCHAR(256)',
	'contact':'VARCHAR(256)',
    'password':'VARCHAR(256)',
    'location':'VARCHAR(256)'
})

else:
    conn = sqlite3.connect('accounts.db')

conn.row_factory = sqlite3.Row

# Make a convenience function for running SQL queries
def sql_query(query):
    conn = sqlite3.connect('accounts.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def authenticate(query,var):
    print(query, var)
    conn = sqlite3.connect('accounts.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query,var)
    rows = cur.fetchall()
    for rw in rows:
        print(rw['user_name'], rw['password'])
    return rows

def sql_edit_insert(query,var):
    conn = sqlite3.connect('accounts.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query,var)
    conn.commit()

def sql_delete(query,var):
    cur = conn.cursor()
    cur.execute(query,var)

def sql_query2(query,var):
    conn = sqlite3.connect('accounts.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query,var)
    rows = cur.fetchall()
    return rows

def sql_disconnect():
    conn.close()    
