"""
Functions to recognize and process voice commands
"""

import security
import azure.cognitiveservices.speech as speechsdk
from draw import grid_fill, grid_draw, erase_image


def speech_recognize() -> str:
    """
    Using Microsoft Azure to convert your speech into text. It will process after you finish speaking.
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
    Speak to draw, using Azure voice recognition You can use voice commands to erase the image,
    place an image onto a part of the grid, or fill a row or column with something.

    Keywords:
    - Erase, to erase the drawing
    - NOUN on X dot Y, to place a noun at that coordinate. i.e. "Crocodile at 3.4."
    - NOUN across/down point X/Y, to fill a row or column i.e. "Skyscraper across .5."

    (You can use dot or point interchangeably. You actually often don't need either, but it helps
    Azure detect that you're saying a number like 1, rather than a homonym like "won".)
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


def speech_correction(noun: str) -> str:
    """
    Corrects common misheard words, and creates shortcut phrases. If you have any, add it to the dictionary!
    """
    misheard_dict = {"son": "sun", "shirt": "t-shirt", "smiley": "smiley face", "year": "ear",
                     "frying": "frying pan", "free": "tree", "suck": "sock", "nodes": "nose"}
    return misheard_dict[noun] if noun in misheard_dict else noun
