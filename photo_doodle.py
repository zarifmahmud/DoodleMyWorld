"""
Functions to doodle-fy photos
"""
from draw import *
import requests
import security


def image_recognizer(image_url: str):
    """
    Takes in an image from a url and outputs objects detected by Microsoft Azure
    """

    vision_base_url = "https://eastus.api.cognitive.microsoft.com/vision/v2.0/"
    analyze_url = vision_base_url + "analyze"
    headers = {'Ocp-Apim-Subscription-Key': security.azure_key}
    params = {'visualFeatures': 'Categories,Description,Objects'}
    data = {'url': image_url}
    try:
        response = requests.post(analyze_url, headers=headers, params=params, json=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return {}
    analysis = response.json()

    output_dict = {}
    output_dict["categories"] = analysis["categories"]
    output_dict["objects"] = analysis["objects"]
    output_dict["description"] = analysis["description"]
    print(analysis["categories"])
    print(analysis["objects"])
    print(analysis["description"])
    return output_dict


def pic_to_doodle(input_path: str):
    """
    The main function, put in an image, and it outputs a sketch
    """
    if input_path != "":
        azure_dict = image_recognizer(input_path)
        if azure_dict == {}:
            return
        erase_image("image.png")
        for obj in azure_dict["objects"]:
            noun = obj["object"]

            xcor = obj["rectangle"]["x"] + 750
            ycor = obj["rectangle"]["y"] + 850
            if bad_sketch(noun) is not None:
                add_to_drawing(noun, (xcor, ycor))
                if noun == "person":
                    add_to_drawing("t-shirt", (xcor, ycor + 200))
            else:
                if "parent" in obj:
                    parent = obj["parent"]["object"]
                    if bad_sketch(parent) is not None:
                        add_to_drawing(parent, (xcor, ycor))
