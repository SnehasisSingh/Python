import pandas as pd
import openpyxl
import json
import time


try:
    df = pd.read_excel('excel_extract_file (1).xlsx')
    json_data = df.to_json(orient='records')
    with open('converted_json.json','w') as f:
        f.write(json_data)
    
   
    
except FileNotFoundError:
    print("File 'resource_groups.xlsx' not found.")
except Exception as e:
    print("An error occurred:", e)

print("------------------------------Converted to Json---------------------------------")
time.sleep(2)
with open('converted_json.json', 'r') as json_file:
    data = json.load(json_file)


with open('Variable.tf', 'w') as f:
    for item in data:
        
        f.write(f'variable "{item["Variable_Name"]}" {{\n')

        if item["Description"] is not None:

            f.write(f'  description = "{item["Description"]}" \n')
       
        f.write(f'  default = "{item["Defult_Value"]}"\n')
        
        f.write('}\n')
print("----------------------------Converted to Variable-------------------------------")
