"""
TODO: Add thesaurus functionality, speech functionality, grid drawing functionality
More importantly, add GUI before all this.
grid system for drawings

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
    url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/" + word + "?key=" + thesaurus_key
    r = requests.get(url)
    json = r.json()
    #return json
    return json[0]["def"][0]["sseq"][0][0][1]["rel_list"]


def image_recognizer(filepath: str):
    """
    Takes in an image and outputs objects detected by Microsoft Azure
    """

    vision_base_url = "https://eastus.api.cognitive.microsoft.com/vision/v2.0/"
    analyze_url = vision_base_url + "analyze"
    image_url = "https://arbordayblog.org/wp-content/uploads/2018/06/oak-tree-sunset-iStock-477164218-1080x608.jpg"
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
    qd = QuickDrawData()
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
    object_list = []
    for obj in azure_dict["objects"]:
        if bad_sketch(obj["object"]) is not None:
            img = Image.open('keyword.gif', 'r')




def speak_your_dream(output_path: str):
    """
    Speak to draw, using Azure voice recognition
    """

def add_to_drawing(word: str, xcor, ycor):
    # img = Image.new('RGB', (800, 1280), (255, 255, 255))
    # img.save("image.png", "PNG")
    bad_sketch(word)
    img = Image.open('keyword.gif', 'r')
    img_w, img_h = img.size
    background = Image.new('RGBA', (2000, 2000), (255, 255, 255, 255))
    # background = Image.open("image.png", "r")
    bg_w, bg_h = background.size
    #offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(img, (xcor, ycor))
    background.save('image.png', "PNG")


if __name__ == '__main__':
    # image_recognizer("bob")
    # print(thesaurize("building"))
    # bad_sketch("car")
    add_to_drawing("star", 0, 500)
