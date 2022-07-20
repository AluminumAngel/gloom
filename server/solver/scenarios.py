from past.utils import old_div


# def unreduce_actions(s, actions):
#     def fix_location(location):
#         column = old_div(location, s.MAP_HEIGHT)
#         row = location % s.MAP_HEIGHT
#         column += s.REDUCE_COLUMN
#         row += s.REDUCE_ROW
#         return row + column * s.OLD_MAP_HEIGHT

#     def fix_location_list(location_list):
#         new_location_list = []
#         for item in location_list:
#             new_location_list.append(fix_location(item))
#         return new_location_list

#     new_actions = []
#     for action in actions:
#         new_action = {}
#         new_action['move'] = fix_location(action['move'])
#         new_action['attacks'] = fix_location_list(action['attacks'])
#         new_action['focuses'] = fix_location_list(action['focuses'])
#         new_action['destinations'] = fix_location_list(action['destinations'])
#         new_actions.append(new_action)

#     return new_actions

# def reduce_scenario( s, scenario ):
#   # TODO: reduce the scenario in-place

#   min_row = 9999
#   min_column = 9999
#   max_row = 0
#   max_column = 0

#   # TODO: don't need to prepare first map

#   figures = [ _ for _, figure in enumerate( s.figures ) if figure != ' ' ]
#   contents = [ _ for _, content in enumerate( s.contents ) if content != ' ' ]
#   for location in figures:
#     column = location / s.MAP_HEIGHT
#     min_column = min( min_column, column )
#     max_column = max( max_column, column )
#     row = location % s.MAP_HEIGHT
#     min_row = min( min_row, row )
#     max_row = max( max_row, row )
#     print s.figures[location], column, row
#   for location in contents:
#     column = location / s.MAP_HEIGHT
#     min_column = min( min_column, column )
#     max_column = max( max_column, column )
#     row = location % s.MAP_HEIGHT
#     min_row = min( min_row, row )
#     max_row = max( max_row, row )
#     print s.figures[location], column, row
#   print min_column, max_column
#   print min_row, max_row

#   reduce_column = min_column / 2 * 2
#   reduce_row = min_row

#   scenario.REDUCE_COLUMN = reduce_column
#   scenario.REDUCE_ROW = reduce_row
#   scenario.OLD_MAP_HEIGHT = s.MAP_HEIGHT

#   width = max_column - reduce_column + 1
#   height = max_row - reduce_row + 1

#   init( scenario, width, height, s.AOE_WIDTH, s.AOE_HEIGHT )

#   for location in figures:
#     column = location / s.MAP_HEIGHT
#     row = location % s.MAP_HEIGHT
#     column -= reduce_column
#     row -= reduce_row
#     new_location = row + column * scenario.MAP_HEIGHT
#     print new_location, location
#     scenario.figures[new_location] = s.figures[location]
#     scenario.initiatives[new_location] = s.initiatives[location]
#   for location in contents:
#     column = location / s.MAP_HEIGHT
#     row = location % s.MAP_HEIGHT
#     column -= reduce_column
#     row -= reduce_row
#     new_location = row + column * scenario.MAP_HEIGHT
#     print new_location, location
#     scenario.contents[new_location] = s.contents[location]

#   # copy aoe
#   # copy initiative
#   # copy thin walls

#   scenario.message = s.message
#   scenario.ACTION_MOVE = s.ACTION_MOVE
#   scenario.ACTION_RANGE = s.ACTION_RANGE
#   scenario.ACTION_TARGET = s.ACTION_TARGET
#   scenario.FLYING = s.FLYING
#   scenario.JUMPING = s.JUMPING
#   scenario.MUDDLED = s.MUDDLED
#   scenario.aoe = s.aoe

#   scenario.prepare_map()

# TODO should be a member function


# def init(s, width, height, aoe_width, aoe_height):
#     s.test_switch = False
#     s.reduced = False

#     s.MAP_WIDTH = width
#     s.MAP_HEIGHT = height
#     s.MAP_SIZE = s.MAP_WIDTH * s.MAP_HEIGHT
#     s.MAP_VERTEX_COUNT = 6 * s.MAP_SIZE
#     # s.MAP_CENTER = ( s.MAP_SIZE - 1 ) / 2;

#     s.AOE_WIDTH = aoe_width
#     s.AOE_HEIGHT = aoe_height
#     s.AOE_SIZE = s.AOE_WIDTH * s.AOE_HEIGHT
#     s.AOE_CENTER = old_div((s.AOE_SIZE - 1), 2)
#     if s.AOE_WIDTH != 7 or s.AOE_HEIGHT != 7:
#         exit()
#     if int(s.AOE_CENTER) - s.AOE_CENTER != 0:
#         exit('aoe has no center')

#     s.walls = [[False] * 6 for _ in range(s.MAP_SIZE)]
#     s.contents = [' '] * s.MAP_SIZE
#     s.figures = [' '] * s.MAP_SIZE
#     s.initiatives = [0] * s.MAP_SIZE
#     s.aoe = [False] * s.AOE_SIZE
#     s.message = ''

#     s.ACTION_MOVE = 0
#     s.ACTION_RANGE = 0
#     s.ACTION_TARGET = 1
#     s.FLYING = False
#     s.JUMPING = False
#     s.MUDDLED = False

#     s.DEBUG_TOGGLE = False