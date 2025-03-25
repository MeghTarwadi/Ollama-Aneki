# Use this to recreate ascii art if you want to add or remove any of them
from pathlib import Path

from utility.textSearch import txt


class AsciiMerge:
    # It will merge two ascii arts if they have been edited or been added in custom folder
    def merge():
        asciis1_path = txt.search("asciis1_path", "saves/default/config.conf")
        arts = open(asciis1_path, "r", encoding="utf-8").read().split("\n\n\n")
        ascii2_path = txt.search("ascii2_path", "saves/default/config.conf")
        Aneki = open(ascii2_path, "r", encoding="utf-8").read()

        # Based on size which ever ascii is bigger in height it will remain first and other will
        # remain on right side if image art is bigger than text art than image will remain on left
        # side else it will be merged that way so that text remains on left and image remains on right
        def ascii_art(fulllarge, fullshort):
            outcome = ""
            short = fullshort.split("\n")
            large = fulllarge.split("\n")
            min = int(len(large) / 2 - len(short) / 2) - 1
            max = int(len(large) / 2 + len(short) / 2)
            i, j = 0, 0
            # One assumption is that that ascii art has the same length in every rows/lines.
            for lrg in large:
                if j < len(short) and len(short[j]) < 2:
                    j += 1
                outcome += lrg + "\t\t"
                if min + 1 < i and max + 1 > i and j < len(short):
                    outcome += short[j]
                    j += 1
                else:
                    for _ in range(len(short[1])):
                        outcome += " "
                i += 1
                outcome += "​"
                outcome += "\n"
            return outcome

        file = ""
        # It will split the ascii arts into art by \n\n\n\n
        for art in arts:
            if (len(Aneki.split("\n")) - len(art.split("\n"))) < 0:
                file += ascii_art(art, Aneki) + "\n\n\n"
            else:
                file += ascii_art(Aneki, art) + "\n\n\n"

        with open(
            txt.pathOs("saves/default/art.txt"), "r", encoding="utf-8"
        ) as txtfile:
            # If generated ascii art is same as default ascii art
            if file == txtfile.read():
                print("Default Ascii art detected, skipping...")
            # Else it will save it to custom
            else:
                print("Custom Ascii art detected, adding into custom...")
                Path(txt.search("custom_path", "saves/default/config.conf")).mkdir(
                    parents=True, exist_ok=True
                )
                with open(
                    txt.pathOs(
                        txt.search("custom_path", "saves/default/config.conf")
                        + "/art.txt"
                    ),
                    "w",
                    encoding="utf-8",
                ) as customtxtfile:
                    customtxtfile.write(file)
