class Command:
    def __init__(self, command_array):
        self.commandName = command_array[0]
        x, y = 0, 0
        if len(command_array) > 1:
            x, y = map(int, command_array[1].split())
        self.tabPosition = (x, y)

