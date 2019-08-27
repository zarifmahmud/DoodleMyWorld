"""
TODO: Add drawn on grid, undo feature, spot erase feature.
Program that
"""

from quickdraw import QuickDrawData
from PIL import Image


def bad_sketch(keyword: str) -> str:
    """
    Input a noun you want a sketch of, and if Google Quickdraw finds it,
    it will save a random doodle of it to keyword.gif, and return the filepath.
    """
    qd = QuickDrawData()
    if keyword is not None:
        keyword = keyword.lower()
        if keyword == "person":
            keyword = "smiley face"
    try:
        key = qd.get_drawing(keyword)
        filepath = "keyword.gif"
        key.image.save(filepath)
        return filepath
    except ValueError:
        return "blank.png"


def add_to_drawing(word: str, xytuple: tuple):
    """
    This is what puts images into the communal drawing at image.png. The doodle you want is
    given by word, and its location given by a tuple of pixel coordinates (not grid coordinates).
    Ex:
    >>> add_to_drawing("star", (1350, 700))
    This will add a doodle of a star to coordinates (1350, 700).
    """
    filepath = bad_sketch(word)
    img = Image.open(filepath, 'r')
    # background = Image.new('RGBA', (2600, 2000), (255, 255, 255, 255))
    background = Image.open("image.png", "r")
    background.paste(img, xytuple)
    background.save('image.png', "PNG")


def erase_image(image_name: str):
    """
    Replaces image with a blank image.
    """
    background = Image.new('RGBA', (2000, 2000), (255, 255, 255, 255))
    background.save(image_name, "PNG")


def grid_to_pixel(x: int, y: int) -> tuple:
    """
    Converts grid coordinates into pixel coordinates. Each grid square is 250 x 300 pixels large,
    and there's 100 pixels of buffer room around the edges of the picture.
    Ex:
    >>> grid_to_pixel(5, 2)
    >>> (1350, 700)
    """
    horiz = x * 250 + 100
    vert = y * 300 + 100
    return (horiz, vert)


def grid_draw(x: int, y: int, word: str):
    """
    Takes in grid coordinates, and plots onto image
    >>> grid_draw(5, 2, "star")
    This will draw a star at the box at grid coordinates (5, 2).
    """
    pixel_coor = grid_to_pixel(x, y)
    print(pixel_coor[0])
    add_to_drawing(word, pixel_coor)


def grid_fill(row: bool, coordinate: int, word: str):
    """
    Fill a row or column with the given word.

    >>> grid_fill(True, 3, "mountain")
    This will fill row 3 with drawings of mountains.
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

    # image_recognizer("bob")
    # print(thesaurize("plant"))
    # bad_sketch("smiley face")
    # add_to_drawing("star", (0, 500))
    # dream("blah", "blah")
    # num = 100
    # while num <= 2100:
    #     shift_to_drawing("tree", num, 900)
    #     num += 200

    # num = 0
    # while num < 10:
    #     grid_draw(num, 2, "skull")
    #     num += 1
    # grid_fill(False, 4, "mountain")
    # speech_to_doodle("blach")
    # img = Image.new('RGB', (50, 50), (255, 255, 255))
    # img.save("blank.png", "PNG")
    # pic_to_doodle("gogo")
    pass

"""
[{'name': 'plant_tree', 'score': 0.984375}]
[{'rectangle': {'x': 161, 'y': 88, 'w': 680, 'h': 458}, 'object': 'tree', 'confidence': 0.837, 
'parent': {'object': 'plant', 'confidence': 0.876}}]
{'tags': ['grass', 'outdoor', 'water', 'field', 'green', 'cow', 'tree', 'herd', 'grassy', 'lake', 'grazing', 
'body', 'large', 'bench', 'front', 'lush', 'cattle', 'riding', 'view', 'sheep', 'river', 'standing', 
'mountain', 'street', 'walking', 'motorcycle', 'man', 'boat', 'sunset', 'sign', 'red', 'bird', 
'hill', 'ocean', 'parked', 'flying', 'elephant', 'horse', 'blue', 'white'], 'captions': 
[{'text': 'a large green field with trees in the background', 'confidence': 0.9170250836752474}]}
"""


"""
Funny urls:
https://adobe99u.files.wordpress.com/2018/01/antonio-guillem-girl-winning-good-news-stock-photography.jpg?quality=100&w=1640&h=1200

https://previews.123rf.com/images/stockbroker/stockbroker1111/stockbroker111100001/11183288-business-meeting-in-an-office.jpg
"""
