import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os, sys

load_dotenv()
mysql_pass = os.environ.get("MYSQL_PASSWORD")

queries = [
    #"SELECT * FROM Challenges;",
    #"SELECT Category, SUM(Attempts_Successful) AS successes, SUM(Attempts_Fail) AS fails, ROUND(SUM(Attempts_Successful)/SUM(Attempts_Fail) * 100.0, 2) AS success_rate FROM Challenges GROUP BY Category;",
    #"SELECT Challenge_Name, Category, Attempts_Successful AS successes, (Attempts_Successful + Attempts_Fail) AS attempts, IFNULL(ROUND(Attempts_Successful/(Attempts_Successful + Attempts_Fail) * 100.0, 2), 0) AS success_rate FROM Challenges ORDER BY success_rate DESC LIMIT 30;",
    #"SELECT Category, SUM(Attempts_Successful) AS successes, SUM(Attempts_Fail) AS fails, (SUM(Attempts_Successful) + SUM(Attempts_Fail)) AS attempts, ROUND(SUM(Attempts_Successful)/SUM(Attempts_Fail) * 100.0, 2) AS success_rate FROM Challenges GROUP BY Category;",
    #"SELECT Category, COUNT(*) AS NUM_Challenges, ROUND(COUNT(*) / (SELECT COUNT(*) FROM Challenges) * 100, 2) AS RATIO FROM Challenges GROUP BY Category",
    "SELECT Challenge_Name, Category, Difficulty, Attempts_Successful, Attempts_Fail, (Attempts_Successful + Attempts_Fail) AS attempts, IFNULL(ROUND(Attempts_Successful/(Attempts_Successful + Attempts_Fail) * 100.0, 2), 0) AS success_rate FROM Challenges ORDER BY Category, FIELD(Difficulty, 'Easy', 'Medium', 'Hard');",
]

def main():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password=mysql_pass,
        database="ctf_2025"
    )

    if len(sys.argv) == 2:
        df = pd.read_sql(sys.argv[1], conn)
        print(df)
    else:
        for query in queries: 
            df = pd.read_sql(query, conn)
            print(df)

    conn.close()

if __name__ == "__main__":
    main()