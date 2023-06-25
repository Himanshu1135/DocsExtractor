import os
import re
import csv
import time
import glob
from utilis import dob,pan_No,pan_names_person
from utilis import pytess_text,pan_names_father

# Only for generation of csv for many pan docs together and testing pan function


def pan_info_extractor(img_path):
    '''
    nput : image path
    working : Extract information from image using ocr and regex
    return : List of information
    '''
    res = []
    #-------- for filename extraction 
    filename_with_extension = os.path.basename(img_path)
    filename = os.path.splitext(filename_with_extension)[0]

    text = pytess_text(img_path)
#------------- cleaning text using regular expressions
    text = text.strip().replace('\n', ' ').replace('  ', ' ')
    text = re.sub(r'[^A-Za-z0-9/\s]', '', text)
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

    res.append([filename,Name,Date,pan_no,f_Name,text])
    return res

#--------------------------------------------------- CSV -------------------------------------------------------------------------------#

# IMAGE_FOLDER_PATH = r'D:\Stractmine\image\testing\A'  # Replace with your folder path
# image_extensions = ['*.jpg', '*.jpeg', '*.png']  # Add more extensions if needed

# image_files = []
# for ext in image_extensions:
#     image_files.extend(glob.glob(IMAGE_FOLDER_PATH + '/' + ext))

# # --------- extracting info for each img and adding to data array

# data = []
# data.append(['FileName','Name','DOB','Pan_No','father_Name','Text'])
# t1 = time.time()
# for img_path in image_files:
#     res = pan_info_extractor(img_path)
#     data.append([res[0][0],res[0][1],res[0][2],res[0][3],res[0][4],res[0][5]])

# # ------------Open the file in write mode with newline=''
# file = 'results\Pan_data_new7.csv'
# with open(file, 'w', newline='') as file:
#     writer = csv.writer(file)
#     # Write the data rows
#     for row in data:
#         writer.writerow(row)

# print(' written successfully.')
# t2 = time.time()   
# print("Time taken :",t2-t1)

