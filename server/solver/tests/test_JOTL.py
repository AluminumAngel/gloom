from solver.scenarios import init_from_test_scenario
from solver.solver import Scenario

def test_JOTLScenario1():
  scenario = Scenario()
  init_from_test_scenario(scenario, 1, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario2():
  scenario = Scenario()
  init_from_test_scenario(scenario, 2, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario3():
  scenario = Scenario()
  init_from_test_scenario(scenario, 3, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario4():
  scenario = Scenario()
  init_from_test_scenario(scenario, 4, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario5():
  scenario = Scenario()
  init_from_test_scenario(scenario, 5, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario6():
  scenario = Scenario()
  init_from_test_scenario(scenario, 6, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario7():
  scenario = Scenario()
  init_from_test_scenario(scenario, 7, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario8():
  scenario = Scenario()
  init_from_test_scenario(scenario, 8, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario9():
  scenario = Scenario()
  init_from_test_scenario(scenario, 9, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario10():
  scenario = Scenario()
  init_from_test_scenario(scenario, 10, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario11():
  scenario = Scenario()
  init_from_test_scenario(scenario, 11, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario12():
  scenario = Scenario()
  init_from_test_scenario(scenario, 12, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario13():
  scenario = Scenario()
  init_from_test_scenario(scenario, 13, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario14():
  scenario = Scenario()
  init_from_test_scenario(scenario, 14, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario15():
  scenario = Scenario()
  init_from_test_scenario(scenario, 15, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario16():
  scenario = Scenario()
  init_from_test_scenario(scenario, 16, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario17():
  scenario = Scenario()
  init_from_test_scenario(scenario, 17, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario18():
  scenario = Scenario()
  init_from_test_scenario(scenario, 18, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario19():
  scenario = Scenario()
  init_from_test_scenario(scenario, 19, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario20():
  scenario = Scenario()
  init_from_test_scenario(scenario, 20, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario21():
  scenario = Scenario()
  init_from_test_scenario(scenario, 21, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario22():
  scenario = Scenario()
  init_from_test_scenario(scenario, 22, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario23():
  scenario = Scenario()
  init_from_test_scenario(scenario, 23, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario24():
  scenario = Scenario()
  init_from_test_scenario(scenario, 24, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario25():
  scenario = Scenario()
  init_from_test_scenario(scenario, 25, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario26():
  scenario = Scenario()
  init_from_test_scenario(scenario, 26, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario27():
  scenario = Scenario()
  init_from_test_scenario(scenario, 27, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario28():
  scenario = Scenario()
  init_from_test_scenario(scenario, 28, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario29():
  scenario = Scenario()
  init_from_test_scenario(scenario, 29, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario30():
  scenario = Scenario()
  init_from_test_scenario(scenario, 30, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario31():
  scenario = Scenario()
  init_from_test_scenario(scenario, 31, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario32():
  scenario = Scenario()
  init_from_test_scenario(scenario, 32, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario33():
  scenario = Scenario()
  init_from_test_scenario(scenario, 33, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario34():
  scenario = Scenario()
  init_from_test_scenario(scenario, 34, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario35():
  scenario = Scenario()
  init_from_test_scenario(scenario, 35, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario36():
  scenario = Scenario()
  init_from_test_scenario(scenario, 36, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario37():
  scenario = Scenario()
  init_from_test_scenario(scenario, 37, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario38():
  scenario = Scenario()
  init_from_test_scenario(scenario, 38, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario39():
  scenario = Scenario()
  init_from_test_scenario(scenario, 39, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario40():
  scenario = Scenario()
  init_from_test_scenario(scenario, 40, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario41():
  scenario = Scenario()
  init_from_test_scenario(scenario, 41, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario42():
  scenario = Scenario()
  init_from_test_scenario(scenario, 42, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario43():
  scenario = Scenario()
  init_from_test_scenario(scenario, 43, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario44():
  scenario = Scenario()
  init_from_test_scenario(scenario, 44, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario45():
  scenario = Scenario()
  init_from_test_scenario(scenario, 45, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario46():
  scenario = Scenario()
  init_from_test_scenario(scenario, 46, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario47():
  scenario = Scenario()
  init_from_test_scenario(scenario, 47, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario48():
  scenario = Scenario()
  init_from_test_scenario(scenario, 48, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario49():
  scenario = Scenario()
  init_from_test_scenario(scenario, 49, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario50():
  scenario = Scenario()
  init_from_test_scenario(scenario, 50, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario51():
  scenario = Scenario()
  init_from_test_scenario(scenario, 51, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario52():
  scenario = Scenario()
  init_from_test_scenario(scenario, 52, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario53():
  scenario = Scenario()
  init_from_test_scenario(scenario, 53, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario54():
  scenario = Scenario()
  init_from_test_scenario(scenario, 54, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario55():
  scenario = Scenario()
  init_from_test_scenario(scenario, 55, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario56():
  scenario = Scenario()
  init_from_test_scenario(scenario, 56, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario57():
  scenario = Scenario()
  init_from_test_scenario(scenario, 57, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario58():
  scenario = Scenario()
  init_from_test_scenario(scenario, 58, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario59():
  scenario = Scenario()
  init_from_test_scenario(scenario, 59, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario60():
  scenario = Scenario()
  init_from_test_scenario(scenario, 60, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario61():
  scenario = Scenario()
  init_from_test_scenario(scenario, 61, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario62():
  scenario = Scenario()
  init_from_test_scenario(scenario, 62, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario63():
  scenario = Scenario()
  init_from_test_scenario(scenario, 63, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario64():
  scenario = Scenario()
  init_from_test_scenario(scenario, 64, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario65():
  scenario = Scenario()
  init_from_test_scenario(scenario, 65, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario66():
  scenario = Scenario()
  init_from_test_scenario(scenario, 66, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario67():
  scenario = Scenario()
  init_from_test_scenario(scenario, 67, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario68():
  scenario = Scenario()
  init_from_test_scenario(scenario, 68, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario69():
  scenario = Scenario()
  init_from_test_scenario(scenario, 69, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario70():
  scenario = Scenario()
  init_from_test_scenario(scenario, 70, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario71():
  scenario = Scenario()
  init_from_test_scenario(scenario, 71, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario72():
  scenario = Scenario()
  init_from_test_scenario(scenario, 72, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario73():
  scenario = Scenario()
  init_from_test_scenario(scenario, 73, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario74():
  scenario = Scenario()
  init_from_test_scenario(scenario, 74, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario75():
  scenario = Scenario()
  init_from_test_scenario(scenario, 75, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario76():
  scenario = Scenario()
  init_from_test_scenario(scenario, 76, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario77():
  scenario = Scenario()
  init_from_test_scenario(scenario, 77, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario78():
  scenario = Scenario()
  init_from_test_scenario(scenario, 78, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario79():
  scenario = Scenario()
  init_from_test_scenario(scenario, 79, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario80():
  scenario = Scenario()
  init_from_test_scenario(scenario, 80, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario81():
  scenario = Scenario()
  init_from_test_scenario(scenario, 81, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario82():
  scenario = Scenario()
  init_from_test_scenario(scenario, 82, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario83():
  scenario = Scenario()
  init_from_test_scenario(scenario, 83, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario84():
  scenario = Scenario()
  init_from_test_scenario(scenario, 84, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario85():
  scenario = Scenario()
  init_from_test_scenario(scenario, 85, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario86():
  scenario = Scenario()
  init_from_test_scenario(scenario, 86, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario87():
  scenario = Scenario()
  init_from_test_scenario(scenario, 87, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario88():
  scenario = Scenario()
  init_from_test_scenario(scenario, 88, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario89():
  scenario = Scenario()
  init_from_test_scenario(scenario, 89, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario90():
  scenario = Scenario()
  init_from_test_scenario(scenario, 90, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario91():
  scenario = Scenario()
  init_from_test_scenario(scenario, 91, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario92():
  scenario = Scenario()
  init_from_test_scenario(scenario, 92, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario93():
  scenario = Scenario()
  init_from_test_scenario(scenario, 93, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario94():
  scenario = Scenario()
  init_from_test_scenario(scenario, 94, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario95():
  scenario = Scenario()
  init_from_test_scenario(scenario, 95, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario96():
  scenario = Scenario()
  init_from_test_scenario(scenario, 96, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario97():
  scenario = Scenario()
  init_from_test_scenario(scenario, 97, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario98():
  scenario = Scenario()
  init_from_test_scenario(scenario, 98, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario99():
  scenario = Scenario()
  init_from_test_scenario(scenario, 99, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario100():
  scenario = Scenario()
  init_from_test_scenario(scenario, 100, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario101():
  scenario = Scenario()
  init_from_test_scenario(scenario, 101, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario102():
  scenario = Scenario()
  init_from_test_scenario(scenario, 102, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario103():
  scenario = Scenario()
  init_from_test_scenario(scenario, 103, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario104():
  scenario = Scenario()
  init_from_test_scenario(scenario, 104, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario105():
  scenario = Scenario()
  init_from_test_scenario(scenario, 105, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario106():
  scenario = Scenario()
  init_from_test_scenario(scenario, 106, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario107():
  scenario = Scenario()
  init_from_test_scenario(scenario, 107, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario108():
  scenario = Scenario()
  init_from_test_scenario(scenario, 108, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario109():
  scenario = Scenario()
  init_from_test_scenario(scenario, 109, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario110():
  scenario = Scenario()
  init_from_test_scenario(scenario, 110, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario111():
  scenario = Scenario()
  init_from_test_scenario(scenario, 111, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario112():
  scenario = Scenario()
  init_from_test_scenario(scenario, 112, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario113():
  scenario = Scenario()
  init_from_test_scenario(scenario, 113, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario114():
  scenario = Scenario()
  init_from_test_scenario(scenario, 114, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario115():
  scenario = Scenario()
  init_from_test_scenario(scenario, 115, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario116():
  scenario = Scenario()
  init_from_test_scenario(scenario, 116, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario117():
  scenario = Scenario()
  init_from_test_scenario(scenario, 117, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario118():
  scenario = Scenario()
  init_from_test_scenario(scenario, 118, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario119():
  scenario = Scenario()
  init_from_test_scenario(scenario, 119, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario120():
  scenario = Scenario()
  init_from_test_scenario(scenario, 120, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario121():
  scenario = Scenario()
  init_from_test_scenario(scenario, 121, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario122():
  scenario = Scenario()
  init_from_test_scenario(scenario, 122, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario123():
  scenario = Scenario()
  init_from_test_scenario(scenario, 123, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario124():
  scenario = Scenario()
  init_from_test_scenario(scenario, 124, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario125():
  scenario = Scenario()
  init_from_test_scenario(scenario, 125, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario126():
  scenario = Scenario()
  init_from_test_scenario(scenario, 126, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario127():
  scenario = Scenario()
  init_from_test_scenario(scenario, 127, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario128():
  scenario = Scenario()
  init_from_test_scenario(scenario, 128, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario129():
  scenario = Scenario()
  init_from_test_scenario(scenario, 129, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario130():
  scenario = Scenario()
  init_from_test_scenario(scenario, 130, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario131():
  scenario = Scenario()
  init_from_test_scenario(scenario, 131, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario132():
  scenario = Scenario()
  init_from_test_scenario(scenario, 132, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario133():
  scenario = Scenario()
  init_from_test_scenario(scenario, 133, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario134():
  scenario = Scenario()
  init_from_test_scenario(scenario, 134, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario135():
  scenario = Scenario()
  init_from_test_scenario(scenario, 135, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario136():
  scenario = Scenario()
  init_from_test_scenario(scenario, 136, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario137():
  scenario = Scenario()
  init_from_test_scenario(scenario, 137, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario138():
  scenario = Scenario()
  init_from_test_scenario(scenario, 138, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario139():
  scenario = Scenario()
  init_from_test_scenario(scenario, 139, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario140():
  scenario = Scenario()
  init_from_test_scenario(scenario, 140, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario141():
  scenario = Scenario()
  init_from_test_scenario(scenario, 141, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario142():
  scenario = Scenario()
  init_from_test_scenario(scenario, 142, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario143():
  scenario = Scenario()
  init_from_test_scenario(scenario, 143, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario144():
  scenario = Scenario()
  init_from_test_scenario(scenario, 144, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario145():
  scenario = Scenario()
  init_from_test_scenario(scenario, 145, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario146():
  scenario = Scenario()
  init_from_test_scenario(scenario, 146, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario147():
  scenario = Scenario()
  init_from_test_scenario(scenario, 147, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario148():
  scenario = Scenario()
  init_from_test_scenario(scenario, 148, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario149():
  scenario = Scenario()
  init_from_test_scenario(scenario, 149, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_JOTLScenario150():
  scenario = Scenario()
  init_from_test_scenario(scenario, 150, 1 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer