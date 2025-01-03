# Writer      : Adrien Duchâtel
# Date        : 2025/01/03
# Customer    : ABC News
# Environment : ALL
# Description : This script is used to modify Pyramid JSON Inspectors based on old and new fields. It parses JSON inspectors, look for a list of new fields in it and replace it with an associated new field, creating a new JSON Inspector.


import json
import os
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
        oldFields = self.searchFieldDict.keys()
        modified = []   # list of fields to modify
        
        # find all fields to modify
        for k in tqdm(oldFields, desc=f'[{self.filename}] : Check fields'):
            if k in str(self.jsonData):
                if DEBUG:
                    print(f' [{self.filename}] Found   : {k}')
                modified.append(k)

        # modify json and write new one
        if len(modified) > 0:
            self.Write(modified)

            

    # 3. Write new JSON
    def Write(self, modified):

        # replace all fields
        for oldField in tqdm(modified, desc=f'[{self.filename}] : Replace fields'):
        #for oldField in modified:
            fieldIndex = list(self.searchFieldDict.keys()).index(oldField)
            newField = list(self.searchFieldDict.values())[fieldIndex]

            if DEBUG : 
                print(f' [{self.filename}] Replace : {oldField} --> {newField}')

            str(self.jsonData).replace(oldField, newField)


        # write new json
        with open(f'./{self.newInspectorFolder}/{self.filename}', 'w') as f:
            json.dump(self.jsonData, f, indent=2)





if __name__ == '__main__' :
    
    # Cmd & Help
    parser = argparse.ArgumentParser(description= "Replace fields in Inspector", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-old',    action='store', type=str,  help='Path of the folder for the JSON inspectors to check',           required=False, default='./old')
    parser.add_argument('-new',    action='store', type=str,  help='Path of the folder for the newly created JSON inspectors',      required=False, default='./new')
    parser.add_argument('-fields',  action='store', type=str, help='Path of the CSV file listing all the fields to check & modify', required=False, default ='.fields.csv')
    parser.add_argument('-debug',  action='store', type=bool, help='DEBUG mode - log more info about found & modified fields',      required=False, default =False)

    args   = parser.parse_args()
    config = vars(args)
    oldInspectorFolder = config.get('old')
    newInspectorFolder = config.get('new')
    fields             = config.get('fields')
    DEBUG              = config.get('debug')

    # Old field : new field
    searchFieldDict = {
        "TITLE_Id" : "Asset ID",
        "TITLE_Name" : "Asset Name",
        "TITLE_Duration" : "Duration",
        "Show_Show" : "Show",
        "ABC_Common_ShootAirDate" : "Shoot Air Date",
        "abc-shoot-source" : "Shoot Feed Source",
        "abc-shoot-sender" : "Shoot Sender",
        "abc-shoot-location" : "Shoot Location",
        "ABC_Mars_AssignmentOrIDNumber" : "Assignment Number",
        "ABC_Mars _Restrictions" : "Restriction_Description",
        "abc-visual-verification-status" : "Visual Verification",
        "abc-asset-licensed" : "Licensed",
        "abc-clearance" : "Clearance",
        "abc-asset-credits" : "Credits",
        "TITLE_Keywords" : "Keyword",
        "ABC_Snapstream_Actor" : "Person",
        "ABC_Avid_VideoID" : "Video ID",
        "Package Name" : "Batch Name",
        "ABC_Snapstream_StationCallsign" : "Call Sign",
        "ABC_Snapstream_StationName" : "Station Name",
        "ABC_Snapstream_SeriesTitle" : "Series Title",
        "ABC_Snapstream_Description" : "Show Info",
        "ABC_Snapstream_Actor" : "Actor",
        "abc-mob-id" : "MOB ID"
    }

    # parse all jsons into directory
    jsons = os.listdir(oldInspectorFolder)

    for filename in jsons:
        filePath = f'{oldInspectorFolder}/{filename}'

        with open(filePath) as data :
            d = json.load(data)

            run = Main(d, filename, searchFieldDict, newInspectorFolder, DEBUG)
            run.CheckField()