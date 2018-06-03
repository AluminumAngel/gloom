import senarios
import solver

from flask import Flask, url_for, jsonify, redirect, request, render_template, abort
import time
app = Flask( __name__, static_folder='../static/dist', template_folder='../static' )
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# Configuration
from production import production
debug = not production

title = 'Gloomhaven Monster Mover'
version = '1.4.1'

# Routes

@app.route( '/' )
def root():
  return templates( 'index.html' )

@app.route( '/templates/<filename>' )
def templates( filename ):
  template_version = version
  if debug:
    template_version += '.' + str( time.time() )
    
  return render_template(
    filename,
    debug_server=debug,
    title=title,
    version=template_version
  )

@app.route( '/solve', methods=[ 'PUT' ] )
def solve():
  packed_senario = request.json
  if not production:
    print packed_senario

  # todo: validate packed senario format
  map_width = packed_senario['width']
  map_height = packed_senario['height']
  senario_id = packed_senario['senario_id']

  s = solver.Senario()
  if not production:
    s.logging = True
  senarios.init( s, map_width, map_height, 7, 7 )
  s.unpack_senario( packed_senario )
  actions = s.solve()
  if not production:
    print actions

  solution = {
    'senario_id': senario_id,
    'actions': actions,
  }

  return jsonify(
    solution
  )

@app.route( '/senario/<senario_index>' )
def senario( senario_index ):
  # todo: validate senario_index is legal
  senario_index = int( senario_index )

  s = solver.Senario()
  senarios.init_from_test_senario( s, senario_index )
  packed_senario = s.pack_senario()
  if not production:
    print packed_senario

  return jsonify(
    packed_senario
  )

# Debug Server
if __name__ == '__main__':
  import os

  if not production:
    if os.environ.get( 'WERKZEUG_RUN_MAIN' ) != 'true':
      failures = solver.perform_unit_tests( 1 )
      if failures > 0:
        exit()

  extra_files = []
  if not production:
    template_diretory = '../static'
    for _, _, files in os.walk( template_diretory ):
      for file in files:
        file = os.path.join( template_diretory, file )
        extra_files.append( file )
    template_diretory = '../static/dist'
    for _, _, files in os.walk( template_diretory ):
      for file in files:
        file = os.path.join( template_diretory, file )
        extra_files.append( file )

  app.run( debug=debug, extra_files=extra_files )
