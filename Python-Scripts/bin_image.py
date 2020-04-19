from PIL import Image, ImageDraw
import argparse

def make_column_from_byte(draw, x_pos, binary, y_spacing):
    x1, x2 = x_pos
    y1, y2 = 0, size_of_squares
    if len(binary) != 8:
        raise Exception('size err')
    for bit in binary:
        if bit == '1':
            draw.rectangle(((x1, y1), (x2, y2)), fill="white")
        y1 += y_spacing
        y2 += y_spacing
    draw.rectangle(((x1, y1), (x2, y2)), fill="white")
    return draw

def make_bitmap_helper(list_of_bytes, draw, size_of_squares, x_spacing, y_spacing):
    x1, x2 = (0, size_of_squares)
    make_column_from_byte(draw, (0,size_of_squares), '11111111', y_spacing)
    x1 += x_spacing
    x2 += x_spacing
    for byte in list_of_bytes:
        make_column_from_byte(draw, (x1, x2), byte, y_spacing)
        x1 += x_spacing
        x2 += x_spacing
    make_column_from_byte(draw, (x1,x2), '11111111', y_spacing)

def make_bitmap(str, size_of_squares, x_spacing, y_spacing):
    byte_list = []
    x_spacing += size_of_squares
    y_spacing += size_of_squares
    for char in str:
        byte = bin(ord(char))[2:]
        if len(byte) != 8:
            pad = 8-len(byte)
            byte = '0'*pad + byte
        byte_list.append(byte)

    img_len = ((len(byte_list)+1) * x_spacing) + size_of_squares + 1
    img_height = (size_of_squares*9) +(y_spacing-size_of_squares)*8 + 1
    img = Image.new( 'RGB', (img_len ,img_height), "black")
    draw = ImageDraw.Draw(img)

    make_bitmap_helper(byte_list, draw, size_of_squares, x_spacing, y_spacing)

    img.save('bitmap.jpg', "JPEG")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--quite', dest='quite', help='shut pwntools up', action='store_true')
    parser.add_argument('-r', '--remote', dest='remote', help='run on remote', action='store_true')
    parser.add_argument('-g', '--gdb', dest='gdb', help='attach to gdb', action='store_true')
    return parser.parse_args()

def main():
    args = parse_args()
    print(args)
    string = 'cat flag'
    size_of_squares = 1
    x_spacing = 2
    y_spacing = 2
    make_bitmap(string, size_of_squares, x_spacing, y_spacing)
