import os
import openpyxl
import shutil

# load in the xlxs file with the font names
xlsx_file = '/Users/tiananoll-walker/Documents/bmsis/alphabets_code/alphabet_complexity-main/data/ttfs/Graphic_Complexity_Script_Data.xlsx'
workbook = openpyxl.load_workbook(xlsx_file)

# select the active worksheet
worksheet = workbook.active

# get the values from column k(which is column 10)
column_index = 10
column_font = list(worksheet.columns)[column_index]
font_list = [cell.value for cell in column_font if cell.value is not None]

# copy the fonts from the repo to the data folder
repo_path = '/Users/tiananoll-walker/Documents/bmsis/alphabets_code/alphabet_complexity-main/notofonts.github.io'

# destination folder
destination_folder = '/Users/tiananoll-walker/Documents/bmsis/alphabets_code/alphabet_complexity-main/data/ttfs/'

# iterate thru the repo directory and copy the fonts to the destination folder
for filename in os.listdir(repo_path):
    if filename.endswith(('.ttf', '.otf')) and filename[:-4] in font_list:
        font_file = os.path.join(repo_path, filename)
        shutil.copy(font_file, destination_folder)
