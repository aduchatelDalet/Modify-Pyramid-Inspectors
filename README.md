# Finding & replacing fields into an Inspector

### Motivation 
At ABC we had to recreate new fields and modify the existing ones, so going through each Inspector to verify if it includes one of the modified fields would have been really long and we would most likely forgot to update few fields. 

Here we can specify a list of old and new fields, and the code will replace the values into the inspectors, so we have a new inspector with all the modified fields.

***

### Usage 
#### General 
We have one CSV file regrouping all the old fields (to be replaced) and the new fields. 
We have two folders, one for storing the old Inspectors (the ones to modify) and one for the newly created Inspectors, based on the fields you specified on the CSV.

#### CSV file 
It regroups all the fields you want to replace. 
Edit that CSV file, first column is "old fields" and second column is "new fields".

WARNING : DO NOT put any space on the CSV file, or it will be included into the string for comparison

#### Running code
```cmd
python3 main.py [-h] [-old OLD] [-new NEW] [-fields FIELDS] [-debug DEBUG]
```
  - OLD : Path of the folder for the JSON inspectors to check (default: ./old)
  - NEW : Path of the folder for the newly created JSON inspectors (default: ./new)
  - FIELDS : Path of the CSV file listing all the fields to check & modify (default: .fields.csv)
  - DEBUG : DEBUG level - log more info from low (1) to many (3) (1, 2, 3)
    - Level 1 : Only logs the steps and the number of fields handled for each JSON
    - Level 2 : Logs everything specified in debug level 1 + the value of the replaced fields for each JSON
    - Level 3 : Logs everything specified in debug level 1 and 2 + the field index and associated old-new value

    Example : 
    ```cmd 
     python3 main.py 
     -old '/home/adrien/Documents/oldInspectors/' 
     -new '/home/adrien/Documents/newInspectors/' 
     -fields '/home/adrien/Documents/fieldsToChange.csv'
     -debug 2
     ```