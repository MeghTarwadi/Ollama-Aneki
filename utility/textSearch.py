import os

from rich_pixels import Pixels


class txt:
    # This will search for attribute in given path of .txt file it follows some rules eg it will avoid every white spaces and comments which can be made with //
    def pathOs(location):
        newpath = location.replace(" ","")
        newpath = location.replace(":","")
        location = os.path.join(*location.split("/"))
        return newpath

    def search(text, location):
        location = os.path.join(*location.split("/"))
        with open(location, "r", encoding="utf-8") as txt:
            try:
                testlist = txt.readlines()
                for line in testlist:
                    line = line.replace(" ", "")
                    if line.__contains__("//"):
                        line = line[: line.index("//")]
                    if text == line[: len(text)]:
                        return line.replace("\n", "").replace(text + "=", "")
                raise
            except:
                print(f"Something({text}) is missing from {location}")
                raise ValueError

    # This will give image as pixels whether they are in custome folder or in default
    def search_image(emotion, custom_path):
        try:
            return Pixels.from_image_path(
                os.path.join(*((custom_path + f"/lowres/{emotion}.png").split("/")))
            )
        except:
            return Pixels.from_image_path(
                os.path.join(*(("saves/default" + f"/lowres/{emotion}.png").split("/")))
            )
