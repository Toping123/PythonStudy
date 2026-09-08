class Horse:
    def __init__(self, color):
        """
        构造
        """
        self.name = "马"
        self.color = color

    def run(self):
        print(self.name + "善于奔跑，力气大")


class Donkey:

    def __init__(self):
        self.name = "驴"

    def tough(self):
        print(self.name + "耐力出众")


class Mule(Horse, Donkey):
    def __init__(self):
        Horse.__init__(self, "白色")
        Donkey.__init__(self)
        self.name = "骡子"

    def run_and_tough(self):
        Horse.run(self)
        Donkey.tough(self)


if __name__ == '__main__':
    mule = Mule()
    mule.run_and_tough()
