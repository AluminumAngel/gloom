from solver.scenarios import init_from_test_scenario
from solver.solver import Scenario

def test_FrosthavenScenario1():
  scenario = Scenario()
  init_from_test_scenario(scenario, 1, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario2():
  scenario = Scenario()
  init_from_test_scenario(scenario, 2, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario3():
  scenario = Scenario()
  init_from_test_scenario(scenario, 3, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario4():
  scenario = Scenario()
  init_from_test_scenario(scenario, 4, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario5():
  scenario = Scenario()
  init_from_test_scenario(scenario, 5, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario6():
  scenario = Scenario()
  init_from_test_scenario(scenario, 6, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario7():
  scenario = Scenario()
  init_from_test_scenario(scenario, 7, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario8():
  scenario = Scenario()
  init_from_test_scenario(scenario, 8, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario9():
  scenario = Scenario()
  init_from_test_scenario(scenario, 9, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario10():
  scenario = Scenario()
  init_from_test_scenario(scenario, 10, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario11():
  scenario = Scenario()
  init_from_test_scenario(scenario, 11, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario12():
  scenario = Scenario()
  init_from_test_scenario(scenario, 12, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario13():
  scenario = Scenario()
  init_from_test_scenario(scenario, 13, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario14():
  scenario = Scenario()
  init_from_test_scenario(scenario, 14, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario15():
  scenario = Scenario()
  init_from_test_scenario(scenario, 15, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario16():
  scenario = Scenario()
  init_from_test_scenario(scenario, 16, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario17():
  scenario = Scenario()
  init_from_test_scenario(scenario, 17, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario18():
  scenario = Scenario()
  init_from_test_scenario(scenario, 18, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario19():
  scenario = Scenario()
  init_from_test_scenario(scenario, 19, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario20():
  scenario = Scenario()
  init_from_test_scenario(scenario, 20, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario21():
  scenario = Scenario()
  init_from_test_scenario(scenario, 21, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario22():
  scenario = Scenario()
  init_from_test_scenario(scenario, 22, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario23():
  scenario = Scenario()
  init_from_test_scenario(scenario, 23, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario24():
  scenario = Scenario()
  init_from_test_scenario(scenario, 24, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario25():
  scenario = Scenario()
  init_from_test_scenario(scenario, 25, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario26():
  scenario = Scenario()
  init_from_test_scenario(scenario, 26, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario27():
  scenario = Scenario()
  init_from_test_scenario(scenario, 27, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario28():
  scenario = Scenario()
  init_from_test_scenario(scenario, 28, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario29():
  scenario = Scenario()
  init_from_test_scenario(scenario, 29, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario30():
  scenario = Scenario()
  init_from_test_scenario(scenario, 30, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario31():
  scenario = Scenario()
  init_from_test_scenario(scenario, 31, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario32():
  scenario = Scenario()
  init_from_test_scenario(scenario, 32, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario33():
  scenario = Scenario()
  init_from_test_scenario(scenario, 33, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario34():
  scenario = Scenario()
  init_from_test_scenario(scenario, 34, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario35():
  scenario = Scenario()
  init_from_test_scenario(scenario, 35, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario36():
  scenario = Scenario()
  init_from_test_scenario(scenario, 36, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario37():
  scenario = Scenario()
  init_from_test_scenario(scenario, 37, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario38():
  scenario = Scenario()
  init_from_test_scenario(scenario, 38, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario39():
  scenario = Scenario()
  init_from_test_scenario(scenario, 39, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario40():
  scenario = Scenario()
  init_from_test_scenario(scenario, 40, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario41():
  scenario = Scenario()
  init_from_test_scenario(scenario, 41, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario42():
  scenario = Scenario()
  init_from_test_scenario(scenario, 42, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario43():
  scenario = Scenario()
  init_from_test_scenario(scenario, 43, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario44():
  scenario = Scenario()
  init_from_test_scenario(scenario, 44, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario45():
  scenario = Scenario()
  init_from_test_scenario(scenario, 45, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario46():
  scenario = Scenario()
  init_from_test_scenario(scenario, 46, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario47():
  scenario = Scenario()
  init_from_test_scenario(scenario, 47, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario48():
  scenario = Scenario()
  init_from_test_scenario(scenario, 48, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario49():
  scenario = Scenario()
  init_from_test_scenario(scenario, 49, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario50():
  scenario = Scenario()
  init_from_test_scenario(scenario, 50, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario51():
  scenario = Scenario()
  init_from_test_scenario(scenario, 51, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario52():
  scenario = Scenario()
  init_from_test_scenario(scenario, 52, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario53():
  scenario = Scenario()
  init_from_test_scenario(scenario, 53, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario54():
  scenario = Scenario()
  init_from_test_scenario(scenario, 54, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario55():
  scenario = Scenario()
  init_from_test_scenario(scenario, 55, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario56():
  scenario = Scenario()
  init_from_test_scenario(scenario, 56, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario57():
  scenario = Scenario()
  init_from_test_scenario(scenario, 57, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario58():
  scenario = Scenario()
  init_from_test_scenario(scenario, 58, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario59():
  scenario = Scenario()
  init_from_test_scenario(scenario, 59, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario60():
  scenario = Scenario()
  init_from_test_scenario(scenario, 60, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario61():
  scenario = Scenario()
  init_from_test_scenario(scenario, 61, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario62():
  scenario = Scenario()
  init_from_test_scenario(scenario, 62, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario63():
  scenario = Scenario()
  init_from_test_scenario(scenario, 63, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario64():
  scenario = Scenario()
  init_from_test_scenario(scenario, 64, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario65():
  scenario = Scenario()
  init_from_test_scenario(scenario, 65, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario66():
  scenario = Scenario()
  init_from_test_scenario(scenario, 66, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario67():
  scenario = Scenario()
  init_from_test_scenario(scenario, 67, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario68():
  scenario = Scenario()
  init_from_test_scenario(scenario, 68, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario69():
  scenario = Scenario()
  init_from_test_scenario(scenario, 69, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario70():
  scenario = Scenario()
  init_from_test_scenario(scenario, 70, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario71():
  scenario = Scenario()
  init_from_test_scenario(scenario, 71, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario72():
  scenario = Scenario()
  init_from_test_scenario(scenario, 72, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario73():
  scenario = Scenario()
  init_from_test_scenario(scenario, 73, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario74():
  scenario = Scenario()
  init_from_test_scenario(scenario, 74, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario75():
  scenario = Scenario()
  init_from_test_scenario(scenario, 75, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario76():
  scenario = Scenario()
  init_from_test_scenario(scenario, 76, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario77():
  scenario = Scenario()
  init_from_test_scenario(scenario, 77, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario78():
  scenario = Scenario()
  init_from_test_scenario(scenario, 78, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario79():
  scenario = Scenario()
  init_from_test_scenario(scenario, 79, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario80():
  scenario = Scenario()
  init_from_test_scenario(scenario, 80, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario81():
  scenario = Scenario()
  init_from_test_scenario(scenario, 81, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario82():
  scenario = Scenario()
  init_from_test_scenario(scenario, 82, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario83():
  scenario = Scenario()
  init_from_test_scenario(scenario, 83, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario84():
  scenario = Scenario()
  init_from_test_scenario(scenario, 84, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario85():
  scenario = Scenario()
  init_from_test_scenario(scenario, 85, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario86():
  scenario = Scenario()
  init_from_test_scenario(scenario, 86, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario87():
  scenario = Scenario()
  init_from_test_scenario(scenario, 87, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario88():
  scenario = Scenario()
  init_from_test_scenario(scenario, 88, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario89():
  scenario = Scenario()
  init_from_test_scenario(scenario, 89, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario90():
  scenario = Scenario()
  init_from_test_scenario(scenario, 90, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario91():
  scenario = Scenario()
  init_from_test_scenario(scenario, 91, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario92():
  scenario = Scenario()
  init_from_test_scenario(scenario, 92, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario93():
  scenario = Scenario()
  init_from_test_scenario(scenario, 93, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario94():
  scenario = Scenario()
  init_from_test_scenario(scenario, 94, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario95():
  scenario = Scenario()
  init_from_test_scenario(scenario, 95, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario96():
  scenario = Scenario()
  init_from_test_scenario(scenario, 96, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario97():
  scenario = Scenario()
  init_from_test_scenario(scenario, 97, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario98():
  scenario = Scenario()
  init_from_test_scenario(scenario, 98, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario99():
  scenario = Scenario()
  init_from_test_scenario(scenario, 99, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario100():
  scenario = Scenario()
  init_from_test_scenario(scenario, 100, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario101():
  scenario = Scenario()
  init_from_test_scenario(scenario, 101, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario102():
  scenario = Scenario()
  init_from_test_scenario(scenario, 102, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario103():
  scenario = Scenario()
  init_from_test_scenario(scenario, 103, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario104():
  scenario = Scenario()
  init_from_test_scenario(scenario, 104, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario105():
  scenario = Scenario()
  init_from_test_scenario(scenario, 105, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario106():
  scenario = Scenario()
  init_from_test_scenario(scenario, 106, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario107():
  scenario = Scenario()
  init_from_test_scenario(scenario, 107, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario108():
  scenario = Scenario()
  init_from_test_scenario(scenario, 108, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario109():
  scenario = Scenario()
  init_from_test_scenario(scenario, 109, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario110():
  scenario = Scenario()
  init_from_test_scenario(scenario, 110, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario111():
  scenario = Scenario()
  init_from_test_scenario(scenario, 111, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario112():
  scenario = Scenario()
  init_from_test_scenario(scenario, 112, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario113():
  scenario = Scenario()
  init_from_test_scenario(scenario, 113, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario114():
  scenario = Scenario()
  init_from_test_scenario(scenario, 114, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario115():
  scenario = Scenario()
  init_from_test_scenario(scenario, 115, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario116():
  scenario = Scenario()
  init_from_test_scenario(scenario, 116, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario117():
  scenario = Scenario()
  init_from_test_scenario(scenario, 117, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario118():
  scenario = Scenario()
  init_from_test_scenario(scenario, 118, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario119():
  scenario = Scenario()
  init_from_test_scenario(scenario, 119, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario120():
  scenario = Scenario()
  init_from_test_scenario(scenario, 120, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario121():
  scenario = Scenario()
  init_from_test_scenario(scenario, 121, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario122():
  scenario = Scenario()
  init_from_test_scenario(scenario, 122, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario123():
  scenario = Scenario()
  init_from_test_scenario(scenario, 123, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario124():
  scenario = Scenario()
  init_from_test_scenario(scenario, 124, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario125():
  scenario = Scenario()
  init_from_test_scenario(scenario, 125, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario126():
  scenario = Scenario()
  init_from_test_scenario(scenario, 126, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario127():
  scenario = Scenario()
  init_from_test_scenario(scenario, 127, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario128():
  scenario = Scenario()
  init_from_test_scenario(scenario, 128, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario129():
  scenario = Scenario()
  init_from_test_scenario(scenario, 129, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario130():
  scenario = Scenario()
  init_from_test_scenario(scenario, 130, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario131():
  scenario = Scenario()
  init_from_test_scenario(scenario, 131, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario132():
  scenario = Scenario()
  init_from_test_scenario(scenario, 132, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario133():
  scenario = Scenario()
  init_from_test_scenario(scenario, 133, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario134():
  scenario = Scenario()
  init_from_test_scenario(scenario, 134, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario135():
  scenario = Scenario()
  init_from_test_scenario(scenario, 135, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario136():
  scenario = Scenario()
  init_from_test_scenario(scenario, 136, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario137():
  scenario = Scenario()
  init_from_test_scenario(scenario, 137, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario138():
  scenario = Scenario()
  init_from_test_scenario(scenario, 138, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario139():
  scenario = Scenario()
  init_from_test_scenario(scenario, 139, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario140():
  scenario = Scenario()
  init_from_test_scenario(scenario, 140, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario141():
  scenario = Scenario()
  init_from_test_scenario(scenario, 141, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario142():
  scenario = Scenario()
  init_from_test_scenario(scenario, 142, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario143():
  scenario = Scenario()
  init_from_test_scenario(scenario, 143, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario144():
  scenario = Scenario()
  init_from_test_scenario(scenario, 144, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario145():
  scenario = Scenario()
  init_from_test_scenario(scenario, 145, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario146():
  scenario = Scenario()
  init_from_test_scenario(scenario, 146, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario147():
  scenario = Scenario()
  init_from_test_scenario(scenario, 147, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario148():
  scenario = Scenario()
  init_from_test_scenario(scenario, 148, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario149():
  scenario = Scenario()
  init_from_test_scenario(scenario, 149, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer

def test_FrosthavenScenario150():
  scenario = Scenario()
  init_from_test_scenario(scenario, 150, 2 )
  answers, _, _, _, _, _ = scenario.calculate_monster_move()
  answers = set(
    tuple( scenario.dereduce_location( _ ) for _ in _ )
    for _ in answers
  )
  assert answers == scenario.correct_answer