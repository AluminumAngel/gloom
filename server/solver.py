# todo:
# - los and range are broken with reduce_map()
# - clean up reduce_map - make it official

import sys, collections, textwrap, itertools, pprint
import scenarios
from utils import *
from settings import *
from print_map import *

# import time
# perf_timers = {}
# start_time = 0
# last_time = 0

class Scenario:
  def __init__( self ):
    self.correct_answer = None
    self.valid = True
    self.logging = False
    self.debug_visuals = False
    self.show_each_action_separately = False

    self.visibility_cache = {}
    self.path_cache = [ {}, {}, {}, {} ]

    self.debug_lines = set()

  def reduce_map( self ):
    assert not self.reduced
    self.reduced = True
    # print self.effective_walls
    # if hasattr( self, 'effective_walls' ):
    #   exit(-1)

    # TODO: currently not used
    assert False
    print 'reduce_map works for solves and is tested, but range and line-of-sight do not yet support it correct'

    # TODO: make sure we don't prepare twice

    old_height = self.MAP_HEIGHT
    old_width = self.MAP_WIDTH
    old_walls = self.walls
    old_contents = self.contents
    old_figures = self.figures
    old_initiatives = self.initiatives

    min_row = 9999
    min_column = 9999
    max_row = 0
    max_column = 0
    targets_min_row = 9999
    targets_min_column = 9999
    targets_max_row = 0
    targets_max_column = 0

    # TODO: don't need to prepare_map first map

    figures = [ _ for _, figure in enumerate( self.figures ) if figure != ' ' ]
    contents = [ _ for _, content in enumerate( self.contents ) if content != ' ' ]
    walls = [
      [ _ for _, wall in enumerate( self.walls ) if wall[a] ]
      for a in range( 6 )
    ]

    # TODO
    # only need ACTION_RANGE to potential targets
    # handle AOE based range extensions (need test cases)
    # time

    for location in figures:
      column = location / old_height
      min_column = min( min_column, column )
      max_column = max( max_column, column )
      row = location % old_height
      min_row = min( min_row, row )
      max_row = max( max_row, row )
      if old_figures[location] == 'C':
        targets_min_column = min( targets_min_column, column )
        targets_max_column = max( targets_max_column, column )
        targets_min_row = min( targets_min_row, row )
        targets_max_row = max( targets_max_row, row )
    for location in contents:
      column = location / old_height
      min_column = min( min_column, column )
      max_column = max( max_column, column )
      row = location % old_height
      min_row = min( min_row, row )
      max_row = max( max_row, row )
    for i in range( 6 ):
      for location in walls[i]:
        column = location / old_height
        min_column = min( min_column, column )
        max_column = max( max_column, column )
        row = location % old_height
        min_row = min( min_row, row )
        max_row = max( max_row, row )

    edge = 1
    # edge = max( 1, self.ACTION_RANGE )
    min_row = max( min_row - edge, 0 )
    min_column = max( min_column - edge, 0 )
    max_row = min( max_row + edge, old_height - 1 )
    max_column = min( max_column + edge, old_width - 1 )

    attack_range = self.ACTION_RANGE
    # TODO - account for AOE here
    edge = max( 1, attack_range )
    targets_min_row = max( targets_min_row - edge, 0 )
    targets_min_column = max( targets_min_column - edge, 0 )
    targets_max_row = min( targets_max_row + edge, old_height - 1 )
    targets_max_column = min( targets_max_column + edge, old_width - 1 )

    min_row = min( min_row, targets_min_row )
    min_column = min( min_column, targets_min_column )
    max_row = max( max_row, targets_max_row )
    max_column = max( max_column, targets_max_column )

    reduce_column = min_column / 2 * 2
    reduce_row = min_row

    self.REDUCE_COLUMN = reduce_column
    self.REDUCE_ROW = reduce_row
    self.ORIGINAL_MAP_HEIGHT = old_height

    width = max_column - reduce_column + 1
    height = max_row - reduce_row + 1

    # init( scenario, width, height, s.AOE_WIDTH, s.AOE_HEIGHT )
    self.MAP_WIDTH = width
    self.MAP_HEIGHT = height
    self.MAP_SIZE = self.MAP_WIDTH * self.MAP_HEIGHT
    self.MAP_VERTEX_COUNT = 6 * self.MAP_SIZE
    # s.MAP_CENTER = ( s.MAP_SIZE - 1 ) / 2;

    self.walls = [ [ False ] * 6 for _ in range( self.MAP_SIZE ) ]
    self.contents = [ ' ' ] * self.MAP_SIZE
    self.figures = [ ' ' ] * self.MAP_SIZE
    self.initiatives = [ 0 ] * self.MAP_SIZE

    for location in figures:
      column = location / old_height
      row = location % old_height
      column -= reduce_column
      row -= reduce_row
      new_location = row + column * self.MAP_HEIGHT
      self.figures[new_location] = old_figures[location]
      self.initiatives[new_location] = old_initiatives[location]
    for location in contents:
      column = location / old_height
      row = location % old_height
      column -= reduce_column
      row -= reduce_row
      new_location = row + column * self.MAP_HEIGHT
      self.contents[new_location] = old_contents[location]
    for i in range( 6 ):
      for location in walls[i]:
        column = location / old_height
        row = location % old_height
        column -= reduce_column
        row -= reduce_row
        new_location = row + column * self.MAP_HEIGHT
        self.walls[new_location][i] = True

    self.prepare_map()

  def prepare_map( self ):
    self.setup_vertices_list()
    self.setup_neighbors_mapping()

    self.HAS_ICY_TERRAIN = 'I' in self.contents

    contents_walls = [ None ] * self.MAP_SIZE
    self.effective_walls = [ 0 ] * self.MAP_SIZE
    for location in range( self.MAP_SIZE ):
      if self.contents[location] == 'X':
        contents_walls[location] = [ True ] * 6
        self.effective_walls[location] = [ True ] * 6
      else:
        contents_walls[location] = [ False ] * 6
        self.effective_walls[location] = list( self.walls[location] )

    for location in range( self.MAP_SIZE ):
      for edge, neighbor in enumerate( self.neighbors[location] ):
        if neighbor != -1:
          neighbor_edge = ( edge + 3 ) % 6
          if self.walls[location][edge]:
            self.walls[neighbor][neighbor_edge] = True
          if self.effective_walls[location][edge]:
            self.effective_walls[neighbor][neighbor_edge] = True
          if contents_walls[location][edge]:
            contents_walls[neighbor][neighbor_edge] = True

    self.extra_walls = [ 0 ] * self.MAP_SIZE
    for location in range( self.MAP_SIZE ):
      self.extra_walls[location] = [ self.walls[location][_] and not contents_walls[location][_] for _ in range( 6 ) ]

  def set_rules( self, rules ):
    self.FROST_RULES = rules == 0
    self.GLOOM_RULES = rules == 1
    self.JOTL_RULES = rules == 2
    self.set_rules_flags()

  def set_rules_flags( self ):
    # RULE_VERTEX_LOS:                      LOS is only checked between vertices
    # RULE_JUMP_DIFFICULT_TERRAIN:          difficult terrain effects the last hex of a jump move
    # RULE_PROXIMITY_FOCUS:                 proximity is ignored when determining moster focus
    # RULE_PRIORITIZE_FOCUS_DISADVANTAGE:   avoiding disadvantage against focus is prioritized over target count
    # RULE_MAXIMIZE_FUTURE_MULTIATTACK:     move towards best multiattack if no attack possible this turn
    # RULE_RANK_SECONDARY_TARGETS:          rank secondary targets' priority using focus rules
    if self.FROST_RULES:
      self.RULE_VERTEX_LOS = False
      self.RULE_DIFFICULT_TERRAIN_JUMP = False
      self.RULE_PROXIMITY_FOCUS = False
      self.RULE_PRIORITIZE_FOCUS_DISADVANTAGE = False
      self.RULE_MAXIMIZE_FUTURE_MULTIATTACK = False
      self.RULE_RANK_SECONDARY_TARGETS = False
    elif self.GLOOM_RULES:
      self.RULE_VERTEX_LOS = True
      self.RULE_DIFFICULT_TERRAIN_JUMP = True
      self.RULE_PROXIMITY_FOCUS = False
      self.RULE_PRIORITIZE_FOCUS_DISADVANTAGE = True
      self.RULE_MAXIMIZE_FUTURE_MULTIATTACK = True
      self.RULE_RANK_SECONDARY_TARGETS = True
    elif self.JOTL_RULES:
      self.RULE_VERTEX_LOS = False
      self.RULE_DIFFICULT_TERRAIN_JUMP = False
      self.RULE_PROXIMITY_FOCUS = True
      self.RULE_PRIORITIZE_FOCUS_DISADVANTAGE = True
      self.RULE_MAXIMIZE_FUTURE_MULTIATTACK = True
      self.RULE_RANK_SECONDARY_TARGETS = True

  def unpack_scenario( self, packed_scenario ):
    self.ACTION_MOVE = int( packed_scenario['move'] )
    self.ACTION_RANGE = int( packed_scenario['range'] )
    self.ACTION_TARGET = int( packed_scenario['target'] )
    self.JUMPING = int( packed_scenario['flying'] ) == 1
    self.FLYING = int( packed_scenario['flying'] ) == 2
    self.MUDDLED = int( packed_scenario['muddled'] ) == 1

    # added to packed_scenario in v2.10.0
    self.TELEPORT = int( packed_scenario.get( 'teleport', '0' ) ) == 1
    
    # added to packed_scenario in v2.5.0; removed in v2.6.0
    #self.JOTL_RULES = int( packed_scenario.get( 'jotl', '0' ) ) == 1

    # added to packed_scenario in v2.6.0
    self.set_rules( int( packed_scenario.get( 'game_rules', '0' ) ) )

    self.DEBUG_TOGGLE = int( packed_scenario.get( 'debug_toggle', '0' ) )

    def add_elements( grid, key, content ):
      for _ in packed_scenario['map'].get( key, [] ):
        grid[_] = content

    add_elements( self.contents, 'walls', 'X' )
    add_elements( self.contents, 'obstacles', 'O' )
    add_elements( self.contents, 'traps', 'T' )
    add_elements( self.contents, 'hazardous', 'H' )
    add_elements( self.contents, 'difficult', 'D' )
    add_elements( self.figures, 'characters', 'C' )
    add_elements( self.figures, 'monsters', 'M' )
    add_elements( self.figures, 'test', 'M' )

    # added to packed_scenario in v2.8.0
    add_elements( self.contents, 'icy', 'I' )

    active_figure_location = packed_scenario['active_figure']
    switch_factions = self.figures[active_figure_location] == 'C'
    self.figures[active_figure_location] = 'A'

    if switch_factions:
      for _ in range( self.MAP_SIZE ):
        if self.figures[_] == 'C':
          self.figures[_] = 'M'
        elif self.figures[_] == 'M':
          self.figures[_] = 'C'

    for _ in packed_scenario['aoe']:
      if _ != self.AOE_CENTER or self.ACTION_RANGE > 0:
        self.aoe[_] = True

    remap = {
      1: 0,
      0: 1,
      2: 5,
    }
    for _ in packed_scenario['map']['thin_walls']:
      s = remap[_[1]]
      self.walls[_[0]][s] = True

    if switch_factions:
      victims = packed_scenario['map']['monsters']
    else:
      victims = packed_scenario['map']['characters']

    for i, j in zip( packed_scenario['map']['initiatives'], victims ):
      self.initiatives[j] = int( i )

    self.prepare_map()

  # TODO: clean
  def unpack_scenario_forviews( self, packed_scenario ):
    self.ACTION_RANGE = int( packed_scenario['range'] )
    self.ACTION_TARGET = int( packed_scenario['target'] )

    self.set_rules( int( packed_scenario.get( 'game_rules', '0' ) ) )

    def add_elements( grid, key, content ):
      for _ in packed_scenario['map'][key]:
        grid[_] = content

    add_elements( self.contents, 'walls', 'X' )

    remap = {
      1: 0,
      0: 1,
      2: 5,
    }
    for _ in packed_scenario['map']['thin_walls']:
      s = remap[_[1]]
      self.walls[_[0]][s] = True

    self.prepare_map()

  def can_end_move_on_standard( self, location ):
    return self.contents[location] in [ ' ', 'T', 'H', 'D', 'I' ] and self.figures[location] in [ ' ', 'A' ]
  def can_end_move_on_flying( self, location ):
    return self.contents[location] in [ ' ', 'T', 'O', 'H', 'D', 'I' ] and self.figures[location] in [ ' ', 'A' ]

  def can_travel_through_standard( self, location ):
    return self.contents[location] in [ ' ', 'T', 'H', 'D', 'I' ] and self.figures[location] != 'C'
  def can_travel_through_flying( self, location ):
    return self.contents[location] in [ ' ', 'T', 'H', 'D', 'O', 'I' ]
  def can_travel_through_teleport( self, location ):
    return self.contents[location] in [ ' ', 'X', 'T', 'H', 'D', 'O', 'I' ]

  def is_icy_standard( self, location ):
    return self.contents[location] == 'I'
  def is_icy_flying( self, location ):
    return False

  def is_trap_standard( self, location ):
    return self.contents[location] in [ 'T', 'H' ]
  def is_trap_flying( self, location ):
    return False

  def measure_proximity_through( self, location ):
    return self.contents[location] != 'X'

  def blocks_los( self, location ):
    return self.contents[location] == 'X'

  def additional_path_cost( self, location ):
    return int( self.contents[location] == 'D' )

  def setup_vertices_list( self ):
    def calculate_vertex( location, vertex ):
      hex_row = location % self.MAP_HEIGHT
      hex_column = location / self.MAP_HEIGHT

      vertex_column = hex_column + [ 1, 1, 0, 0, 0, 1 ][vertex]
      vertex_row = 2 * hex_row + [ 1, 2, 2, 1, 0, 0 ][vertex] + ( hex_column % 2 )

      x = 3 * ( vertex_column / 2 )
      if vertex_row % 2 == 0:
        x += 0.5 + vertex_column % 2
      else:
        x += 2.0 * ( vertex_column % 2 )

      y = SQRT_3_OVER_2 * vertex_row

      return ( x, y )

    self.vertices = [ 0 ] * ( self.MAP_SIZE * 6 )
    for location in range( self.MAP_SIZE ):
      for vertex in range( 6 ):
        self.vertices[location * 6 + vertex] = calculate_vertex( location, vertex )

  def get_vertex( self, location, vertex ):
    return self.vertices[location * 6 + vertex]

  def setup_neighbors_mapping( self ):
    def get_neighbors( location ):
      row = location % self.MAP_HEIGHT
      column = location / self.MAP_HEIGHT

      bottom_edge = row == 0
      top_edge = row == self.MAP_HEIGHT - 1
      left_edge = column == 0
      right_edge = column == self.MAP_WIDTH - 1
      base_column_value = ( column + 1 ) % 2
      base_column = base_column_value == 1

      neighbors = [ -1, -1, -1, -1, -1, -1 ]
      if not left_edge:
        if not bottom_edge or not base_column:
          neighbors[3] = location - self.MAP_HEIGHT - base_column_value
        if not top_edge or base_column:
          neighbors[2] = location - self.MAP_HEIGHT + 1 - base_column_value
      if not top_edge:
        neighbors[1] = location + 1
      if not right_edge:
        if not top_edge or base_column:
          neighbors[0] = location + self.MAP_HEIGHT + 1 - base_column_value
        if not bottom_edge or not base_column:
          neighbors[5] = location + self.MAP_HEIGHT - base_column_value
      if not bottom_edge:
        neighbors[4] = location - 1

      return neighbors

    self.neighbors = {
      _: get_neighbors( _ )
      for _ in range( self.MAP_SIZE )
    }

  def is_adjacent( self, location_a, location_b ):
    if location_b not in self.neighbors[location_a]:
      return False
    distances = self.find_proximity_distances( location_a, 2 )
    return distances[location_b] == 1

  def apply_rotated_aoe_offset( self, center, offset, rotation ):
    offset = rotate_offset( offset, rotation )
    return apply_offset( center, offset, self.MAP_HEIGHT, self.MAP_SIZE )

  def apply_aoe_offset( self, center, offset ):
    return apply_offset( center, offset, self.MAP_HEIGHT, self.MAP_SIZE )

  def calculate_bounds( self, location_a, location_b ):
    column_a = location_a / self.MAP_HEIGHT
    column_b = location_b / self.MAP_HEIGHT
    if column_a < column_b:
      column_lower = max( column_a - 1, 0 )
      column_upper = min( column_b + 2, self.MAP_WIDTH )
    else:
      column_lower = max( column_b - 1, 0 )
      column_upper = min( column_a + 2, self.MAP_WIDTH )

    row_a = location_a - column_a * self.MAP_HEIGHT
    row_b = location_b - column_b * self.MAP_HEIGHT
    if row_a < row_b:
      row_lower = max( row_a - 1, 0 )
      row_upper = min( row_b + 2, self.MAP_HEIGHT )
    else:
      row_lower = max( row_b - 1, 0 )
      row_upper = min( row_a + 2, self.MAP_HEIGHT )

    return ( row_lower, column_lower, row_upper, column_upper )

  def occluders_in( self, bounds ):
    for column in range( bounds[1], bounds[3] ):
      column_location = column * self.MAP_HEIGHT
      for row in range( bounds[0], bounds[2] ):
        location = column_location + row

        if self.blocks_los( location ):
          for vertex in range( 3 ):
            hex_edge_a = self.get_vertex( location, vertex )
            hex_edge_b = self.get_vertex( location, ( vertex + 3 ) % 6 )
            yield ( hex_edge_a, hex_edge_b )

        for edge in range( 3 ):
          if self.extra_walls[location][edge]:
            wall_vertex_a = self.get_vertex( location, edge )
            wall_vertex_b = self.get_vertex( location, ( edge + 1 ) % 6 )
            yield ( wall_vertex_a, wall_vertex_b )

  def walls_in( self, bounds ):
    for column in range( bounds[1], bounds[3] ):
      column_location = column * self.MAP_HEIGHT
      for row in range( bounds[0], bounds[2] ):
        location = column_location + row

        encoded_wall = 0
        for edge in range( 3 ):
          if self.extra_walls[location][edge]:
            encoded_wall += 1 << edge

        if self.blocks_los( location ):
          encoded_wall += 1 << 3

        if encoded_wall != 0:
          yield location, encoded_wall

  def test_line( self, bounds, vertex_position_a, vertex_position_b ):
    if vertex_position_a == vertex_position_b:
      return True
    for occluder in self.occluders_in( bounds ):
      if line_line_intersection( ( vertex_position_a, vertex_position_b ), occluder ):
        return False
    return True

  def determine_los_cross_section_edge( self, location_a, location_b ):
    hex_to_hex_direction = direction( ( self.get_vertex( location_a, 0 ), self.get_vertex( location_b, 0 ) ) )
    dot_with_up = hex_to_hex_direction[1]
    if dot_with_up > COS_30:
      return 0
    elif dot_with_up <= -COS_30:
      return 3
    else:
      cross_with_up = hex_to_hex_direction[0]
      if dot_with_up > 0.0:
        if cross_with_up < 0.0:
          return 1
        else:
          return 5
      else:
        if cross_with_up < 0.0:
          return 2
        else:
          return 4

  def calculate_occluder_mapping_set( self, location_a, location_b ):
    # determine the appropiate cross section to represent the hex volumes 
    cross_section_edge = self.determine_los_cross_section_edge( location_a, location_b )

    # setup quadrilateral bounding occluders
    source_vertex_0 = self.get_vertex( location_a, cross_section_edge )
    source_vertex_1 = self.get_vertex( location_a, ( cross_section_edge + 3 ) % 6 )
    target_vertex_0 = self.get_vertex( location_b, cross_section_edge )
    target_vertex_1 = self.get_vertex( location_b, ( cross_section_edge + 3 ) % 6 )
    edge_source = ( source_vertex_0, source_vertex_1 )
    edge_one = ( source_vertex_1, target_vertex_1 )
    edge_target = ( target_vertex_1, target_vertex_0 )
    edge_zero = ( target_vertex_0, source_vertex_0 )
    edge_direction_source = direction( edge_source )
    edge_direction_one = direction( edge_one )
    edge_direction_target = direction( edge_target )
    edge_direction_zero = direction( edge_zero )

    def calculate_occluder_mapping( point ):
      value_at_zero = occluder_target_intersection( ( source_vertex_0, point ), ( target_vertex_0, target_vertex_1 ) )
      value_at_one = occluder_target_intersection( ( source_vertex_1, point ), ( target_vertex_0, target_vertex_1 ) )
      return (
        value_at_zero,
        value_at_one,
        value_at_one - value_at_zero
      )

    occluder_mappings = [ ( 0.0, 0.0, 0.0 ), ( 1.0, 1.0, 0.0 ) ]
    occluder_mappings_below = []
    occluder_mappings_above = []
    occluder_mappings_internal = []
    for line in self.occluders_in( self.calculate_bounds( location_a, location_b ) ):
      # self.debug_lines.add( (1, line ) )

      if not within_bound( line[0], edge_source, edge_direction_source ) or not within_bound( line[0], edge_target, edge_direction_target ):
        if not within_bound( line[1], edge_source, edge_direction_source ) or not within_bound( line[1], edge_target, edge_direction_target ):
          continue

      if within_bound( line[0], edge_one, edge_direction_one ):
        if within_bound( line[0], edge_zero, edge_direction_zero ):
          status_a = VERTEX_INSIDE
        else:
          status_a = VERTEX_OUTSIDE_BOUND_ZERO
      else:
        status_a = VERTEX_OUTSIDE_BOUND_ONE
      if within_bound( line[1], edge_one, edge_direction_one ):
        if within_bound( line[1], edge_zero, edge_direction_zero ):
          status_b = VERTEX_INSIDE
        else:
          status_b = VERTEX_OUTSIDE_BOUND_ZERO
      else:
        status_b = VERTEX_OUTSIDE_BOUND_ONE
 
      if ( status_a == VERTEX_OUTSIDE_BOUND_ZERO and status_b == VERTEX_OUTSIDE_BOUND_ONE ) or ( status_a == VERTEX_OUTSIDE_BOUND_ONE and status_b == VERTEX_OUTSIDE_BOUND_ZERO ):
        return None

      elif status_a == VERTEX_INSIDE and status_b == VERTEX_OUTSIDE_BOUND_ZERO:
        mapping = calculate_occluder_mapping( line[0] )
        occluder_mappings_below.append( ( mapping, len( occluder_mappings ) ) )
        occluder_mappings.append( mapping )

      elif status_a == VERTEX_INSIDE and status_b == VERTEX_OUTSIDE_BOUND_ONE:
        mapping = calculate_occluder_mapping( line[0] )
        occluder_mappings_above.append( ( mapping, len( occluder_mappings ) ) )
        occluder_mappings.append( mapping )

      elif status_a == VERTEX_OUTSIDE_BOUND_ZERO and status_b == VERTEX_INSIDE:
        mapping = calculate_occluder_mapping( line[1] )
        occluder_mappings_below.append( ( mapping, len( occluder_mappings ) ) )
        occluder_mappings.append( mapping )

      elif status_a == VERTEX_OUTSIDE_BOUND_ONE and status_b == VERTEX_INSIDE:
        mapping = calculate_occluder_mapping( line[1] )
        occluder_mappings_above.append( ( mapping, len( occluder_mappings ) ) )
        occluder_mappings.append( mapping )

      elif status_a == VERTEX_INSIDE and status_b == VERTEX_INSIDE:
        mapping_0 = calculate_occluder_mapping( line[0] )
        mapping_1 = calculate_occluder_mapping( line[1] )
        occluder_mappings_internal.append( ( mapping_0, mapping_1, len( occluder_mappings ), len( occluder_mappings ) + 1 ) )
        occluder_mappings.append( mapping_0 )
        occluder_mappings.append( mapping_1 )

    return occluder_mappings, occluder_mappings_below, occluder_mappings_above, occluder_mappings_internal

  def plot_debug_visibility_graph( self, occluder_mapping_set ):
    (
      occluder_mappings,
      occluder_mappings_below,
      occluder_mappings_above,
      occluder_mappings_internal
    ) = occluder_mapping_set

    # the visibility windows are:
    # - below all blue lines
    # - above all purple lines
    # - below green and above red line pairs

    # upper bounds - blue
    self.debug_plot_line( 3, ( ( 0.0, 1.0 ), ( 1.0, 1.0 ) ) )
    for mapping, _ in occluder_mappings_above:
      self.debug_plot_line( 3, ( ( 0.0, mapping[0] ), ( 1.0, mapping[1] ) ) )

    # lower bounds - purple
    self.debug_plot_line( 0, ( ( 0.0, 0.0 ), ( 1.0, 0.0 ) ) )
    for mapping, _ in occluder_mappings_below:
      self.debug_plot_line( 0, ( ( 0.0, mapping[0] ), ( 1.0, mapping[1] ) ) )

    # top of internal occluder - red
    # bottom of internal occluder - green
    for mapping in occluder_mappings_internal:
      half_point = ( lerp( mapping[0][0], mapping[0][1], 0.5 ), lerp( mapping[1][0], mapping[1][1], 0.5 ) )

      value_0 = get_occluder_value_at( mapping[0], 0.0 )
      value_1 = get_occluder_value_at( mapping[1], 0.0 )
      color = ( 1, 2 ) if occluder_greater_than( value_0, value_1 ) else ( 2, 1 )
      self.debug_plot_line( color[0], ( ( 0.0, mapping[0][0] ), ( 0.5, half_point[0] ) ) )
      self.debug_plot_line( color[1], ( ( 0.0, mapping[1][0] ), ( 0.5, half_point[1] ) ) )

      value_0 = get_occluder_value_at( mapping[0], 1.0 )
      value_1 = get_occluder_value_at( mapping[1], 1.0 )
      color = ( 1, 2 ) if occluder_greater_than( value_0, value_1 ) else ( 2, 1 )
      self.debug_plot_line( color[0], ( ( 0.5, half_point[0] ), ( 1.0, mapping[0][1] ) ) )
      self.debug_plot_line( color[1], ( ( 0.5, half_point[1] ), ( 1.0, mapping[1][1] ) ) )

    # shade the graph to indicate visibility windows
    POINT_DENSITY = 40
    for nx in range( POINT_DENSITY ):
      x = nx / float( POINT_DENSITY - 1 )
      windows = get_visibility_windows_at( x, occluder_mapping_set, False )
      for ny in range( POINT_DENSITY ):
        y = ny / float( POINT_DENSITY - 1 )
        for window in windows:
          if y >= window[1] and y <= window[2]:
            color = 7
            break
        else:
          color = 6
        self.debug_plot_point( color, ( x, y ) )

  def calculate_symmetric_coordinates( self, origin, location ):
    column_a = origin / self.MAP_HEIGHT
    row_a = origin % self.MAP_HEIGHT
    column_b = location / self.MAP_HEIGHT
    row_b = location % self.MAP_HEIGHT

    c = column_b - column_a;
    r = row_b - row_a;
    q = column_a % 2

    if c == 0:
      if r > 0:
        t = 0
      else:
        t = 3
    elif c < 0:
      if r < ( q + c ) / 2:
        t = 3
      elif r < ( q - c ) / 2:
        t = 2
      else:
        t = 1
    else:
      if r <= ( q - c ) / 2:
        t = 4
      elif r <= ( q + c ) / 2:
        t = 5
      else:
        t = 0

    if t == 0:
      u = r - ( q - c ) / 2
      v = c
    elif t == 1:
      u = r - ( q + c ) / 2
      v = r - ( q - c ) / 2
    elif t == 2:
      u = -c
      v = r - ( q + c ) / 2
    elif t == 3:
      u = -r + ( q - c ) / 2
      v = -c
    elif t == 4:
      u = -r + ( q + c ) / 2
      v = -r + ( q - c ) / 2
    else:
      u = c
      v = -r + ( q + c ) / 2

    return t, u, v

  # can be used to implement a long-term collision cache
  # that is, a server-wide cache not cleared between scenarios
  # to do so, use FileSystemCache of flask_caching 
  # tested, but not in use do to size concerns
  # cache quickly grows to be many MB and has relatively unbounded size
  # gives ~24% speed up on standard (simple) senarios with long, blocking walls
  # gives ~10% speed up on 131 (complex unit test)
  # gives no speed up on many unit tests (as they have very few occluders)
  # the savings was measured with an in-memory cache (dictionary), not FileSystemCache, which may be slower
  # later idea: bound the cache size; first in, first out
  # should speed up results as your editing 
  def calculate_occluder_cache_key( self, location_a, location_b ):
    # does not take advantage of reflection symetry
    t, u, v = self.calculate_symmetric_coordinates( location_a, location_b )
    orientation = 6 - t
    cache_key = [ ( u, v ) ]

    for location, encoded_wall in self.walls_in( self.calculate_bounds( location_a, location_b ) ):
      t, u, v = self.calculate_symmetric_coordinates( location_a, location )
      t = ( t + orientation ) % 6
      cache_key.append( ( t, u, v, encoded_wall ) )

    if len( cache_key ) == 1:
      # no occluders; use None to short circuit los test in calling function
      return None

    cache_key.sort()
    return tuple( cache_key )

  def test_full_hex_los_between_locations( self, location_a, location_b ):
    # handle simple case of neighboring locations
    if location_b in self.neighbors[location_a]:
      edge = self.neighbors[location_a].index( location_b )
      if not self.effective_walls[location_a][edge]:
        return True
      neighbor_edge = ( edge + 3 ) % 6
      if not self.effective_walls[location_a][( edge + 1 ) % 6] and not self.effective_walls[location_b][( neighbor_edge + 5 ) % 6]:
        return True
      if not self.effective_walls[location_a][( edge + 5 ) % 6] and not self.effective_walls[location_b][( neighbor_edge + 1 ) % 6]:
        return True
      return False

    # A visibility test between two hexes can be simplified to a visibility test
    # between two lines. Any point on one line can potentially see any point on
    # the other line. That visibility space between the two lines can be mapped to
    # a unit square.

    # An occluder blocks visibility in an area bound on one side by a line cutting
    # through the square. Such lines are determined by how that occluder's end point
    # maps one line onto the other. Those are lines, not curves, when the two tested
    # lines are parallel.

    # Testing for visibility is equivalent to overlaying all blocked areas onto the
    # square, then testing if any unblocked regions remain.

    # find occluders and generate the lines that bound each occluder's blocked area
    occluder_mapping_set = self.calculate_occluder_mapping_set( location_a, location_b )
    if occluder_mapping_set is None:
      return False
    # at each line intersection, determine whether there is a visibility window
    for x in occluder_intersections( occluder_mapping_set[0] ):
      if get_visibility_windows_at( x, occluder_mapping_set, True ):
        return True

    # this logic can be used to prove that both cross_sections are not needed with
    # Gloomhaven's grid-locked occluders
    # https://www.reddit.com/r/Gloomhaven/comments/saevcj/comment/huedfq9/?utm_source=share&utm_medium=web2x&context=3
    # the third parameter to calculate_occluder_mapping_set is meant to return the
    # second-most perpendicular cross section
    # # for each cross section line
    # for cross_section in [ False, True ]:
    #   # find occluders and generate the lines that bound each occluder's blocked area
    #   occluder_mapping_set = self.calculate_occluder_mapping_set( location_a, location_b, cross_section )
    #   if occluder_mapping_set is None:
    #     continue
    #   # at each line intersection, determine whether there is a visibility window
    #   for x in occluder_intersections( occluder_mapping_set[0] ):
    #     if get_visibility_windows_at( x, occluder_mapping_set, True ):
    #       assert not cross_section
    #       return True

    return False

  def find_best_full_hex_los_sightline( self, location_a, location_b ):
    # Find the unblocked region in the visibility square with the largest area.
    # Place the sightline at its center of mass.

    # find occluders and generate the lines that bound each occluder's blocked area
    occluder_mapping_set = self.calculate_occluder_mapping_set( location_a, location_b )
    if occluder_mapping_set is None:
      return ( -1.0, -1.0 )
    occluder_mappings = occluder_mapping_set[0]

    # self.plot_debug_visibility_graph( occluder_mapping_set )

    # translate the occluder mappings (which are stored as the value of y at
    # x = 0 and x = 1) into 2d lines and include the x = 0 and x = 1 vertial
    # lines
    lines = []
    for occluder in occluder_mappings:
      line = ( ( 0.0, occluder[0] ), ( 1.0, occluder[1] ) )
      lines.append( ( line, direction( line ) ) )
    lines.append( ( ( ( 0.0, 0.0 ), ( 0.0, 1.0 ) ), ( 0.0, 1.0 ) ) )
    lines.append( ( ( ( 1.0, 0.0 ), ( 1.0, 1.0 ) ), ( 0.0, 1.0 ) ) )

    # loop over every window at every occluder mapping intersection
    window_polygons = []
    polygon_starts = []
    for x in occluder_intersections( occluder_mappings ):
      for window in get_visibility_windows_at( x, occluder_mapping_set, False ):
        # build a polygon around the open area
        polygon = map_window_polygon( window, polygon_starts, occluder_mappings, lines )
        if polygon is not None:
          window_polygons.append( calculate_polygon_properties( polygon ) )

    # place the sightline at the center of the polygon with the largest area
    _, ( x, y ) = max( window_polygons, key=lambda polygon: polygon[0] )
    # self.debug_plot_point( 4, ( x, y ) )

    # clip the sightline to the hex edges
    cross_section_edge = self.determine_los_cross_section_edge( location_a, location_b )
    source_vertex_0 = self.get_vertex( location_a, cross_section_edge )
    source_vertex_1 = self.get_vertex( location_a, ( cross_section_edge + 3 ) % 6 )
    target_vertex_0 = self.get_vertex( location_b, cross_section_edge )
    target_vertex_1 = self.get_vertex( location_b, ( cross_section_edge + 3 ) % 6 )
    edge_source = ( source_vertex_0, source_vertex_1 )
    edge_target = ( target_vertex_1, target_vertex_0 )
    start_point = lerp_along_line( edge_source, x )
    end_point = lerp_along_line( edge_target, 1.0 - y )
    for edge in [ cross_section_edge, ( cross_section_edge + 1 ) % 6, ( cross_section_edge + 2 ) % 6 ]:
      edge_line = ( self.get_vertex( location_a, edge ), self.get_vertex( location_a, ( edge + 1 ) % 6 ) )
      factor = line_hex_edge_intersection( ( start_point, end_point ), edge_line )
      if factor is not None:
        sightline_start = lerp_along_line( edge_line, factor )
        break
    for edge in [ ( cross_section_edge + 3 ) % 6, ( cross_section_edge + 4 ) % 6, ( cross_section_edge + 5 ) % 6 ]:
      edge_line = ( self.get_vertex( location_b, edge ), self.get_vertex( location_b, ( edge + 1 ) % 6 ) )
      factor = line_hex_edge_intersection( ( start_point, end_point ), edge_line )
      if factor is not None:
        sightline_end = lerp_along_line( edge_line, factor )
        break

    # edge_one = ( source_vertex_1, target_vertex_1 )
    # edge_zero = ( target_vertex_0, source_vertex_0 )
    # self.debug_lines.add( ( 2, edge_source ) )
    # self.debug_lines.add( ( 2, edge_one ) )
    # self.debug_lines.add( ( 2, edge_target ) )
    # self.debug_lines.add( ( 2, edge_zero ) )
    # N = 4
    # for n in range( N ):
    #   x = n / float( N - 1 )
    #   y, _ = get_occluder_value_at( occluder_mappings[2], x )
    #   self.debug_lines.add( ( 3, ( lerp_along_line( edge_source, x ), lerp_along_line( edge_target, 1.0 - y ) ) ) )

    return ( sightline_start, sightline_end )

  def vertex_at_wall( self, location, vertex ):
    if self.effective_walls[location][vertex]:
      return True
    if self.effective_walls[location][( vertex + 5 ) % 6]:
      return True
    if self.effective_walls[self.neighbors[location][vertex]][( vertex + 4 ) % 6]:
      return True
    return False

  def test_los_between_locations( self, location_a, location_b ):
    cache_key = visibility_cache_key( location_a, location_b )
    if cache_key in self.visibility_cache:
      return self.visibility_cache[cache_key]

    if not self.RULE_VERTEX_LOS:
      result = self.test_full_hex_los_between_locations( location_a, location_b )
    else:
      result = self.test_vertex_los_between_locations( location_a, location_b )

    self.visibility_cache[cache_key] = result
    return result

  def test_vertex_los_between_locations( self, location_a, location_b ):
    bounds = self.calculate_bounds( location_a, location_b )

    for vertex_a in range( 6 ):
      if self.vertex_at_wall( location_a, vertex_a ):
        continue 
      vertex_position_a = self.get_vertex( location_a, vertex_a )

      for vertex_b in range( 6 ):
        if self.vertex_at_wall( location_b, vertex_b ):
          continue 
        vertex_position_b = self.get_vertex( location_b, vertex_b )

        if self.test_line( bounds, vertex_position_a, vertex_position_b ):
          return True

    return False

  def find_shortest_sightline( self, location_a, location_b ):
    if not self.RULE_VERTEX_LOS:
      return self.find_best_full_hex_los_sightline( location_a, location_b )

    bounds = self.calculate_bounds( location_a, location_b )

    class v:
      shortest_length = float( 'inf' )
      shortest_line = None
    def consider_sightline( location_a, vertex_a, location_b, vertex_b ):
      length = calculate_distance( vertex_position_a, vertex_position_b )
      if length < v.shortest_length:
        if self.test_line( bounds, vertex_position_a, vertex_position_b ):
          v.shortest_length = length
          v.shortest_line = ( self.get_vertex( location_a, vertex_a ), self.get_vertex( location_b, vertex_b ) )

    for vertex_a in range( 6 ):
      if self.vertex_at_wall( location_a, vertex_a ):
        continue 
      vertex_position_a = self.get_vertex( location_a, vertex_a )

      for vertex_b in range( 6 ):
        if self.vertex_at_wall( location_b, vertex_b ):
          continue 
        vertex_position_b = self.get_vertex( location_b, vertex_b )

        consider_sightline( location_a, vertex_a, location_b, vertex_b )

    return v.shortest_line

  def pack_point( self, location, vertex ):
    if vertex == 2:
      if self.neighbors[location][2] != -1:
        location = self.neighbors[location][2]
        vertex = 0
    elif vertex == 3:
      if self.neighbors[location][3] != -1:
        location = self.neighbors[location][3]
        vertex = 1
      elif self.neighbors[location][2] != -1:
        location = self.neighbors[location][2]
        vertex = 5
    elif vertex == 4:
      if self.neighbors[location][3] != -1:
        location = self.neighbors[location][3]
        vertex = 0
      elif self.neighbors[location][4] != -1:
        location = self.neighbors[location][4]
        vertex = 2
    elif vertex == 5:
      if self.neighbors[location][4] != -1:
        location = self.neighbors[location][4]
        vertex = 1
    return self.dereduce_location( location ) * 6 + vertex

  def pack_line( self, location_a, vertex_a, location_b, vertex_b ):
    point_a = self.pack_point( location_a, vertex_a )
    point_b = self.pack_point( location_b, vertex_b )
    return point_a * self.MAP_VERTEX_COUNT + point_b

  def dereduce_location( self, location ):
    if not self.reduced:
      return location
    column = location / self.MAP_HEIGHT
    row = location % self.MAP_HEIGHT
    column += self.REDUCE_COLUMN
    row += self.REDUCE_ROW
    return row + column * self.ORIGINAL_MAP_HEIGHT

  def find_path_distances( self, start, traversal_test ):
    cache_key = ( start, traversal_test )
    if cache_key in self.path_cache[0]:
      return self.path_cache[0][cache_key]

    distances = [ MAX_VALUE ] * self.MAP_SIZE
    traps = [ MAX_VALUE ] * self.MAP_SIZE

    frontier = collections.deque()
    frontier.append( start )
    distances[start] = 0
    traps[start] = 0

    while not len( frontier ) == 0:
      current = frontier.popleft()
      distance = distances[current]
      trap = traps[current]
      for edge, neighbor in enumerate( self.neighbors[current] ):
        if neighbor == -1:
          continue
        if not traversal_test( self, neighbor ):
          continue
        if self.walls[current][edge]:
          continue

        slide = False
        while self.is_icy( self, neighbor ):
          slide = True
          next_neighbor = self.neighbors[neighbor][edge]
          if next_neighbor == -1:
            break
          if not traversal_test( self, next_neighbor ):
            break
          if self.figures[next_neighbor] == 'M':
            break
          elif self.walls[neighbor][edge]:
            break
          neighbor = next_neighbor

        neighbor_distance = distance + 1 + ( 0 if self.FLYING or self.JUMPING or self.TELEPORT or slide else self.additional_path_cost( neighbor ) )
        neighbor_trap = self.is_trap( self, neighbor ) + ( 0 if self.JUMPING or self.TELEPORT else trap )
        if ( neighbor_trap, neighbor_distance ) < ( traps[neighbor], distances[neighbor] ):
          frontier.append( neighbor )
          distances[neighbor] = neighbor_distance
          traps[neighbor] = neighbor_trap

    if self.RULE_DIFFICULT_TERRAIN_JUMP:
      if self.JUMPING and not self.TELEPORT:
        for location in range( self.MAP_SIZE ):
          distances[location] += self.additional_path_cost( location )
        distances[start] -= self.additional_path_cost( start )

    self.path_cache[0][cache_key] = ( distances, traps )
    return distances, traps

  def find_path_distances_reverse( self, destination, traversal_test ):
    # reverse in that we find the path distance to the destination from every location
    # path distance is symetric except for difficult terrain and traps
    # we correct for the asymetry of starting vs ending on difficult terrain
    # we correct for the asymetry of starting vs ending on traps
    distances, traps = self.find_path_distances( destination, traversal_test )
    distances = list( distances )
    traps = list( traps )
    if not self.FLYING:
      if not self.TELEPORT:
        if not self.JUMPING or self.RULE_DIFFICULT_TERRAIN_JUMP:
          destination_additional_path_cost = self.additional_path_cost( destination )
          if destination_additional_path_cost > 0:
            distances = [ _ + destination_additional_path_cost if _ != MAX_VALUE else _ for _ in distances ]
          for location in range( self.MAP_SIZE ):
            distances[location] -= self.additional_path_cost( location )

      if self.is_trap( self, destination ):
        traps = [ _ + 1 if _ != MAX_VALUE else _ for _ in traps ]
      for location in range( self.MAP_SIZE ):
        traps[location] -= int( self.is_trap( self, location ) )
    
    return distances, traps

  def find_path_distances_to_destination( self, destination, traversal_test ):
    cache_key = ( destination, traversal_test )
    if cache_key in self.path_cache[1]:
      return self.path_cache[1][cache_key]

    # optimization to share cache with find_path_distances
    # only valid when there is no icy terrain
    if not self.HAS_ICY_TERRAIN:
      distances, traps = self.find_path_distances_reverse( destination, traversal_test )
      self.path_cache[1][cache_key] = ( distances, traps )
      return distances, traps

    distances = [ MAX_VALUE ] * self.MAP_SIZE
    traps = [ MAX_VALUE ] * self.MAP_SIZE

    frontier = collections.deque()
    frontier.append( destination )

    distances[destination] = 0
    traps[destination] = 0
    if self.JUMPING or self.TELEPORT:
      if not self.TELEPORT and self.RULE_DIFFICULT_TERRAIN_JUMP:
        distances[destination] += self.additional_path_cost( destination )
      traps[destination] += int( self.is_trap( self, destination ) )

    while not len( frontier ) == 0:
      current = frontier.popleft()
      distance = distances[current]
      trap = traps[current]
      for edge, neighbor in enumerate( self.neighbors[current] ):
        if neighbor == -1:
          continue
        if not traversal_test( self, neighbor ):
          continue
        if self.walls[current][edge]:
          continue

        if self.is_icy( self, current ):
          opposite_edge = ( edge + 3 ) % 6
          opposite_neighbor = self.neighbors[current][opposite_edge]

          could_have_stopped_here = False
          if opposite_neighbor == -1:
            could_have_stopped_here = True
          elif not traversal_test( self, opposite_neighbor ):
            could_have_stopped_here = True
          elif self.figures[opposite_neighbor] == 'M':
            could_have_stopped_here = True
          elif self.walls[current][opposite_edge]:
            could_have_stopped_here = True
          if not could_have_stopped_here:
            continue

        slide = False
        prev_neighbor = current
        while True:
          neighbor_distance = distance + 1 + ( 0 if self.FLYING or self.JUMPING or self.TELEPORT or slide else self.additional_path_cost( current ) )
          neighbor_trap = trap + ( 0 if self.JUMPING or self.TELEPORT else self.is_trap( self, current ) )
          if ( neighbor_trap, neighbor_distance ) < ( traps[neighbor], distances[neighbor] ):
            frontier.append( neighbor )
            distances[neighbor] = neighbor_distance
            traps[neighbor] = neighbor_trap

          if not self.is_icy( self, neighbor ) or self.figures[prev_neighbor] == 'M':
            break
          slide = True
            
          next_neighbor = self.neighbors[neighbor][edge]
          if next_neighbor == -1:
            break
          if not traversal_test( self, next_neighbor ):
            break
          elif self.walls[neighbor][edge]:
            break
          prev_neighbor = neighbor
          neighbor = next_neighbor

    if self.JUMPING or self.TELEPORT:
      if not self.TELEPORT and self.RULE_DIFFICULT_TERRAIN_JUMP:
        distances[destination] -= self.additional_path_cost( destination )
      traps[destination] -= int( self.is_trap( self, destination ) )

    # # test against ground truth
    # gt_distances = [ MAX_VALUE ] * self.MAP_SIZE
    # gt_traps = [ MAX_VALUE ] * self.MAP_SIZE
    # for location in range( self.MAP_SIZE ):
    #   if traversal_test( self, location ):
    #     d, t = self.find_path_distances( location, traversal_test )
    #     gt_distances[location] = d[destination]
    #     gt_traps[location] = t[destination]
    # if distances != gt_distances:
    #   print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_numerical_label( _ ) for _ in distances ] )
    #   print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_numerical_label( _ ) for _ in gt_distances ] )
    # assert distances == gt_distances
    # assert traps == gt_traps

    self.path_cache[1][cache_key] = ( distances, traps )
    return distances, traps

  def find_proximity_distances( self, start, limit ):
    cache_key = ( start, limit )
    if cache_key in self.path_cache[2]:
      return self.path_cache[2][cache_key]

    distances = [ MAX_VALUE ] * self.MAP_SIZE

    frontier = collections.deque()
    frontier.append( start )
    distances[start] = 0

    while not len( frontier ) == 0:
      current = frontier.popleft()
      distance = distances[current]
      for edge, neighbor in enumerate( self.neighbors[current] ):
        if neighbor == -1:
          continue
        if not self.measure_proximity_through( neighbor ):
          continue
        if self.walls[current][edge]:
          continue
        neighbor_distance = distance + 1
        if neighbor_distance < distances[neighbor]:
          if neighbor_distance < limit:
            frontier.append( neighbor )
          distances[neighbor] = neighbor_distance

    self.path_cache[2][cache_key] = distances
    return distances

  def find_distances( self, start ):
    cache_key = ( start )
    if cache_key in self.path_cache[3]:
      return self.path_cache[3][cache_key]

    distances = [ MAX_VALUE ] * self.MAP_SIZE

    frontier = collections.deque()
    frontier.append( start )
    distances[start] = 0

    while not len( frontier ) == 0:
      current = frontier.popleft()
      distance = distances[current]
      for neighbor in self.neighbors[current]:
        if neighbor == -1:
          continue
        neighbor_distance = distance + 1
        if neighbor_distance < distances[neighbor]:
          frontier.append( neighbor )
          distances[neighbor] = neighbor_distance

    self.path_cache[3][cache_key] = distances
    return distances

  def calculate_monster_move( self ):
    # global start_time
    # global last_time
    # global perf_timers
    # start_time = last_time = time.time()

    assert not self.reduced

    if self.ACTION_RANGE == 0 or self.ACTION_TARGET == 0:
      ATTACK_RANGE = 1
      SUSCEPTIBLE_TO_DISADVANTAGE = False
    else:
      ATTACK_RANGE = self.ACTION_RANGE
      SUSCEPTIBLE_TO_DISADVANTAGE = not self.MUDDLED
    PLUS_TARGET = self.ACTION_TARGET - 1
    PLUS_TARGET_FOR_MOVEMENT = max( 0, PLUS_TARGET )
    ALL_TARGETS = self.ACTION_TARGET == 6

    AOE_ACTION = self.ACTION_TARGET > 0 and True in self.aoe
    AOE_MELEE = AOE_ACTION and self.ACTION_RANGE == 0

    if self.FLYING:
      self.can_end_move_on = Scenario.can_end_move_on_flying
      self.can_travel_through = Scenario.can_travel_through_flying
      self.is_icy = Scenario.is_icy_flying
      self.is_trap = Scenario.is_trap_flying
    elif self.JUMPING:
      self.can_end_move_on = Scenario.can_end_move_on_standard
      self.can_travel_through = Scenario.can_travel_through_flying
      self.is_icy = Scenario.is_icy_flying
      self.is_trap = Scenario.is_trap_standard
    else:
      self.can_end_move_on = Scenario.can_end_move_on_standard
      self.can_travel_through = Scenario.can_travel_through_standard
      self.is_icy = Scenario.is_icy_standard
      self.is_trap = Scenario.is_trap_standard
    if self.TELEPORT:
      self.can_travel_through = Scenario.can_travel_through_teleport
      self.is_icy = Scenario.is_icy_flying

    if self.logging:
      map_debug_tags = [ ' ' ] * self.MAP_SIZE
      print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_numerical_label( _ ) for _ in range( self.MAP_SIZE ) ] )
      if AOE_ACTION:
        false_contents = [ '   ' ] * self.AOE_SIZE
        if AOE_MELEE:
          false_contents[ self.AOE_CENTER ] = ' A '
        # print_map( self, self.AOE_WIDTH, self.AOE_HEIGHT, [ [ False ] * 6 ] * self.AOE_SIZE, false_contents, [ format_aoe( _ ) for _ in self.aoe ] )
      # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_initiative( _ ) for _ in self.initiatives ] )

      out = ''
      if self.FROST_RULES:
        out += ', FROSTHAVEN'
      if self.GLOOM_RULES:
        out += ', GLOOMHAVEN'
      if self.JOTL_RULES:
        out += ', JAWS OF THE LION'
      if self.ACTION_MOVE > 0 :
        out += ', MOVE %i' % self.ACTION_MOVE
      if self.ACTION_RANGE > 0 and self.ACTION_TARGET > 0:
        out += ', RANGE %i' % self.ACTION_RANGE
      if self.ACTION_TARGET > 0:
        out += ', ATTACK'
      if AOE_ACTION:
        out += ', AOE'
      if PLUS_TARGET > 0:
        if ALL_TARGETS:
          out += ', TARGET ALL'
        else:
          out += ', +TARGET %i' % PLUS_TARGET
      if self.FLYING:
        out += ', FLYING'
      elif self.JUMPING:
        out += ', JUMPING'
      if self.MUDDLED:
        out += ', MUDDLED'
      # out += ', DEBUG_TOGGLE = %s' % ( 'TRUE' if self.DEBUG_TOGGLE else 'FALSE' )
      if out == '':
        out = 'NO ACTION'
      else:
        out = out[2:]
      print out
      if self.message:
        print textwrap.fill( self.message, 82 )

    actions = set()
    aoes = {}
    destinations = {}
    focus_map = {}

    # find active monster
    active_monster = self.figures.index( 'A' )
    travel_distances, trap_counts = self.find_path_distances( active_monster, self.can_travel_through )
    proximity_distances = self.find_proximity_distances( active_monster, MAX_VALUE )
    # rev_travel_distances, rev_trap_counts = self.find_path_distances_to_destination( active_monster, self.can_travel_through )
    # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_numerical_label( _ ) for _ in trap_counts ] )
    # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_numerical_label( _ ) for _ in travel_distances ] )
    # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_numerical_label( _ ) for _ in proximity_distances ] )
    # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_numerical_label( _ ) for _ in rev_travel_distances ] )

    # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_numerical_label( self.calculate_symmetric_coordinates( active_monster, _ )[0] ) for _ in range( self.MAP_SIZE ) ] )
    # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_numerical_label( self.calculate_symmetric_coordinates( active_monster, _ )[1] ) for _ in range( self.MAP_SIZE ) ] )
    # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_numerical_label( self.calculate_symmetric_coordinates( active_monster, _ )[2] ) for _ in range( self.MAP_SIZE ) ] )
    # _ = [ self.calculate_symmetric_coordinates( active_monster, _ ) for _ in range( self.MAP_SIZE ) ]

    # doesn't speed things up but makes los testing order more intuitive for debugging
    travel_distance_sorted_map = sorted( range( self.MAP_SIZE ), key=lambda x: travel_distances[x] )

    # process aoe
    if AOE_ACTION:
      center_location = self.AOE_CENTER if AOE_MELEE else self.aoe.index( True )
      aoe = [
        get_offset( center_location, location, self.AOE_HEIGHT )
        for location in range( self.AOE_SIZE ) if self.aoe[location]
      ]

    # precalculate aoe patterns to remove degenerate cases
    if AOE_ACTION and not AOE_MELEE:
      PRECALC_GRID_HEIGHT = 21
      PRECALC_GRID_WIDTH = 21
      PRECALC_GRID_SIZE = PRECALC_GRID_HEIGHT * PRECALC_GRID_WIDTH
      PRECALC_GRID_CENTER = ( PRECALC_GRID_SIZE - 1 ) / 2

      aoe_pattern_set = set()
      for aoe_pin in aoe:
        for aoe_rotation in range( 12 ):
          aoe_hexes = []
          for aoe_offset in aoe:
            aoe_offset = pin_offset( aoe_offset, aoe_pin )
            aoe_offset = rotate_offset( aoe_offset, aoe_rotation )
            location = apply_offset( PRECALC_GRID_CENTER, aoe_offset, PRECALC_GRID_HEIGHT, PRECALC_GRID_SIZE )
            aoe_hexes.append( location )
          aoe_hexes.sort()
          aoe_pattern_set.add( tuple( aoe_hexes ) )

      aoe_pattern_list = [
        [
          get_offset( PRECALC_GRID_CENTER, location, PRECALC_GRID_HEIGHT )
          for location in aoe
        ]
        for aoe in aoe_pattern_set
      ]

    # find characters
    characters = [ _ for _, figure in enumerate( self.figures ) if figure == 'C' ]

    # _ = time.time()
    # perf_timers['0 setup'] = _ - last_time
    # last_time = _

    # find monster focuses

    if not len( characters ):
      focuses = set()

    else:
      class s:
        focuses = set()
        shortest_path = (
          MAX_VALUE - 1, # traps to attack potential focus
          MAX_VALUE - 1, # distance to attack potential focus
          MAX_VALUE - 1, # proximity of potential focus
          MAX_VALUE - 1, # initiative of potential focus
        )
      def consider_focus():
        this_path = (
          trap_counts[location],
          travel_distances[location],
          0 if self.RULE_PROXIMITY_FOCUS else proximity_distances[character],
          self.initiatives[character],
        )
        if this_path == s.shortest_path:
          if self.test_los_between_locations( character, location ):
            s.focuses.add( character )
        if this_path < s.shortest_path:
          if self.test_los_between_locations( character, location ):
            s.shortest_path = this_path
            s.focuses = { character }

      for character in characters:
        range_to_character = self.find_proximity_distances( character, ATTACK_RANGE )
        # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( _ ) for _ in self.contents ], [ format_numerical_label( _ ) for _ in range_to_character ] )

        for location in travel_distance_sorted_map:
        # for location in range( self.MAP_SIZE ):

          # early test of location using the first two elements of the minimized tuple
          if trap_counts[location] > s.shortest_path[0]:
            continue
          if trap_counts[location] == s.shortest_path[0]:
            if travel_distances[location] > s.shortest_path[1]:
              continue

          def inner():
            if self.can_end_move_on( self, location ):
              if not AOE_ACTION or PLUS_TARGET > 0:
                if range_to_character[location] <= ATTACK_RANGE:
                  consider_focus()
                  return
              if AOE_ACTION:
                if AOE_MELEE:
                  for aoe_rotation in range( 12 ):
                    for aoe_offset in aoe:
                      if character == self.apply_rotated_aoe_offset( location, aoe_offset, aoe_rotation ):
                        consider_focus()
                        return
                else:
                  distances = self.find_proximity_distances( location, ATTACK_RANGE )
                  for aoe_pattern in aoe_pattern_list:
                    for aoe_offset in aoe_pattern:
                      target = self.apply_aoe_offset( character, aoe_offset )
                      if target:
                        if distances[target] <= ATTACK_RANGE:
                          consider_focus()
                          return

          inner()

      focuses = s.focuses
      can_attack_focus = s.shortest_path[1] <= self.ACTION_MOVE
      heed_only_focus = not self.RULE_MAXIMIZE_FUTURE_MULTIATTACK and not can_attack_focus

      # rank characters for secondary targeting
      focus_ranks = {}
      if self.RULE_RANK_SECONDARY_TARGETS:
        sorted_infos = sorted(
          ( ( 0 if self.RULE_PROXIMITY_FOCUS else proximity_distances[_], self.initiatives[_] ), _ )
          for _ in characters
        )
        best_info = sorted_infos[0][0]
        rank = 0
        for info, character in sorted_infos:
          if info != best_info:
            rank += 1
            best_info = info
          focus_ranks[character] = rank
        num_focus_ranks = rank + 1
      else:
        for character in characters:
          focus_ranks[character] = 0
        num_focus_ranks = 1

    # _ = time.time()
    # perf_timers['1 focus'] = _ - last_time
    # last_time = _

    # players choose among focus ties
    for focus in focuses:

      if heed_only_focus:
        heeded_characters = [ focus ]
      else:
        heeded_characters = characters

      # find the best group of targets based on the following priorities

      class t:
        groups = set()
        TRAP_COUNT_INDEX = 0
        CAN_REACH_INDEX = 1
        DISADVANTAGE_AGAINST_FOCUS_INDEX = 2
        TARGET_COUNT_INDEX = 3 if self.RULE_PRIORITIZE_FOCUS_DISADVANTAGE else 2
        if self.RULE_PRIORITIZE_FOCUS_DISADVANTAGE:
          best_group = (
            MAX_VALUE - 1, # traps to the attack location
            0,             # can reach the attack location
            1,             # disadvantage against the focus
            0,             # total number of targets
            MAX_VALUE - 1, # path length to the attack location
          ) + tuple( [ 0 ] * num_focus_ranks ) # target count for each focus rank
        else:
          best_group = (
            MAX_VALUE - 1, # traps to the attack location
            0,             # can reach the attack location
            0,             # total number of targets
            MAX_VALUE - 1, # number of targts with disadvantage
            MAX_VALUE - 1, # path length to the attack location
          ) + tuple( [ 0 ] * num_focus_ranks ) # target count for each focus rank
      def consider_group( num_targets, preexisting_targets, preexisting_targets_of_rank, preexisting_targets_disadvantage ):
        available_targets = targetable_characters - set( preexisting_targets )
        max_num_targets = min( num_targets, len( available_targets ) ) if not ALL_TARGETS else len( available_targets )

        # loop over every possible set of potential targets
        for target_set in itertools.combinations( available_targets, max_num_targets ):
          targets = preexisting_targets + list( target_set )

          # only consider actions that hit the focus
          if not focus in targets:
            continue

          targets_of_rank = list( preexisting_targets_of_rank )
          for target in target_set:
            targets_of_rank[focus_ranks[target]] += 1

          if self.RULE_PRIORITIZE_FOCUS_DISADVANTAGE:
            this_group = (
              trap_counts[location],
              -can_reach_location,
              int( has_disadvantage_against_focus ),
              -len( targets ),
              travel_distances[location],
            ) + tuple( -_ for _ in targets_of_rank )
          else:
            targets_disadvantage = preexisting_targets_disadvantage
            if SUSCEPTIBLE_TO_DISADVANTAGE:
              for target in target_set:
                targets_disadvantage += int( self.is_adjacent( location, target ) )
            this_group = (
              trap_counts[location],
              -can_reach_location,
              -len( targets ),
              targets_disadvantage,
              travel_distances[location],
            ) + tuple( -_ for _ in targets_of_rank )

          # print location, this_group, t.best_group
          if this_group == t.best_group:
            group = tuple( sorted( targets ) )
            t.groups.add( group )
          elif this_group < t.best_group:
            group = tuple( sorted( targets ) )
            t.best_group = this_group
            t.groups = { group }
          # print t.groups

      for location in range( self.MAP_SIZE ):
        if self.can_end_move_on( self, location ):
          can_reach_location = travel_distances[location] <= self.ACTION_MOVE

          # early test of location using the first two elements of the minimized tuple
          if trap_counts[location] > t.best_group[t.TRAP_COUNT_INDEX]:
            continue
          if trap_counts[location] == t.best_group[t.TRAP_COUNT_INDEX]:
            if not can_reach_location and t.best_group[t.CAN_REACH_INDEX] == -1:
              continue

          has_disadvantage_against_focus = SUSCEPTIBLE_TO_DISADVANTAGE and self.is_adjacent( location, focus )

          # determine the set of characters attackable by non-AoE attacks
          range_to_location = self.find_proximity_distances( location, ATTACK_RANGE )
          targetable_characters = {
            _
            for _ in heeded_characters
            if range_to_location[_] <= ATTACK_RANGE and self.test_los_between_locations( _, location )
          }

          if not AOE_ACTION:
            if focus not in targetable_characters:
              continue
            # add non-AoE targets and consider resulting actions
            consider_group( 1 + PLUS_TARGET_FOR_MOVEMENT, [], [ 0 ] * num_focus_ranks, 0 )

          elif AOE_MELEE:
            # loop over every possible aoe placement
            for aoe_rotation in range( 12 ):
              aoe_targets = []
              aoe_targets_of_rank = [ 0 ] * num_focus_ranks
              aoe_targets_disadvantage = 0

              # loop over each hex in the aoe, adding targets
              for aoe_offset in aoe:
                target = self.apply_rotated_aoe_offset( location, aoe_offset, aoe_rotation )
                if target in heeded_characters:
                  if self.test_los_between_locations( target, location ):
                    aoe_targets.append( target )
                    aoe_targets_of_rank[focus_ranks[target]] += 1
                    aoe_targets_disadvantage += int( SUSCEPTIBLE_TO_DISADVANTAGE and self.is_adjacent( location, target ) )

              # add non-AoE targets and consider result
              if aoe_targets:
                consider_group( PLUS_TARGET, aoe_targets, aoe_targets_of_rank, aoe_targets_disadvantage )

          else:
            # loop over all aoe placements that hit characters
            distances = self.find_proximity_distances( location, ATTACK_RANGE )
            for aoe_location in heeded_characters:
              for aoe_pattern in aoe_pattern_list:
                aoe_targets = []
                aoe_targets_of_rank = [ 0 ] * num_focus_ranks
                aoe_targets_disadvantage = 0

                # loop over each hex in the aoe, adding targets
                in_range = False
                for aoe_offset in aoe_pattern:
                  target = self.apply_aoe_offset( aoe_location, aoe_offset )
                  if target:
                    if distances[target] <= ATTACK_RANGE:
                      in_range = True
                    if target in heeded_characters:
                      if self.test_los_between_locations( target, location ):
                        aoe_targets.append( target )
                        aoe_targets_of_rank[focus_ranks[target]] += 1
                        aoe_targets_disadvantage += int( SUSCEPTIBLE_TO_DISADVANTAGE and self.is_adjacent( location, target ) )

                # add non-AoE targets and consider result
                if in_range:
                  if aoe_targets:
                    consider_group( PLUS_TARGET, aoe_targets, aoe_targets_of_rank, aoe_targets_disadvantage )

      # _ = time.time()
      # perf_timers['2 target group'] = _ - last_time
      # last_time = _

      # given the target group, find the best destinations to attack from
      # based on the following priorities

      # optimization: Frosthaven rules do not require the following separate minimization step.
      # Instead, the locations can be found in above minimization and used directly.

      class u:
        destinations = set()
        aoes = {}
        best_destination = (
          MAX_VALUE - 1, # number of targts with disadvantage
          MAX_VALUE - 1, # path length to the destination
        )
      def consider_destination( num_targets, preexisting_targets, preexisting_targets_of_rank, preexisting_targets_disadvantage, aoe_hexes ):
        available_targets = targetable_characters - set( preexisting_targets )
        max_num_targets = min( num_targets, len( available_targets ) ) if not ALL_TARGETS else len( available_targets )

        # if its impossible to attack a group as big as a chosen target group
        if len( preexisting_targets ) + max_num_targets != -t.best_group[t.TARGET_COUNT_INDEX]:
          return

        # loop over every possible set of potential targets
        for target_set in itertools.combinations( available_targets, max_num_targets ):
          targets = preexisting_targets + list( target_set )

          # if this target group does not match any chosen group
          group = tuple( sorted( targets ) )
          if not group in t.groups:
            continue

          targets_disadvantage = preexisting_targets_disadvantage
          if SUSCEPTIBLE_TO_DISADVANTAGE:
            for target in target_set:
              targets_disadvantage += int( self.is_adjacent( location, target ) )

          this_destination = (
            targets_disadvantage,
            travel_distances[location],
          )

          if this_destination == u.best_destination:
            action = ( location, ) + group
            u.destinations.add( action )
            u.aoes[action] = aoe_hexes
          elif this_destination < u.best_destination:
            action = ( location, ) + group
            u.best_destination = this_destination
            u.destinations = { action }
            u.aoes = { action: aoe_hexes }
          # print action, this_destination, u.best_destination
          # print u.destinations

      for location in range( self.MAP_SIZE ):
        if self.can_end_move_on( self, location ):

          # early test of location using the first two elements of the minimized tuple

          if trap_counts[location] != t.best_group[t.TRAP_COUNT_INDEX]:
            continue

          can_reach_location = travel_distances[location] <= self.ACTION_MOVE
          if -can_reach_location != t.best_group[t.CAN_REACH_INDEX]:
            continue

          if self.RULE_PRIORITIZE_FOCUS_DISADVANTAGE:
            has_disadvantage_against_focus = SUSCEPTIBLE_TO_DISADVANTAGE and self.is_adjacent( location, focus )
            if int( has_disadvantage_against_focus ) != t.best_group[t.DISADVANTAGE_AGAINST_FOCUS_INDEX]:
              continue 

          # determine the set of characters attackable by non-AoE attacks
          range_to_location = self.find_proximity_distances( location, ATTACK_RANGE )
          targetable_characters = {
            _
            for _ in heeded_characters
            if range_to_location[_] <= ATTACK_RANGE and self.test_los_between_locations( _, location )
          }

          if not AOE_ACTION:
            if focus not in targetable_characters:
              continue
            # add non-AoE targets and consider resulting actions
            consider_destination( 1 + PLUS_TARGET_FOR_MOVEMENT, [], [ 0 ] * num_focus_ranks, 0, [] )

          elif AOE_MELEE:
            # loop over every possible aoe placement
            for aoe_rotation in range( 12 ):
              aoe_targets = []
              aoe_targets_of_rank = [ 0 ] * num_focus_ranks
              aoe_targets_disadvantage = 0
              aoe_hexes = []

              # loop over each hex in the aoe, adding targets
              for aoe_offset in aoe:
                target = self.apply_rotated_aoe_offset( location, aoe_offset, aoe_rotation )
                aoe_hexes.append( target )
                if target in heeded_characters:
                  if self.test_los_between_locations( target, location ):
                    aoe_targets.append( target )
                    aoe_targets_of_rank[focus_ranks[target]] += 1
                    aoe_targets_disadvantage += int( SUSCEPTIBLE_TO_DISADVANTAGE and self.is_adjacent( location, target ) )

              # add non-AoE targets and consider result
              if aoe_targets:
                consider_destination( PLUS_TARGET, aoe_targets, aoe_targets_of_rank, aoe_targets_disadvantage, aoe_hexes )

          else:
            # loop over all aoe placements that hit characters
            distances = self.find_proximity_distances( location, ATTACK_RANGE )
            for aoe_location in heeded_characters:
              for aoe_pattern in aoe_pattern_list:
                aoe_targets = []
                aoe_targets_of_rank = [ 0 ] * num_focus_ranks
                aoe_targets_disadvantage = 0
                aoe_hexes = []

                # loop over each hex in the aoe, adding targets
                in_range = False
                for aoe_offset in aoe_pattern:
                  target = self.apply_aoe_offset( aoe_location, aoe_offset )
                  if target:
                    if distances[target] <= ATTACK_RANGE:
                      in_range = True
                    aoe_hexes.append( target )
                    if target in heeded_characters:
                      if self.test_los_between_locations( target, location ):
                        aoe_targets.append( target )
                        aoe_targets_of_rank[focus_ranks[target]] += 1
                        aoe_targets_disadvantage += int( SUSCEPTIBLE_TO_DISADVANTAGE and self.is_adjacent( location, target ) )

                # add non-AoE targets and consider result
                if in_range:
                  if aoe_targets:
                    consider_destination( PLUS_TARGET, aoe_targets, aoe_targets_of_rank, aoe_targets_disadvantage, aoe_hexes )

      # determine the best move based on the chosen destinations

      can_reach_destinations = t.best_group[1] == -1
      assert can_reach_destinations == can_attack_focus
      if can_reach_destinations:
        if PLUS_TARGET >= 0:
          actions_for_this_focus = u.destinations
          aoes_for_this_focus = u.aoes
        else:
          actions_for_this_focus = [ ( _[0], ) for _ in u.destinations ]
          aoes_for_this_focus = { _: [] for _ in actions_for_this_focus }
        destinations_for_this_focus = { _: { _[0] } for _ in actions_for_this_focus }
      else:
        actions_for_this_focus = []
        destinations_for_this_focus = {}
        for destination in u.destinations:
          actions_for_this_destination = []
          best_move = (
            MAX_VALUE - 1, # traps to destination and along travel
            MAX_VALUE - 1, # distance to destination
            MAX_VALUE - 1, # travel distance
          )
          distance_to_destination, traps_to_destination = self.find_path_distances_to_destination( destination[0], self.can_travel_through )
          for location in range( self.MAP_SIZE ):
            if travel_distances[location] <= self.ACTION_MOVE:
              if self.can_end_move_on( self, location ):
                this_move = (
                  traps_to_destination[location] + trap_counts[location],
                  distance_to_destination[location],
                  travel_distances[location],
                )
                if this_move == best_move:
                  actions_for_this_destination.append( ( location, ) )
                elif this_move < best_move:
                  best_move = this_move
                  actions_for_this_destination = [ ( location, ) ]
                # print ( location, ), this_move, best_move
                # print actions_for_this_destination

          actions_for_this_focus += actions_for_this_destination

          for action in actions_for_this_destination:
            if action in destinations_for_this_focus:
              destinations_for_this_focus[action].add( destination[0] )
            else:
              destinations_for_this_focus[action] = { destination[0] }

        aoes_for_this_focus = { _: [] for _ in actions_for_this_focus }

      actions_for_this_focus = set( actions_for_this_focus )
      actions |= actions_for_this_focus
      aoes.update( aoes_for_this_focus )
      for action in actions_for_this_focus:
        if action in destinations:
          destinations[action] |= destinations_for_this_focus[action]
        else:
          destinations[action] = destinations_for_this_focus[action]
        if action in focus_map:
          focus_map[action].add( focus )
        else:
          focus_map[action] = { focus }

      # _ = time.time()
      # perf_timers['3 destination group'] = _ - last_time
      # last_time = _

    # if we find no actions, stand still
    if not actions:
      action = ( active_monster, )
      actions.add( action )
      aoes[action] = []
      destinations[action] = {}
      focus_map[action] = {}

    # calculate sightlines for visualization
    sightlines = {}
    debug_lines = {}
    for action in actions:
      sightlines[action] = set()
      if action[1:]:
        for attack in action[1:]:
          sightlines[action].add( self.find_shortest_sightline( action[0], attack ) )

      debug_lines[action] = self.debug_lines
      self.debug_lines = set()

    # move monster
    if self.logging:
      self.figures[active_monster] = ' '
      map_debug_tags[active_monster] = 's'
      if not self.show_each_action_separately:
        for action in actions:
          self.figures[action[0]] = 'A'
          for destination in destinations[action]:
            map_debug_tags[destination] = 'd'
          for target in action[1:]:
            map_debug_tags[target] = 'a'
        # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_initiative( _ ) for _ in self.initiatives ], map_debug_tags )
      else:
        for action in actions:
          figures = list( self.figures )
          action_debug_tags = list( map_debug_tags )
          figures[action[0]] = 'A'
          for destination in destinations[action]:
            action_debug_tags[destination] = 'd'
          for target in action[1:]:
            action_debug_tags[target] = 'a'
          # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( figures, self.contents ) ], [ format_initiative( _ ) for _ in self.initiatives ], action_debug_tags )

    # _ = time.time()
    # perf_timers['4 finalize'] = _ - last_time
    # perf_timers['total'] = _ - start_time

    # total = perf_timers['total'] * 10000.0
    # if total > 1:
    #   keys = perf_timers.keys()
    #   keys.sort()
    #   for key in keys:
    #     if key != 'total':
    #       print '[%20s] %7i (%i%%)' % ( key, perf_timers[key] * 10000, 100 * perf_timers[key] * 10000 / total )
    #   print '[%20s] %7i' % ( 'total', perf_timers['total'] * 10000 )

    return actions, aoes, destinations, focus_map, sightlines, debug_lines

  def solve_reach( self, monster ):
    if self.ACTION_TARGET == 0:
      return []
    if self.ACTION_RANGE == 0:
      ATTACK_RANGE = 1
    else:
      ATTACK_RANGE = self.ACTION_RANGE

    distances = self.find_proximity_distances( monster, ATTACK_RANGE )

    reach = []
    run_begin = None
    for location in range( self.MAP_SIZE ):
      has_reach = False
      if distances[location] <= ATTACK_RANGE:
        if not self.blocks_los( location ):
          if location != monster:
            if self.test_los_between_locations( monster, location ):
              has_reach = True
      if has_reach:
        if run_begin == None:
          run_begin = location
      elif run_begin != None:
        reach.append( ( run_begin, location ) )
        run_begin = None
    if run_begin != None:
      reach.append( ( run_begin, self.MAP_SIZE ) )
    return reach

  def solve_sight( self, monster ):
    sight = []
    run_begin = None
    for location in range( self.MAP_SIZE ):
      has_sight = False
      if not self.blocks_los( location ):
        if location != monster:
          if self.test_los_between_locations( monster, location ):
            has_sight = True
      if has_sight:
        if run_begin == None:
          run_begin = location
      elif run_begin != None:
        sight.append( ( run_begin, location ) )
        run_begin = None
    if run_begin != None:
      sight.append( ( run_begin, self.MAP_SIZE ) )
    return sight

  def solve_move( self, test ):
    if self.logging:
      # export to scenario
      # to create using client, set GRID_HEIGHT to 7
      print '#######################################'
      for index, ( figure, initiative ) in enumerate( zip( self.figures, self.initiatives ) ):
        if figure != ' ':
          print '    s.figures[%r] = %r' % ( index, figure )
          if initiative != 0:
            print '    s.initiatives[%r] = %r' % ( index, initiative )
      print
      for index, content in enumerate( self.contents ):
        if content != ' ':
          print '    s.contents[%r] = %r' % ( index, content )
      for index, walls in enumerate( self.walls ):
        for edge in range( 3 ):
          if walls[edge]:
            print '    s.walls[%r][%r] = %r' % ( index, edge, walls[edge] )
      if True in self.aoe:
        print
        for index, aoe in enumerate( self.aoe ):
          if aoe:
            print '    s.aoe[%r] = True' % index
      print
      print '    s.ACTION_MOVE = %r' % self.ACTION_MOVE
      if self.ACTION_RANGE != 0:
        print '    s.ACTION_RANGE = %r' % self.ACTION_RANGE
      if self.ACTION_TARGET != 1:
        print '    s.ACTION_TARGET = %r' % self.ACTION_TARGET
      if self.FLYING:
        print '    s.FLYING = %r' % self.FLYING
      if self.JUMPING:
        print '    s.JUMPING = %r' % self.JUMPING
      if self.TELEPORT:
        print '    s.TELEPORT = %r' % self.TELEPORT
      if self.MUDDLED:
        print '    s.MUDDLED = %r' % self.MUDDLED
      print '#######################################'

    start_location = self.figures.index( 'A' )

    raw_actions, aoes, destinations, focuses, sightlines, debug_lines = self.calculate_monster_move()

    def dereduce_locations( locations ):
      return [ self.dereduce_location( _ ) for _ in locations ]

    actions = [
      {
        'move': self.dereduce_location( _[0] ),
        'attacks': dereduce_locations( _[1:] ),
        'aoe': dereduce_locations( aoes[_] ),
        'destinations': dereduce_locations( destinations[_] ),
        'focuses': dereduce_locations( focuses[_] ),
        'sightlines': list( sightlines[_] ),
      }
      for _ in raw_actions
    ]
    if self.debug_visuals:
      for _, raw_action in enumerate( raw_actions ):
        actions[_]['debug_lines'] = list( debug_lines[raw_action] )

    if self.logging:
      print '%i option(s):' % len( actions )
      for action in actions:
        if action['move'] == self.dereduce_location( start_location ):
          out = '- no movement'
        else:
          out = '- move to %i' % action['move']
        if action['attacks']:
          for attack in action['attacks']:
            out += ', attack %i' % attack
        print out

    return actions

  def solve_reaches( self, viewpoints ):
    return [ self.solve_reach( _ ) for _ in viewpoints ]

  def solve_sights( self, viewpoints ):
    return [ self.solve_sight( _ ) for _ in viewpoints ]

  def solve( self, solve_reach, solve_sight ):
    actions = self.solve_move( False )
    reach = self.solve_reaches( _['move'] for _ in actions ) if solve_reach else None
    sight = self.solve_sights( _['move'] for _ in actions ) if solve_sight else None
    return actions, reach, sight

  def debug_plot_line( self, color, line ):
    self.debug_lines.add( ( color, ( scale_vector( DEBUG_PLOT_SCALE, line[0] ), scale_vector( DEBUG_PLOT_SCALE, line[1] ) ) ) )
  def debug_plot_point( self, color, point ):
    self.debug_lines.add( ( color, ( scale_vector( DEBUG_PLOT_SCALE, point ), ) ) )

def perform_unit_tests( starting_scenario ):
  print 'performing unit tests...'

  failed_scenarios = []

  scenario_index = starting_scenario - 1
  rules = 0
  while True:
    scenario_index += 1
    scenario = Scenario()
    scenarios.init_from_test_scenario( scenario, scenario_index, rules )
    if not scenario.valid:
      if rules == 2:
        break
      rules += 1
      scenario_index = starting_scenario - 1
      continue

    # map reduction is not yet used in deployed solver
    # scenario.reduce_map()

    if not scenario.correct_answer:
      print 'test %3i: no answer listed' % scenario_index
      continue

    answers, _, _, _, _, _ = scenario.calculate_monster_move()
    answers = set(
      tuple( scenario.dereduce_location( _ ) for _ in _ )
      for _ in answers
    )
    if answers == scenario.correct_answer:
      result = 'pass'
    else:
      failed_scenarios.append( ( rules, scenario_index ) )
      result = 'fail'
    print 'test %s-%3i: %s' % ( [ 'F', 'G', 'J' ][rules], scenario_index, result )

  print
  if len( failed_scenarios ) == 0:
    print 'passed all tests'
  else:
    print 'failed %i test(s):' % len( failed_scenarios )
    for rules, scenario in failed_scenarios:
      rule_text = [ 'Frosthaven', 'Gloomhaven', 'Jaws of the Lion' ][rules]
      print '  %s - %i' % ( rule_text, scenario )