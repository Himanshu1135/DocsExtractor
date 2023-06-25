import os
import re
import json
from utilis import dob,pan_No,pan_names_person
from utilis import pytess_text,pan_names_father
from utilis import get_Aadhaar_name,dob,gender,Aadhaar_no
from utilis import pytess_text


def info_Extractor(option,img_path,result_path):
    '''
    input1 : Option{0,1} 0 = Aadhaar card , 1 = Pan Card docs
    input2 : image path
    input3 : result path where to save result directory
    working : Extract information from image using ocr and regex
    return : List of information
    '''
    result = []
    
#-------- for filename extraction 
    filename_with_extension = os.path.basename(img_path)       
    filename = os.path.splitext(filename_with_extension)[0]

#-------- for text extraction using pytess OCR 
    text = pytess_text(img_path)                               
#-------- Cleaning Text 
    text = text.strip().replace('\n', ' ').replace('  ', ' ')  
    text = re.sub(r'[^A-Za-z0-9/\s]', '', text)

    if option == 0:
#-------------- Aadhaar Card

    #------- infomation extracction 
        name_arr = get_Aadhaar_name(text)                           
        Gender =gender(text)
        Aadhaar_No=Aadhaar_no(text)
        Date = dob(text)

    #-------- joining name and cleaning 
        Name = ' '.join(name_arr)
        Name = re.sub(r'[^A-Za-z\s]', '', Name)

        # result.append([filename,Name,Gender,Aadhaar_No,Date,text])

    # ----------- Storing data in json format
        data = {
        "Name ": Name,
        "Gender": Gender,
        "Aadhaar No": Aadhaar_No,
        "Date of Birth": Date,
    }
        file_path = result_path +"/" + filename  # Replace with the desired directory path
        with open(file_path, "w") as json_file:
            json.dump(data, json_file)

    elif option == 1:
#--------------- Pan Card 

    #-------- Extracting info
        name = pan_names_person(text)
        f_name = pan_names_father(text)
        pan_no = pan_No(text)
        Date = dob(text)
    #----- Clean names info 
        Name = ' '.join(name)
        Name = re.sub(r'[^A-Za-z\s]', '', Name)
        f_Name = ' '.join(f_name)
        f_Name = re.sub(r'[^A-Za-z\s]', '', f_Name)
# ----------- Storing data in json format
        data = {
        "Name ": Name,
        "Father Name": f_Name,
        "Date of Birth": Date,
        "Pan No": pan_no
    }
        file_path = result_path +"/" + filename  # Replace with the desired directory path
        with open(file_path, "w") as json_file:
            json.dump(data, json_file)

    else:
        print("Enter correct option : 0 - Aadhaar card , 1 - pan card")

if __name__ == "__main__":
    
    PATH = r"D:\Stractmine\image\testing\t3.png"
    RESULT_PATH = "D:\Stractmine\Final_results"
    try:
        info_Extractor(1,PATH,RESULT_PATH)
        print("Done")   
    except Exception as e:
        print("Error Found : ",e)
    

    