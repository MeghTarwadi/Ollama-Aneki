from rich import print as rprint
from rich.prompt import Prompt
from rich.table import Table

from model import createModel
from tui.asciart import asciiArt
from tui.pngpixel import pngPix
from utility.richtables import Tables
from utility.textSearch import txt

asciiart = txt.search("asciiart", "saves/default/config.txt")
normal = txt.search("normal", "saves/default/config.txt")
highlight = txt.search("highlight", "saves/default/config.txt")
alert = txt.search("alert", "saves/default/config.txt")
user = ""


Tables.center_table(
    asciiart
    + asciiArt.LoadArt(
        int(txt.search("asciiart_index", "saves/default/config.txt")),
        txt.search("custom_path", "saves/default/config.txt"),
    )
)

while user != "exit":
    user = Prompt.ask(
        "",
        default="pixelize",
        choices=["run", "help", "exit", "new", "history", "pixelize"],
    )
    if user == "run":
        print("Running...")
    elif user == "help":
        text = []
        rprint(
            f"{normal}\nWelcome to the help section! Here’s a brief overview of the commands available:{normal.replace('[', '[/')} "
        )
        text = [
            [
                f"{highlight}run{highlight.replace('[', '[/')}",
                "Launch a model by name.",
                "If it exists, it will run.",
                f"{alert}Make sure the model is available!{alert.replace('[', '[/')}",
            ],
            [
                f"{highlight}exit{highlight.replace('[', '[/')}",
                "Exit the setup program.",
                "All progress is saved automatically.",
                f"{alert}You can return later to continue!{alert.replace('[', '[/')}",
            ],
            [
                f"{highlight}new{highlight.replace('[', '[/')}",
                "Create a new custom model.",
                "Base it on an existing model.",
                f"{alert}Choose a unique name for it!{alert.replace('[', '[/')}",
            ],
            [
                f"{highlight}history{highlight.replace('[', '[/')}",
                "View past model configurations.",
                "Even deleted ones can be restored.",
                f"{alert}Recreate them if needed!{alert.replace('[', '[/')}",
            ],
            [
                f"{highlight}pixelize{highlight.replace('[', '[/')}",
                "Change emotional model files.",
                "Replace files with the same name.",
                f"{alert}Improper changes may cause issues!{alert.replace('[', '[/')}",
            ],
        ]
        Tables.multi_table(text)
        rprint(
            f"{normal}Feel free to ask for help anytime!{normal.replace('[', '[/')}"
        )

    elif user == "exit":
        print("Exiting...")
    elif user == "new":
        createModel.NewModel()
    elif user == "history":
        createModel.History()

    elif user == "pixelize":
        cls = pngPix(
            height=int(txt.search("height", "saves/default/config.txt")),
            width=int(txt.search("width", "saves/default/config.txt")),
            normal=str(txt.search("normal", "saves/default/config.txt")),
            highlight=str(txt.search("highlight", "saves/default/config.txt")),
            alert=str(txt.search("alert", "saves/default/config.txt")),
            paths=str(txt.search("custom_path", "saves/default/config.txt")),
        )
        cls.lower_resolution()
    else:
        pass
    print("\n")
