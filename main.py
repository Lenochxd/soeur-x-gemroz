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

def get_darkest_color(colors):
    darkest = None
    min_brightness = float('inf')
    for color in colors:
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        brightness = (r * 299 + g * 587 + b * 114) // 1000
        if brightness < min_brightness:
            min_brightness = brightness
            darkest = color
    return darkest

def get_average_color(colors):
    total_r = total_g = total_b = 0
    for color in colors:
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        total_r += r
        total_g += g
        total_b += b
    
    num_colors = len(colors)
    avg_r = total_r // num_colors
    avg_g = total_g // num_colors
    avg_b = total_b // num_colors
    
    return f"{avg_r:02X}{avg_g:02X}{avg_b:02X}"
    
def is_brightest(color):
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    brightness = (r * 299 + g * 587 + b * 114) // 1000
    return brightness < 127
    

def get_color(colors):
    average = get_average_color(colors)
    if is_brightest(average):
        return get_brightest_color(colors)
    else:
        return get_darkest_color(colors)


def get_all_colors(all_pixels):
    brightest = {}

    for pos, colors in all_pixels.items():
        if method == 1:
            brightest[pos] = get_brightest_color(colors)
        elif method == 2:
            brightest[pos] = get_color(colors)
        elif method == 3:
            brightest[pos] = get_average_color(colors)
        elif method == 4:
            brightest[pos] = get_darkest_color(colors)
            

    with open("brightest_pixels.json", "w") as f:
        json.dump(all_pixels, f)
    
    return brightest


def create_image_from_pixels(pixel_data, name):
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
        if not color.startswith('#'):
            color = '#' + color
                
        image.putpixel((x, y), ImageColor.getrgb(color))
    

    image.save(name)


def main():
    global all_pixels, method
    
    if os.path.isfile("pixels_output.json"):
        choice = input(
            "A previous data file has been found. Do you want to use it? (y/n): " # ကလဌ ୟ્ઃ᳹
        )
        
    method = int(input(
        "\nChoose your method (1/2/3):\n" \
        "1: Keep the brightest pixels\n" \
        "2: First look at the average brightness of each pixel, keep the brightest if the average is brighter, and keep the darkest if the average is darker\n" \
        "3: Keep the average color of each pixels\n" \
        "\nMethod (1/2/3): "
    ).strip())

    if os.path.isfile("pixels_output.json"):
        if choice.lower() in ['y','']:
            with open("pixels_output.json", "r") as f:
                all_pixels = json.load(f)
                brightest = get_all_colors(all_pixels)
                create_image_from_pixels(brightest, 'output.png')
            print("done :3")
            return
        else:
            move("pixels_output.json", "pixels_output-old.json")
        
        

    all_pixels = {}

    choice = input("Use twitter frames, instagram frames or both (t/i/b): ").lower()


    if choice.startswith("t"):
        for filename in os.listdir("frames-twi"):
            print("=====", filename, "=====")
            get_image_pixels(os.path.join("frames-twi", filename))

        brightest = get_all_colors(all_pixels)
        create_image_from_pixels(brightest, 'output-TWITTER.png')

    elif choice.startswith("i"):
        for filename in os.listdir("frames-insta"):
            print("=====", filename, "=====")
            get_image_pixels(os.path.join("frames-insta", filename))

        brightest = get_all_colors(all_pixels)
        create_image_from_pixels(brightest, 'output-INSTAGRAM.png')
        

    else:
        for filename in os.listdir("frames-twi"):
            print("===== t:", filename, "=====")
            get_image_pixels(os.path.join("frames-twi", filename))
        for filename in os.listdir("frames-insta"):
            print("===== i:", filename, "=====")
            get_image_pixels(os.path.join("frames-insta", filename))

        brightest = get_all_colors(all_pixels)
        create_image_from_pixels(brightest, 'output-BOTH.png')
    
    print("done :3")
        
        
if __name__ == "__main__":
    main()