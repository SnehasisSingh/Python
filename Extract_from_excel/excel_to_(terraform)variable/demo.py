import json
import pandas as pd
import openpyxl
import json
import time

######################   Declare Section ##############################################
 
Access_type_opt = ["shared","single_user","no_issolation_shared"]
max_worker=100000
auto_terminate_min=43200  # 43200 Minitues 
#########################################################################################
try:
    df = pd.read_excel('excel_extract_file (1).xlsx')
    json_data = df.to_json(orient='records')
    with open('converted_json.json','w') as f:
        f.write(json_data)
    
   
    
except FileNotFoundError:
    print("File 'resource_groups.xlsx' not found.")
except Exception as e:
    print("An error occurred:", e)


# Read data from JSON file
with open('converted_json.json', 'r') as json_file:
    data = json.load(json_file)

time.sleep(3) #avoid  error

with open('Variable_test.tf', 'w') as f:
    for item in data:


    #######################   Variable Name    ########################################
        #No_space #lower # convert '-' to '_'
        validate_new_variable  = item["Variable_Name"].lower() and item["Variable_Name"].replace(" ", "") and item["Variable_Name"].replace("-", "_")

        if  validate_new_variable.isidentifier() == True:
            f.write(f'variable "{validate_new_variable}" {{\n')
        else:
            raise Exception("InvalidIdentifier (Startes with a number/White_Space/ Special_character)")
        

    #######################   Description      ##########################################
        if item["Description"] is not None:
            f.write(f'description = "{item["Description"]}" \n')
       
    #####################   Defult  configuration (diff (str,int and (sub id , resourse_id)))            ###########################################
        if validate_new_variable!="databricks_resource_id" or "subscription_id":
            if type(item["Defult_Value"]) == str:
                defult_value_valaidate = item["Defult_Value"].replace(" ","") and item["Defult_Value"].lower()
            else:
                defult_value_valaidate = item["Defult_Value"]
        else:
            f.write(f'  default = "{defult_value_valaidate}"\n')
        ###########################            owner          ###########################################

        if validate_new_variable == 'owmner':
            if  defult_value_valaidate.endswith("@virtusa.com"):
                f.write(f'  default = "{defult_value_valaidate}"\n')
            else:
               raise Exception(f"Invalid Email of Virtusa.com : {defult_value_valaidate}")
            
        #######################   cluster_autotermination_minutes ##################################

        elif validate_new_variable == 'cluster_autotermination_minutes':
            if  type(defult_value_valaidate) == int and defult_value_valaidate< auto_terminate_min:
               f.write(f'  default = "{defult_value_valaidate}"\n')
            else:
                raise Exception (f"InvalidDataType/Time Limit Exceed {validate_new_variable}:{defult_value_valaidate}")
            
        ##########################    cluster_num_workers ########################################

        elif validate_new_variable == 'cluster_num_workers':
            if type(defult_value_valaidate) == int and defult_value_valaidate <= max_worker :
                f.write(f'  default = "{defult_value_valaidate}"\n')
            else:
                raise Exception (f"InvalidDataType or Out of Index Error :{defult_value_valaidate}")
            
        elif validate_new_variable =='access_type':
            for access_var in Access_type_opt:
                if defult_value_valaidate == access_var :
                    found = True
                    f.write(f'default = "{defult_value_valaidate}"\n')
                    break
                if not found:
                    raise ValueError(f"Invalid option {defult_value_valaidate}")  
                

            

        ############################# 
        else:
            f.write(f'  default = "{defult_value_valaidate}"\n')
        f.write('}\n\n')