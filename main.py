from PIL import Image
from shutil import move
import os
import json


all_pixels = {}

def resize_image(image, new_width, new_height):
    width, height = image.size
    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = left + new_width
    bottom = top + new_height
    image = image.crop((left, top, right, bottom))
    image = image.resize((new_width, new_height))
    return image


def get_image_pixels(image_path):
    image = Image.open(image_path)
    new_width = 720
    new_height = 140
    image = resize_image(image, new_width, new_height)
    pixels = image.load()

    for y in range(new_height):
        for x in range(new_width):
            if not all_pixels.get(f'{x};{y}'):
                all_pixels[f'{x};{y}'] = []
                
            pixel = pixels[x, y]
            
            all_pixels[f'{x};{y}'].append(f"#{pixel[0]:02X}{pixel[1]:02X}{pixel[2]:02X}")
            # print(f"#{pixel[0]:02X}{pixel[1]:02X}{pixel[2]:02X}")
    
    with open('output.json', 'w') as f:
        json.dump(all_pixels, f)


if __name__ == "__main__":
    if os.path.isfile('output.json'):
        move('output.json', 'output-old.json')
        
    get_image_pixels("frames/0-00001.png")
    
    # for filename in os.listdir("frames"):
    #     print('=====', filename, '=====')
    #     get_image_pixels(os.path.join("frames", filename))
