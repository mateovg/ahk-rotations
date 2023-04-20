import csv
import random

modifiers = {"shift", "ctrl", "alt"}


class Ability:
    def __init__(self, keybind, tick):
        self.keybind = keybind.lower().split()
        self.tick = int(tick)

    def to_ahk(self):
        ahk_string = ""
        for key in self.keybind:
            down = ["Send", "{", key, "Down", "}", "\n"]
            ahk_string += " ".join(down)
        ahk_string += " ".join(["Sleep, ", str(random.randint(2, 20)), "\n"])
        for key in self.keybind:
            up = ["Send", "{", key, "Up", "}", "\n"]
            ahk_string += " ".join(up)
        for key in self.keybind:
            if key in modifiers:
                ahk_string += f"Send, {{{key}Up}}\n"
        return ahk_string


def get_rotation(filename):
    rotation = []

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            # (keybind, tick used)
            if len(row) == 2:
                if row[1].strip() != "":
                    rotation.append(Ability(row[1], row[0].strip()))
    return rotation


def create_ahk(rotation):
    # create ahk file from rotation and keybinds
    current_tick = 1  # liam starts at 1 lol?
    with open("rotation.ahk", "w") as f:
        header = "#MaxThreadsPerHotkey 1\n#SingleInstance Force\n#IfWinActive RuneScape"
        f.write(header + "\n")

        macro_key = "F12"
        f.write(f"{macro_key}::\nToolTip, Botting lol\n")

        for i, ability in enumerate(rotation):
            # get tick used from rotation
            print(f"{ability.tick} - {ability.keybind}")
            tick = ability.tick
            # get keybind from keybinds dict
            if (tick - current_tick) != 0:
                f.write(
                    f"Sleep {((tick - current_tick) * 590 )}\n")
            f.write(ability.to_ahk())
            current_tick = tick

        f.write("return\n")
        f.write("+Esc::Reload\n")
    f.close()


rotation_file = "Telos.csv"
rotation = get_rotation(rotation_file)
create_ahk(rotation)
