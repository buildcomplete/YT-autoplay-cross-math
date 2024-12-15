class Command:
    def __init__(self, command_array):
        self.commandName = command_array[0]
        r, c = 0, 0
        if len(command_array) > 1:
            r, c = map(int, command_array[1].split())
        self.tabPosition = (r, c)

    def CreateCommandFromOctaveFile(fileNamew):
        with  open(fileNamew, "r") as fHandle:
            lines = [line.strip() for line in fHandle]
            return Command(lines)
