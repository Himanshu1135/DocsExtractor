import os
import re
import time
import csv
import glob
from utilis import get_Aadhaar_name,dob,gender,Aadhaar_no
from utilis import pytess_text

# Only for generation of csv for many Aadhaar docs together and testing Aadhaar function


def Aadhaar_info_extractor(img_path):
    '''
    input : image path
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
    text = re.sub(r'[^A-Za-z0-9/\s-]', '', text)

#------- infomation extracction 

    name_arr = get_Aadhaar_name(text)                           
    Gender =gender(text)
    Aadhaar_No=Aadhaar_no(text)
    Date = dob(text)

#-------- joining name and cleaning 
    Name = ' '.join(name_arr)
    Name = re.sub(r'[^A-Za-z\s]', '', Name)

    result.append([filename,Name,Gender,Aadhaar_No,Date,text])

    return result

# -------------------------------------------------------------- CSV GENERATION --------------------------------------------#

##------------ Use glob to get a list of all image file paths in the folder
# IMAGE_FOLDER_PATH = r'D:\Stractmine\image\testing\A'  # Replace with your folder path
# image_extensions = ['*.jpg', '*.jpeg', '*.png']  # Add more extensions if needed

# image_files = []
# for ext in image_extensions:
#     image_files.extend(glob.glob(IMAGE_FOLDER_PATH + '/' + ext))

# #-------- for collecting all info in data 
# data = []
# data.append(['FileName','Name','Gender','Aadhaar_No','DOB','Text'])

# # --------- for time taken 
# t1 = time.time()

# # --------- extracting info for each img and adding to data array
# for img_path in image_files:
#     res = Aadhaar_info_extractor(img_path)
#     data.append([res[0][0],res[0][1],res[0][2],res[0][3],res[0][4],res[0][5]])

# # -------------- Open the file in write mode with newline=''

# FILE_PATH = 'results\Aadhaar_data_test.csv'
# with open(FILE_PATH, 'w', newline='') as file:
#     writer = csv.writer(file)
#     # Write the data rows
#     for row in data:
#         writer.writerow(row)
# print('written successfully.')

# t2 = time.time()   
# print("Time taken :",t2-t1)
