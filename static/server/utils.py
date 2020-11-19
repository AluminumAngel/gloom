import math
import sys
import itertools
from settings import *

def debug(expression):
  frame = sys._getframe(1)
  print '%s = %s' % ( expression, repr( eval( expression, frame.f_globals, frame.f_locals ) ) )

def is_pair_less_than( a1, a2, b1, b2 ):
  return a1 < a2 or ( a1 == a2 and b1 < b2 )
def is_tuple_equal( a, b ):
  for ai, bi in itertools.izip( a, b ):
    if ai != bi:
      return False
  return True
def is_tuple_less_than( a, b ):
  for ai, bi in itertools.izip( a, b ):
    if ai == bi:
      continue
    return ai < bi
  return False

def get_offset( center, location, grid_height ):
  location_row = location % grid_height
  location_column = location / grid_height
  center_row = center % grid_height
  center_column = center / grid_height

  x = location_row - center_row

  column_delta = center_column - location_column
  if center_column % 2 == 0:
    y = ( column_delta + 1 ) / 2
  else:
    y = column_delta / 2

  z = column_delta - y

  return ( x, y, z )

def apply_offset( center, offset, grid_height, grid_size ):
  location = center
  column = center / grid_height

  column_delta = offset[1] + offset[2]

  location += offset[0] - offset[2]
  location -= column_delta * grid_height
  location += ( column_delta + column % 2 ) / 2

  column -= column_delta

  # test whether we went off the top or bottom of the board
  final_column = location / grid_height
  if final_column != column:
    return None

  # test whether we went off the left or right of the board
  if location < 0 or location >= grid_size:
    return None

  return location

def rotate_offset( offset, rotation ):
  # rotations 6 through 11 are mirrored
  if rotation < 6:
    offset = ( offset[0], offset[1], offset[2], 0, 0, 0 )
  else:
    rotation -= 6
    offset = ( offset[0], 0, 0, 0, offset[2], offset[1] )

  offset = offset[rotation:] + offset[:rotation]

  offset = (
    offset[0] - offset[3],
    offset[1] - offset[4],
    offset[2] - offset[5],
  )

  return offset    

def pin_offset( offset, pin ):
  return (
    offset[0] - pin[0],
    offset[1] - pin[1],
    offset[2] - pin[2],
  )

ADDITIONAL_LENGTH = 0.001
def lengthen_line( line ):
  delta = ( line[1][0] - line[0][0], line[1][1] - line[0][1] )
  length = math.sqrt( delta[0] * delta[0] + delta[1] * delta[1] )
  normal = ( delta[0] / length, delta[1] / length )
  addition = ( ADDITIONAL_LENGTH * normal[0], ADDITIONAL_LENGTH * normal[1] )
  return (
    ( line[0][0] - addition[0], line[0][1] - addition[1] ),
    ( line[1][0] + addition[0], line[1][1] + addition[1] )
  )

def line_line_intersection( line_a, line_b ):
  line_a = lengthen_line( line_a )
  line_b = lengthen_line( line_b )

  a = line_a[0]
  b = line_a[1]
  c = line_b[0]
  d = line_b[1]
  denominator = ( ( b[0] - a[0] ) * ( d[1] - c[1] ) ) - ( ( b[1] - a[1] ) * ( d[0] - c[0] ) )
  numerator1 = ( ( a[1] - c[1] ) * ( d[0] - c[0] ) ) - ( ( a[0] - c[0] ) * ( d[1] - c[1] ) )
  numerator2 = ( ( a[1] - c[1] ) * ( b[0] - a[0] ) ) - ( ( a[0] - c[0] ) * ( b[1] - a[1] ) )

  # if parallel
  if denominator == 0:
    # if collinear
    if numerator1 == 0 and numerator2 == 0:
      if a[0] != b[0]:
        u = min( a[0], b[0] )
        v = max( a[0], b[0] )
        x = min( c[0], d[0] )
        y = max( c[0], d[0] )
      else:
        u = min( a[1], b[1] )
        v = max( a[1], b[1] )
        x = min( c[1], d[1] )
        y = max( c[1], d[1] )
      if x <= u and y >= u:
        return True
      if x <= v and y >= v:
        return True
      if x >= u and y <= v:
        return True
    return False

  r = numerator1 / denominator
  s = numerator2 / denominator

  return r >= 0 and r <= 1 and s >= 0 and s <= 1

def visibility_cache_key( location_a, location_b ):
  if location_a < location_b:
    return ( location_a, location_b )
  else:
    return ( location_b, location_a )

def calculate_distance( vertex_position_a, vertex_position_b ):
  delta_0 = vertex_position_b[0] - vertex_position_a[0]
  delta_1 = vertex_position_b[1] - vertex_position_a[1]
  distance = math.sqrt( delta_0 * delta_0 + delta_1 * delta_1 )
  return distance