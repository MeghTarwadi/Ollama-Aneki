import random
from utility.textSearch import txt


class asciiArt:
    # It will load ascii art as string wthetehr its custom or default
    def LoadArt(index, location):
        Ascii_Art = []
        location = txt.pathOs(location + "/art.txt")
        try:
            with open(location, "r", encoding="utf-8") as file:
                Ascii_Art = file.read().split("\n\n\n\n")
        except:
            with open(
                txt.pathOs("saves/default/art.txt"), "r", encoding="utf-8"
            ) as file:
                Ascii_Art = file.read().split("\n\n\n\n")

        # will return ascii art randomly
        if index < 0:
            return Ascii_Art[random.randint(0, len(Ascii_Art) - 2)]

        # will return as indexed if index is outof bound it will do % modulus
        else:
            if index < len(Ascii_Art):
                return Ascii_Art[index]
            else:
                return "Index is out of range...\n" + Ascii_Art[index % len(Ascii_Art)]
