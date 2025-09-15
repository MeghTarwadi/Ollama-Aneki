import datetime
import json
import os

import subprocess
from pathlib import Path

import ollama
from llmware.models import ModelCatalog
from prompt_toolkit import prompt as input
from rich import print as rprint
from rich.live import Live
from rich.prompt import Prompt
from rich.table import Table


from utility.richtables import Tables
from utility.textSearch import txt
from utility.search import Search

class RunModel:

    # Its used to read the past conversation
    def read(self, logs):
        # Loading previous conversations titles
        cpath = txt.search("custom_path", "saves/default/config.conf")
        with open(
            txt.pathOs(cpath + "/history/" + logs + ".json"),
            "r",
            encoding="utf-8",
        ) as history:
            history = json.load(history)[2:]
            user_conversation = txt.search(
                "user_conversation", "saves/default/config.conf"
            )
            current = 0
            # There is a big reason to use try and except here it is because if user has previously enebled the emotion
            # generation than desabled it and currently its active so its like first 5 conversation has emotions now again
            # 5 doesnt has emotions but remaining 5 which were added lastly by aneki run cont hence it will throw an error
            # so to manage that because there are total 15 and emotions are 10 only to show conversation without emotions
            try:
                if (
                    int(txt.search("emotion_generation", "saves/default/config.conf"))
                    < 1
                ):
                    raise
                with open(
                    txt.pathOs(cpath + "/history/" + logs + "-emotions.json"),
                    "r",
                    encoding="utf-8",
                ) as emotionlist:
                    emotionlist = json.load(emotionlist)
                    j = 0
                    for i in range(int(len(history) / 2)):
                        rprint("\n" + user_conversation + " " + history[j]["content"])
                        rprint(
                            Tables.table_with_emotion(
                                history[j + 1]["content"],
                                txt.search_image(emotionlist[i], cpath),
                            )
                        )
                        current = j
                        j += 2
            # If emotion generation is disabled or some error happens in finding emotions in file eg. missing 1 outof 5 emotion
            except:
                for i in range(current, len(history)):
                    if i % 2 == 0:
                        rprint("\n" + user_conversation + " " + history[i]["content"])
                    else:
                        rprint(Tables.table_without_emotion(history[i]["content"]))

    # It will allow to continue from where we left the conversation and with or without the same model as previous
    def ConinueFromWhereItLeft(self, logs):
        searchKeyword = txt.search("search", "saves/default/config.conf")
        # Since ollama-aneki give current time to model too as command to memorize it so that they stay aware about time
        # it will be added here by removing previous time from history logs
        now = str(datetime.datetime.now())
        cpath = txt.search("custom_path", "saves/default/config.conf")
        models = (
            open(
                txt.pathOs(cpath + "/model-list.txt"),
                "r",
                encoding="utf-8",
            )
            .read()
            .split("\n")[:-1]
        )
        model_name = Prompt.ask(
            "Select Model: ",
            default=models[0],
            choices=models,
        )
        memory_list = [
            {
                "role": "user",
                "content": "Here are some info for you to memorized about me. ",
            },
            {"role": "assistant", "content": "I have memorized it..."},
        ]
        emotionlist = []

        try:
            memory_list = json.load(
                open(
                    txt.pathOs(cpath + f"/models/{model_name}.json"),
                    "r",
                    encoding="utf-8",
                )
            )
        except:
            pass

        # Loading previous conversations
        with open(
            txt.pathOs(cpath + "/history/" + logs + ".json"),
            "r",
            encoding="utf-8",
        ) as history:
            history = json.load(history)[2:]
            choices = []
            print("\n")
            # To ask from where they want to continue by number as input choices
            for i in range(int(len(history) / 2)):
                choices.append(str(i + 1))
                rprint(
                    txt.search("highlight", "saves/default/config.conf")
                    + str(i + 1)
                    + " "
                    + txt.search("normal", "saves/default/config.conf")
                    + history[i * 2]["content"]
                )
            print("\n")
            indexs = int(
                Prompt.ask(
                    "From where do you want to continue",
                    default=str(int(len(history) / 2)),
                    choices=choices,
                )
            )
            # Based on choice made by user we create new history by removing remaining conversation
            history = history[: (indexs) * 2]
            with open(
                txt.pathOs(cpath + "/history/" + logs + ".json"), "w", encoding="utf-8"
            ) as chats:
                for h in history:
                    memory_list.append(h)
                json.dump(memory_list, chats, indent=2)
            # Now we try to load previous emotions if any.
            try:
                with open(
                    txt.pathOs(cpath + "/history/" + logs + "-emotions.json"),
                    "r",
                    encoding="utf-8",
                ) as emotionlist:
                    emotionlist = json.load(emotionlist)
                    emotionlist = emotionlist[:indexs]
                    with open(
                        txt.pathOs(cpath + "/history/" + logs + "-emotions.json"),
                        "w",
                        encoding="utf-8",
                    ) as emotion:

                        json.dump(emotionlist, emotion, indent=2)
            except:
                pass

        max_respose_size = int(
            txt.search("max_respose_size", "saves/default/config.conf")
        )
        length = 2 * int(txt.search("memory_length", "saves/default/config.conf"))
        user_conversation = txt.search("user_conversation", "saves/default/config.conf")
        frequency = int(txt.search("frequency", "saves/default/config.conf"))
        memory = [
            {
                "role": "user",
                "content": "Here are some info for you to memorized about me. ",
            },
            {"role": "assistant", "content": "I have memorized it..."},
        ]
        try:
            memory = json.load(
                open(
                    txt.pathOs(custom + f"/models/{model_name}.json"),
                    "r",
                    encoding="utf-8",
                )
            )
        except:
            pass
            # To generate inintial memory

        memory[0]["content"] += ". The current time is " + now

        # It will return history based on memory_length
        def length_ret(leng, hist):
            if leng < len(hist):
                hist = hist[(len(hist) - leng) + 1 :]
                new_hist = memory
                for h in hist:
                    new_hist.append(h)
                # print(new_hist)
                return new_hist
            else:
                return hist

        history = memory_list
        # Calling emotion generation model
        if int(txt.search("emotion_generation", "saves/default/config.conf")) >= 1:
            emotions = emotionlist
            model = ModelCatalog().load_model("slim-emotions-tool")
            if int(txt.search("auto_clear", "saves/default/config.conf")) >= 1:
                (
                    subprocess.run("cls", shell=True)
                    if os.name == "nt"
                    else subprocess.run(["clear"])
                )
                self.read(logs)
            user_input = Search.getData(input("\n" + user_conversation + " "),searchKeyword)
            while (
                user_input.lower()
                != txt.search("exit_code", "saves/default/config.conf").lower()
            ):
                # Appending user input in formate that ollama understands eg. {"role":"user" , "content":"i am otaku"}
                history.append({"role": "user", "content": user_input})
                # Used stream to get continues response from ollama
                stream = ollama.chat(
                    model=model_name,
                    messages=length_ret(length, history),
                    stream=True,
                )
                msg = ""
                # Since text is updateing with ollama stream we use rich live tables to update table
                with Live(Table(), auto_refresh=True) as live:
                    # initial emotion is joyfull
                    response = "joyful"
                    art = txt.search_image(response, cpath)
                    for chunk in stream:
                        # appending chunks into messaage to get whole response by ollama
                        msg += chunk["message"]["content"]
                        # Have you played gensshin impact ? There is a thing which called
                        # crit hit which depends on crit rate. The frequency is like crit rate.
                        # That shows how ofter do you want to trigger emotion generation
                        if len(msg) % frequency < 3 and len(msg) < max_respose_size:
                            response = model.function_call(msg)["llm_response"][
                                "emotions"
                            ][0]
                            art = txt.search_image(response, cpath)
                        # The new emotion it will replace it in table
                        live.update(Tables.table_with_emotion(msg, art))
                    # To make emotion generation faster for after complete generation of content by ollama, it will be done here
                    if len(msg) > max_respose_size:
                        response = model.function_call(msg[: max_respose_size - 1])[
                            "llm_response"
                        ]["emotions"][0]
                    else:
                        response = model.function_call(msg)["llm_response"]["emotions"][
                            0
                        ]
                    live.update(
                        Tables.table_with_emotion(
                            msg, txt.search_image(response, cpath)
                        )
                    )
                emotions.append(response)
                with open(
                    txt.pathOs(cpath + f"/history/{logs}-emotions.json"),
                    "w",
                    encoding="utf-8",
                ) as emotion:
                    json.dump(emotions, emotion, indent=2)
                history.append(
                    {
                        "role": "assistant",
                        "content": msg,
                    }
                )
                # Saving history
                with open(
                    txt.pathOs(cpath + f"/history/{logs}.json"),
                    "w",
                    encoding="utf-8",
                ) as chats:
                    json.dump(history, chats, indent=2)
                if (
                    int(txt.search("reprint_everytime", "saves/default/config.conf"))
                    >= 1
                ):
                    (
                        subprocess.run("cls", shell=True)
                        if os.name == "nt"
                        else subprocess.run(["clear"])
                    )
                    self.read(logs)
                user_input = Search.getData(input("\n" + user_conversation + " "),searchKeyword)
        # Its a part that will run without emotion generation
        else:
            self.read(logs)
            user_input = Search.getData(input("\n" + user_conversation + " "),searchKeyword)
            while (
                user_input.lower()
                != txt.search("exit_code", "saves/default/config.conf").lower()
            ):
                history.append({"role": "user", "content": user_input})
                stream = ollama.chat(
                    model=model_name,
                    messages=length_ret(length, history),
                    stream=True,
                )
                msg = ""
                with Live(Table(), auto_refresh=True) as live:
                    for chunk in stream:
                        msg += chunk["message"]["content"]
                        live.update(Tables.table_without_emotion(msg))
                history.append(
                    {
                        "role": "assistant",
                        "content": msg,
                    }
                )
                # Saving history
                with open(
                    txt.pathOs(cpath + f"/history/{logs}.json"),
                    "w",
                    encoding="utf-8",
                ) as chats:
                    json.dump(history, chats, indent=2)
                if (
                    int(txt.search("reprint_everytime", "saves/default/config.conf"))
                    >= 1
                ):
                    (
                        subprocess.run("cls", shell=True)
                        if os.name == "nt"
                        else subprocess.run(["clear"])
                    )
                    self.read(logs)
                user_input = Search.getData(input("\n" + user_conversation + " "),searchKeyword)

    def new_run(self, model_name):
        searchKeyword = txt.search("search", "saves/default/config.conf")
        # Since ollama-aneki give current time to model too as command to memorize
        # it so that they stay aware about time and date it is done here
        now = str(datetime.datetime.now())
        custom = txt.search("custom_path", "saves/default/config.conf")
        user_conversation = txt.search("user_conversation", "saves/default/config.conf")
        # By this we can give name to history as we desired eg. title: charged ionized plazma thruster
        ask_for_Topic = (
            int(txt.search("ask_for_Topic", "saves/default/config.conf")) == 1
        )
        Topic = ""
        if ask_for_Topic:
            Topic = Prompt.ask("Save history with name: ", default=now)
            with open(
                txt.pathOs(custom + "/historylog.txt"), "a", encoding="utf-8"
            ) as historylog:
                historylog.write(f"{model_name}-{Topic}\n")
        # If user dont want to give name to history then it will be saved with current time
        else:
            with open(
                txt.pathOs(custom + "/historylog.txt"), "a", encoding="utf-8"
            ) as historylog:
                historylog.write(f"{model_name}-{now}\n")

        length = 2 * int(txt.search("memory_length", "saves/default/config.conf"))
        max_respose_size = int(
            txt.search("max_respose_size", "saves/default/config.conf")
        )
        frequency = int(txt.search("frequency", "saves/default/config.conf"))
        # In case if path is not been created
        Path(txt.pathOs(custom + "/history/")).mkdir(parents=True, exist_ok=True)
        memory = [
            {
                "role": "user",
                "content": "Here are some info for you to memorized about me. ",
            },
            {"role": "assistant", "content": "I have memorized it..."},
        ]
        try:
            memory = json.load(
                open(
                    txt.pathOs(custom + f"/models/{model_name}.json"),
                    "r",
                    encoding="utf-8",
                )
            )
        except:
            pass
        memory[0]["content"] += ". The current time is " + now

        # It will return history based on memory_length
        def length_ret(leng, hist):
            if leng < len(hist):
                hist = hist[(len(hist) - leng) + 1 :]
                new_hist = memory
                for h in hist:
                    new_hist.append(h)
                return new_hist
            else:
                return hist

        # Remaining process is same as continue from where it left
        history = []
        history.append(memory[0])
        history.append(memory[1])
        if int(txt.search("emotion_generation", "saves/default/config.conf")) >= 1:
            emotions = []
            model = ModelCatalog().load_model("slim-emotions-tool")
            if int(txt.search("auto_clear", "saves/default/config.conf")) >= 1:
                (
                    subprocess.run("cls", shell=True)
                    if os.name == "nt"
                    else subprocess.run(["clear"])
                )
            user_input = Search.getData(input("\n" + user_conversation + " "),searchKeyword)
            while (
                user_input.lower()
                != txt.search("exit_code", "saves/default/config.conf").lower()
            ):
                history.append({"role": "user", "content": user_input})
                stream = ollama.chat(
                    model=model_name,
                    messages=length_ret(length, history),
                    stream=True,
                )
                msg = ""
                with Live(Table(), auto_refresh=True) as live:
                    response = "joyful"
                    art = txt.search_image(response, custom)
                    for chunk in stream:
                        msg += chunk["message"]["content"]
                        if len(msg) % frequency < 3 and len(msg) < max_respose_size:
                            response = model.function_call(msg)["llm_response"][
                                "emotions"
                            ][0]
                            art = txt.search_image(response, custom)
                        live.update(Tables.table_with_emotion(msg, art))
                    if len(msg) > max_respose_size:
                        response = model.function_call(msg[: max_respose_size - 1])[
                            "llm_response"
                        ]["emotions"][0]
                    else:
                        response = model.function_call(msg)["llm_response"]["emotions"][
                            0
                        ]
                    live.update(
                        Tables.table_with_emotion(
                            msg, txt.search_image(response, custom)
                        )
                    )
                emotions.append(response)
                # If asked for topic is true then it will save history with the title as topic for emotions
                if ask_for_Topic:
                    with open(
                        txt.pathOs(
                            custom + f"/history/{model_name}-{Topic}-emotions.json"
                        ),
                        "w",
                        encoding="utf-8",
                    ) as emotion:
                        json.dump(emotions, emotion, indent=2)
                else:
                    with open(
                        txt.pathOs(
                            custom + f"/history/{model_name}-{now}-emotions.json"
                        ),
                        "w",
                    ) as emotion:
                        json.dump(emotions, emotion, indent=2)
                history.append(
                    {
                        "role": "assistant",
                        "content": msg,
                    }
                )
                # If asked for topic is true then it will save history with the title as topic for conversation
                if ask_for_Topic:
                    with open(
                        txt.pathOs(custom + f"/history/{model_name}-{Topic}.json"),
                        "w",
                        encoding="utf-8",
                    ) as chats:
                        json.dump(history, chats, indent=2)
                    # Since we neew to load history with topic so it will print history with topic
                    if (
                        int(
                            txt.search("reprint_everytime", "saves/default/config.conf")
                        )
                        >= 1
                    ):
                        (
                            subprocess.run("cls", shell=True)
                            if os.name == "nt"
                            else subprocess.run(["clear"])
                        )
                        self.read(Topic)
                else:
                    with open(
                        txt.pathOs(custom + f"/history/{model_name}-{now}.json"),
                        "w",
                        encoding="utf-8",
                    ) as chats:
                        json.dump(history, chats, indent=2)
                    if (
                        int(
                            txt.search("reprint_everytime", "saves/default/config.conf")
                        )
                        >= 1
                    ):
                        (
                            subprocess.run("cls", shell=True)
                            if os.name == "nt"
                            else subprocess.run(["clear"])
                        )
                        self.read(f"{model_name}-{now}")
                user_input = Search.getData(input("\n" + user_conversation + " "),searchKeyword)
        else:
            user_input = Search.getData(input("\n" + user_conversation + " "),searchKeyword)
            while (
                user_input.lower()
                != txt.search("exit_code", "saves/default/config.conf").lower()
            ):
                history.append({"role": "user", "content": user_input})
                stream = ollama.chat(
                    model=model_name,
                    messages=length_ret(length, history),
                    stream=True,
                )
                msg = ""
                with Live(Table(), auto_refresh=True) as live:
                    for chunk in stream:
                        msg += chunk["message"]["content"]
                        live.update(Tables.table_without_emotion(msg))
                history.append(
                    {
                        "role": "assistant",
                        "content": msg,
                    }
                )
                # If asked for topic is true then it will save history with the title as topic for conversation
                if ask_for_Topic:
                    with open(
                        txt.pathOs(custom + f"/history/{model_name}-{Topic}.json"),
                        "w",
                        encoding="utf-8",
                    ) as chats:
                        json.dump(history, chats, indent=2)
                    if (
                        int(
                            txt.search("reprint_everytime", "saves/default/config.conf")
                        )
                        >= 1
                    ):
                        (
                            subprocess.run("cls", shell=True)
                            if os.name == "nt"
                            else subprocess.run(["clear"])
                        )
                        self.read(f"{model_name}-{now}")
                else:
                    with open(
                        txt.pathOs(custom + f"/history/{model_name}-{now}.json"),
                        "w",
                        encoding="utf-8",
                    ) as chats:
                        json.dump(history, chats, indent=2)
                    if (
                        int(
                            txt.search("reprint_everytime", "saves/default/config.conf")
                        )
                        >= 1
                    ):
                        (
                            subprocess.run("cls", shell=True)
                            if os.name == "nt"
                            else subprocess.run(["clear"])
                        )
                        self.read(f"{model_name}-{now}")
                user_input = Search.getData(input("\n" + user_conversation + " "),searchKeyword)
