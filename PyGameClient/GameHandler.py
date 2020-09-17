import time
from collections import OrderedDict

from Displayer.PyGameDisplay import PyGameDisplay
from MapHandler import MapHandler
from Entities import *
from utils import *


class GameHandler(object):
    def __init__(s, seed=0):
        random.seed(seed)
        ### MAP ###
        map_config = {
            'map_size': 64,
            'chunk_size': 64,
            'seed': seed,
            'noise_scale': 5,
        }
        s.map_handler = MapHandler(map_config)
        ### DISPLAY ###
        display_config = {
            'fps': 4,
            'target_resolution': Pos(x=1800, y=1000),
            'hud_width_px': 200,
            'tile_size': 32,
            'borders_width': 2,
        }
        s.cli_handler = PyGameDisplay(display_config)
        ### HUD ###
        s.start_time = time.time()
        s.hud_infos = OrderedDict()
        s.hud_infos["score"] = 0
        s.hud_infos["time"] = int(time.time() - s.start_time)
        ### MOVEMENTS ###
        s.avail_inputs = {
            'UP': Pos(-1, 0),
            'DOWN': Pos(1, 0),
            'LEFT': Pos(0, -1),
            'RIGHT': Pos(0, 1),
        }

    def launch(s):
        while 42:
            s.handle_inputs()
            s.handle_ia()
            s.hud_infos["time"] = int(time.time() - s.start_time)
            s.cli_handler.draw(s.map_handler, s.hud_infos)

    def handle_ia(s):
        return

    def handle_inputs(s):
        """ Exit if needed, otherwise try to execute the first move, if not successful (collision)
        try the next one etc, otherwise return """
        player_inputs = s.cli_handler.get_inputs()
        if not player_inputs: return
        if "EXIT" in player_inputs: exit()
        for player_input in player_inputs:
            if player_input in s.avail_inputs.keys():
                if s.map_handler.move_entity_relative(s.map_handler.player_pos, s.avail_inputs[player_input]):
                    s.map_handler.player_pos += s.avail_inputs[player_input]
                    break