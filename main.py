# Writer      : Adrien Duchâtel
# Date        : 2025/01/03
# Customer    : ABC News
# Environment : ALL
# Description : This script is used to modify Pyramid JSON Inspectors based on old and new fields. It parses JSON inspectors, look for a list of new fields in it and replace it with an associated new field, creating a new JSON Inspector.


import json
import os
import csv
from tqdm import tqdm
import argparse


class Main():

    # Define HTTP call parameters
    def __init__(self, jsonData, filename, searchFieldDict, newInspectorFolder, DEBUG):
        self.jsonData = jsonData
        self.filename = filename
        self.searchFieldDict = searchFieldDict
        self.newInspectorFolder = newInspectorFolder
        self.DEBUG = DEBUG

                    

    # 2. Find old fields
    def CheckField(self):
        oldFields = [] # list of old fields
        newFields = [] # list of new fields
        modified = []  # list of fields to modify

        # get all the old fields
        for values in self.searchFieldDict :
            oldFields.append(values['old field'])
            newFields.append(values['new field'])
        
        # find all fields to modify
        for k in tqdm(oldFields, desc=f'[{self.filename}] : Check fields'):
            if k in str(self.jsonData):
                modified.append(k)

        # modify json and write new one
        if len(modified) > 0:
            if DEBUG >= 2: 
                print(f' [{self.filename}] Fields to modify : {modified}')
            self.Write(modified, oldFields, newFields)
        else : 
            if DEBUG == 3: 
                print(f' [{self.filename}] No fields to modify - Skip')

            

    # 3. Write new JSON
    def Write(self, modified, oldFields, newFields):
        jsonData = json.dumps(self.jsonData, indent=4)

        # replace all fields
        for oldField in tqdm(modified, desc=f'[{self.filename}] : Replace fields'):
            fieldIndex = oldFields.index(oldField)
            if DEBUG == 3: 
                print(f' [{self.filename}] Old field {oldField} has index {fieldIndex}')
            newField = newFields[fieldIndex]
            if DEBUG == 3:
                print(f' [{self.filename}] Old field {oldField} have associated new field {newField}')

            jsonData = jsonData.replace(oldField, newField)            
            if DEBUG >= 2: 
                print(f' [{self.filename}] Replace : {oldField} --> {newField}')

        # write new json
        with open(f'./{self.newInspectorFolder}/{self.filename}', 'w', encoding='utf-8') as f:
            f.write(jsonData)





if __name__ == '__main__' :
    
    # Cmd & Help
    parser = argparse.ArgumentParser(description= "Replace fields in Inspector", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-old',    action='store', type=str, help='Path of the folder for the JSON inspectors to check',           required=False, default='./old')
    parser.add_argument('-new',    action='store', type=str, help='Path of the folder for the newly created JSON inspectors',      required=False, default='./new')
    parser.add_argument('-fields', action='store', type=str, help='Path of the CSV file listing all the fields to check & modify', required=False, default ='fields.csv')
    parser.add_argument('-debug',  action='store', type=int, help='DEBUG level - log more info from low (1) to many (3) (1, 2, 3)', required=False, default =1)

    args   = parser.parse_args()
    config = vars(args)
    oldInspectorFolder = config.get('old')
    newInspectorFolder = config.get('new')
    fields             = config.get('fields')
    DEBUG              = config.get('debug')


    # Get fields from CSV
    with open(fields, 'r') as file:
        csv_reader = csv.DictReader(file)
        searchFieldDict = [row for row in csv_reader]


    # parse all jsons into directory
    jsons = os.listdir(oldInspectorFolder)

    for filename in jsons:
        filePath = f'{oldInspectorFolder}/{filename}'

        with open(filePath) as data :
            d = json.load(data)

            run = Main(d, filename, searchFieldDict, newInspectorFolder, DEBUG)
            run.CheckField()