from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pandas as pd
import os
import cairosvg
import io


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
    df_unicode.note.apply(lambda x: x.split()[0]).value_counts().index.tolist()
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


def make_picture(code, ttf, canvas_size=500, initial_font_size=60):
    """
    Creates a picture of a character given a Unicode code and font.

    Inputs:
        code: Hex representation of the Unicode character.
        ttf: Location of the .ttf file for the font.
        canvas_size: Size of the output canvas (default: 500).
        initial_font_size: Initial font size for drawing the symbol (default: 60).

    Returns:
        picture: 2D NumPy array representing the image.
    """
    # Create a blank canvas
    canvas = Image.new('RGB', (canvas_size, canvas_size), (255, 255, 255))

    try:
        font_size = initial_font_size
        font = ImageFont.truetype(ttf, font_size)
    except IOError:
        print(f"Error: Could not load the font file '{ttf}'.")
        return None

    # Calculate the required font size to fit the character within the canvas
    while True:
        char_width, char_height = font.getsize(code)
        if char_width <= canvas_size and char_height <= canvas_size:
            break
        font_size -= 5
        font = ImageFont.truetype(ttf, font_size)

    # Determine resizing ratio based on the largest dimension of the character image
    max_dimension = max(char_width, char_height)
    resize_ratio = canvas_size / max_dimension

    # Resize character image to fit the canvas
    resized_char_width = int(char_width * resize_ratio)
    resized_char_height = int(char_height * resize_ratio)
    resized_char = font.getmask(code).resize(
        (resized_char_width, resized_char_height))

    # Calculate the position to center the character image on the canvas
    x = (canvas_size - resized_char_width) // 2
    y = (canvas_size - resized_char_height) // 2

    # Paste the resized character onto the canvas
    canvas.paste(resized_char, (x, y))

    # Convert image to grayscale
    grayscale_canvas = canvas.convert('L')

    # Normalize pixel values between 0 and 1
    picture = np.array(grayscale_canvas) / 255.0

    return picture
