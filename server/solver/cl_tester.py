# import sys
# import time
# import math

# from . import scenarios
# from . import solver
# from .print_map import *
# from past.utils import old_div

# chosen_scenario_index = 1
# unit_tests = False
# print_los = False
# show_each_action_separately = False
# profile = False
# rules = 1

# for arg in sys.argv[1:]:
#     if arg == '--run_unit_tests' or arg == '-t':
#         unit_tests = True
#     elif arg == '--los' or arg == '-l':
#         print_los = True
#     elif arg == '--show_actions' or arg == '-a':
#         show_each_action_separately = True
#     elif arg == '--profile' or arg == '-p':
#         profile = True
#     elif arg == '--frost' or arg == '-f':
#         rules = 0
#     elif arg == '--gloom' or arg == '-g':
#         rules = 1
#     elif arg == '--jotl' or arg == '-j':
#         rules = 2
#     else:
#         chosen_scenario_index = int(arg)

# if unit_tests:
#     solver.perform_unit_tests(chosen_scenario_index)

# elif print_los:
#     scenario = solver.Scenario()
#     scenarios.init_from_test_scenario(scenario, chosen_scenario_index, rules)
#     scenario.prepare_map()

#     character = scenario.figures.index('C')
#     sight = scenario.solve_sight(character)
#     visible_locations = [False] * scenario.MAP_SIZE
#     visible_locations[character] = True
#     for visible_range in sight:
#         for location in range(*visible_range):
#             visible_locations[location] = True

#     print_map(scenario, scenario.MAP_WIDTH, scenario.MAP_HEIGHT, scenario.effective_walls, [format_content(
#         *_) for _ in zip(scenario.figures, scenario.contents)], [format_numerical_label(_) for _ in range(0, scenario.MAP_SIZE)])
#     print_map(scenario, scenario.MAP_WIDTH, scenario.MAP_HEIGHT, scenario.effective_walls, [format_content(
#         *_) for _ in zip(scenario.figures, scenario.contents)], [format_los(_) for _ in visible_locations])

# elif profile:
#     SAMPLE_COUNT = 5

#     results = {}
#     for test in (False, True):
#         results[test] = []
#         print('test parameters: %d' % test)
#         for sample in range(0, SAMPLE_COUNT):
#             scenario = solver.Scenario()
#             scenarios.init_from_test_scenario(
#                 scenario, chosen_scenario_index, rules)
#             scenario.test_switch = test

#             start = time.time()
#             actions = scenario.solve_move(test)
#             # for action in actions:
#             # scenario.solve_sight( action['move'] )
#             # scenario.solve_sight( 27 )

#             end = time.time()
#             results[test].append(end - start)
#             print('run %d: %.2fs' % (sample + 1, end - start))

#         test_average = old_div(sum(_ for _ in results[test]), SAMPLE_COUNT)
#         test_error = old_div(math.sqrt(
#             old_div(sum((_ - test_average) **
#                     2 for _ in results[test]), (SAMPLE_COUNT - 1))
#         ), math.sqrt(SAMPLE_COUNT))

#         print('average = %f +/- %f seconds' % (test_average, test_error))
#         print()

#     zipped_results = list(zip(results[False], results[True]))
#     average = old_div(sum(_[1] - _[0] for _ in zipped_results), SAMPLE_COUNT)
#     error = old_div(math.sqrt(
#         old_div(sum((_[1] - _[0] - average) **
#                 2 for _ in zipped_results), (SAMPLE_COUNT - 1))
#     ), math.sqrt(SAMPLE_COUNT))
#     print('delta = %f +/- %f seconds' % (average, error))
#     if -average > error:
#         a0 = old_div(sum(_ for _ in results[False]), SAMPLE_COUNT)
#         a1 = old_div(sum(_ for _ in results[True]), SAMPLE_COUNT)
#         savings = old_div((a0 - a1), a0 * 100)
#         print('SUCCESS; savings exceeds noise; %.1f%% savings' % savings)
#     elif average > error:
#         print('FAIL; new method is slower')
#     else:
#         print('any savings is less than noise')

# else:
#     scenario = solver.Scenario()
#     scenarios.init_from_test_scenario(scenario, chosen_scenario_index, rules)
#     print_map(scenario, scenario.MAP_WIDTH, scenario.MAP_HEIGHT, scenario.effective_walls, [format_content(
#         *_) for _ in zip(scenario.figures, scenario.contents)], [format_numerical_label(_) for _ in range(0, scenario.MAP_SIZE)])
#     # scenario.reduce_map()
#     # print_map( scenario, scenario.MAP_WIDTH, scenario.MAP_HEIGHT, scenario.effective_walls, [ format_content( *_ ) for _ in zip( scenario.figures, scenario.contents ) ], [ format_numerical_label( _ ) for _ in range( 0, scenario.MAP_SIZE ) ] )
#     # scenario__ = solver.Scenario()
#     # scenarios.reduce_scenario( scenario, scenario__ )
#     # print_map( scenario__, scenario__.MAP_WIDTH, scenario__.MAP_HEIGHT, scenario__.effective_walls, [ format_content( *_ ) for _ in zip( scenario__.figures, scenario__.contents ) ], [ format_numerical_label( _ ) for _ in range( 0, scenario__.MAP_SIZE ) ] )
#     scenario.logging = True
#     scenario.show_each_action_separately = show_each_action_separately
#     actions = scenario.solve_move(False)
#     # scenario__.logging = True
#     # scenario__.show_each_action_separately = show_each_action_separately
#     # actions = scenario__.solve_move( False )
#     # print actions

#     # new_actions = scenarios.unreduce_actions( scenario__, actions )

#     # OLD_MAP_HEIGHT = scenario.MAP_HEIGHT
#     # OLD_MAP_WIDTH = scenario.MAP_WIDTH
#     # NEW_MAP_HEIGHT = scenario__.MAP_HEIGHT
#     # NEW_MAP_WIDTH = scenario__.MAP_WIDTH

#     # def fix_location( location ):
#     #   column = old_div(location , NEW_MAP_HEIGHT)
#     #   row = location % NEW_MAP_HEIGHT
#     #   column += scenario__.REDUCE_COLUMN
#     #   row += scenario__.REDUCE_ROW
#     #   return row + column * OLD_MAP_HEIGHT

#     # new_actions = []
#     # for action in actions:
#     #   new_action = {}
#     #   new_action['move'] = fix_location( action['move'] )
#     #   attacks = []
#     #   for attack in action['attacks']:
#     #     attacks.append( fix_location( attack ) )
#     #   new_action['attacks'] = attacks
#     #   new_actions.append( new_action )

#     # MAP REDUCE TODO LIST:
#     # - without fixing actions, do some profiling
#     # - see waht the win is
#     # - move this logic to unit tests
#     # - fix all unit tests
#     # - move this fix-up logic deeper into the solve (if REDUCE set)
#     # - make sure CL map prints look OK; OK to just print the smaller map?
#     # - do more timing
#     # - setup ability to run unit tests with and without reduction
#     # - add more weird test cases
#     # --- muddle backoff
#     # --- bizare ranged aoe
#     # --- bizare melle aoe
