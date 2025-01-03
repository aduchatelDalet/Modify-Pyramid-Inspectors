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

#### Running code
```cmd
python3 main.py [-h] [-old OLD] [-new NEW] [-fields FIELDS] [-debug DEBUG]
```
  - OLD : Path of the folder for the JSON inspectors to check (default: ./old)
  - NEW : Path of the folder for the newly created JSON inspectors (default: ./new)
  - FIELDS : Path of the CSV file listing all the fields to check & modify (default: .fields.csv)
  - DEBUG : DEBUG mode - log more info about found & modified fields (default: False)