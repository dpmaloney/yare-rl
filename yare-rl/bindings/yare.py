import os
from ctypes import WinDLL, Structure, CFUNCTYPE, c_float, c_ulong, c_long, c_ulong, c_void_p, c_char_p


class Vec2(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float)]

class SimResult(Structure):
    """
    result = -1 (game still on going)
             0 player 0 won
             1 player 1 won
             2 draw (game timed out)
    """
    _fields_ = [("tick", c_ulong),
                ("result", c_long)]

class Id(Structure):
    _fields_ = [("player_id", c_ulong),
                ("index", c_ulong)]

TICKFN = CFUNCTYPE(None, c_ulong)


class YareBindings:
    def __init__(self):
        yare_lib = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yareio.dll")
        # TODO: allow to load library for Windows, Linux (and MacOS?)
        self.lib = WinDLL(name=str(yare_lib))

        # Headless functions
        self.lib.headless_simulate.argtypes = [TICKFN, c_ulong, TICKFN, c_ulong, c_char_p]
        self.lib.headless_simulate.restype = SimResult
        self.lib.headless_init.argtypes = [TICKFN, c_ulong, TICKFN, c_ulong, c_char_p]
        self.lib.headless_init.restype = c_void_p
        self.lib.headless_update_env.argtypes = [c_void_p]
        self.lib.headless_update_env.restype = None
        self.lib.headless_gather_commands.argtypes = [c_void_p, c_ulong]
        self.lib.headless_gather_commands.restype = None
        self.lib.headless_process_commands.argtypes = [c_void_p]
        self.lib.headless_process_commands.restype = SimResult
        self.lib.headless_free.argtypes = [c_void_p]
        self.lib.headless_free.restype = None

        # Spirit Info
        self.lib.spirit_count.argtypes = []
        self.lib.spirit_count.restype = c_ulong
        self.lib.spirit_energy.argtypes = [c_ulong]
        self.lib.spirit_energy.restype = c_long
        self.lib.spirit_energy_capacity.argtypes = [c_ulong]
        self.lib.spirit_energy_capacity.restype = c_long
        self.lib.spirit_hp.argtypes = [c_ulong]
        self.lib.spirit_hp.restype = c_ulong
        self.lib.spirit_id.argtypes = [c_ulong]
        self.lib.spirit_id.restype = Id
        self.lib.spirit_position.argtypes = [c_ulong]
        self.lib.spirit_position.restype = Vec2
        self.lib.spirit_shape.argtypes = [c_ulong]
        self.lib.spirit_shape.restype = c_ulong
        self.lib.spirit_size.argtypes = [c_ulong]
        self.lib.spirit_size.restype = c_long


        # Commands
        self.lib.spirit_energize_base.argtypes = [c_ulong, c_ulong]
        self.lib.spirit_energize_base.restype = None
        self.lib.spirit_energize_outpost.argtypes = [c_ulong, c_ulong]
        self.lib.spirit_energize_outpost.restype = None
        self.lib.spirit_energize.argtypes = [c_ulong, c_ulong]
        self.lib.spirit_energize.restype = None
        self.lib.spirit_goto.argtypes = [c_ulong, c_float, c_float]
        self.lib.spirit_goto.restype = None

        # Shape Specific Commands
        self.lib.spirit_explode.argtypes = [c_ulong]
        self.lib.spirit_explode.restype = None
        self.lib.spirit_jump.argtypes = [c_ulong, c_float, c_float]
        self.lib.spirit_jump.restype = None
        self.lib.spirit_merge.argtypes = [c_ulong, c_ulong]
        self.lib.spirit_merge.restype = None
        self.lib.spirit_divide.argtypes = [c_ulong]
        self.lib.spirit_divide.restype = None

        # Star
        self.lib.star_active_at.argtypes = [c_ulong]
        self.lib.star_active_at.restype = c_ulong
        self.lib.star_count.argtypes = []
        self.lib.star_count.restype = c_ulong
        self.lib.star_energy_capacity.argtypes = [c_ulong]
        self.lib.star_energy_capacity.restype = c_long
        self.lib.star_energy.argtypes = [c_ulong]
        self.lib.star_energy.restype = c_long
        self.lib.star_position.argtypes = [c_ulong]
        self.lib.star_position.restype = Vec2

        # Outpost
        self.lib.outpost_count.argtypes = []
        self.lib.outpost_count.restype = c_ulong
        self.lib.outpost_energy_capacity.argtypes = [c_ulong]
        self.lib.outpost_energy_capacity.restype = c_long
        self.lib.outpost_energy.argtypes = [c_ulong]
        self.lib.outpost_energy.restype = c_long
        self.lib.outpost_player_id.argtypes = [c_ulong]
        self.lib.outpost_player_id.restype = c_ulong
        self.lib.outpost_position.argtypes = [c_ulong]
        self.lib.outpost_position.restype = Vec2
        self.lib.outpost_range.argtypes = [c_ulong]
        self.lib.outpost_range.restype = c_float

        # Base
        self.lib.base_count.argtypes = []
        self.lib.base_count.restype = c_ulong
        self.lib.base_current_spirit_cost.argtypes = [c_ulong]
        self.lib.base_current_spirit_cost.restype = c_long
        self.lib.base_energy_capacity.argtypes = [c_ulong]
        self.lib.base_energy_capacity.restype = c_long
        self.lib.base_energy.argtypes = [c_ulong]
        self.lib.base_energy.restype = c_long
        self.lib.base_hp.argtypes = [c_ulong]
        self.lib.base_hp.restype = c_ulong
        self.lib.base_player_id.argtypes = [c_ulong]
        self.lib.base_player_id.restype = c_ulong
        self.lib.base_position.argtypes = [c_ulong]
        self.lib.base_position.restype = Vec2


if __name__ == "__main__":
    yare = YareBindings().lib

    def print_pos(_):
        print(yare.spirit_position(0).x, yare.spirit_position(0).y)
        return

    bot1 = TICKFN(print_pos)
    bot2 = TICKFN(print_pos)
    i = c_ulong(0)
    ptr = yare.headless_init(bot1, i, bot2, i, c_char_p(b"replay.json"))
    result = -1
    while result < 0:
        yare.headless_update_env(ptr)
        yare.headless_gather_commands(ptr, c_ulong(0))
        yare.headless_gather_commands(ptr, c_ulong(1))
        res = yare.headless_process_commands(ptr)
        result = res.result
    yare.headless_free(ptr)

    print("Game finished in " + str(res.tick) + " ticks.")




