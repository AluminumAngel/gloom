import sys
import time
import math

import senarios
import solver
from print_map import *

chosen_senario_index = 1
unit_tests = False
print_los = False
show_each_action_separately = False
profile = False

for arg in sys.argv[1:]:
  if arg == '--run_unit_tests' or arg == '-t':
    unit_tests = True
  elif arg == '--los' or arg == '-l':
    print_los = True
  elif arg == '--show_actions' or arg == '-a':
    show_each_action_separately = True
  elif arg == '--profile' or arg == '-p':
    profile = True
  else:
    chosen_senario_index = int( arg )

if unit_tests:
  failures = solver.perform_unit_tests( chosen_senario_index )

elif print_los:
  senario = solver.Senario()
  senarios.init_from_test_senario( senario, chosen_senario_index )
  senario.prepare_map()

  character = senario.figures.index( 'C' )
  visible_locations = senario.calculate_los_from_location( character )
  print_map( senario, senario.MAP_WIDTH, senario.MAP_HEIGHT, senario.effective_walls, [ format_content( *_ ) for _ in zip( senario.figures, senario.contents ) ], [ format_numerical_label( _ ) for _ in range( 0, senario.MAP_SIZE ) ] )
  print_map( senario, senario.MAP_WIDTH, senario.MAP_HEIGHT, senario.effective_walls, [ format_content( *_ ) for _ in zip( senario.figures, senario.contents ) ], [ format_los( _ ) for _ in visible_locations ] )

# TODO: i'm miss using std deviation here; should be dropping by root-N; i'm showing std error
elif profile:
  SAMPLE_COUNT = 10

  results = {}
  for test in ( False, True ):
    results[test] = []
    print 'test parameters: %d' % test
    for sample in range( 0, SAMPLE_COUNT ):
      senario = solver.Senario()
      senarios.init_from_test_senario( senario, chosen_senario_index )

      start = time.time()
      senario.solve()
      end = time.time()
      results[test].append( end - start )
      print 'run %d: %.2fs' % ( sample + 1, end - start )

    test_average = sum( _ for _ in results[test] ) / SAMPLE_COUNT
    test_standard_deviation = math.sqrt(
      sum( ( _ - test_average )**2 for _ in results[test] ) / ( SAMPLE_COUNT - 1 )
    )

    print 'average = %f +/- %f seconds' % ( test_average, test_standard_deviation )
    print

  zipped_results = zip( results[False], results[True] )
  average = sum( _[1] - _[0] for _ in zipped_results ) / SAMPLE_COUNT
  standard_deviation = math.sqrt(
    sum( ( _[1] - _[0] - average )**2 for _ in zipped_results ) / ( SAMPLE_COUNT - 1 )
  )
  print 'delta = %f +/- %f seconds' % ( average, standard_deviation )
  if -average > standard_deviation:
    print 'SUCCESS; savings exceeds noise'
  elif average > standard_deviation:
    print 'FAIL; new method is slower'
  else:
    print 'any savings is less than noise'

else:
  senario = solver.Senario()
  senarios.init_from_test_senario( senario, chosen_senario_index )
  senario.logging = True
  senario.show_each_action_separately = show_each_action_separately
  senario.solve()