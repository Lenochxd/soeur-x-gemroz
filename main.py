from PIL import Image, ImageColor
from shutil import move
import os
import json


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
    global all_pixels
    
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
    
    with open('pixels_output.json', 'w') as f:
        json.dump(all_pixels, f)

def get_brightest_color(colors):
    brightest = None
    max_brightness = 0
    for color in colors:
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        brightness = (r * 299 + g * 587 + b * 114) // 1000
        if brightness > max_brightness:
            max_brightness = brightness
            brightest = color
    return brightest


def get_all_colors(all_pixels):
    brightest = {}

    for pos, colors in all_pixels.items():
        brightest[pos] = get_brightest_color(colors)

    with open("brightest_pixels.json", "w") as f:
        json.dump(all_pixels, f)
    
    return brightest


def create_image_from_pixels(pixel_data):
    max_x = max_y = 0
    for key in pixel_data.keys():
        x, y = map(int, key.split(';'))
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
    
    image = Image.new("RGB", (max_x + 1, max_y + 1))
    
    for key, color in pixel_data.items():
        x, y = map(int, key.split(';'))
        image.putpixel((x, y), ImageColor.getrgb(color))
    

    image.save("output.png")


def main():
    global all_pixels
    
    if os.path.isfile("pixels_output.json"):
        choice = input(
            "A previous data file has been found. Do you want to use it? (y/n): " # ကလဌ ୟ્ઃ᳹
        )
        if choice.lower() in ['y','']:
            with open("pixels_output.json", "r") as f:
                all_pixels = json.load(f)
                brightest = get_all_colors(all_pixels)
                create_image_from_pixels(brightest)
            print("done :3")
            return
        else:
            move("pixels_output.json", "pixels_output-old.json")
        
        

    all_pixels = {}

    for filename in os.listdir("frames"):
        print('=====', filename, '=====')
        get_image_pixels(os.path.join("frames", filename))
    
    brightest = get_all_colors(all_pixels)
    create_image_from_pixels(brightest)
    print("done :3")
        
        
if __name__ == "__main__":
    main()