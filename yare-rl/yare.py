# ctypes_test.py
from ctypes import *
import pathlib
libname = pathlib.Path().absolute() / "yare_rust.dll"
lib = WinDLL(name=str(libname))
class Vec2(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float)]


# result = -1 (game still on going)
#           0 player 0 won
#           1 player 1 won
#           2 draw (game timed out)
class SimResult(Structure):
    _fields_ = [("tick", c_ulong),
                ("result", c_long)]

class Id(Structure):
    _fields_ = [("player_id", c_uint),
                ("index", c_uint)]

TICKFN = CFUNCTYPE(None, c_ulong)

# Headless functions
lib.headless_simulate.argtypes = [TICKFN, c_uint, TICKFN, c_uint]
lib.headless_simulate.restype = SimResult
lib.headless_init.argtypes = [TICKFN, c_uint, TICKFN, c_uint]
lib.headless_init.restype = c_void_p
lib.headless_update_env.argtypes = [c_void_p]
lib.headless_update_env.restype = None
lib.headless_gather_commands.argtypes = [c_void_p, c_uint]
lib.headless_gather_commands.restype = None
lib.headless_process_commands.argtypes = [c_void_p]
lib.headless_process_commands.restype = SimResult
lib.headless_free.argtypes = [c_void_p]
lib.headless_free.restype = None

# Spirit Info
lib.spirit_count.argtypes = []
lib.spirit_count.restype = c_uint
lib.spirit_energy.argtypes = [c_uint]
lib.spirit_energy.restype = c_long
lib.spirit_energy_capacity.argtypes = [c_uint]
lib.spirit_energy_capacity.restype = c_long
lib.spirit_hp.argtypes = [c_uint]
lib.spirit_hp.restype = c_ulong
lib.spirit_id.argtypes = [c_uint]
lib.spirit_id.restype = Id
lib.spirit_position.argtypes = [c_uint]
lib.spirit_position.restype = Vec2
lib.spirit_shape.argtypes = [c_uint]
lib.spirit_shape.restype = c_uint
lib.spirit_size.argtypes = [c_uint]
lib.spirit_size.restype = c_long


# Commands
lib.spirit_energize_base.argtypes = [c_uint, c_uint]
lib.spirit_energize_base.restype = None
lib.spirit_energize_outpost.argtypes = [c_uint, c_uint]
lib.spirit_energize_outpost.restype = None
lib.spirit_energize.argtypes = [c_uint, c_uint]
lib.spirit_energize.restype = None
lib.spirit_goto.argtypes = [c_uint]
lib.spirit_goto.restype = None

# Shape Specific Commands
lib.spirit_explode.argtypes = [c_uint]
lib.spirit_explode.restype = None
lib.spirit_jump.argtypes = [c_uint, c_float, c_float]
lib.spirit_jump.restype = None
lib.spirit_merge.argtypes = [c_uint, c_uint]
lib.spirit_merge.restype = None
lib.spirit_divide.argtypes = [c_uint]
lib.spirit_divide.restype = None

# Star
lib.star_active_at.argtypes = [c_uint]
lib.star_active_at.restype = c_ulong
lib.star_count.argtypes = []
lib.star_count.restype = c_uint
lib.star_energy_capacity.argtypes = [c_uint]
lib.star_energy_capacity.restype = c_long
lib.star_energy.argtypes = [c_uint]
lib.star_energy.restype = c_long
lib.star_position.argtypes = [c_uint]
lib.star_position.restype = Vec2

# Outpost
lib.outpost_count.argtypes = []
lib.outpost_count.restype = c_uint
lib.outpost_energy_capacity.argtypes = [c_uint]
lib.outpost_energy_capacity.restype = c_long
lib.outpost_energy.argtypes = [c_uint]
lib.outpost_energy.restype = c_long
lib.outpost_player_id.argtypes = [c_uint]
lib.outpost_player_id.restype = c_uint
lib.outpost_position.argtypes = [c_uint]
lib.outpost_position.restype = Vec2
lib.outpost_range.argtypes = [c_uint]
lib.outpost_range.restype = c_float

# Base
lib.base_count.argtypes = []
lib.base_count.restype = c_uint
lib.base_current_spirit_cost.argtypes = [c_uint]
lib.base_current_spirit_cost.restype = c_long
lib.base_energy_capacity.argtypes = [c_uint]
lib.base_energy_capacity.restype = c_long
lib.base_energy.argtypes = [c_uint]
lib.base_energy.restype = c_long
lib.base_hp.argtypes = [c_uint]
lib.base_hp.restype = c_ulong
lib.base_player_id.argtypes = [c_uint]
lib.base_player_id.restype = c_uint
lib.base_position.argtypes = [c_uint]
lib.base_position.restype = Vec2



def test(x):
    print(lib.spirit_position(0).x, lib.spirit_position(0).y)
    return

if __name__ == "__main__":
    bot1 = TICKFN(test)
    bot2 = TICKFN(test)
    i = c_uint(0)
    ptr = lib.headless_init(bot1, i, bot2, i)
    res = None
    result = -1
    while result < 0:
        lib.headless_update_env(ptr)
        lib.headless_gather_commands(ptr, c_uint(0))
        lib.headless_gather_commands(ptr, c_uint(1))
        res = lib.headless_process_commands(ptr)
        result = res.result

    lib.headless_free(ptr)

    print("Game finished in " + str(res.tick) + " ticks")




