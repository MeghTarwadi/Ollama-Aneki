class txt:
    def search(text, path):
        with open(path, "r") as txt:
            try:
                testlist = txt.readlines()
                for line in testlist:
                    line = line.replace(" ", "")
                    if line.__contains__("//"):
                        line = line[: line.index("//")]
                    if text in line:
                        return line.replace("\n", "").replace(text + "=", "")
                # print(testlist.index(text))
            except ValueError:
                print(f"Something({text}) is missing from {path}")
                raise ValueError
