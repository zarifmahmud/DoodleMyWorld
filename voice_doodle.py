"""
Functions to recognize and process voice commands
"""

import azure.cognitiveservices.speech as speechsdk
from draw import *


def speech_recognize():
    """
    Keywords:
    - Erase, to erase the drawing
    - "Noun" on x dot y, to place a noun at that coordinate. i.e. "Tree at 3.4."
    - Noun across/down point x/y, to fill a row or column i.e. "Mountain across .5."
    """
    speech_key, service_region = security.azure_speech_key, "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Say something...")
    result = speech_recognizer.recognize_once()

    # Checks result.
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
        return result.text

    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    return ""


def keyword_finder(speech: str) -> list:
    """
    Attempts to find command phrases in the speech transcript.
    ex:
    >>> keyword_finder("Nose at 6.3.")
    >>> ["Nose", (6,3), 0]
    """
    said = speech
    if said[:-1] == "Erase":
        return ["Erase", (-1, -1), 0]

    # Get in form of number dot number
    potential = (said[-4], said[-2])
    said = said.strip()
    noun = said.split()[0]
    print(said)
    if speech[-2].isdigit():
        digit = int(speech[-2])
        print(digit + 2)
        if "row" in said or "road" in said or "across" in said:
            return [noun, (0, digit), 1]
        elif "column" in said or "down" in said:
            return [noun, (digit, 0), 2]

    if potential[0].isdigit() and potential[1].isdigit():
        coordinate = (int(potential[0]), int(potential[1]))
        output = [noun, coordinate, 0]
        print(coordinate)
        return output


def speech_to_doodle(to_draw=""):
    """
    Speak to draw, using Azure voice recognition
    You can use voice commands to erase the image,
    place an image onto a part of the grid,
     or fill a row or column with something
    """
    if to_draw == "":
        to_draw = keyword_finder(speech_recognize())

    if to_draw is not None:
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
        return to_draw
    else:
        print("Sorry! Couldn't catch that.")


def speech_correction(noun):
    """
    Corrects common misheard words. If you have any, add it to the dictionary!
    """
    misheard_dict = {"son": "sun", "shirt": "t-shirt", "smiley": "smiley face", "year": "ear",
                     "frying": "frying pan", "free": "tree", "suck": "sock", "nodes": "nose"}
    return misheard_dict[noun] if noun in misheard_dict else noun
