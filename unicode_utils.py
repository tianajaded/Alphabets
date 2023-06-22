from PIL import Image, ImageFont, ImageOps
from PIL import Image
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import pandas as pd
import cv2


def create_df_unicode():
    
    """
    Parses unicode names list into pandas dataframe
    Data downloaded from https://www.unicode.org/Public/UCD/latest/ucd/
    """
    file_path = '/Users/tiananoll-walker/Documents/bmsis/alphabets_code/alphabet_complexity-main/data/unicode_names_list.txt'

    print("Resolved file path:", file_path)

    with open(file_path, 'r') as f:
        unicode = f.read()

    unicode = unicode.split('\n')
    df_unicode = pd.DataFrame([u.split('\t')
                               for u in unicode if len(u) > 0 and u[0] not in '\t;@'],
                              columns=['code', 'note'])

    df_unicode = df_unicode[df_unicode.note.apply(
        lambda x: x[0] != '<')].reset_index(drop=True)
    
    # Define the u function to convert Unicode code to character
    def u(code):
        try:
            return chr(int(code, 16))
        except:
            return code
    
    # Apply the u function to populate the 'rep' column
    df_unicode['rep'] = df_unicode.code.apply(u)

    return df_unicode



def code_type(code):
    """
    Determines code type of unicode code.
    """
    u = '0x'+code
    for a, b, c in [('0x1F600', '0x1F64F', 'Emoticons'),
                    ('0x1F300', '0x1F5FF', 'Misc Symbols and Pictographs'),
                    ('0x1F680', '0x1F6FF', 'Transport and Map'),
                    ('0x2600', '0x26FF', 'Misc symbols'),
                    ('0x2700', '0x27BF', 'Dingbats'),
                    ('0xFE00', '0xFE0F', 'Variation Selectors'),
                    ('0x1F900', '0x1F9FF', 'Supplemental Symbols and Pictographs'),
                    ('0x1F1E6', '0x1F1FF', 'Flags')]:
        if a <= u <= b:
            return c
    return 'Writing Symbol'


def u(i):
    try:
        return chr(int(i, 16))
    except:
        return i


def get_language(note):
    """
    Extracts language from unicode note.
    Assumes first word of note is the language.
    """
    return note.split()[0]


def preprocess_code(code):
    if code is None:
        return ""  # or any default value you prefer
    elif isinstance(code, str):
        # Remove any leading/trailing whitespace and convert to uppercase
        code = code.strip().upper()
        if code.startswith("U+"):
            # Remove the "U+" prefix if present
            code = code[2:]
        return code
    else:
        return str(code).strip()


def make_picture(code, ttf, font_size):
    # Create a blank canvas
    canvas_size = 500
    canvas = np.ones((canvas_size, canvas_size), dtype=np.uint8) * 255

    try:
        font = ImageFont.truetype(ttf, font_size)
    except IOError:
        print(f"Error: Could not load the font file '{ttf}'.")
        return None

    # Render character onto the canvas
    character_image = Image.new('L', (canvas_size, canvas_size), 255)
    draw = ImageDraw.Draw(character_image)
    draw.text((0, 0), code, font=font, fill=0)

    # Resize character image to fit the canvas using OpenCV
    resized_char = cv2.resize(np.array(
        character_image), (canvas_size - 20, canvas_size - 20), interpolation=cv2.INTER_LANCZOS4)

    # Calculate the position to center the character image on the canvas
    x = (canvas_size - resized_char.shape[1]) // 2
    y = (canvas_size - resized_char.shape[0]) // 2

    # Paste the resized character onto the canvas
    canvas[y:y + resized_char.shape[0], x:x +
           resized_char.shape[1]] = resized_char

    # Normalize pixel values between 0 and 1
    picture = canvas / 255.0

    return picture
