import csv
import re
from pathlib import Path
from dotenv import load_dotenv
import os


load_dotenv()
challenge_stats_csv = os.environ.get("CHALLENGE_STATS")
challenge_archive_csv = os.environ.get("CHALLENGE_DATASHEETS")

folder = Path(challenge_archive_csv)

table_name = "Challenges"
table_fields = {
    "uuid": "INTEGER PRIMARY KEY", 
    "Challenge_Name": "VARCHAR(50)", 
    "Category": "VARCHAR(50)", 
    "Points": "INTEGER", 
    "Difficulty": "VARCHAR(20)", 
    "Attempts_Successful": "INTEGER", 
    "Attempts_Fail": "INTEGER"
}

def get_challengeDifficulties() -> dict:
    difficulty_levels: dict = {}
    
    for file in folder.iterdir():
        if file.is_file():
            with open(file, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    if row.get("Added to Cloud CTF") == "TRUE":
                        c_name = row.get("Challenge Name").strip()

                        if "VMs" in file.name:
                            match = re.search(r"\[(.*?)\]", c_name)
                            c_name = match.group(1) 
                        
                        difficulty_levels[c_name] = f"\"{row.get("Difficulty").strip().capitalize()}\""

    return difficulty_levels


def create_tableQuery() -> str:
    s = f"DROP TABLE {table_name};\n\nCREATE TABLE {table_name} (\n"
    for key, val in table_fields.items():
        s += f"\t{key} {val}"

        if key != list(table_fields.keys())[-1]:
            s += ","
        
        s += "\n"

    s += ");"
    
    return s

def main() -> None:
    total_queries = 0
    with open("ctfChallengeStats_table.sql", "w") as sqlFile:
        sqlFile.write(create_tableQuery() + "\n\n")

        with open(challenge_stats_csv, newline="", encoding="utf-8") as csvfile: 
            reader = csv.DictReader(csvfile)    

            diff_levels = get_challengeDifficulties()

            uuid = 0
            for row in reader:
                uuid += 1

                diff = "NULL"
                if row.get("Challenge").strip() in diff_levels:
                    diff = diff_levels[row.get("Challenge").strip()]

                category = row.get("Category").capitalize().strip()
                if category == "Linux" or category == "Windows":
                    category = "VM_"+category

                values = f'''{uuid}, "{row.get("Challenge").strip()}", "{category}", {row.get("Points").strip()}, {diff}, {row.get("Successful Attempts").strip()}, {row.get("Failed Attempts").strip()}'''
                
                sqlFile.write(f"INSERT INTO {table_name} ({", ".join(table_fields.keys())}) VALUES ({values});\n")

        sqlFile.write("\n\n")


        total_queries = uuid


    print(f"\nSQL queries for {total_queries} CTF challenges created!")

if __name__ == "__main__":
    main()