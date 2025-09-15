import json
from pathlib import Path

import ollama
from rich.prompt import Prompt

from utility.richtables import Tables
from utility.textSearch import txt


class createModel:
    def History():
        # this 4 are colors
        normal = str(txt.search("normal", "saves/default/config.conf"))
        highlight = str(txt.search("highlight", "saves/default/config.conf"))
        alert = str(txt.search("alert", "saves/default/config.conf"))
        custom = txt.search("custom_path", "saves/default/config.conf")
        # checking whether user has created any model file yet or not
        try:
            with open(
                txt.pathOs(custom + "/model-list.txt"), "r", encoding="utf-8"
            ) as file:
                pass
        except:
            Tables.normal_table(
                f"{alert}No model is configured, skipping...\n{alert.replace('[', '[/')}"
            )
            return
        # reading model file list to get list of every model created
        text = ""
        with open(
            txt.pathOs(custom + "/model-list.txt"), "r", encoding="utf-8"
        ) as file:
            # If model file exist and it has only 1 length of data that means its \n
            # which means there is no model created yet
            modellist = file.read().split("\n")
            if len(modellist) == 1:
                text += f"{alert}You haven't configured any new model yet...{alert.replace('[', '[/')}\n"
                text += f"{alert}No model is configured, skipping...\n{alert.replace('[', '[/')}\n"
                Tables.normal_table(text)
                return
            selected = Prompt().ask(
                "Select one of the configured models:",
                default=modellist[0],
                choices=modellist,
            )
            # printing the selected model configration
            with open(
                txt.pathOs(custom + f"/models/{selected}.txt"), "r", encoding="utf-8"
            ) as configuration:
                conf = configuration.read()
                conf = conf.split("\n\n")
                text += f"\n{normal}Selected model is: {highlight}{selected}{highlight.replace('[', '[/')}\n"
                text += f"{normal}Which was based on: {normal}{highlight}{conf[0]}{highlight.replace('[', '[/')} \n".replace(
                    "FROM ", ""
                )
                text += f"{normal}Configuration of {highlight}{selected}{highlight.replace('[', '[/')} : {normal}{conf[1]}\n".replace(
                    "SYSTEM ", ""
                )
                Tables.normal_table(text)

    def NewModel():
        # colors here
        normal = str(txt.search("normal", "saves/default/config.conf"))
        highlight = str(txt.search("highlight", "saves/default/config.conf"))
        alert = str(txt.search("alert", "saves/default/config.conf"))
        asciiart = str(txt.search("asciiart", "saves/default/config.conf"))
        custom = txt.search("custom_path", "saves/default/config.conf")
        text = ""
        text += f"\n{normal}Things to Know About Creating a {normal.replace('[', '[/')}{highlight}New Model{highlight.replace('[', '[/')}:"
        text += f"\n{normal}1. Download your model from Ollama {normal.replace('[', '[/')}{highlight}(like Llama or Phi){highlight.replace('[', '[/')}."
        text += f"\n{alert}2. Creating a new model won’t erase your current one (unless the names are the same)."
        text += f"\n{normal}3. It will use not duplicate the model instead it will use the existing model. Hence memory will be saved."
        text += f"\n{alert}4. Behavior of model is adviced to keep simple\n\n"
        #   In model you sepcifie your predonwloaded model like mistral phi3.5 llama3.2 etc
        availables=[model.model for model in ollama.list().models]
        if availables:
            model = Prompt().ask("Name of the existing model ", default=availables[0] , choices=availables)
        else:
            raise
        #   Name will be the parametere that you model will be named after
        name = Prompt().ask("Name for the new model ", default="aneki").lower()

        #   System is command that you want your assistant to alway keep in mind before responcing

        system = "SYSTEM " + Prompt().ask(
            "Set behavior of model ",
            default=(
                f"from now on, you are a smart otaku with coding skills named {name.capitalize()} who speaks in English. The tone of your text allows to judge emotion you feel You are polite, soft-spoken, and your responses must be short and to the point."
            ),
        )
        info = ""
        # If user wants to add something that model should always remember than the data that user eneters will always be saved in and whever the model is called the memory will be loaeded with this data
        if (
            Prompt().ask(
                f"Do you want to add something to {name}/'s memory ",
                default="yes",
                choices=["yes", "no"],
            )
            != "no"
        ):
            info = Prompt().ask(
                f"Things to be memorized by {name}",
                default="I am an Otaku. My birthday is on 14th feb.My name is megh",
            )

        text += f"\n{normal}Creating a fresh model based on {highlight}{model}{highlight.replace('[', '[/')}{normal.replace('[', '[/')}"
        # Checks whether the modellist already exist or not.If not than it will create one
        try:
            with open(
                txt.pathOs(custom + f"/models/{name}.txt"), "w", encoding="utf-8"
            ) as file:
                pass
        except:
            Path(txt.pathOs(custom + "/models/")).mkdir(parents=True, exist_ok=True)
            with open(
                txt.pathOs(custom + "/model-list.txt"),
                "w",
                encoding="utf-8",
            ) as file:
                file.write("")
        try:
            # Creating a new model
            ollama.create(model=name, from_=model, system=system)
            # Saving memory in json file
            with open(
                txt.pathOs(custom + f"/models/{name}.txt"), "w", encoding="utf-8"
            ) as file:
                file.write("FROM " + model + "\n\n" + system + "\n\n" + "\n\n")
            with open(
                txt.pathOs(custom + f"/models/{name}.json"), "w", encoding="utf-8"
            ) as file:
                json.dump(
                    (
                        {
                            "role": "user",
                            "content": "Here are some info for you to memorized about me. "
                            + info,
                        },
                        {
                            "role": "assistant",
                            "content": "I have memorized it...",
                        },
                    ),
                    file,
                )
            # Adding model name to model list
            with open(
                txt.pathOs(custom + "/model-list.txt"), "r", encoding="utf-8"
            ) as modelslist:
                text += f"\n{normal}Checking if the model is already in the model list...{normal.replace('[', '[/')}"
                modellist = modelslist.read()
                try:
                    modellist = modellist.split("\n").index(name)
                    text += f"\n{highlight}Overwriting existing model: {name}{highlight.replace('[', '[/')}"
                except:
                    text += f"\n{normal}{name} is a different model name...{normal.replace('[', '[/')}"
                    text += f"\n{normal}{name} has been added to the model list.{normal.replace('[', '[/')}"
                    with open(
                        txt.pathOs(custom + "/model-list.txt"), "w", encoding="utf-8"
                    ) as newlist:
                        newlist.write(modellist + name + "\n")
            text += (
                f"\n{highlight}{name} has been created!{highlight.replace('[', '[/')}\n"
            )
        except Exception as error:
            text += f"\n{alert}{error}{alert.replace('[', '[/')}"
            text += f"\n{alert}Something went wrong. Please check for any typos in the model name and verify if you have downloaded the model.{alert.replace('[', '[/')}\n"

        Tables.normal_table(text)