## Doodle My World
This is the project I made for Hack the 6ix, that won "Most Fun Hack"! You can check out the writeup for it here: https://devpost.com/software/doodle-my-world.

## For Personal Use
If you want to use this on your own computer, the only extra thing you will need to do is to make a file called "security.py", and add your personal keys to Azure's speech and vision resources.

## Guide to Voice Commands
Imagine that the image is split into an 8x6 grid (each of these 48 squares is 250 x 300 pixels large).
You can specify a particular square for a doodle to go, or fill an entire row or column with a particular doodle.

The only thing that's a little tricky is that I used computer graphics convention so that the origin, coordinate (0, 0),
is on the top left of the screen rather than the bottom left. This means that while x-coordinates increase from left
to right as you're probably used to, y-coordinates increase from top to bottom. So the top row is row 0, the
one under it is row 1, etc.

    Key phrases:
    - Erase, to erase the drawing
    - NOUN on X dot Y, to place a noun at that coordinate. i.e. "Crocodile at 3.4."
    - NOUN across/down point X/Y, to fill a row or column i.e. "Skyscraper across .5."

    (You can use dot or point interchangeably. You actually often don't need either, but it helps
    Azure detect that you're saying a number like 1, rather than a homonym like "won".)
