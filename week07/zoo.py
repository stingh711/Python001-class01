from abc import ABCMeta


class Animal(metaclass=ABCMeta):
    def __init__(self, category, size, character):
        self.category = category
        self.size = size
        self.character = character

    @property
    def is_beast(self):
        return self.category == "食肉" and self.character == "凶猛" and self.size != "小"


class Cat(Animal):
    sound = "喵喵"

    def __init__(self, name, category, size, character):
        super().__init__(category, size, character)
        self.name = name
        self.pet = True


class Zoo:
    def __init__(self, name):
        self.name = name
        self.animals = set()

    def add_animal(self, animal):
        self.animals.add(animal)
        name = type(animal).__name__
        setattr(self, name, True)


if __name__ == "__main__":
    z = Zoo("时间动物园")
    cat1 = Cat("大花猫1", "食肉", "小", "温顺")
    z.add_animal(cat1)
    have_cat = getattr(z, "Cat")
    print(have_cat)
