import os
import openpyxl
import shutil
from pathlib import Path


#load xlsx file with font names
xlsx_file = '/Users/tiananoll-walker/Documents/bmsis/alphabets_code/alphabet_complexity-main/data/ttfs/Graphic_Complexity_Script_Data.xlsx'
workbook = openpyxl.load_workbook(xlsx_file)

#get the active worksheet
worksheet = workbook.active

# get the column index for the font names(k=10th col)
column_index = 10
column_font = list(worksheet.columns)[column_index]
font_list = [cell.value for cell in column_font if cell.value is not None]

#repo path for fonts
repo_path = '/Users/tiananoll-walker/Documents/bmsis/alphabets_code/alphabet_complexity-main/notofonts.github.io/fonts'

#destination folder for fonts
destination_folder = '/Users/tiananoll-walker/Documents/bmsis/alphabets_code/alphabet_complexity-main/data/ttfs/'

# Iterate thru repo_path and copy fonts to destination_folder
for root, dirs, files in os.walk(repo_path):
    for filename in files:
        _, file_ext = os.path.splitext(filename)
        if file_ext.lower() not in ['.ttf', '.otf']:
            continue  # Skip if it's not a font file

        font_name = filename[:-4]
        if font_name in font_list:
            print("Matching Font List:", font_list)
            print("Complete Filename:", font_name)

            font_file = os.path.join(root, filename)
            shutil.copy(font_file, destination_folder)

print("Font copying complete.")
