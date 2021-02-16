import random

from GameEngine.Components.Position import Position
from GameEngine.Components.Sprite import Sprite
from GameEngine.Components.Vegeteable import Vegetable
from GameEngine.GameServer import ecs
from GameEngine.Components.Fox import Fox
from GameEngine.Components.Rabbit import Rabbit

""" Multi process the AI """


def fox_update():
    """ What does the fow says ? """
    foxs = ecs.get_component(Fox)
    for fox in foxs:
        print("Ring-ding-ding-ding-dingeringeding!\n" +
              "Gering-ding-ding-ding-dingeringeding!\n" +
              "Gering-ding-ding-ding-dingeringeding!")
    return {}


def rabbit_update():
    """ Rabbits will make different actions depending on their status """
    rabbit = ecs.get_component(Rabbit)
    vegetable = ecs.get_component(Vegetable)
    fox = ecs.get_component(Fox)
    positions = ecs.get_component(Position)
    rabbit_ids = ecs.filter(Rabbit, Position)
    fox_ids = ecs.filter(Fox, Position)
    food_ids = ecs.filter(Vegetable, Position)

    for id in rabbit_ids:
        food_direction = [0,0]
        fear_direction = [0,0]
        repr_direction = [0,0]

        for food in food_ids:
            if positions[id] == positions[food]:
                rabbit[id].hunger = min(0, rabbit[id].hunger - vegetable[food].nutritionnal_score)

        select_direction = random.randint(0, 3)
        if select_direction == 0:
            positions[id].x += 1
        if select_direction == 1:
            positions[id].x -= 1
        if select_direction == 2:
            positions[id].y += 1
        if select_direction == 3:
            positions[id].y -= 1
    return positions