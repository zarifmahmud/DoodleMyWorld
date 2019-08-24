"""
TODO: Add thesaurus functionality, speech functionality, grid drawing functionality
More importantly, add GUI before all this.
grid system for drawings
refresh feature
"""
from security import *
import requests
from quickdraw import QuickDrawData
from PIL import Image

import json


def thesaurize(word: str):
    """
    Returns words related to the word we have
    """
    url = "https://www.dictionaryapi.com/api/v3/references/ithesaurus/json/" + word + "?key=" + ithesaurus_key
    r = requests.get(url)
    json = r.json()
    #return json
    #return json[0]["def"][0]["sseq"][0][0][1]["rel_list"]
    return json


def image_recognizer(filepath: str):
    """
    Takes in an image and outputs objects detected by Microsoft Azure
    """

    vision_base_url = "https://eastus.api.cognitive.microsoft.com/vision/v2.0/"
    analyze_url = vision_base_url + "analyze"
    image_url = "https://previews.123rf.com/images/stockbroker/stockbroker1111/stockbroker111100001/11183288-business-meeting-in-an-office.jpg"
    headers = {'Ocp-Apim-Subscription-Key': azure_key}
    params = {'visualFeatures': 'Categories,Description,Objects'}
    data = {'url': image_url}
    response = requests.post(analyze_url, headers=headers,
                             params=params, json=data)
    response.raise_for_status()
    analysis = response.json()
    output_dict = {}
    output_dict["categories"] = analysis["categories"]
    output_dict["objects"] = analysis["objects"]
    output_dict["description"] = analysis["description"]
    print(analysis["categories"])
    print(analysis["objects"])
    print(analysis["description"])
    return output_dict


def bad_sketch(keyword: str):
    """
    Input a noun you want a sketch of, and if Google Quickdraw finds it,
    it will output a drawing
    """
    if keyword == "person":
        keyword = "smiley face"
    qd = QuickDrawData()
    keyword = keyword.lower()
    try:
        key = qd.get_drawing(keyword)
        filepath = "keyword.gif"
        key.image.save(filepath)
        return filepath
    except ValueError:
        return None


def bad_sketch_related(keyword: str):
    """
    Input a noun you want a sketch of, and if Google Quickdraw finds it,
    it will output a drawing.
    If no drawing found, will feed the word through a thesaurus and see if
    Quickdraw
    """
    pass


def dream(input_path: str, output_path:str):
    """
    The main function, put in an image, and it outputs a sketch
    """
    azure_dict = image_recognizer(output_path)
    erase_image("image.png")
    for obj in azure_dict["objects"]:
        print("ab")
        noun = obj["object"]

        xcor = obj["rectangle"]["x"]
        ycor = obj["rectangle"]["y"]
        if bad_sketch(noun) is not None:
            print("ba")
            add_to_drawing(noun, (xcor, ycor))
            if noun == "person":
                add_to_drawing("t-shirt", (xcor, ycor + 200))
        else:
            if "parent" in obj:
                parent = obj["parent"]["object"]
                if bad_sketch(parent) is not None:
                    add_to_drawing(parent, (xcor, ycor))





def speak_your_dream(output_path: str):
    """
    Speak to draw, using Azure voice recognition
    """

def add_to_drawing(word: str, xytuple):
    """
    This is what puts images into a communal drawing
    """
    # img = Image.new('RGB', (800, 1280), (255, 255, 255))
    # img.save("image.png", "PNG")
    bad_sketch(word)
    img = Image.open('keyword.gif', 'r')
    img_w, img_h = img.size
    #background = Image.new('RGBA', (2600, 2000), (255, 255, 255, 255))
    background = Image.open("image.png", "r")
    bg_w, bg_h = background.size
    #offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(img, xytuple)
    background.save('image.png', "PNG")

def erase_image(image_name):
    background = Image.new('RGBA', (2000, 2000), (255, 255, 255, 255))
    background.save(image_name, "PNG")

def shift_to_drawing(word: str, xcor, ycor):
    # img = Image.new('RGB', (800, 1280), (255, 255, 255))
    # img.save("image.png", "PNG")
    #erase_image("gridcheck.png")
    bad_sketch(word)
    img = Image.open('keyword.gif', 'r')
    img_w, img_h = img.size
    #background = Image.new('RGBA', (2200, 2000), (255, 255, 255, 255))
    background = Image.open("gridcheck.png", "r")
    bg_w, bg_h = background.size
    #offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(img, (xcor, ycor))
    background.save('gridcheck.png', "PNG")

def grid_to_pixel(x, y):
    """
    Converts grid coordinates into pixel coordinates
    """
    horiz = x * 250 + 100
    vert = y * 300 + 100
    return (horiz, vert)

def grid_draw(x, y, word):
    pixel_coor = grid_to_pixel(x, y)
    print(pixel_coor[0])
    add_to_drawing(word, pixel_coor)





if __name__ == '__main__':
    #image_recognizer("bob")
    #print(thesaurize("plant"))
    #bad_sketch("smiley face")
    #add_to_drawing("star", (0, 500))
    dream("blah", "blah")
    # num = 100
    # while num <= 2100:
    #     shift_to_drawing("tree", num, 900)
    #     num += 200

    # num = 0
    # while num < 10:
    #     grid_draw(num, 2, "skull")
    #     num += 1


"""
[{'name': 'plant_tree', 'score': 0.984375}]
[{'rectangle': {'x': 161, 'y': 88, 'w': 680, 'h': 458}, 'object': 'tree', 'confidence': 0.837, 'parent': {'object': 'plant', 'confidence': 0.876}}]
{'tags': ['grass', 'outdoor', 'water', 'field', 'green', 'cow', 'tree', 'herd', 'grassy', 'lake', 'grazing', 'body', 'large', 'bench', 'front', 'lush', 'cattle', 'riding', 'view', 'sheep', 'river', 'standing', 'mountain', 'street', 'walking', 'motorcycle', 'man', 'boat', 'sunset', 'sign', 'red', 'bird', 'hill', 'ocean', 'parked', 'flying', 'elephant', 'horse', 'blue', 'white'], 'captions': [{'text': 'a large green field with trees in the background', 'confidence': 0.9170250836752474}]}
"""


"""
Funny urls:
https://adobe99u.files.wordpress.com/2018/01/antonio-guillem-girl-winning-good-news-stock-photography.jpg?quality=100&w=1640&h=1200

https://previews.123rf.com/images/stockbroker/stockbroker1111/stockbroker111100001/11183288-business-meeting-in-an-office.jpg
"""
