import pyodbc
import pandas as pd

from tqdm import tqdm




def insert_data_from_linkedin(conn, table_name, df):

    for index, row in tqdm(df.iterrows(), total=len(df), desc='Inserting linkedin jobs to DB'):
        post_date = row.iloc[0]
        job_title = str(row.iloc[1])
        job_description = str(row.iloc[2])
        company = str(row.iloc[3])
        location = str(row.iloc[4])
        seniority = str(row.iloc[5])
        employement_type = str(row.iloc[6])
        job_functions = str(row.iloc[7])
        industry = str(row.iloc[8])
        

        cursor = conn.cursor()
        cursor.execute('INSERT INTO ' + table_name + ' VALUES(?,?,?,?,?,?,?,?,?)', post_date,job_title,job_description,company,location,seniority,employement_type,job_functions,industry)
        conn.commit()




def insert_data_from_bayt(conn, table_name, df):


    for index, row in tqdm(df.iterrows(), total=len(df), desc='Inserting bayt jobs to DB'):
        post_date = row.iloc[0]
        job_title = str(row.iloc[1])
        job_description = str(row.iloc[2])
        company = str(row.iloc[3])
        location = str(row.iloc[4])
        industry = str(row.iloc[5])
        

        cursor = conn.cursor()
        cursor.execute('INSERT INTO ' + table_name + ' VALUES(?,?,?,?,?,?)', post_date,job_title,job_description,company,location,industry)
        conn.commit()
        





df = pd.read_csv('total_skills_test27072024.csv')

#Database connection
con_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:prepa-insights.database.windows.net,1433;Database=stevenjobs;Uid=aziz_admin;Pwd=Insightsprepa12;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=700;"

conn = pyodbc.connect(con_string)

conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
conn.setencoding(encoding='utf-8')

conn.autocommit = True


def insert_skills (conn, table_name, df):

    for row in tqdm(df.skills.values):
        skills = row
        

        cursor = conn.cursor()
        cursor.execute('INSERT INTO ' + table_name + ' VALUES(?)', skills)
        conn.commit()

