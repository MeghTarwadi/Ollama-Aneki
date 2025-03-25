from pathlib import Path


from PIL import Image
from utility.textSearch import txt

from utility.richtables import Tables


class pngPix:
    def __init__(self, height, width, highlight, alert, normal, paths, pngfolder):
        self.height = height
        self.width = width
        self.highlight = highlight
        self.alert = alert
        self.normal = normal
        self.dLowResPath = txt.pathOs("saves/default/lowres/")
        self.dHighResPath = txt.pathOs("saves/default/exp/" + pngfolder + "/")
        self.cLowResPath = txt.pathOs(paths + "/lowres/")
        self.cHighResPath = txt.pathOs(paths + "/exp/")
        self.emotions = [
            "afraid",
            "anger",
            "angry",
            "annoyed",
            "anticipating",
            "anxious",
            "apprehensive",
            "ashamed",
            "caring",
            "confident",
            "content",
            "devastated",
            "disappointed",
            "disgusted",
            "embarrassed",
            "excited",
            "faithful",
            "fear",
            "furious",
            "grateful",
            "guilty",
            "hopeful",
            "impressed",
            "jealous",
            "joy",
            "joyful",
            "lonely",
            "love",
            "nostalgic",
            "prepared",
            "proud",
            "sad",
            "sadness",
            "sentimental",
            "surprise",
            "surprised",
            "terrified",
            "trusting",
        ]

    def lower_resolution(self):

        # created libraries for default and custom

        Path(self.cLowResPath).mkdir(parents=True, exist_ok=True)
        Path(self.dLowResPath).mkdir(parents=True, exist_ok=True)
        Path(self.cHighResPath).mkdir(parents=True, exist_ok=True)
        text = "\n"

        try:
            text += f"{self.normal}Searching for custom images...\n"
            # Chceking wherether every emotion exist or not
            # If it does not exist, the program will move to default
            for emotion in self.emotions:
                image = Image.open(self.cHighResPath + emotion + ".png")
            text += f"{self.alert}Custom images found...  \n"
            text += f"{self.highlight}Converting custom images in {self.height}x{self.width}... \n"
            for emotion in self.emotions:
                # open image in high res
                image = Image.open(self.cHighResPath + emotion + ".png")
                # connvert it to low res
                new_image = image.resize((self.height, self.width))

                # save it
                new_image.save(f"{self.cLowResPath}{emotion}.png")
        # If custome has missing image eg if image consist 37 out of 38 emotions with correct
        # name in custome but 1 is misplelled or not found, the program will move to default
        except:
            text += f"{self.alert}NO custom images found...\n"
            text += f"{self.highlight}Converting default images in {self.height}x{self.width}...\n"
            for emotion in self.emotions:
                # open image in high res
                image = Image.open(self.dHighResPath + emotion + ".png")
                # connvert it to low res
                new_image = image.resize((self.height, self.width))

                # save it
                new_image.save(f"{self.dLowResPath}{emotion}.png")

        Tables.normal_table(text)
