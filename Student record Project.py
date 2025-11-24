import json
import os
import pandas as pd
from sys import exit

save_file = "C:\\Python\\assignment\\savedata.json"
    

def main():
    data = load_data(save_file)
    menu = "\nStudent Management\n1) List all\n2) Add student\n3) Update student\n4) Delete student\n5) Save and exit\n6) Exit without saving\nEnter an option :)\n "

    while True:
        userInp = input(menu)

        if userInp == "1":
            print_students(data)
        elif userInp == "2":
            name = input("Enter name: ").strip()
            age = input("Enter age (optional): ").strip() or None
            grade = input("Enter grade (optional): ").strip() or None
            email = input("Enter email (optional): ").strip() or None
            address = input("Enter address (optional): ").strip() or None
            data = add_studentRec(data, name, age, grade, email, address)
            print("Student added :)")
        elif userInp == "3":
            studentID = input("Enter student ID to update: ").strip()
            if studentID.isdigit() == False:
                print("Invalid Input")
                continue
            studentID = int(studentID)
            fields = {}
            for field in ["name", "age", "grade", "email", "address"]:
                val = input(f"Enter new {field} (leave blank to skip): ").strip()
                if val != "":
                    fields[field] = val
            try:
                data = update_student_rec(data, studentID, **fields)
                print("Student updated :)")
            except KeyError as p:
                print(p)
            
        elif userInp == "4":
            studentID = input("Enter student ID to delete: ").strip()
            if studentID.isdigit() == False:
                print("Invalid Input")
                continue
            studentID = int(studentID)
            try:
                data = delete_student_rec(data, studentID)
                print("Student deleted :)")
            except KeyError as q:
                print(q)

        elif userInp == "5":
            save_data(data, save_file)
            print("Data saved :D")
            exit()

        elif userInp == "6":
            print("Exiting without saving :)")
            exit()

        else:
            print("Invalid option, try again :(")

import os
import pandas as pd

default_headers = ["id", "name", "age", "grade", "email", "address"]

def load_data(path):
    # if path doesn't exist, return empty dataframe
    if os.path.exists(path) == False:
        return pd.DataFrame(columns=default_headers)
    try:
        data = pd.read_json(path, orient="records")
        # make sure that dataframe always has all the default headers
        for c in default_headers:
            if c not in data.columns:
                data[c] = pd.NA
        data = data[default_headers]
        return data
    except ValueError:
        # if the file is invalid
        return pd.DataFrame(columns=default_headers)

def create_new_rec(data):
    if data.empty:
        return 1
    try:
        return int(data["id"].max()) + 1
    except Exception:
        return 1

def add_studentRec(data, name, age=None, grade=None, email=None, address=None):
    studentID = create_new_rec(data)
    new_student = {"id": studentID, "name": name, "age": age, "grade": grade, "email": email, "address": address}
    data = pd.concat([data, pd.DataFrame([new_student])], ignore_index=True)
    return data

def save_data(data, path):
    data.to_json(path, orient="records", indent=2, force_ascii=False)
    print(path)

def update_student_rec(data, student_id, **fields):
    thingy = data["id"] == student_id
    if thingy.any() == False:
        raise KeyError(f"Student id {student_id} not found")
    for k, v in fields.items():
        if k in data.columns:
            data.loc[thingy, k] = v
    return data

def print_students(data):
    if data.empty:
        print("No records found.")
    else:
        print(data.to_string(index=False))

def delete_student_rec(data, student_id):
    if (data["id"] == student_id).any() == False:
        raise KeyError(f"Student id {student_id} not found")
    return data[data["id"] != student_id].reset_index(drop=True)

main()
