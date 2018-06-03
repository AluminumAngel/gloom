# TODO:

# need to add timings

# need many more ranged aoe tests
# - plus attack
# - focus choice based on correct AoE orientation
# - also see below

# add remaining online tests

# aoe tests
# aoe plus extra aoe_targets
# make sure aoe hits primary target
#
# draw aoe in output (all spots, not just attacks)
#
# cache pathing results?
#
# test - monster prioritizes disadvantage over extra aoe_targets
# test - monster prioritizes better focus-rank extra target over disadvantage on extra aoe_targets
#
# test: https://boardgamegeek.com/geeklist/234575/gloomhaven-rules-quiz
# faq: https://boardgamegeek.com/thread/1897763/official-faq-game-revs-1-and-2
# los: https://boardgamegeek.com/image/3930242/caseyharris

import sys, collections, textwrap, itertools
import senarios
from utils import *
from settings import *
from print_map import *

class Senario:
  def __init__( self ):
    self.correct_answer = None
    self.valid = True
    self.logging = False
    self.show_each_action_separately = False

    self.visibility_cache = {}
    self.path_cache = [ {}, {}, {}, {} ]

  def prepare_map( self ):
    self.effective_walls = [ 0 ] * self.MAP_SIZE
    for location in range( 0, self.MAP_SIZE ):
      if self.contents[location] == 'X':
        self.effective_walls[location] = [ True ] * 6
      else:
        self.effective_walls[location] = list( self.walls[location] )

    for location in range( 0, self.MAP_SIZE ):
      neighbors = self.get_neighbors( location )
      for edge in range( 0, 6 ):
        if neighbors[edge] != -1:
          neighbor_edge = ( edge + 3 ) % 6
          if self.walls[location][edge]:
            self.walls[neighbors[edge]][neighbor_edge] = True
          if self.effective_walls[location][edge]:
            self.effective_walls[neighbors[edge]][neighbor_edge] = True

  # TODO: clean this shit up!!!!!!!
  # TODO: move web interface to a different file
  def pack_senario( self ):
    def get_coords( location ):
      row = location % self.MAP_HEIGHT + 13
      column = location / self.MAP_HEIGHT
      return ( column, row )
    def get_locations( grid, content ):
      return [ get_coords( _ ) for _ in range( 0, self.MAP_SIZE ) if grid[_] == content ]
    def get_initiatives():
      return [ self.initiatives[_] for _ in range( 0, self.MAP_SIZE ) if self.figures[_] == 'C' ]

    asdf = zip( get_initiatives(), get_locations( self.figures, 'C' ) )
    asdf.sort()
    order = 0
    curr = -1
    results = []
    for _ in asdf:
      if _[0] > curr:
        order += 1
        curr = _[0]
      results.append( ( order, _[1] ) )
    r, sorted_characters = zip( *results )

    remap = {
      0: 1,
      1: 0,
      5: 2,
    }
    w = [ [], [], [] ]
    for _ in range( 0, self.MAP_SIZE ):
      for j in [ 0, 1, 5 ]:
        if self.walls[_][j]:
          coords = get_coords( _ )
          w[remap[j]].append( coords )

    a = []
    for _ in range( 0, self.AOE_SIZE ):
      if self.aoe[_]:
        a.append( _ )

    packed_senario = {
      'map': {
        'walls': get_locations( self.contents, 'X' ),
        'obsticles': get_locations( self.contents, 'O' ),
        'traps': get_locations( self.contents, 'T' ),
        'hazardous': get_locations( self.contents, 'H' ),
        'difficult': get_locations( self.contents, 'D' ),
        'characters': sorted_characters,
        'monsters': get_locations( self.figures, 'M' ),
        'active_monster': get_locations( self.figures, 'A' ),
        'initiatives': r,
        'thin_walls': w,
      },
      'move': self.ACTION_MOVE,
      'range': self.ACTION_RANGE,
      'target': self.ACTION_TARGET,
      'flying': self.JUMPING and 1 or ( self.FLYING and 2 or 0 ),
      'muddled': self.MUDDLED and 1 or 0,
      'aoe': a,
    }

    return packed_senario

  def unpack_senario( self, packed_senario ):
    self.ACTION_MOVE = int( packed_senario['move'] )
    self.ACTION_RANGE = int( packed_senario['range'] )
    self.ACTION_TARGET = int( packed_senario['target'] )
    self.JUMPING = int( packed_senario['flying'] ) == 1
    self.FLYING = int( packed_senario['flying'] ) == 2
    self.MUDDLED = int( packed_senario['muddled'] ) == 1

    def get_index( column, row ):
      index = column * self.MAP_HEIGHT + row
      return index
    def add_elements( grid, key, content ):
      for _ in packed_senario['map'][key]:
        grid[_] = content
        # grid[get_index( _[0], _[1] )] = content

    add_elements( self.contents, 'walls', 'X' )
    add_elements( self.contents, 'obsticles', 'O' )
    add_elements( self.contents, 'traps', 'T' )
    add_elements( self.contents, 'hazardous', 'H' )
    add_elements( self.contents, 'difficult', 'D' )
    add_elements( self.figures, 'characters', 'C' )
    add_elements( self.figures, 'monsters', 'M' )
    # add_elements( self.figures, 'active_monster', 'A' )

    active_figure_location = packed_senario['active_figure']
    switch_factions = self.figures[active_figure_location] == 'C'
    self.figures[active_figure_location] = 'A'

    if switch_factions:
      for _ in range( 0, self.MAP_SIZE ):
        if self.figures[_] == 'C':
          self.figures[_] = 'M'
        elif self.figures[_] == 'M':
          self.figures[_] = 'C'

    for _ in packed_senario['aoe']:
      if _ != self.AOE_CENTER or self.ACTION_RANGE > 0:
        self.aoe[_] = True

    remap = {
      1: 0,
      0: 1,
      2: 5,
    }
    for _ in packed_senario['map']['thin_walls']:
      # index = get_index( _[0], _[1] )
      # s = remap[_[2]]
      s = remap[_[1]]
      self.walls[_[0]][s] = True

    for i, j in zip( packed_senario['map']['initiatives'], packed_senario['map']['characters'] ):
      self.initiatives[j] = int( i )
      # self.initiatives[get_index(j[0],j[1])] = int( i )

  def can_end_move_on_standard( self, location ):
    return self.contents[location] in [ ' ', 'T', 'H', 'D' ] and self.figures[location] in [ ' ', 'A' ]
  def can_end_move_on_flying( self, location ):
    return self.contents[location] in [ ' ', 'T', 'O', 'H', 'D' ] and self.figures[location] in [ ' ', 'A' ]

  def can_travel_through_standard( self, location ):
    return self.contents[location] in [ ' ', 'T', 'H', 'D' ] and self.figures[location] != 'C'
  def can_travel_through_flying( self, location ):
    return self.contents[location] in [ ' ', 'T', 'H', 'D', 'O' ]

  def is_trap_standard( self, location ):
    return self.contents[location] in [ 'T', 'H' ]
  def is_trap_flying( self, location ):
    return False

  def measure_proximity_through( self, location ):
    return self.contents[location] != 'X'
  def measure_distance_through( self, location ):
    return True

  def blocks_los( self, location ):
    return self.contents[location] == 'X'

  def additional_path_cost( self, location ):
    return int( self.contents[location] == 'D' )

  def get_vertex( self, location, vertex ):
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

  def get_neighbors( self, location ):
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

  def is_adjacent( self, location_a, location_b ):
    return location_b in self.get_neighbors( location_a )

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

  def test_los_between_locations( self, location_a, location_b ):
    cache_key = visibility_cache_key( location_a, location_b )
    if cache_key in self.visibility_cache:
      return self.visibility_cache[cache_key]

    for vertex_a in range( 0, 6 ):
      if self.effective_walls[location_a][vertex_a] or self.effective_walls[location_a][(vertex_a+5)%6]:
        continue 

      vertex_position_a = self.get_vertex( location_a, vertex_a )

      for vertex_b in range( 0, 6 ):
        if self.effective_walls[location_b][vertex_b] or self.effective_walls[location_b][(vertex_b+5)%6]:
          continue 

        vertex_position_b = self.get_vertex( location_b, vertex_b )

        blocked = False
        
        if vertex_position_a != vertex_position_b:
          for location in range( 0, self.MAP_SIZE ):
            if self.blocks_los( location ):
              if self.line_hex_intersection( ( vertex_position_a, vertex_position_b ), location ):
                blocked = True
                break
            else:
              for edge in range( 0, 6 ):
                if self.walls[location][edge]:
                  wall_vertex_a = self.get_vertex( location, edge )
                  wall_vertex_b = self.get_vertex( location, ( edge + 1 ) % 6 )
                  if line_line_intersection( ( vertex_position_a, vertex_position_b ), ( wall_vertex_a, wall_vertex_b ) ):
                    blocked = True
                    break
              if blocked:
                break

        if not blocked:
          self.visibility_cache[cache_key] = True
          return True

    self.visibility_cache[cache_key] = False
    return False

  def calculate_los_from_location( self, eye ):
    visible_locations = [ True ] * self.MAP_SIZE
    for location in range( 0, self.MAP_SIZE ):
      if self.blocks_los( location ) or not self.test_los_between_locations( eye, location ):
        visible_locations[location] = False
    return visible_locations

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
      neighbors = self.get_neighbors( current )
      for edge in range( 0, 6 ):
        neighbor = neighbors[edge]
        if neighbor == -1:
          continue
        if not traversal_test( self, neighbor ):
          continue
        if self.walls[current][edge]:
          continue
        neighbor_distance = distance + 1 + int( not self.FLYING and not self.JUMPING and self.additional_path_cost( neighbor ) )
        neighbor_trap = int( not self.JUMPING ) * trap + int( self.is_trap( self, neighbor ) )
        if is_pair_less_than( neighbor_trap, traps[neighbor], neighbor_distance, distances[neighbor] ):
          frontier.append( neighbor )
          distances[neighbor] = neighbor_distance
          traps[neighbor] = neighbor_trap

    if self.JUMPING:
      for location in range( 0, self.MAP_SIZE ):
        distances[location] += self.additional_path_cost( location )

    self.path_cache[0][cache_key] = ( distances, traps )
    return distances, traps

  def find_path_distances_reverse( self, start, traversal_test ):
    # reverse in that we find the path distance to the start from every location
    # path distance is symetric except for difficult terrain
    # we correct for the asymetry of starting vs ending on difficult terrain
    # we do not correct in that way for traps
    cache_key = ( start, traversal_test )
    if cache_key in self.path_cache[1]:
      return self.path_cache[1][cache_key]

    distances, traps = self.find_path_distances( start, traversal_test )
    if not self.FLYING:
      start_additional_path_cost = self.additional_path_cost( start )
      if start_additional_path_cost > 0:
        distances = [ _ != MAX_VALUE and _ + start_additional_path_cost or _ for _ in distances ]
        if self.JUMPING:
          distances[start] -= start_additional_path_cost
      for location in range( 0, self.MAP_SIZE ):
        distances[location] -= self.additional_path_cost( location )
    
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
      neighbors = self.get_neighbors( current )
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
      neighbors = self.get_neighbors( current )
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
    self.prepare_map()

    if self.ACTION_RANGE == 0 or self.ACTION_TARGET == 0:
      ATTACK_RANGE = 1
      SUSCEPTIBLE_TO_DISADVANTAGE = False
    else:
      ATTACK_RANGE = self.ACTION_RANGE
      SUSCEPTIBLE_TO_DISADVANTAGE = not self.MUDDLED
    PLUS_TARGET = self.ACTION_TARGET - 1

    AOE_ACTION = self.ACTION_TARGET > 0 and True in self.aoe
    AOE_MELEE = AOE_ACTION and self.ACTION_RANGE == 0

    if self.FLYING:
      self.can_end_move_on = Senario.can_end_move_on_flying
      self.can_travel_through = Senario.can_travel_through_flying
      self.is_trap = Senario.is_trap_flying
    elif self.JUMPING:
      self.can_end_move_on = Senario.can_end_move_on_standard
      self.can_travel_through = Senario.can_travel_through_flying
      self.is_trap = Senario.is_trap_standard
    else:
      self.can_end_move_on = Senario.can_end_move_on_standard
      self.can_travel_through = Senario.can_travel_through_standard
      self.is_trap = Senario.is_trap_standard

    map_debug_tags = [ ' ' ] * self.MAP_SIZE
    if self.logging:
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

    # find active monster
    active_monster = self.figures.index( 'A' )
    travel_distances, trap_counts = self.find_path_distances( active_monster, self.can_travel_through )
    proximity_distances = self.find_proximity_distances( active_monster )
    # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( _ ) for _ in self.contents ], [ format_numerical_label( _ ) for _ in trap_counts ] )
    # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( _ ) for _ in self.contents ], [ format_numerical_label( _ ) for _ in travel_distances ] )
    # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( _ ) for _ in self.contents ], [ format_numerical_label( _ ) for _ in proximity_distances ] )

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

    # find monster focus

    if not len( characters ):
      focuses = []
    else:

      # collect character information
      focus_infos=[]
      for character in characters:

        class s:
          shortest_path = (
            MAX_VALUE - 1,
            MAX_VALUE - 1,
          )
        def consider_path():
          this_path = (
            trap_counts[location],
            travel_distances[location],
          )
          if is_tuple_less_than( this_path, s.shortest_path ):
            if self.test_los_between_locations( character, location ):
              s.shortest_path = this_path

        range_to_character = self.find_proximity_distances( character )
        # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( _ ) for _ in self.contents ], [ format_numerical_label( _ ) for _ in range_to_character ] )
        for location in range( 0, self.MAP_SIZE ):
          def inner():
            if self.can_end_move_on( self, location ):
              if not AOE_ACTION or PLUS_TARGET > 0:
                if range_to_character[location] <= ATTACK_RANGE:
                  consider_path()
                  return
              if AOE_ACTION:
                if AOE_MELEE:
                  for aoe_rotation in range( 0, 12 ):
                    for aoe_offset in aoe:
                      if character == self.apply_rotated_aoe_offset( location, aoe_offset, aoe_rotation ):
                        consider_path()
                        return
                else:
                  distances = self.find_distances( location )
                  for aoe_pattern in aoe_pattern_list:
                    for aoe_offset in aoe_pattern:
                      target = self.apply_aoe_offset( character, aoe_offset )
                      if target:
                        if distances[target] <= ATTACK_RANGE:
                          consider_path()
                          return

          inner()

        # choose focus with the least traps on the path to an attack position
        # amoung those, choose focus with shortest travel distance to an attack position
        # break ties with proximity distance
        # break remaining ties with self.initiatives
        focus_infos.append( s.shortest_path + (
          proximity_distances[character],
          self.initiatives[character],
        ) )

      # determine focus ranking
      focus_ranks = {}
      focus_infos, characters = zip( *sorted( zip( focus_infos, characters ) ) )
      best_info = focus_infos[0]
      rank = 0
      for info, character in zip( focus_infos, characters ):
        if info != best_info:
          rank += 1
          best_info = info
        focus_ranks[character] = rank
      num_focus_ranks = rank + 1

      # set focuses
      focuses = [ _ for _ in focus_ranks if focus_ranks[_] == 0 ]

    # players choose among focus ties
    for focus in focuses:

      # find the best desination
      # - that we can stand on
      # - from which the focus can be attacked, via AoE or otherwise
      # - that has los to the focus 
      # - that requires crossing the minimum number of traps
      # - that is the closest

      class s:
        destinations = set()
        best_destination = (
          MAX_VALUE - 1, # trap count
          MAX_VALUE - 1, # closest destination
        )
      def consider_destination():
        this_destination = (
          trap_counts[location],
          travel_distances[location]
        )
        if is_tuple_equal( this_destination, s.best_destination ):
          if self.test_los_between_locations( focus, location ):
            s.destinations.add( location )
        elif is_tuple_less_than( this_destination, s.best_destination ):
          if self.test_los_between_locations( focus, location ):
            s.best_destination = this_destination
            s.destinations = { location }

      range_to_focus = self.find_proximity_distances( focus )
      for location in range( 0, self.MAP_SIZE ):
        def inner():
          if self.can_end_move_on( self, location ):
            if not AOE_ACTION or PLUS_TARGET > 0:
              if range_to_focus[location] <= ATTACK_RANGE:
                consider_destination()
                return
            if AOE_ACTION:
              if AOE_MELEE:
                for aoe_rotation in range( 0, 12 ):
                  for aoe_offset in aoe:
                    if focus == self.apply_rotated_aoe_offset( location, aoe_offset, aoe_rotation ):
                      consider_destination()
                      return
              else:
                distances = self.find_distances( location )
                for aoe_pattern in aoe_pattern_list:
                  for aoe_offset in aoe_pattern:
                    target = self.apply_aoe_offset( character, aoe_offset )
                    if target:
                      if distances[target] <= ATTACK_RANGE:
                        consider_destination()
                        return

        inner()
      destinations = s.destinations

      # find the best move towards the destination
      # - that is within our move range
      # - that we can stand on
      # - that ideally attacks the focus
      # - that crosses the minimum number of traps
      # - that ideally doesn't have disadvantage against the focus
      # - that has the maximum number of targets, via AoE or otherwise
      # - that has the highest ranking targets
      # - that has the maximum number of targets without disadvantage
      # - that is closets to the destination
      # - that is closest to our start position

      class s:
        aoes_for_this_focus = {}
        actions_for_this_focus = set()
        best_move = (
          0,             # can attack focus
          MAX_VALUE - 1, # traps
          MAX_VALUE - 1, # disadvantage against focus
          0,             # total targets
        ) + tuple( [ 0 ] * num_focus_ranks ) + ( # targets of each rank
          0,             # targts without disadvantage
          MAX_VALUE - 1, # distance to destination
          MAX_VALUE - 1, # travel distance
        )
      def consider_actions( num_targets, preexisting_targets, preexisting_targets_of_rank, preexisting_targets_disadvantage, aoe_hexes ):
        if len( preexisting_targets ) == 0:
          aoe_hexes = []
        available_targets = set( characters ) - set( preexisting_targets )
        max_num_targets = min( num_targets, len( available_targets ) )

        # loop over every possible set of potential targets
        for target_set in itertools.combinations( available_targets, max_num_targets ):
          targets = list( preexisting_targets )
          targets_of_rank = list( preexisting_targets_of_rank )
          targets_disadvantage = preexisting_targets_disadvantage

          # loop over the potential targets
          for target in target_set:
            if range_to_location[target] <= ATTACK_RANGE:
              if self.test_los_between_locations( target, location ):
                targets.append( target )
                targets_of_rank[focus_ranks[target]] += 1
                targets_disadvantage += int( SUSCEPTIBLE_TO_DISADVANTAGE and self.is_adjacent( location, target ) )

          # are we are attacking the focus if we expect to be able to attack the focus,
          focus_in_targets = focus in targets and can_reach_destination

          this_move = (
            -int( focus_in_targets ),
            traps_to_destination[location],
            int( focus_in_targets and has_disadvantage_against_focus ),
            -len( targets ),
          ) + tuple( -_ for _ in targets_of_rank ) + (
            targets_disadvantage,
            distance_to_destination[location],
            travel_distances[location],
          )

          if is_tuple_equal( this_move, s.best_move ):
            action = ( location, ) + tuple( sorted( targets ) )
            s.actions_for_this_focus.add( action )
            s.aoes_for_this_focus[action] = aoe_hexes
          elif is_tuple_less_than( this_move, s.best_move ):
            s.best_move = this_move
            action = ( location, ) + tuple( sorted( targets ) )
            s.actions_for_this_focus = { action }
            s.aoes_for_this_focus = { action: aoe_hexes }

      for destination in destinations:
        distance_to_destination, traps_to_destination = self.find_path_distances_reverse( destination, self.can_travel_through )
        # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( _ ) for _ in self.contents ], [ format_numerical_label( _ ) for _ in traps_to_destination ] )
        # print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( _ ) for _ in self.contents ], [ format_numerical_label( _ ) for _ in distance_to_destination ] )
        can_reach_destination = travel_distances[destination] <= self.ACTION_MOVE

        for location in range( 0, self.MAP_SIZE ):
          if travel_distances[location] <= self.ACTION_MOVE:
            if self.can_end_move_on( self, location ):
              range_to_location = self.find_proximity_distances( location )

              # determine disadvantage against focus
              has_disadvantage_against_focus = SUSCEPTIBLE_TO_DISADVANTAGE and self.is_adjacent( location, focus )

              if not AOE_ACTION:
                # add non-AoE targets and consider resulting actions
                consider_actions( 1 + PLUS_TARGET, [], [ 0 ] * num_focus_ranks, 0, [] )

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

                  # add non-AoE targets and consider resulting actions
                  consider_actions( PLUS_TARGET, aoe_targets, aoe_targets_of_rank, aoe_targets_disadvantage, aoe_hexes )

              else:
                # loop over all aoe placements that hit characters
                distances = self.find_distances( location )
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
                    if in_range:
                      consider_actions( PLUS_TARGET, aoe_targets, aoe_targets_of_rank, aoe_targets_disadvantage, aoe_hexes )

      actions |= s.actions_for_this_focus
      aoes.update( s.aoes_for_this_focus )

    # if we find no actions, stand still
    if len( actions ) == 0:
      action = ( active_monster, )
      actions.add( action )
      aoes[action] = []

    # move monster
    self.figures[active_monster] = ' '
    map_debug_tags[active_monster] = 's'
    if self.logging:
      if not self.show_each_action_separately:
        for action in actions:
          self.figures[action[0]] = 'A'
          for target in action[1:]:
            map_debug_tags[target] = 'a'
        print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( self.figures, self.contents ) ], [ format_initiative( _ ) for _ in self.initiatives ], map_debug_tags )
      else:
        for action in actions:
          figures = list( self.figures )
          action_debug_tags = list( map_debug_tags )
          figures[action[0]] = 'A'
          for target in action[1:]:
            action_debug_tags[target] = 'a'
          print_map( self, self.MAP_WIDTH, self.MAP_HEIGHT, self.effective_walls, [ format_content( *_ ) for _ in zip( figures, self.contents ) ], [ format_initiative( _ ) for _ in self.initiatives ], action_debug_tags )

    return actions, aoes

  def solve( self ):
    start_location = self.figures.index( 'A' )

    raw_actions, aoes = self.calculate_monster_move()
    actions = [ {
        'move': _[0],
        'attacks': _[1:],
        'aoe': aoes[_],
    } for _ in raw_actions ]

    if self.logging:
      print '%i option(s):' % len( actions )
      for action in actions:
        if action['move'] == start_location:
          out = '- no movement'
        else:
          out = '- move to %i' % action['move']
        if len( action['attacks'] ) > 0:
          for attack in action['attacks']:
            out += ', attack %i' % attack
        print out

    return actions

def perform_unit_tests( starting_senario ):
  print 'performing unit tests...'

  failures = 0
  senario_index = starting_senario - 1
  while True:
    senario_index += 1
    senario = Senario()
    senarios.init_from_test_senario( senario, senario_index )
    if not senario.valid:
      break

    if not senario.correct_answer:
      print 'test %2i: no answer listed' % senario_index
      continue

    answers, _ = senario.calculate_monster_move()
    if answers == senario.correct_answer:
      print 'test %2i: pass' % senario_index
    else:
      failures += 1
      print 'test %2i: fail' % senario_index

  print
  if failures == 0:
    print 'passed all tests'
  else:
    print 'failed %i test(s)' % failures

  return failures
