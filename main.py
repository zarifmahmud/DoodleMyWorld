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
import azure.cognitiveservices.speech as speechsdk
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QApplication
from PyQt5.QtGui import QPixmap
import sys


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Title'
        self.left = 10
        self.top = 10
        self.width = 60
        self.height = 80
        self.text = "https://ichef.bbci.co.uk/news/660/cpsprodpb/E9DF/production/_96317895_gettyimages-164067218.jpg"
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create widget
        self.label = QLabel(self)
        pixmap = QPixmap('image.png')
        self.label.setPixmap(pixmap)
        self.label.resize(1500, 1000)
        self.resize(pixmap.width(), pixmap.height())
        button = QPushButton('Voice Command', self)
        button.setToolTip('This is an example button')
        button.move(1600, 800)
        button.clicked.connect(self.on_click)
        self.textbox = QLineEdit(self)
        self.textbox.move(1600, 300)
        self.textbox.resize(280, 40)

        # Create a button in the window
        button2 = QPushButton('Upload image from link', self)
        button2.move(1600, 350)
        button2.clicked.connect(self.on_click2)

        button3 = QPushButton('Refresh Image!', self)
        button3.move(1600, 400)
        button3.clicked.connect(self.refresh)

        self.label.setScaledContents(True)
        self.show()

    def on_click(self):
        speech_to_doodle("blah")
        pixmap = QPixmap('image.png')
        self.label.setPixmap(pixmap)

    def on_click2(self):
        textboxValue = self.textbox.text()
        self.text = textboxValue
        self.textbox.setText("")
        pic_to_doodle(textboxValue)
        pixmap = QPixmap('image.png')
        self.label.setPixmap(pixmap)

    def refresh(self):
        pic_to_doodle(self.text)
        pixmap = QPixmap('image.png')
        self.label.setPixmap(pixmap)



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
    image_url = filepath
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

def speech_recognize():
    """
    Keywords:
    - Erase, to erase the drawing
    - "Noun" on x dot y, to place a noun at that coordinate
    - Noun across/down point x/y, to fill a row or column
    """
    speech_key, service_region = azure_speech_key, "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Say something...")
    result = speech_recognizer.recognize_once()

    # Checks result.
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
        said = result.text
        if said[:-1] == "Erase":
            return ["Erase", (-1, -1), 0]

        # Get in form of number dot number
        potential = (said[-4], said[-2])
        said = said.strip()
        noun = said.split()[0]
        print(said)
        print(result.text[-2])
        if result.text[-2].isdigit():
            digit = int(result.text[-2])
            print(digit + 2)
            if "row" in said or "road" in said or "across" in said:
                return [noun, (0, digit), 1]
            elif "column" in said or "down" in said:
                return [noun, (digit, 0), 2]

        if potential[0].isdigit() and potential[1].isdigit():
            coordinate = (int(potential[0]), int(potential[1]))
            output = [noun, coordinate, 0]
            print(coordinate)
            # Check if filling row or column
            # if "row" in said or "road" in said or "across" in said:
            #     output[1] = result.text[:-2]
            #     output[2] = 1
            # elif "column" in said or "down" in said:
            #     output[1] = result.text[:-2]
            #     output[2] = 2
            return output
        else:
            return None
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))


def bad_sketch(keyword: str):
    """
    Input a noun you want a sketch of, and if Google Quickdraw finds it,
    it will output a drawing
    """
    if keyword == "person":
        keyword = "smiley face"
    qd = QuickDrawData()
    if keyword is not None:
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


def pic_to_doodle(input_path: str):
    """
    The main function, put in an image, and it outputs a sketch
    """
    azure_dict = image_recognizer(input_path)
    erase_image("image.png")
    for obj in azure_dict["objects"]:
        print("ab")
        noun = obj["object"]

        xcor = obj["rectangle"]["x"] + 750
        ycor = obj["rectangle"]["y"] + 850
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

def speech_to_info(speech):
    """
    Parses speech for keywords to convert
    """
    pass

def speech_to_doodle(event):
    """
    Speak to draw, using Azure voice recognition
    You can use voice commands to erase the image,
    place an image onto a part of the grid,
     or fill a row or column with something
    """
    to_draw = speech_recognize()
    if to_draw is not None:
        #print("bro")
        noun = to_draw[0].lower()
        noun = speech_correction(noun)
        xcor = to_draw[1][0]
        ycor = to_draw[1][1]
        fill = to_draw[2]
        if noun == "erase":
            erase_image("image.png")
        elif fill == 1:
            grid_fill(True, ycor, noun)
        elif fill == 2:
            grid_fill(False, xcor, noun)
        else:
            grid_draw(xcor, ycor, noun)

    else:
        print("Sorry! Couldn't catch that.")


def speech_correction(noun):
    """
    Corrects common misheard words
    """
    if noun == "son":
        return "sun"
    elif noun == "shirt":
        return "t-shirt"
    elif noun == "smiley":
        return "smiley face"
    elif noun == "year":
        return "ear"
    elif noun == "frying":
        return "frying pan"
    else:
        return noun

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

# def shift_to_drawing(word: str, xcor, ycor):
#     # img = Image.new('RGB', (800, 1280), (255, 255, 255))
#     # img.save("image.png", "PNG")
#     #erase_image("gridcheck.png")
#     bad_sketch(word)
#     img = Image.open('keyword.gif', 'r')
#     img_w, img_h = img.size
#     #background = Image.new('RGBA', (2200, 2000), (255, 255, 255, 255))
#     background = Image.open("gridcheck.png", "r")
#     bg_w, bg_h = background.size
#     #offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
#     background.paste(img, (xcor, ycor))
#     background.save('gridcheck.png', "PNG")


def grid_to_pixel(x, y):
    """
    Converts grid coordinates into pixel coordinates
    """
    horiz = x * 250 + 100
    vert = y * 300 + 100
    return (horiz, vert)


def grid_draw(x, y, word):
    """
    Takes in Cartesian coordinates, and plots onto image
    """
    pixel_coor = grid_to_pixel(x, y)
    print(pixel_coor[0])
    add_to_drawing(word, pixel_coor)


def grid_fill(row: bool, coordinate, word: str):
    """
    Fill a row or column with the given word
    """

    if row:
        num = 0
        while num <= 10:
            pixel_coor = grid_to_pixel(num, coordinate)
            add_to_drawing(word, pixel_coor)
            num += 1
    else:
        num = 8
        while num > 0:
            pixel_coor = grid_to_pixel(coordinate, num)
            add_to_drawing(word, pixel_coor)
            num -= 1

if __name__ == '__main__':
    #image_recognizer("bob")
    #print(thesaurize("plant"))
    #bad_sketch("smiley face")
    #add_to_drawing("star", (0, 500))
    #dream("blah", "blah")
    # num = 100
    # while num <= 2100:
    #     shift_to_drawing("tree", num, 900)
    #     num += 200

    # num = 0
    # while num < 10:
    #     grid_draw(num, 2, "skull")
    #     num += 1
    #grid_fill(False, 4, "mountain")
    #speak_your_dream("blach")
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

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
