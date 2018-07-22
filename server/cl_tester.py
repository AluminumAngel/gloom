import sys
import time
import math

import senarios
import solver
from print_map import *

chosen_scenario_index = 1
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
    chosen_scenario_index = int( arg )

if unit_tests:
  failures = solver.perform_unit_tests( chosen_scenario_index )

elif print_los:
  scenario = solver.Scenario()
  senarios.init_from_test_scenario( scenario, chosen_scenario_index )
  scenario.prepare_map()

  character = scenario.figures.index( 'C' )
  sight = scenario.solve_sight( character )
  visible_locations = [ False ] * scenario.MAP_SIZE
  visible_locations[character] = True
  for visible_range in sight:
    for location in range( *visible_range ):
      visible_locations[location] = True

  print_map( scenario, scenario.MAP_WIDTH, scenario.MAP_HEIGHT, scenario.effective_walls, [ format_content( *_ ) for _ in zip( scenario.figures, scenario.contents ) ], [ format_numerical_label( _ ) for _ in range( 0, scenario.MAP_SIZE ) ] )
  print_map( scenario, scenario.MAP_WIDTH, scenario.MAP_HEIGHT, scenario.effective_walls, [ format_content( *_ ) for _ in zip( scenario.figures, scenario.contents ) ], [ format_los( _ ) for _ in visible_locations ] )

elif profile:
  SAMPLE_COUNT = 3

  results = {}
  for test in ( False, True ):
    results[test] = []
    print 'test parameters: %d' % test
    for sample in range( 0, SAMPLE_COUNT ):
      scenario = solver.Scenario()
      senarios.init_from_test_scenario( scenario, chosen_scenario_index )
      scenario.test_switch = test

      start = time.time()
      actions = scenario.solve_move()
      # for action in actions:
        # scenario.solve_sight( action['move'] )
      # scenario.solve_sight( 27 )

      end = time.time()
      results[test].append( end - start )
      print 'run %d: %.2fs' % ( sample + 1, end - start )

    test_average = sum( _ for _ in results[test] ) / SAMPLE_COUNT
    test_error = math.sqrt(
      sum( ( _ - test_average )**2 for _ in results[test] ) / ( SAMPLE_COUNT - 1 )
    ) / math.sqrt( SAMPLE_COUNT )

    print 'average = %f +/- %f seconds' % ( test_average, test_error )
    print

  zipped_results = zip( results[False], results[True] )
  average = sum( _[1] - _[0] for _ in zipped_results ) / SAMPLE_COUNT
  error = math.sqrt(
    sum( ( _[1] - _[0] - average )**2 for _ in zipped_results ) / ( SAMPLE_COUNT - 1 )
  ) / math.sqrt( SAMPLE_COUNT )
  print 'delta = %f +/- %f seconds' % ( average, error )
  if -average > error:
    a0 = sum( _ for _ in results[False] ) / SAMPLE_COUNT
    a1 = sum( _ for _ in results[True] ) / SAMPLE_COUNT
    savings = ( a0 - a1 ) / a0 * 100
    print 'SUCCESS; savings exceeds noise; %.1f%% savings' % savings
  elif average > error:
    print 'FAIL; new method is slower'
  else:
    print 'any savings is less than noise'

else:
  scenario = solver.Scenario()
  senarios.init_from_test_scenario( scenario, chosen_scenario_index )
  scenario.logging = True
  scenario.show_each_action_separately = show_each_action_separately
  scenario.solve_move()