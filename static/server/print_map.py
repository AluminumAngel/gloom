from settings import *

class Colors:
  purple = '\033[95m'
  blue = '\033[94m'
  green = '\033[92m'
  yellow = '\033[93m'
  red = '\033[91m'
  white = '\033[1m'
  end = '\033[0m'

def format_content( figure, content ):
  color = ''
  if figure != ' ':
    value = figure
  else:
    value = content
  if figure == 'A':
    color = Colors.red
  elif figure == 'M':
    color = Colors.purple
  elif figure == 'C':
    color = Colors.blue
  elif content in [ 'T', 'H' ]:
    color = Colors.green
  return color + ' %s ' % value + Colors.end 

def format_aoe_content( value ):
  if value == 'A':
    return Colors.red + ' A ' + Colors.end 
  return '   '

def format_numerical_label( value ):
  if value == MAX_VALUE:
    return '   '
  elif value < 10:
    return ' %1i ' % value
  else:
    return '%3i' % value

def format_initiative( value ):
  if value == 0:
    return '   '
  elif value < 10:
    return '%s %1i %s' % ( Colors.blue, value, Colors.end )
  else:
    return '%s%3i%s' % ( Colors.blue, value, Colors.end )

def format_los( value ):
  if value:
    return '   '
  else:
    return ' # '

def format_aoe( value ):
  if value:
    return ' % '
  else:
    return '   '

def top_edge_glyph( walls, location, edge ):
  if walls[location][edge]:
    return '___'
  else:
    return '...'

def north_edge_glyph( walls, location, edge ):
  if walls[location][edge]:
    return '/'
  else:
    return '\''

def south_edge_glyph( walls, location, edge ):
  if walls[location][edge]:
    return '\\'
  else:
    return '\''

def print_map( s, grid_width, grid_height, walls, top_label, bottom_label, extra_label=False ):
  grid_size = grid_width * grid_height

  if not extra_label:
    extra_label = [ ' ' ] * grid_size
  for i in range( 0, grid_size ):
    extra_label[i] = Colors.yellow + extra_label[i] + Colors.end

  out = ''
  for j in range( 0, grid_width / 2 ):
    location = 2 * grid_height + 2 * j * grid_height - 1
    out += '       %s' % top_edge_glyph( walls, location, 1 )
  print out

  out = ' '
  for j in range( 0, grid_width / 2 ):
    location = 2 * grid_height + 2 * j * grid_height - 1
    out += '     %s %s %s' % ( north_edge_glyph( walls, location, 2 ), extra_label[location], south_edge_glyph( walls, location, 0 ) )
  print out

  out = '  '
  for j in range( 0, grid_width / 2 ):
    label_location = 2 * grid_height + 2 * j * grid_height - 1
    base_edge_location = grid_height + 2 * j * grid_height - 1
    out += '%s%s %s %s' % ( top_edge_glyph( walls, base_edge_location, 1 ), north_edge_glyph( walls, label_location, 2 ), top_label[label_location], south_edge_glyph( walls, label_location, 0 ) )
  if grid_width % 2:
    base_edge_location = grid_height + ( grid_width - 1 ) * grid_height - 1
    out += '%s' % ( top_edge_glyph( walls, base_edge_location, 1 ) )
  print out

  for i in range( 0, grid_height - 1 ):
    left_location = grid_height - i - 1

    out = ' %s' % north_edge_glyph( walls, left_location, 2 )
    for j in range( 0, grid_width / 2 ):
      extra_label_location = grid_height - i + j * 2 * grid_height - 1
      label_location = 2 * grid_height - i + j * 2 * grid_height - 1
      out += ' %s %s %s %s' % ( extra_label[extra_label_location], south_edge_glyph( walls, extra_label_location, 0 ), bottom_label[label_location], north_edge_glyph( walls, label_location, 5 ) )
    if grid_width % 2:
      extra_label_location = grid_height - i + ( grid_width - 1 ) * grid_height - 1
      out += ' %s %s' % ( extra_label[extra_label_location], south_edge_glyph( walls, extra_label_location, 0 ) )
    print out

    out = '%s' % north_edge_glyph( walls, left_location, 2 )
    for j in range( 0, grid_width / 2 ):
      label_location = grid_height - i + j * 2 * grid_height - 1
      edge_location = 2 * grid_height - i + j * 2 * grid_height - 1
      out += ' %s %s%s%s' % ( top_label[label_location], south_edge_glyph( walls, label_location, 0 ), top_edge_glyph( walls, edge_location, 4 ), north_edge_glyph( walls, edge_location, 5 ) )
    if grid_width % 2:
      label_location = grid_height - i + ( grid_width - 1 ) * grid_height - 1
      out += ' %s %s' % ( top_label[label_location], south_edge_glyph( walls, label_location, 0 ) )
    print out

    out = '%s' % south_edge_glyph( walls, left_location, 3 )
    for j in range( 0, grid_width / 2 ):
      label_location = grid_height - i + j * 2 * grid_height - 1
      edge_location = 2 * grid_height - i + j * 2 * grid_height - 2
      out += ' %s %s %s %s' % ( bottom_label[label_location], north_edge_glyph( walls, label_location, 5 ), extra_label[edge_location], south_edge_glyph( walls, edge_location, 0 ) )
    if grid_width % 2:
      label_location = grid_height - i + ( grid_width - 1 ) * grid_height - 1
      out += ' %s %s' % ( bottom_label[label_location], north_edge_glyph( walls, label_location, 5 ) )
    print out

    out = ' %s' % south_edge_glyph( walls, left_location, 3 )
    for j in range( 0, grid_width / 2 ):
      label_location = 2 * grid_height - i + j * 2 * grid_height - 2
      base_edge_location = grid_height - i + j * 2 * grid_height - 1
      out += '%s%s %s %s' % ( top_edge_glyph( walls, base_edge_location, 4 ), north_edge_glyph( walls, base_edge_location, 5 ), top_label[label_location], south_edge_glyph( walls, label_location, 0 ) )
    if grid_width % 2:
      base_edge_location = grid_height - i + ( grid_width - 1 ) * grid_height - 1
      out += '%s%s' % ( top_edge_glyph( walls, base_edge_location, 4 ), north_edge_glyph( walls, base_edge_location, 5 ) )
    print out

  out = ' %s' % north_edge_glyph( walls, 0, 2 )
  for j in range( 0, grid_width / 2 ):
    location = grid_height + j * 2 * grid_height
    label_location = j * 2 * grid_height
    out += ' %s %s %s %s' % ( extra_label[label_location], south_edge_glyph( walls, label_location, 0 ), bottom_label[location], north_edge_glyph( walls, location, 5 ) )
  if grid_width % 2:
    label_location = ( grid_width - 1 ) * grid_height
    out += ' %s %s' % ( extra_label[label_location], south_edge_glyph( walls, label_location, 0 ) )
  print out

  out = '%s' % north_edge_glyph( walls, 0, 2 )
  for j in range( 0, grid_width / 2 ):
    label_location = j * 2 * grid_height
    edge_location = grid_height + j * 2 * grid_height
    out += ' %s %s%s%s' % ( top_label[label_location], south_edge_glyph( walls, label_location, 0 ), top_edge_glyph( walls, edge_location, 4 ), north_edge_glyph( walls, edge_location, 5 ) )
  if grid_width % 2:
    label_location = ( grid_width - 1 ) * grid_height
    out += ' %s %s' % ( top_label[label_location], south_edge_glyph( walls, label_location, 0 ) )
  print out

  out = ''
  for j in range( 0, grid_width / 2 ):
    location = j * 2 * grid_height
    out += '%s %s %s   ' % ( south_edge_glyph( walls, location, 3 ), bottom_label[location], north_edge_glyph( walls, location, 5 ) )
  if grid_width % 2:
    location = ( grid_width - 1 ) * grid_height
    out += '%s %s %s' % ( south_edge_glyph( walls, location, 3 ), bottom_label[location], north_edge_glyph( walls, location, 5 ) )
  print out

  out = ''
  for j in range( 0, grid_width / 2 ):
    location = j * 2 * grid_height
    out += ' %s%s%s    ' % ( south_edge_glyph( walls, location, 3 ), top_edge_glyph( walls, location, 4 ), north_edge_glyph( walls, location, 5 ) )
  if grid_width % 2:
    location = ( grid_width - 1 ) * grid_height
    out += ' %s%s%s' % ( south_edge_glyph( walls, location, 3 ), top_edge_glyph( walls, location, 4 ), north_edge_glyph( walls, location, 5 ) )
  print out