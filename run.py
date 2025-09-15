import subprocess
import sys
import os

from rich import print as rprint
from rich.prompt import Prompt
import ollama

from tui.asciart import asciiArt
from tui.ascimerge import AsciiMerge
from tui.pngpixel import pngPix
from utility.model import createModel
from utility.richtables import Tables
from utility.runModel import RunModel
from utility.textSearch import txt


# Get data fromcustomes and colors
auto_clear = bool((int(txt.search("auto_clear", "saves/default/config.conf"))))
asciiart = txt.search("asciiart", "saves/default/config.conf")
normal = txt.search("normal", "saves/default/config.conf")
highlight = txt.search("highlight", "saves/default/config.conf")
alert = txt.search("alert", "saves/default/config.conf")
user = ""

# To clear the terminal
if auto_clear:
    subprocess.run("cls", shell=True) if os.name == "nt" else subprocess.run(["clear"])

# Loads asciiart and prints in table
Tables.center_table(
    asciiart
    + asciiArt.LoadArt(
        int(txt.search("asciiart_index", "saves/default/config.conf")),
        txt.search("custom_path", "saves/default/config.conf"),
    )
)
print("\n")
# Flag is used in case if user enters wrong argument or user exits from current utility eg runs
# aneki help, to avoid infinity loop and let user ask once again after first time.
flag = True
while user != "exit":
    # sys.argv[1] is the first argument thats been passed down by user from terminal
    try:
        if flag and sys.argv[1] in [
            "run",
            "help",
            "exit",
            "new",
            "history",
            "asciiart",
            "pixelize",
        ]:
            user = sys.argv[1]
            flag = False
        else:
            raise
    # If entered option is wrong than it will ask. If user hevent given the argument than it will ask.
    except:
        flag = False
        user = Prompt.ask(
            "",
            default="new",
            choices=["new", "history", "run", "pixelize", "asciiart", "help", "exit"],
        )

    if auto_clear:
        (
            subprocess.run("cls", shell=True)
            if os.name == "nt"
            else subprocess.run(["clear"])
        )
    if user == "run":
        history = True
        try:
            open(
                txt.pathOs(
                    txt.search("custom_path", "saves/default/config.conf")
                    + "/historylog.txt"
                ),
                "r",
                encoding="utf-8",
            ).read().split("\n")[:-1]
        # If user has not created any custom model yet than it will skip the run and ask user to create one
        except:
            history = False

        def call_fun(mode):
            runmodel = RunModel()
            if mode == "read" or mode == "cont":
                logs = (
                    open(
                        txt.pathOs(
                            txt.search("custom_path", "saves/default/config.conf")
                            + "/historylog.txt"
                        ),
                        "r",
                        encoding="utf-8",
                    )
                    .read()
                    .split("\n")[:-1]
                )
                choices = []
                print("\n")
                for c in range(len(logs)):
                    rprint(f"{highlight} {c + 1}. {normal} {logs[c]}")
                    choices.append(str(c + 1))
                print("\n")
                index = Prompt.ask(
                    "Title of past coversation : ",
                    default=choices[0],
                    choices=choices,
                )
                if mode == "read":
                    runmodel.read(logs[int(index) - 1])
                else:
                    runmodel.ConinueFromWhereItLeft(logs[int(index) - 1])
            else:
                runmodel.new_run(mode)

        try:
            # This will provide all available models which are created by user
            available_option = (
                open(
                    txt.pathOs(
                        txt.search("custom_path", "saves/default/config.conf")
                        + "/model-list.txt"
                    ),
                    "r",
                    encoding="utf-8",
                )
                .read()
                .split("\n")[:-1]
            )
            # To add read and cont only if model have been created by user
            if history:
                available_option.append("read")
                available_option.append("cont")
            # It checks whether second argument is in available_option which consist models and appended option read and cont
            if sys.argv[2] in available_option:
                mode = sys.argv[2]
                call_fun(mode)
                sys.argv[2] = ""
            else:
                raise
        except:
            try:
                available_option = (
                    open(
                        txt.pathOs(
                            txt.search("custom_path", "saves/default/config.conf")
                            + "/model-list.txt"
                        ),
                        "r",
                        encoding="utf-8",
                    )
                    .read()
                    .split("\n")[:-1]
                )
                if history:
                    available_option.append("read")
                    available_option.append("cont")
                # Did the same process as above to get available opt.

                available_option.extend([model.model for model in ollama.list().models])
                mode = Prompt.ask(
                    "Model Name: ",
                    default=(
                        open(
                            txt.pathOs(
                                txt.search("custom_path", "saves/default/config.conf")
                                + "/model-list.txt"
                            ),
                            "r",
                            encoding="utf-8",
                        )
                        .read()
                        .split("\n")[:-1]
                    )[0],
                    choices=available_option,
                )
                # With the mode it will call the function
                call_fun(mode)
            except Exception as e:
                rprint(f"{alert}{e}")
                rprint(
                    f"{alert}No custome model found! Please create custome model using{alert.replace('[', '[/')} {highlight}'new'{highlight.replace('[', '[/')} {alert} command first!{alert.replace('[', '[/')}"
                )

    elif user == "help":
        text = []
        rprint(
            f"{normal}Welcome to the help section! Here’s a brief overview of the commands available:{normal.replace('[', '[/')} "
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
            [
                f"{highlight}asciiart{highlight.replace('[', '[/')}",
                "Merge two ASCII arts.",
                "To saperate two ascii use enters three times.",
                f"{alert}Only ascii1.txt allows multiple art!{alert.replace('[', '[/')}",
            ],
        ]
        Tables.multi_table(text)
        rprint(f"{normal}Feel free to ask for help anytime!{normal.replace('[', '[/')}")
    # If user has created custome Ascii art then it will need to be merged eg there are twos
    # ascii arts one resembles text and other resembles image than if user likes to merge
    # them to make sinle and use it as banner whenever they want to use Ollama-Aneki
    elif user == "asciiart":
        AsciiMerge.merge()
    elif user == "exit":
        print("Exiting...")
    elif user == "new":
        createModel.NewModel()
    elif user == "history":
        createModel.History()
    # If user had added new images than user need to resize them to make them smaller for
    # showing them in pixels, the hight and width will be decided based on what user has given
    # in config file
    elif user == "pixelize":
        cls = pngPix(
            pngfolder=str(txt.search("pngfolder", "saves/default/config.conf")).lower(),
            height=int(txt.search("height", "saves/default/config.conf")),
            width=int(txt.search("width", "saves/default/config.conf")),
            normal=str(txt.search("normal", "saves/default/config.conf")),
            highlight=str(txt.search("highlight", "saves/default/config.conf")),
            alert=str(txt.search("alert", "saves/default/config.conf")),
            paths=str(txt.search("custom_path", "saves/default/config.conf")),
        )
        cls.lower_resolution()
    else:
        pass
    print("\n")
