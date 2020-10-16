
class __ECS(object):
    _instance = None

    def __init__(self):
        self.components = {}
        self.updates = []
        self.entity = 0

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def new_entity(self):
        self.entity += 1
        return self.entity

    def get_component(self, component, entity=None):
        if entity is None:
            return self.components[type(component()).__name__]
        return next(item for item in self.components[type(component()).__name__] if item["entity"] == entity)

    def add_component(self, entity, component):
        if type(component).__name__ not in self.components:
            self.components[type(component).__name__] = []
        self.components[type(component).__name__].append({"entity": entity, "component": component})

    def add_update(self, function):
        self.updates.append(function)

    def update(self):
        for function in self.updates:
            function()


class ECS(__ECS):
    pass


if __name__ == '__main__':
    ecs = ECS()

    ecs.add_component(7, int())
    print(ecs.get_component(int))
    ecs.add_update(lambda: print("mesboules"))
    ecs.update()