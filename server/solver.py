import sys, collections, textwrap, itertools, pprint
import scenarios
from utils import *
from settings import *
from print_map import *

class Scenario:
  def __init__( self ):
    self.correct_answer = None
    self.valid = True
    self.logging = False
    self.show_each_action_separately = False

    self.visibility_cache = {}
    self.path_cache = [ {}, {}, {}, {} ]

  def reduce_map( self ):
    self.reduced = True
    # print self.effective_walls
    # if hasattr( self, 'effective_walls' ):
    #   exit(-1)

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
      for a in range( 0, 6 )
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
    for i in range( 0, 6 ):
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
    for i in range( 0, 6 ):
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

    self.effective_walls = [ 0 ] * self.MAP_SIZE
    for location in range( 0, self.MAP_SIZE ):
      if self.contents[location] == 'X':
        self.effective_walls[location] = [ True ] * 6
      else:
        self.effective_walls[location] = list( self.walls[location] )

    for location in range( 0, self.MAP_SIZE ):
      neighbors = self.neighbors[location]
      for edge in range( 0, 6 ):
        if neighbors[edge] != -1:
          neighbor_edge = ( edge + 3 ) % 6
          if self.walls[location][edge]:
            self.walls[neighbors[edge]][neighbor_edge] = True
          if self.effective_walls[location][edge]:
            self.effective_walls[neighbors[edge]][neighbor_edge] = True

  def unpack_scenario( self, packed_scenario ):
    self.ACTION_MOVE = int( packed_scenario['move'] )
    self.ACTION_RANGE = int( packed_scenario['range'] )
    self.ACTION_TARGET = int( packed_scenario['target'] )
    self.JUMPING = int( packed_scenario['flying'] ) == 1
    self.FLYING = int( packed_scenario['flying'] ) == 2
    self.TELEPORTING = int( packed_scenario['flying'] ) == 3
    self.MUDDLED = int( packed_scenario['muddled'] ) == 1

    def get_index( column, row ):
      index = column * self.MAP_HEIGHT + row
      return index
    def add_elements( grid, key, content ):
      for _ in packed_scenario['map'][key]:
        grid[_] = content

    add_elements( self.contents, 'walls', 'X' )
    add_elements( self.contents, 'obstacles', 'O' )
    add_elements( self.contents, 'traps', 'T' )
    add_elements( self.contents, 'hazardous', 'H' )
    add_elements( self.contents, 'difficult', 'D' )
    add_elements( self.figures, 'characters', 'C' )
    add_elements( self.figures, 'monsters', 'M' )

    active_figure_location = packed_scenario['active_figure']
    switch_factions = self.figures[active_figure_location] == 'C'
    self.figures[active_figure_location] = 'A'

    if switch_factions:
      for _ in range( 0, self.MAP_SIZE ):
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

    def get_index( column, row ):
      index = column * self.MAP_HEIGHT + row
      return index
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
    return self.contents[location] in [ ' ', 'T', 'H', 'D' ] and self.figures[location] in [ ' ', 'A' ]
  def can_end_move_on_flying( self, location ):
    return self.contents[location] in [ ' ', 'T', 'O', 'H', 'D' ] and self.figures[location] in [ ' ', 'A' ]

  def can_travel_through_standard( self, location ):
    return self.contents[location] in [ ' ', 'T', 'H', 'D' ] and self.figures[location] != 'C'
  def can_travel_through_flying( self, location ):
    return self.contents[location] in [ ' ', 'T', 'H', 'D', 'O' ]
  def can_travel_through_teleporting( self, location ):
    return self.contents[location] in [ ' ', 'X', 'T', 'H', 'D', 'O' ]

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
    for location in range( 0, self.MAP_SIZE ):
      for vertex in range( 0, 6 ):
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
      for _ in range( 0, self.MAP_SIZE )
    }

  def is_adjacent( self, location_a, location_b ):
    if location_b not in self.neighbors[location_a]:
      return False
    distances = self.find_proximity_distances( location_a )
    return distances[location_b] == 1

  def apply_rotated_aoe_offset( self, center, offset, rotation ):
    offset = rotate_offset( offset, rotation )
    return apply_offset( center, offset, self.MAP_HEIGHT, self.MAP_SIZE )

  def apply_aoe_offset( self, center, offset ):
    return apply_offset( center, offset, self.MAP_HEIGHT, self.MAP_SIZE )

  def line_hex_intersection( self, delta, location ):
    for vertex in range( 0, 3 ):
      hex_edge_a = self.get_vertex( location, vertex )
      hex_edge_b = self.get_vertex( location, ( vertex + 3 ) % 6 )
      if line_line_intersection( delta, ( hex_edge_a, hex_edge_b ) ):
        return True
    return False

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

  def bounding_locations( self, bounds ):
    for column in range( bounds[1], bounds[3] ):
      column_location = column * self.MAP_HEIGHT
      for row in range( bounds[0], bounds[2] ):
        yield column_location + row

  def test_line( self, bounds, vertex_position_a, vertex_position_b ):
    if vertex_position_a == vertex_position_b:
      return True
    for location in self.bounding_locations( bounds ):
      if self.blocks_los( location ):
        if self.line_hex_intersection( ( vertex_position_a, vertex_position_b ), location ):
          return False
      else:
        for edge in range( 0, 6 ):
          if self.walls[location][edge]:
            wall_vertex_a = self.get_vertex( location, edge )
            wall_vertex_b = self.get_vertex( location, ( edge + 1 ) % 6 )
            if line_line_intersection( ( vertex_position_a, vertex_position_b ), ( wall_vertex_a, wall_vertex_b ) ):
              return False
    return True

  def vertex_blocked( self, location, vertex ):
    return self.effective_walls[location][vertex] or self.effective_walls[location][( vertex + 5 ) % 6]

  def test_los_between_locations( self, location_a, location_b ):
    cache_key = visibility_cache_key( location_a, location_b )
    if cache_key in self.visibility_cache:
      return self.visibility_cache[cache_key]

    bounds = self.calculate_bounds( location_a, location_b )

    for vertex_a in range( 0, 6 ):
      if self.vertex_blocked( location_a, vertex_a ):
        continue 
      vertex_position_a = self.get_vertex( location_a, vertex_a )

      for vertex_b in range( 0, 6 ):
        if self.vertex_blocked( location_b, vertex_b ):
          continue 
        vertex_position_b = self.get_vertex( location_b, vertex_b )

        if self.test_line( bounds, vertex_position_a, vertex_position_b ):
          self.visibility_cache[cache_key] = True
          return True

    self.visibility_cache[cache_key] = False
    return False

  def find_shortest_sightline( self, location_a, location_b ):
    bounds = self.calculate_bounds( location_a, location_b )

    shortest_length = float( 'inf' )
    shortest_line = None

    for vertex_a in range( 0, 6 ):
      if self.vertex_blocked( location_a, vertex_a ):
        continue
      vertex_position_a = self.get_vertex( location_a, vertex_a )

      for vertex_b in range( 0, 6 ):
        if self.vertex_blocked( location_b, vertex_b ):
          continue
        vertex_position_b = self.get_vertex( location_b, vertex_b )

        length = calculate_distance( vertex_position_a, vertex_position_b )
        if length < shortest_length:

          if self.test_line( bounds, vertex_position_a, vertex_position_b ):
            shortest_length = length
            shortest_line = self.pack_line( location_a, vertex_a, location_b, vertex_b )

    return shortest_line

  def determine_obstruction( self, location_a, location_b ):
    lines = []
    blocked_points = []
    clear_points = []

    for vertex_b in range( 0, 6 ):
      if self.vertex_blocked( location_b, vertex_b ):
        blocked_points.append( self.pack_point( location_b, vertex_b ) )
      else:
        clear_points.append( self.pack_point( location_b, vertex_b ) )

    bounds = self.calculate_bounds( location_a, location_b )

    for vertex_a in range( 0, 6 ):
      if self.vertex_blocked( location_a, vertex_a ):
        continue
      vertex_position_a = self.get_vertex( location_a, vertex_a )

      for vertex_b in range( 0, 6 ):
        if self.vertex_blocked( location_b, vertex_b ):
          continue
        vertex_position_b = self.get_vertex( location_b, vertex_b )

        if not self.test_line( bounds, vertex_position_a, vertex_position_b ):
          lines.append( self.pack_line( location_a, vertex_a, location_b, vertex_b ) )

    return lines, blocked_points, clear_points

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
      neighbors = self.neighbors[current]
      for edge in range( 0, 6 ):
        neighbor = neighbors[edge]
        if neighbor == -1:
          continue
        if not traversal_test( self, neighbor ):
          continue
        if self.walls[current][edge]:
          continue
        neighbor_distance = distance + 1 + int( not self.FLYING and not self.JUMPING and not self.TELEPORTING and self.additional_path_cost( neighbor ) )
        neighbor_trap = int( not self.JUMPING and not self.TELEPORTING ) * trap + int( self.is_trap( self, neighbor ) )
        if is_pair_less_than( neighbor_trap, traps[neighbor], neighbor_distance, distances[neighbor] ):
          frontier.append( neighbor )
          distances[neighbor] = neighbor_distance
          traps[neighbor] = neighbor_trap

    if self.JUMPING:
      for location in range( 0, self.MAP_SIZE ):
        distances[location] += self.additional_path_cost( location )
      distances[start] -= self.additional_path_cost( start )

    self.path_cache[0][cache_key] = ( distances, traps )
    return distances, traps

  def find_path_distances_reverse( self, destination, traversal_test ):
    # reverse in that we find the path distance to the start from every location
    # path distance is symetric except for difficult terrain
    # we correct for the asymetry of starting vs ending on difficult terrain
    # we correct for the asymetry of starting vs ending on traps
    cache_key = ( destination, traversal_test )
    if cache_key in self.path_cache[1]:
      return self.path_cache[1][cache_key]

    distances, traps = self.find_path_distances( destination, traversal_test )
    distances = list( distances )
    traps = list( traps )
    if not self.FLYING and not self.TELEPORTING:
      destination_additional_path_cost = self.additional_path_cost( destination )
      if destination_additional_path_cost > 0:
        distances = [ _ != MAX_VALUE and _ + destination_additional_path_cost or _ for _ in distances ]
      if self.is_trap( self, destination ):
        traps = [ _ != MAX_VALUE and _ + 1 or _ for _ in traps ]
      for location in range( 0, self.MAP_SIZE ):
        distances[location] -= self.additional_path_cost( location )
        traps[location] -= int( self.is_trap( self, location ) )
    
    self.path_cache[1][cache_key] = ( distances, traps )
    return distances, traps

  def find_proximity_distances( self, start ):
    cache_key = ( start )
    if cache_key in self.path_cache[2]:
      return self.path_cache[2][cache_key]

    distances = [ MAX_VALUE ] * self.MAP_SIZE

    frontier = collections.deque()
    frontier.append( start )
    distances[start] = 0

    while not len( frontier ) == 0:
      current = frontier.popleft()
      distance = distances[current]
      neighbors = self.neighbors[current]
      for edge in range( 0, 6 ):
        neighbor = neighbors[edge]
        if neighbor == -1:
          continue
        if not self.measure_proximity_through( neighbor ):
          continue
        if self.walls[current][edge]:
          continue
        neighbor_distance = distance + 1
        if neighbor_distance < distances[neighbor]:
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
      neighbors = self.neighbors[current]
      for edge in range( 0, 6 ):
        neighbor = neighbors[edge]
        if neighbor == -1:
          continue
        neighbor_distance = distance + 1
        if neighbor_distance < distances[neighbor]:
          frontier.append( neighbor )
          distances[neighbor] = neighbor_distance

    self.path_cache[3][cache_key] = distances
    return distances

  def calculate_monster_move( self ):
    if self.ACTION_RANGE == 0 or self.ACTION_TARGET == 0:
      ATTACK_RANGE = 1
      SUSCEPTIBLE_TO_DISADVANTAGE = False
    else:
      ATTACK_RANGE = self.ACTION_RANGE
      SUSCEPTIBLE_TO_DISADVANTAGE = not self.MUDDLED
    PLUS_TARGET = self.ACTION_TARGET - 1
    PLUS_TARGET_FOR_MOVEMENT = max( 0, PLUS_TARGET )

    AOE_ACTION = self.ACTION_TARGET > 0 and True in self.aoe
    AOE_MELEE = AOE_ACTION and self.ACTION_RANGE == 0

    if self.FLYING:
      self.can_end_move_on = Scenario.can_end_move_on_flying
      self.can_travel_through = Scenario.can_travel_through_flying
      self.is_trap = Scenario.is_trap_flying
    elif self.JUMPING:
      self.can_end_move_on = Scenario.can_end_move_on_standard
      self.can_travel_through = Scenario.can_travel_through_flying
      self.is_trap = Scenario.is_trap_standard
    elif self.TELEPORTING:
      self.can_end_move_on = Scenario.can_end_move_on_standard
      self.can_travel_through = Scenario.can_travel_through_teleporting
      self.is_trap = Scenario.is_trap_standard
    else:
      self.can_end_move_on = Scenario.can_end_move_on_standard
      self.can_travel_through = Scenario.can_travel_through_standard
      self.is_trap = Scenario.is_trap_standard

    if self.logging:
      map_debug_tags = [ ' ' ] * self.MAP_SIZE
      print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_numerical_label( _ ) for _ in range( 0, self.MAP_SIZE ) ] )
      if AOE_ACTION:
        false_contents = [ '   ' ] * self.AOE_SIZE
        if AOE_MELEE:
          false_contents[ self.AOE_CENTER ] = ' A '
        print_map( self, self.AOE_WIDTH, self.AOE_HEIGHT, [ [ False ] * 6 ] * self.AOE_SIZE, false_contents, [ format_aoe( _ ) for _ in self.aoe ] )
      print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_initiative( _ ) for _ in self.initiatives ] )

      out = ''
      if self.ACTION_MOVE > 0 :
        out += ', MOVE %i' % self.ACTION_MOVE
      if self.ACTION_RANGE > 0 and self.ACTION_TARGET > 0:
        out += ', RANGE %i' % self.ACTION_RANGE
      if self.ACTION_TARGET > 0:
        out += ', ATTACK'
      if AOE_ACTION:
        out += ', AOE'
      if PLUS_TARGET > 0:
        out += ', +TARGET %i' % PLUS_TARGET
      if self.FLYING:
        out += ', FLYING'
      elif self.JUMPING:
        out += ', JUMPING'
      elif self.TELEPORTING:
        out += ', TELEPORTING'
      if self.MUDDLED:
        out += ', MUDDLED'
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
    proximity_distances = self.find_proximity_distances( active_monster )
    asdf, dd = self.find_path_distances_reverse( active_monster, self.can_travel_through )
    # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_numerical_label( _ ) for _ in trap_counts ] )
    # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_numerical_label( _ ) for _ in travel_distances ] )
    # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_numerical_label( _ ) for _ in proximity_distances ] )
    # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_numerical_label( _ ) for _ in asdf ] )
    # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_numerical_label( _ ) for _ in dd ] )
    # process aoe
    if AOE_ACTION:
      center_location = self.AOE_CENTER if AOE_MELEE else self.aoe.index( True )
      aoe = [
        get_offset( center_location, location, self.AOE_HEIGHT )
        for location in range( 0, self.AOE_SIZE ) if self.aoe[location]
      ]

    # precalculate aoe patterns to remove degenerate cases
    if AOE_ACTION and not AOE_MELEE:
      PRECALC_GRID_HEIGHT = 21
      PRECALC_GRID_WIDTH = 21
      PRECALC_GRID_SIZE = PRECALC_GRID_HEIGHT * PRECALC_GRID_WIDTH
      PRECALC_GRID_CENTER = ( PRECALC_GRID_SIZE - 1 ) / 2

      aoe_pattern_set = set()
      for aoe_pin in aoe:
        for aoe_rotation in range( 0, 12 ):
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
          proximity_distances[character],
          self.initiatives[character],
        )
        if is_tuple_equal( this_path, s.shortest_path ):
          if self.test_los_between_locations( character, location ):
            s.focuses.add( character )
        if is_tuple_less_than( this_path, s.shortest_path ):
          if self.test_los_between_locations( character, location ):
            s.shortest_path = this_path
            s.focuses = { character }

      for character in characters:
        range_to_character = self.find_proximity_distances( character )
        # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( _ ) for _ in self.contents ], [ format_numerical_label( _ ) for _ in range_to_character ] )

        for location in range( 0, self.MAP_SIZE ):

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
                  for aoe_rotation in range( 0, 12 ):
                    for aoe_offset in aoe:
                      if character == self.apply_rotated_aoe_offset( location, aoe_offset, aoe_rotation ):
                        consider_focus()
                        return
                else:
                  distances = self.find_proximity_distances( location )
                  for aoe_pattern in aoe_pattern_list:
                    for aoe_offset in aoe_pattern:
                      target = self.apply_aoe_offset( character, aoe_offset )
                      if target:
                        if distances[target] <= ATTACK_RANGE:
                          consider_focus()
                          return

          inner()

      focuses = s.focuses

      # rank characters for secondary targeting
      focus_ranks = {}
      sorted_infos = sorted(
        ( ( proximity_distances[_], self.initiatives[_] ), _ )
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

    # players choose among focus ties
    for focus in focuses:

      # find the best group of targets based on the following priorities

      class t:
        groups = set()
        best_group = (
          MAX_VALUE - 1, # traps to the attack location
          0,             # can reach the attack location
          1,             # disadvantage against the focus
          0,             # total number of targets
          MAX_VALUE - 1, # path length to the attack location
        ) + tuple( [ 0 ] * num_focus_ranks ) # target count for each focus rank
      def consider_group( num_targets, preexisting_targets, preexisting_targets_of_rank, preexisting_targets_disadvantage, aoe_hexes ):
        available_targets = targetable_characters - set( preexisting_targets )
        max_num_targets = min( num_targets, len( available_targets ) )

        # loop over every possible set of potential targets
        for target_set in itertools.combinations( available_targets, max_num_targets ):
          targets = preexisting_targets + list( target_set )

          # only consider actions that hit the focus
          if not focus in targets:
            continue

          targets_of_rank = list( preexisting_targets_of_rank )
          for target in target_set:
            targets_of_rank[focus_ranks[target]] += 1

          this_group = (
            trap_counts[location],
            -can_reach_location,
            int( has_disadvantage_against_focus ),
            -len( targets ),
            travel_distances[location],
          ) + tuple( -_ for _ in targets_of_rank )

          # print location, this_group, t.best_group
          if is_tuple_equal( this_group, t.best_group ):
            group = tuple( sorted( targets ) )
            t.groups.add( group )
          elif is_tuple_less_than( this_group, t.best_group ):
            group = tuple( sorted( targets ) )
            t.best_group = this_group
            t.groups = { group }
          # print t.groups

      for location in range( 0, self.MAP_SIZE ):
        if self.can_end_move_on( self, location ):
          can_reach_location = travel_distances[location] <= self.ACTION_MOVE

          # early test of location using the first two elements of the minimized tuple
          if trap_counts[location] > t.best_group[0]:
            continue
          if trap_counts[location] == t.best_group[0]:
            if not can_reach_location and t.best_group[1] == -1:
              continue

          has_disadvantage_against_focus = SUSCEPTIBLE_TO_DISADVANTAGE and self.is_adjacent( location, focus )

          # determine the set of characters attackable by non-AoE attacks
          range_to_location = self.find_proximity_distances( location )
          targetable_characters = {
            _
            for _ in characters
            if range_to_location[_] <= ATTACK_RANGE and self.test_los_between_locations( _, location )
          }

          if not AOE_ACTION:
            # add non-AoE targets and consider resulting actions
            consider_group( 1 + PLUS_TARGET_FOR_MOVEMENT, [], [ 0 ] * num_focus_ranks, 0, [] )

          elif AOE_MELEE:
            # loop over every possible aoe placement
            for aoe_rotation in range( 0, 12 ):
              aoe_targets = []
              aoe_targets_of_rank = [ 0 ] * num_focus_ranks
              aoe_targets_disadvantage = 0
              aoe_hexes = []

              # loop over each hex in the aoe, adding targets
              for aoe_offset in aoe:
                target = self.apply_rotated_aoe_offset( location, aoe_offset, aoe_rotation )
                aoe_hexes.append( target )
                if target in characters:
                  if self.test_los_between_locations( target, location ):
                    aoe_targets.append( target )
                    aoe_targets_of_rank[focus_ranks[target]] += 1
                    aoe_targets_disadvantage += int( SUSCEPTIBLE_TO_DISADVANTAGE and self.is_adjacent( location, target ) )

              # add non-AoE targets and consider result
              if aoe_targets:
                consider_group( PLUS_TARGET, aoe_targets, aoe_targets_of_rank, aoe_targets_disadvantage, aoe_hexes )

          else:
            # loop over all aoe placements that hit characters
            distances = self.find_proximity_distances( location )
            for aoe_location in characters:
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
                    if target in characters:
                      if self.test_los_between_locations( target, location ):
                        aoe_targets.append( target )
                        aoe_targets_of_rank[focus_ranks[target]] += 1
                        aoe_targets_disadvantage += int( SUSCEPTIBLE_TO_DISADVANTAGE and self.is_adjacent( location, target ) )

                # add non-AoE targets and consider result
                if in_range:
                  if aoe_targets:
                    consider_group( PLUS_TARGET, aoe_targets, aoe_targets_of_rank, aoe_targets_disadvantage, aoe_hexes )

      # given the target group, find the best destinations to attack from
      # based on the following priorities

      class u:
        destinations = set()
        aoes = {}
        best_destination = (
          MAX_VALUE - 1, # number of targts with disadvantage
          MAX_VALUE - 1, # path length to the destination
        )
      def consider_destination( num_targets, preexisting_targets, preexisting_targets_of_rank, preexisting_targets_disadvantage, aoe_hexes ):
        available_targets = targetable_characters - set( preexisting_targets )
        max_num_targets = min( num_targets, len( available_targets ) )

        # if its impossible to attack a group as big as a chosen target group
        if len( preexisting_targets ) + max_num_targets != -t.best_group[3]:
          return

        # loop over every possible set of potential targets
        for target_set in itertools.combinations( available_targets, max_num_targets ):
          targets = preexisting_targets + list( target_set )

          # if this target group does not match any chosen group
          group = tuple( sorted( targets ) )
          if not group in t.groups:
            continue

          targets_disadvantage = preexisting_targets_disadvantage
          for target in target_set:
            targets_disadvantage += int( SUSCEPTIBLE_TO_DISADVANTAGE and self.is_adjacent( location, target ) )

          this_destination = (
            targets_disadvantage,
            travel_distances[location],
          )

          if is_tuple_equal( this_destination, u.best_destination ):
            action = ( location, ) + group
            u.destinations.add( action )
            u.aoes[action] = aoe_hexes
          elif is_tuple_less_than( this_destination, u.best_destination ):
            action = ( location, ) + group
            u.best_destination = this_destination
            u.destinations = { action }
            u.aoes = { action: aoe_hexes }
          # print action, this_destination, u.best_destination
          # print u.destinations

      for location in range( 0, self.MAP_SIZE ):
        if self.can_end_move_on( self, location ):

          # early test of location using the first two elements of the minimized tuple

          if trap_counts[location] != t.best_group[0]:
            continue

          can_reach_location = travel_distances[location] <= self.ACTION_MOVE
          if -can_reach_location != t.best_group[1]:
            continue

          has_disadvantage_against_focus = SUSCEPTIBLE_TO_DISADVANTAGE and self.is_adjacent( location, focus )
          if int( has_disadvantage_against_focus ) != t.best_group[2]:
            continue 

          # determine the set of characters attackable by non-AoE attacks
          range_to_location = self.find_proximity_distances( location )
          targetable_characters = {
            _
            for _ in characters
            if range_to_location[_] <= ATTACK_RANGE and self.test_los_between_locations( _, location )
          }

          if not AOE_ACTION:
            # add non-AoE targets and consider resulting actions
            consider_destination( 1 + PLUS_TARGET_FOR_MOVEMENT, [], [ 0 ] * num_focus_ranks, 0, [] )

          elif AOE_MELEE:
            # loop over every possible aoe placement
            for aoe_rotation in range( 0, 12 ):
              aoe_targets = []
              aoe_targets_of_rank = [ 0 ] * num_focus_ranks
              aoe_targets_disadvantage = 0
              aoe_hexes = []

              # loop over each hex in the aoe, adding targets
              for aoe_offset in aoe:
                target = self.apply_rotated_aoe_offset( location, aoe_offset, aoe_rotation )
                aoe_hexes.append( target )
                if target in characters:
                  if self.test_los_between_locations( target, location ):
                    aoe_targets.append( target )
                    aoe_targets_of_rank[focus_ranks[target]] += 1
                    aoe_targets_disadvantage += int( SUSCEPTIBLE_TO_DISADVANTAGE and self.is_adjacent( location, target ) )

              # add non-AoE targets and consider result
              if aoe_targets:
                consider_destination( PLUS_TARGET, aoe_targets, aoe_targets_of_rank, aoe_targets_disadvantage, aoe_hexes )

          else:
            # loop over all aoe placements that hit characters
            distances = self.find_proximity_distances( location )
            for aoe_location in characters:
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
                    if target in characters:
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
            MAX_VALUE - 1, # traps to destination
            MAX_VALUE - 1, # ???
            MAX_VALUE - 1, # distance to destination
            MAX_VALUE - 1, # travel distance
          )
          distance_to_destination, traps_to_destination = self.find_path_distances_reverse( destination[0], self.can_travel_through )
          for location in range( 0, self.MAP_SIZE ):
            if travel_distances[location] <= self.ACTION_MOVE:
              if self.can_end_move_on( self, location ):
                this_move = (
                  traps_to_destination[location],
                  trap_counts[location],
                  distance_to_destination[location],
                  travel_distances[location],
                )
                if is_tuple_equal( this_move, best_move ):
                  actions_for_this_destination.append( ( location, ) )
                elif is_tuple_less_than( this_move, best_move ):
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

    # if we find no actions, stand still
    if not actions:
      action = ( active_monster, )
      actions.add( action )
      aoes[action] = []
      destinations[action] = {}
      focus_map[action] = {}

    # calculate sightlines or obstructions for visualization
    sightlines = {}
    obstruction_lines = {}
    obstruction_blocked_points = {}
    obstruction_clear_points = {}
    for action in actions:
      sightlines[action] = set()
      obstruction_lines[action] = set()
      obstruction_blocked_points[action] = set()
      obstruction_clear_points[action] = set()

      if action[1:]:
        for attack in action[1:]:
          sightlines[action].add( self.find_shortest_sightline( action[0], attack ) )
      else:
        if focus_map[action]:
          def add_obstruction( focus ):
            lines, blocked_points, clear_points = self.determine_obstruction( action[0], focus )
            obstruction_lines[action].update( lines )
            obstruction_blocked_points[action].update( blocked_points )
            obstruction_clear_points[action].update( clear_points )

          any_focus_in_range = False
          for focus in focus_map[action]:
            if not AOE_ACTION:
              distances = self.find_distances( action[0] )
              if distances[focus] <= ATTACK_RANGE:
                add_obstruction( focus )
                any_focus_in_range = True
            elif AOE_MELEE:
              for aoe_rotation in range( 0, 12 ):
                for aoe_offset in aoe:
                  target = self.apply_rotated_aoe_offset( action[0], aoe_offset, aoe_rotation )
                  if target == focus:
                    add_obstruction( focus )
                    any_focus_in_range = True
                    break
                else:
                  continue
                break
            else:
              proximity_distances = self.find_proximity_distances( action[0] )
              for aoe_pattern in aoe_pattern_list:
                for aoe_offset in aoe_pattern:
                  target = self.apply_aoe_offset( focus, aoe_offset )
                  if target:
                    if proximity_distances[target] <= ATTACK_RANGE:
                      add_obstruction( focus )
                      any_focus_in_range = True
                      break
                else:
                  continue
                break

          if any_focus_in_range:
            for vertex in range( 0, 6 ):
              if self.vertex_blocked( action[0], vertex ):
                obstruction_blocked_points[action].add( self.pack_point( action[0], vertex ) )
              else:
                obstruction_clear_points[action].add( self.pack_point( action[0], vertex ) )

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
        print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_initiative( _ ) for _ in self.initiatives ], map_debug_tags )
      else:
        for action in actions:
          figures = list( self.figures )
          action_debug_tags = list( map_debug_tags )
          figures[action[0]] = 'A'
          for destination in destinations[action]:
            action_debug_tags[destination] = 'd'
          for target in action[1:]:
            action_debug_tags[target] = 'a'
          print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( figures, self.contents ) ], [ format_initiative( _ ) for _ in self.initiatives ], action_debug_tags )

    return actions, aoes, destinations, focus_map, sightlines, obstruction_lines, obstruction_blocked_points, obstruction_clear_points

  def solve_reach( self, monster ):
    if self.ACTION_TARGET == 0:
      return []
    if self.ACTION_RANGE == 0:
      ATTACK_RANGE = 1
    else:
      ATTACK_RANGE = self.ACTION_RANGE

    distances = self.find_proximity_distances( monster )

    reach = []
    run_begin = None
    for location in range( 0, self.MAP_SIZE ):
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
    for location in range( 0, self.MAP_SIZE ):
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
    start_location = self.figures.index( 'A' )

    raw_actions, aoes, destinations, focuses, sightlines, obstruction_lines, obstruction_blocked_points, obstruction_clear_points = self.calculate_monster_move()

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
        'obstruction_lines': list( obstruction_lines[_] ),
        'obstruction_clear_points': list( obstruction_clear_points[_] ),
        'obstruction_blocked_points': list( obstruction_blocked_points[_] ),
      }
      for _ in raw_actions
    ]
    # actions = [
    #   {
    #     'move': _[0],
    #     'attacks': _[1:],
    #     'aoe': aoes[_],
    #     'destinations': list( destinations[_] ),
    #     'focuses': list( focuses[_] ),
    #     'sightlines': list( sightlines[_] ),
    #     'obstruction_lines': list( obstruction_lines[_] ),
    #     'obstruction_clear_points': list( obstruction_clear_points[_] ),
    #     'obstruction_blocked_points': list( obstruction_blocked_points[_] ),
    #   }
    #   for _ in raw_actions
    # ]

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
    reach = solve_reach and self.solve_reaches( _['move'] for _ in actions ) or None
    sight = solve_sight and self.solve_sights( _['move'] for _ in actions ) or None
    return actions, reach, sight

def perform_unit_tests( starting_scenario ):
  print 'performing unit tests...'

  failures = 0
  scenario_index = starting_scenario - 1
  while True:
    scenario_index += 1
    scenario = Scenario()
    scenarios.init_from_test_scenario( scenario, scenario_index )
    if not scenario.valid:
      break
    scenario.reduce_map()

    if not scenario.correct_answer:
      print 'test %3i: no answer listed' % scenario_index
      continue

    answers, _, _, _, _, _, _, _ = scenario.calculate_monster_move()
    answers = set(
      tuple( scenario.dereduce_location( _ ) for _ in _ )
      for _ in answers
    )
    if answers == scenario.correct_answer:
      print 'test %3i: pass' % scenario_index
    else:
      failures += 1
      print 'test %3i: fail' % scenario_index

  print
  if failures == 0:
    print 'passed all tests'
  else:
    print 'failed %i test(s)' % failures

  return failures