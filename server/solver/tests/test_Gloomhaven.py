from solver.solver import Scenario

def init_test():
    scenario = Scenario(16, 7, 7, 7)
    scenario.set_rules(1)
    return scenario

def assert_answers(scenario, correct_answers):
    scenario.prepare_map()
    answers, _, _, _, _, _ = scenario.calculate_monster_move()
    answers = set(
        tuple(scenario.dereduce_location(_) for _ in _)
        for _ in answers
    )
    assert answers == correct_answers

# Move towards the character and offer all valid options for the players to choose among
def test_Scenario1():
    s = init_test()

    s.figures[60] = 'C'
    s.figures[37] = 'M'
    s.figures[38] = 'M'
    s.figures[39] = 'A'

    s.ACTION_MOVE = 1

    assert_answers(s,{(46, ), (47, )})

# Online test question #1. Shorten the path to the destinations
def test_Scenario2():
    s = init_test()

    s.figures[35] = 'C'
    s.figures[36] = 'M'
    s.figures[37] = 'M'
    s.figures[38] = 'A'

    s.ACTION_MOVE = 1

    assert_answers(s,{(45, ), (31, )})

# Online test question #2. The monster cannot shorten the path to the destination, so it stays put
def test_Scenario3():
    s = init_test()

    s.figures[35] = 'C'
    s.figures[37] = 'M'
    s.figures[38] = 'M'
    s.figures[39] = 'A'

    s.ACTION_MOVE = 1

    assert_answers(s,{(39, )})

# Online test question #6. The monster cannot attack the character from the near edge, so it begins the long trek around to the far edge
def test_Scenario4():
    s = init_test()

    s.figures[29] = 'C'

    s.contents[11] = 'O'
    s.contents[12] = 'O'
    s.contents[17] = 'O'
    s.contents[18] = 'O'
    s.contents[22] = 'O'
    s.contents[23] = 'O'
    s.contents[32] = 'O'
    s.contents[33] = 'O'
    s.contents[36] = 'O'
    s.contents[37] = 'O'
    s.contents[38] = 'O'
    s.contents[43] = 'O'

    s.figures[24] = 'M'
    s.figures[30] = 'M'

    s.figures[25] = 'A'

    s.ACTION_MOVE = 2

    assert_answers(s,{(34, ), (20, )})

# When shortening the path to its destination, the monster will move the minimum amount. Players cannot choose a move that puts the monster equally close to its destination, but uses more movement
def test_Scenario5():
    s = init_test()

    s.figures[35] = 'C'
    s.figures[30] = 'M'
    s.figures[36] = 'M'
    s.figures[37] = 'M'
    s.figures[44] = 'M'
    s.figures[38] = 'A'

    s.ACTION_MOVE = 2

    assert_answers(s,{(45, ), (31, )})

# When choosing focus, proximity breaks ties in path delta_length. C20 is in closer proximity
def test_Scenario6():
    s = init_test()

    s.figures[50] = 'C'
    s.initiatives[50] = 10

    s.figures[29] = 'C'
    s.initiatives[29] = 20

    s.contents[30] = 'O'
    s.figures[31] = 'A'

    s.ACTION_MOVE = 2

    assert_answers(s,{(36, 29), (22, 29)})

# When choosing focus, proximity breaks ties in path delta_length, but walls must be pathed around when testing proximity. Proximity is equal here, so initiative breaks the tie
def test_Scenario7():
    s = init_test()

    s.figures[50] = 'C'
    s.initiatives[50] = 10

    s.figures[29] = 'C'
    s.initiatives[29] = 20

    s.contents[30] = 'X'
    s.figures[31] = 'A'

    s.ACTION_MOVE = 2

    assert_answers(s,{(44, 50)})

# Given equal path distance and proximity, lowest initiative breaks the focus tie
def test_Scenario8():
    s = init_test()

    s.figures[9] = 'C'
    s.initiatives[9] = 10

    s.figures[29] = 'C'
    s.initiatives[29] = 20

    s.figures[32] = 'A'

    s.ACTION_MOVE = 2

    assert_answers(s,{(17, 9)})

# Given equal path distance, proximity, and initiative; players choose the foc
def test_Scenario9():
    s = init_test()

    s.figures[9] = 'C'
    s.initiatives[9] = 99

    s.figures[29] = 'C'
    s.initiatives[29] = 99

    s.figures[32] = 'A'

    s.ACTION_MOVE = 2

    assert_answers(s,{(17, 9), (30, 29)})

# Online test question #4. The monster has a valid path to its destination that does not go through a trap. Even though the monster cannot shorten its path to the destination, it will not go through the trap
def test_Scenario10():
    s = init_test()

    s.contents[70] = 'X'
    s.contents[77] = 'X'
    s.contents[84] = 'X'
    s.contents[91] = 'X'
    s.contents[98] = 'X'
    s.contents[105] = 'X'
    s.contents[106] = 'X'
    s.contents[107] = 'X'
    s.contents[108] = 'X'
    s.contents[109] = 'X'
    s.contents[102] = 'X'
    s.contents[95] = 'X'
    s.contents[88] = 'X'
    s.contents[81] = 'X'
    s.contents[74] = 'X'

    s.contents[85] = 'O'
    s.contents[93] = 'O'

    s.contents[87] = 'T'

    s.figures[86] = 'M'
    s.figures[92] = 'M'

    s.figures[79] = 'A'

    s.figures[99] = 'C'

    s.ACTION_MOVE = 2

    assert_answers(s,{(79, )})

# The monster will shorten its distance to focus, even if it means moving off the shortest path
def test_Scenario11():
    s = init_test()

    s.contents[70] = 'X'
    s.contents[77] = 'X'
    s.contents[84] = 'X'
    s.contents[91] = 'X'
    s.contents[98] = 'X'
    s.contents[105] = 'X'
    s.contents[106] = 'X'
    s.contents[107] = 'X'
    s.contents[108] = 'X'
    s.contents[109] = 'X'
    s.contents[102] = 'X'
    s.contents[95] = 'X'
    s.contents[88] = 'X'
    s.contents[81] = 'X'
    s.contents[74] = 'X'

    s.contents[85] = 'O'
    s.contents[93] = 'O'

    s.figures[86] = 'M'
    s.figures[92] = 'M'

    s.figures[79] = 'A'

    s.figures[99] = 'C'

    s.ACTION_MOVE = 2

    assert_answers(s,{(94, )})

# The monster cannot shorten its path to the destination, so it stays put
def test_Scenario12():
    s = init_test()

    s.contents[70] = 'X'
    s.contents[77] = 'X'
    s.contents[84] = 'X'
    s.contents[91] = 'X'
    s.contents[98] = 'X'
    s.contents[105] = 'X'
    s.contents[106] = 'X'
    s.contents[107] = 'X'
    s.contents[108] = 'X'
    s.contents[109] = 'X'
    s.contents[102] = 'X'
    s.contents[95] = 'X'
    s.contents[88] = 'X'
    s.contents[81] = 'X'
    s.contents[74] = 'X'

    s.contents[85] = 'O'
    s.contents[93] = 'O'

    s.figures[86] = 'M'
    s.figures[92] = 'M'

    s.figures[79] = 'A'

    s.figures[99] = 'C'

    s.ACTION_MOVE = 1

    assert_answers(s,{(79, )})

# The players choose between the equally close destinations, even thought the monster can make less progress towards one of the two destinations. See this thread (https://boardgamegeek.com/article/28429917#28429917)
def test_Scenario13():
    s = init_test()

    s.figures[33] = 'A'

    s.figures[24] = 'M'

    s.contents[30] = 'O'
    s.contents[31] = 'O'

    s.figures[29] = 'C'

    s.ACTION_MOVE = 2

    assert_answers(s,{(32, ), (25, ), (38, )})

# Online test question #5
def test_Scenario14():
    s = init_test()

    s.figures[31] = 'A'

    s.figures[37] = 'M'
    s.figures[24] = 'M'

    s.contents[10] = 'O'
    s.contents[17] = 'O'
    s.contents[19] = 'O'
    s.contents[23] = 'O'
    s.contents[25] = 'O'
    s.contents[30] = 'O'
    s.contents[32] = 'O'
    s.contents[36] = 'O'
    s.contents[38] = 'O'
    s.contents[43] = 'O'
    s.contents[45] = 'O'
    s.contents[51] = 'O'

    s.contents[11] = 'T'

    s.figures[44] = 'C'

    s.ACTION_MOVE = 3

    assert_answers(s,{(11, )})

# The monster moves towards the character to which it has the stortest path, C20
def test_Scenario15():
    s = init_test()

    s.figures[17] = 'C'
    s.initiatives[17] = 10

    s.figures[51] = 'C'
    s.initiatives[51] = 20

    s.contents[24] = 'O'
    s.contents[18] = 'O'
    s.contents[31] = 'O'

    s.figures[32] = 'A'

    s.ACTION_MOVE = 2

    assert_answers(s,{(45, 51)})

# The monster chooses its focus based on the shortest path to an attack position, not the shortest path to a character's position. The monster moves towards C20
def test_Scenario16():
    s = init_test()

    s.figures[9] = 'C'
    s.initiatives[9] = 10

    s.figures[58] = 'C'
    s.initiatives[58] = 20

    s.contents[16] = 'O'
    s.contents[23] = 'O'
    s.contents[3] = 'O'
    s.contents[8] = 'O'
    s.contents[10] = 'O'

    s.figures[17] = 'M'

    s.figures[32] = 'A'

    s.ACTION_MOVE = 2

    assert_answers(s,{(45, )})

# The monster will choose its destination without consideration for which destination it can most shorten its path to. The destination is chosen based only on which destination is closest. The monster moves as far as it can down the west side of the obstacle
def test_Scenario17():
    s = init_test()

    s.figures[29] = 'C'

    s.contents[30] = 'O'
    s.contents[31] = 'O'
    s.contents[32] = 'O'
    s.contents[38] = 'O'

    s.figures[17] = 'M'
    s.figures[23] = 'M'
    s.figures[24] = 'M'

    s.figures[33] = 'A'

    s.ACTION_MOVE = 3

    assert_answers(s,{(25, )})

# The monster will path around traps if at all possible
def test_Scenario18():
    s = init_test()

    s.figures[28] = 'C'

    s.contents[31] = 'T'
    s.contents[24] = 'T'
    s.contents[25] = 'T'
    s.contents[38] = 'T'
    s.contents[39] = 'T'

    s.figures[32] = 'A'

    s.ACTION_MOVE = 2

    assert_answers(s,{(40, ), (26, )})

# The monster will move through traps if that is its only option
def test_Scenario19():
    s = init_test()

    s.figures[28] = 'C'

    s.contents[31] = 'T'
    s.contents[33] = 'T'
    s.contents[24] = 'T'
    s.contents[25] = 'T'
    s.contents[38] = 'T'
    s.contents[39] = 'T'

    s.figures[32] = 'A'

    s.ACTION_MOVE = 2

    assert_answers(s,{(30, )})

# The monster will move through the minimium number of traps possible
def test_Scenario20():
    s = init_test()

    s.figures[28] = 'C'

    s.contents[17] = 'T'
    s.contents[23] = 'T'
    s.contents[24] = 'T'
    s.contents[25] = 'T'
    s.contents[30] = 'T'
    s.contents[31] = 'T'
    s.contents[33] = 'T'
    s.contents[37] = 'T'
    s.contents[38] = 'T'
    s.contents[39] = 'T'
    s.contents[45] = 'T'
    s.contents[18] = 'T'
    s.contents[19] = 'T'
    s.contents[34] = 'T'
    s.contents[40] = 'T'
    s.contents[47] = 'T'
    s.contents[46] = 'T'

    s.figures[32] = 'A'

    s.ACTION_MOVE = 3

    assert_answers(s,{(20, )})

# Monsters will fly over tra
def test_Scenario21():
    s = init_test()

    s.figures[28] = 'C'

    s.contents[17] = 'T'
    s.contents[23] = 'T'
    s.contents[24] = 'T'
    s.contents[25] = 'T'
    s.contents[30] = 'T'
    s.contents[31] = 'T'
    s.contents[33] = 'T'
    s.contents[37] = 'T'
    s.contents[38] = 'T'
    s.contents[39] = 'T'
    s.contents[45] = 'T'
    s.contents[18] = 'T'
    s.contents[19] = 'T'
    s.contents[34] = 'T'
    s.contents[40] = 'T'
    s.contents[47] = 'T'
    s.contents[46] = 'T'

    s.figures[32] = 'A'

    s.ACTION_MOVE = 3
    s.FLYING = True

    assert_answers(s,{(29, 28)})

# Monsters will jump over tra
def test_Scenario22():
    s = init_test()

    s.figures[28] = 'C'

    s.contents[17] = 'T'
    s.contents[23] = 'T'
    s.contents[24] = 'T'
    s.contents[25] = 'T'
    s.contents[30] = 'T'
    s.contents[31] = 'T'
    s.contents[33] = 'T'
    s.contents[37] = 'T'
    s.contents[38] = 'T'
    s.contents[39] = 'T'
    s.contents[45] = 'T'
    s.contents[18] = 'T'
    s.contents[19] = 'T'
    s.contents[34] = 'T'
    s.contents[40] = 'T'
    s.contents[47] = 'T'
    s.contents[46] = 'T'

    s.figures[32] = 'A'

    s.ACTION_MOVE = 3
    s.JUMPING = True

    assert_answers(s,{(29, 28)})

# Monsters will jump over traps, but not land of them if possible
def test_Scenario23():
    s = init_test()

    s.figures[28] = 'C'

    s.contents[17] = 'T'
    s.contents[23] = 'T'
    s.contents[24] = 'T'
    s.contents[25] = 'T'
    s.contents[29] = 'T'
    s.contents[30] = 'T'
    s.contents[31] = 'T'
    s.contents[33] = 'T'
    s.contents[37] = 'T'
    s.contents[38] = 'T'
    s.contents[39] = 'T'
    s.contents[45] = 'T'
    s.contents[18] = 'T'
    s.contents[19] = 'T'
    s.contents[34] = 'T'
    s.contents[40] = 'T'
    s.contents[47] = 'T'
    s.contents[46] = 'T'

    s.figures[32] = 'A'

    s.ACTION_MOVE = 3
    s.JUMPING = True

    assert_answers(s,{(22, ), (36, )})

# The monster will focus on a character that does not require it to move through a trap or hazardous terrain, if possible
def test_Scenario24():
    s = init_test()

    s.figures[8] = 'C'
    s.initiatives[8] = 10
    s.figures[80] = 'C'
    s.initiatives[80] = 20

    s.contents[17] = 'H'
    s.contents[18] = 'H'
    s.contents[23] = 'H'
    s.contents[25] = 'H'
    s.contents[30] = 'H'
    s.contents[33] = 'H'
    s.contents[37] = 'H'
    s.contents[39] = 'H'
    s.contents[44] = 'H'
    s.contents[47] = 'H'
    s.contents[51] = 'H'
    s.contents[53] = 'H'
    s.contents[61] = 'H'
    s.contents[67] = 'H'
    s.contents[75] = 'H'
    s.contents[81] = 'H'
    s.contents[88] = 'H'
    s.contents[87] = 'H'
    s.contents[79] = 'H'
    s.contents[72] = 'H'
    s.contents[65] = 'H'
    s.contents[58] = 'H'

    s.figures[24] = 'A'

    s.ACTION_MOVE = 2

    assert_answers(s,{(38, )})

# Online test question #13
def test_Scenario25():
    s = init_test()

    s.figures[16] = 'C'
    s.initiatives[16] = 30
    s.figures[30] = 'C'
    s.initiatives[30] = 20
    s.figures[65] = 'C'
    s.initiatives[65] = 10

    s.contents[18] = 'T'

    s.contents[24] = 'O'
    s.contents[31] = 'O'
    s.contents[38] = 'O'

    s.figures[39] = 'M'
    s.figures[45] = 'M'

    s.figures[32] = 'A'

    s.ACTION_MOVE = 3

    assert_answers(s,{(46, )})

# Online test question #20
def test_Scenario26():
    s = init_test()

    s.figures[37] = 'C'
    s.initiatives[37] = 50
    s.figures[44] = 'C'
    s.initiatives[44] = 4

    s.contents[16] = 'X'
    s.contents[17] = 'X'
    s.contents[18] = 'X'
    s.contents[19] = 'X'
    s.contents[22] = 'X'
    s.contents[33] = 'X'
    s.contents[36] = 'X'
    s.contents[47] = 'X'
    s.contents[50] = 'X'
    s.contents[51] = 'X'
    s.contents[52] = 'X'
    s.contents[53] = 'X'

    s.walls[25][1] = True
    s.walls[29][1] = True
    s.walls[39][1] = True
    s.walls[43][1] = True

    s.contents[32] = 'T'

    s.contents[38] = 'O'
    s.contents[30] = 'O'

    s.figures[31] = 'M'

    s.figures[24] = 'A'

    s.ACTION_MOVE = 2

    assert_answers(s,{(39, )})

# Thin walls block movement. The monster must go around the wall
def test_Scenario27():
    s = init_test()

    s.figures[35] = 'C'

    s.contents[0] = 'X'
    s.contents[1] = 'X'
    s.contents[2] = 'X'
    s.contents[30] = 'X'
    s.contents[44] = 'X'
    s.contents[58] = 'X'
    s.contents[72] = 'X'
    s.contents[84] = 'X'
    s.contents[85] = 'X'
    s.contents[86] = 'X'
    s.walls[8][1] = True
    s.walls[22][1] = True
    s.walls[36][1] = True
    s.walls[50][1] = True
    s.walls[64][1] = True
    s.walls[78][1] = True

    s.figures[38] = 'A'

    s.ACTION_MOVE = 3

    assert_answers(s,{(16, )})

# Thin walls block melee. The monster moves through the doorway
def test_Scenario28():
    s = init_test()

    s.figures[22] = 'C'

    s.contents[0] = 'X'
    s.contents[1] = 'X'
    s.contents[2] = 'X'
    s.contents[16] = 'X'
    s.contents[30] = 'X'
    s.contents[58] = 'X'
    s.contents[72] = 'X'
    s.contents[84] = 'X'
    s.contents[85] = 'X'
    s.contents[86] = 'X'
    s.walls[8][1] = True
    s.walls[22][1] = True
    s.walls[36][1] = True
    s.walls[50][1] = True
    s.walls[64][1] = True
    s.walls[78][1] = True

    s.figures[31] = 'A'

    s.ACTION_MOVE = 3

    assert_answers(s,{(36, )})

# Range follows proximity pathing, even melee attack A melee attack cannot be performed around a thin wall. The monster moves through the door to engage from behind
def test_Scenario29():
    s = init_test()

    s.figures[36] = 'C'

    s.contents[0] = 'X'
    s.contents[1] = 'X'
    s.contents[2] = 'X'
    s.contents[16] = 'X'
    s.contents[30] = 'X'
    s.contents[58] = 'X'
    s.contents[72] = 'X'
    s.contents[84] = 'X'
    s.contents[85] = 'X'
    s.contents[86] = 'X'
    s.walls[8][1] = True
    s.walls[22][1] = True
    s.walls[36][1] = True
    s.walls[50][1] = True
    s.walls[64][1] = True
    s.walls[78][1] = True

    s.figures[44] = 'M'
    s.figures[31] = 'A'

    s.ACTION_MOVE = 3

    assert_answers(s,{(43, 36)})

# Range follows proximity pathing, even melee attack A melee attack cannot be performed around a doorway. The monster chooses the focus with the shorter path to an attack location
def test_Scenario30():
    s = init_test()

    s.figures[36] = 'C'
    s.initiatives[36] = 10
    s.figures[46] = 'C'
    s.initiatives[46] = 20

    s.contents[0] = 'X'
    s.contents[1] = 'X'
    s.contents[2] = 'X'
    s.contents[16] = 'X'
    s.contents[30] = 'X'
    s.contents[58] = 'X'
    s.contents[72] = 'X'
    s.contents[84] = 'X'
    s.contents[85] = 'X'
    s.contents[86] = 'X'
    s.walls[8][1] = True
    s.walls[22][1] = True
    s.walls[36][1] = True
    s.walls[50][1] = True
    s.walls[64][1] = True
    s.walls[78][1] = True

    # s.figures[44] = 'M'
    s.figures[31] = 'A'

    s.ACTION_MOVE = 3

    assert_answers(s,{(38, 46)})

# The monster will not move if it can attack without disadvantage from its position
def test_Scenario31():
    s = init_test()

    s.figures[36] = 'C'
    s.figures[30] = 'A'

    s.ACTION_MOVE = 1

    assert_answers(s,{(30, 36)})

# The monster will not move if in range and line of sight of its foc
def test_Scenario32():
    s = init_test()

    s.figures[29] = 'C'

    s.figures[25] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 4

    assert_answers(s,{(25, 29)})

# The monster will make the minimum move to get within range and line of sight
def test_Scenario33():
    s = init_test()

    s.figures[29] = 'C'

    s.contents[3] = 'X'
    s.contents[17] = 'X'
    s.contents[31] = 'X'
    s.walls[9][1] = True
    s.walls[23][1] = True

    s.figures[26] = 'A'

    s.ACTION_MOVE = 4
    s.ACTION_RANGE = 5

    assert_answers(s,{(39, 29), (40, 29)})

# Doorway line of sight
def test_Scenario34():
    s = init_test()

    s.figures[15] = 'C'

    s.contents[0] = 'X'
    s.contents[1] = 'X'
    s.contents[2] = 'X'
    s.contents[16] = 'X'
    s.contents[30] = 'X'
    s.contents[58] = 'X'
    s.contents[72] = 'X'
    s.contents[84] = 'X'
    s.contents[85] = 'X'
    s.contents[86] = 'X'
    s.walls[8][1] = True
    s.walls[22][1] = True
    s.walls[36][1] = True
    s.walls[50][1] = True
    s.walls[64][1] = True
    s.walls[78][1] = True

    s.figures[3] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7

    assert_answers(s,{(44, 15)})

# Doorway line of sight
def test_Scenario35():
    s = init_test()

    s.figures[21] = 'C'

    s.contents[0] = 'X'
    s.contents[1] = 'X'
    s.contents[2] = 'X'
    s.contents[16] = 'X'
    s.contents[30] = 'X'
    s.contents[58] = 'X'
    s.contents[72] = 'X'
    s.contents[84] = 'X'
    s.contents[85] = 'X'
    s.contents[86] = 'X'
    s.walls[8][1] = True
    s.walls[22][1] = True
    s.walls[36][1] = True
    s.walls[50][1] = True
    s.walls[64][1] = True
    s.walls[78][1] = True

    s.figures[3] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7

    assert_answers(s,{(44, 21), (45, 21)})

# Doorway line of sight
def test_Scenario36():
    s = init_test()

    s.figures[22] = 'C'

    s.contents[0] = 'X'
    s.contents[1] = 'X'
    s.contents[2] = 'X'
    s.contents[16] = 'X'
    s.contents[30] = 'X'
    s.contents[58] = 'X'
    s.contents[72] = 'X'
    s.contents[84] = 'X'
    s.contents[85] = 'X'
    s.contents[86] = 'X'
    s.walls[8][1] = True
    s.walls[22][1] = True
    s.walls[36][1] = True
    s.walls[50][1] = True
    s.walls[64][1] = True
    s.walls[78][1] = True

    s.figures[3] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7

    assert_answers(s, {(44, 22)})

# Doorway line of sight
def test_Scenario37():
    s = init_test()

    s.figures[28] = 'C'

    s.contents[0] = 'X'
    s.contents[1] = 'X'
    s.contents[2] = 'X'
    s.contents[16] = 'X'
    s.contents[30] = 'X'
    s.contents[58] = 'X'
    s.contents[72] = 'X'
    s.contents[84] = 'X'
    s.contents[85] = 'X'
    s.contents[86] = 'X'
    s.walls[8][1] = True
    s.walls[22][1] = True
    s.walls[36][1] = True
    s.walls[50][1] = True
    s.walls[64][1] = True
    s.walls[78][1] = True

    s.figures[3] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7

    assert_answers(s,{(37, 28)})

# Doorway line of sight
def test_Scenario38():
    s = init_test()

    s.figures[29] = 'C'

    s.contents[0] = 'X'
    s.contents[1] = 'X'
    s.contents[2] = 'X'
    s.contents[16] = 'X'
    s.contents[30] = 'X'
    s.contents[58] = 'X'
    s.contents[72] = 'X'
    s.contents[84] = 'X'
    s.contents[85] = 'X'
    s.contents[86] = 'X'
    s.walls[8][1] = True
    s.walls[22][1] = True
    s.walls[36][1] = True
    s.walls[50][1] = True
    s.walls[64][1] = True
    s.walls[78][1] = True

    s.figures[3] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7
    assert_answers(s,{(44, 29), (45, 29)})

# Doorway line of sight
def test_Scenario39():
    s = init_test()
    s.figures[35] = 'C'

    s.contents[0] = 'X'
    s.contents[1] = 'X'
    s.contents[2] = 'X'
    s.contents[16] = 'X'
    s.contents[30] = 'X'
    s.contents[58] = 'X'
    s.contents[72] = 'X'
    s.contents[84] = 'X'
    s.contents[85] = 'X'
    s.contents[86] = 'X'
    s.walls[8][1] = True
    s.walls[22][1] = True
    s.walls[36][1] = True
    s.walls[50][1] = True
    s.walls[64][1] = True
    s.walls[78][1] = True

    s.figures[3] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7

    assert_answers(s,{(40, 35), (34, 35), (37, 35),(38, 35), (39, 35)})

# Doorway line of sight
def test_Scenario40():
    s = init_test()

    s.figures[36] = 'C'

    s.contents[0] = 'X'
    s.contents[1] = 'X'
    s.contents[2] = 'X'
    s.contents[16] = 'X'
    s.contents[30] = 'X'
    s.contents[58] = 'X'
    s.contents[72] = 'X'
    s.contents[84] = 'X'
    s.contents[85] = 'X'
    s.contents[86] = 'X'
    s.walls[8][1] = True
    s.walls[22][1] = True
    s.walls[36][1] = True
    s.walls[50][1] = True
    s.walls[64][1] = True
    s.walls[78][1] = True

    s.figures[3] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7

    assert_answers(s,{(32, 36), (33, 36), (26, 36)})

# Doorway line of sight
def test_Scenario41():
    s = init_test()

    s.figures[42] = 'C'

    s.contents[0] = 'X'
    s.contents[1] = 'X'
    s.contents[2] = 'X'
    s.contents[16] = 'X'
    s.contents[30] = 'X'
    s.contents[58] = 'X'
    s.contents[72] = 'X'
    s.contents[84] = 'X'
    s.contents[85] = 'X'
    s.contents[86] = 'X'
    s.walls[8][1] = True
    s.walls[22][1] = True
    s.walls[36][1] = True
    s.walls[50][1] = True
    s.walls[64][1] = True
    s.walls[78][1] = True

    s.figures[3] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7

    assert_answers(s,{(32, 42), (33, 42), (26, 42)})

# Doorway line of sight
def test_Scenario42():
    s = init_test()

    s.figures[43] = 'C'

    s.contents[0] = 'X'
    s.contents[1] = 'X'
    s.contents[2] = 'X'
    s.contents[16] = 'X'
    s.contents[30] = 'X'
    s.contents[58] = 'X'
    s.contents[72] = 'X'
    s.contents[84] = 'X'
    s.contents[85] = 'X'
    s.contents[86] = 'X'
    s.walls[8][1] = True
    s.walls[22][1] = True
    s.walls[36][1] = True
    s.walls[50][1] = True
    s.walls[64][1] = True
    s.walls[78][1] = True

    s.figures[3] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7

    assert_answers(s,{(18, 43), (11, 43), (5, 43)})

# Doorway line of sight
def test_Scenario43():
    s = init_test()

    s.figures[44] = 'C'
    s.contents[0] = 'X'
    s.contents[1] = 'X'
    s.contents[2] = 'X'
    s.contents[16] = 'X'
    s.contents[30] = 'X'
    s.contents[58] = 'X'
    s.contents[72] = 'X'
    s.contents[84] = 'X'
    s.contents[85] = 'X'
    s.contents[86] = 'X'
    s.walls[8][1] = True
    s.walls[22][1] = True
    s.walls[36][1] = True
    s.walls[50][1] = True
    s.walls[64][1] = True
    s.walls[78][1] = True
    s.figures[3] = 'A'
    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7

    assert_answers(s,{(3, 44)})

# Doorway line of sight
def test_Scenario44():
    s = init_test()

    s.figures[7] = 'C'

    s.contents[34] = 'X'
    s.contents[33] = 'X'
    s.contents[32] = 'X'
    s.contents[30] = 'X'
    s.contents[29] = 'X'
    s.contents[28] = 'X'

    s.figures[35] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7

    assert_answers(s,{(38, 7), (31, 7)})

# Doorway line of sight
def test_Scenario45():
    s = init_test()

    s.figures[15] = 'C'

    s.contents[34] = 'X'
    s.contents[33] = 'X'
    s.contents[32] = 'X'
    s.contents[30] = 'X'
    s.contents[29] = 'X'
    s.contents[28] = 'X'

    s.figures[35] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7

    assert_answers(s, {(38, 15), (31, 15)})

# Doorway line of sight
def test_Scenario46():
    s = init_test()

    s.figures[21] = 'C'

    s.contents[34] = 'X'
    s.contents[33] = 'X'
    s.contents[32] = 'X'
    s.contents[30] = 'X'
    s.contents[29] = 'X'
    s.contents[28] = 'X'

    s.figures[35] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7

    assert_answers(s,{(31, 21)})

# Doorway line of sight
def test_Scenario47():
    s = init_test()

    s.figures[8] = 'C'

    s.contents[34] = 'X'
    s.contents[33] = 'X'
    s.contents[32] = 'X'
    s.contents[30] = 'X'
    s.contents[29] = 'X'
    s.contents[28] = 'X'

    s.figures[35] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7

    assert_answers(s,{(37, 8)})

# Doorway line of sight
def test_Scenario48():
    s = init_test()

    s.figures[16] = 'C'

    s.contents[34] = 'X'
    s.contents[33] = 'X'
    s.contents[32] = 'X'
    s.contents[30] = 'X'
    s.contents[29] = 'X'
    s.contents[28] = 'X'

    s.figures[35] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7

    assert_answers(s,{(37, 16)})

# Doorway line of sight
def test_Scenario49():
    s = init_test()

    s.figures[22] = 'C'

    s.contents[34] = 'X'
    s.contents[33] = 'X'
    s.contents[32] = 'X'
    s.contents[30] = 'X'
    s.contents[29] = 'X'
    s.contents[28] = 'X'

    s.figures[35] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7

    assert_answers(s,{(38, 22), (31, 22)})

# Doorway line of sight
def test_Scenario50():
    s = init_test()

    s.figures[9] = 'C'

    s.contents[34] = 'X'
    s.contents[33] = 'X'
    s.contents[32] = 'X'
    s.contents[30] = 'X'
    s.contents[29] = 'X'
    s.contents[28] = 'X'

    s.figures[35] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7

    assert_answers(s,{(44, 9), (37, 9)})

# Doorway line of sight
def test_Scenario51():
    s = init_test()

    s.figures[17] = 'C'

    s.contents[34] = 'X'
    s.contents[33] = 'X'
    s.contents[32] = 'X'
    s.contents[30] = 'X'
    s.contents[29] = 'X'
    s.contents[28] = 'X'

    s.figures[35] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7

    assert_answers(s, {(50, 17), (44, 17), (37, 17)})

# Doorway line of sight
def test_Scenario52():
    s = init_test()

    s.figures[23] = 'C'

    s.contents[34] = 'X'
    s.contents[33] = 'X'
    s.contents[32] = 'X'
    s.contents[30] = 'X'
    s.contents[29] = 'X'
    s.contents[28] = 'X'

    s.figures[35] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7

    assert_answers(s,{(50, 23), (44, 23), (37, 23)})

# Doorway line of sight
def test_Scenario53():
    s = init_test()

    s.figures[31] = 'C'

    s.contents[34] = 'X'
    s.contents[33] = 'X'
    s.contents[32] = 'X'
    s.contents[30] = 'X'
    s.contents[29] = 'X'
    s.contents[28] = 'X'

    s.figures[35] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7

    assert_answers(s,{(35, 31)})

# The "V" terrain piece represents an unintuitive line of sight example. The monster does not have line of sight to the character from its initial position. (https://boardgamegeek.com/image/3932301/codenamegreyfox
def test_Scenario54():
    s = init_test()

    s.figures[76] = 'C'

    s.contents[21] = 'X'
    s.contents[29] = 'X'
    s.contents[36] = 'X'
    s.contents[44] = 'X'
    s.contents[51] = 'X'
    s.contents[52] = 'X'
    s.contents[53] = 'X'
    s.contents[54] = 'X'
    s.contents[55] = 'X'
    s.contents[70] = 'X'
    s.contents[71] = 'X'
    s.contents[78] = 'X'
    s.contents[79] = 'X'
    s.contents[80] = 'X'
    s.contents[81] = 'X'
    s.contents[82] = 'X'
    s.contents[83] = 'X'
    s.walls[56][5] = True
    s.walls[62][1] = True
    s.walls[63][4] = True
    s.walls[76][1] = True

    s.figures[43] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 7

    assert_answers(s,{(49, 76), (50, 76)})

# The monster cannot trace line of sight from the vertex coincident with the tip of the thin wall. The monster must step out to attack. (https://boardgamegeek.com/image/3932321/codenamegreyfox
def test_Scenario55():
    s = init_test()

    s.figures[65] = 'C'

    s.contents[28] = 'X'
    s.contents[29] = 'X'
    s.contents[56] = 'X'
    s.contents[57] = 'X'
    s.contents[71] = 'X'
    s.contents[72] = 'X'
    s.contents[73] = 'X'
    s.contents[74] = 'X'
    s.contents[75] = 'X'
    s.contents[76] = 'X'
    s.contents[15] = 'X'
    s.contents[16] = 'X'
    s.contents[17] = 'X'
    s.contents[18] = 'X'
    s.contents[19] = 'X'
    s.contents[20] = 'X'
    s.walls[49][1] = True
    s.walls[35][1] = True
    s.walls[63][1] = True
    s.walls[21][1] = True

    s.figures[49] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 3

    assert_answers(s,{(43, 65)})

# Range is measured by pathing around walls. The character is not within range of the monster's initial position. The monster steps forward
def test_Scenario56():
    s = init_test()

    s.figures[36] = 'C'

    s.contents[16] = 'X'
    s.contents[30] = 'X'
    s.walls[22][1] = True
    s.walls[36][1] = True

    s.figures[39] = 'A'

    s.ACTION_MOVE = 1
    s.ACTION_RANGE = 3

    assert_answers(s,{(38, 36), (46, 36)})

# Online test question #7. The monster's only attack position is over the obstacle north of the character. With no other options, the monster will move through the trap
def test_Scenario57():
    s = init_test()

    s.figures[99] = 'C'

    s.contents[70] = 'X'
    s.contents[77] = 'X'
    s.contents[84] = 'X'
    s.contents[91] = 'X'
    s.contents[98] = 'X'
    s.contents[105] = 'X'
    s.contents[106] = 'X'
    s.contents[107] = 'X'
    s.contents[108] = 'X'
    s.contents[109] = 'X'
    s.contents[102] = 'X'
    s.contents[95] = 'X'
    s.contents[88] = 'X'
    s.contents[81] = 'X'
    s.contents[74] = 'X'

    s.contents[85] = 'O'
    s.contents[93] = 'O'
    s.contents[100] = 'O'

    s.contents[87] = 'T'

    s.figures[86] = 'M'
    s.figures[92] = 'M'

    s.figures[79] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 2

    assert_answers(s,{(94, )})

# Even if the monster cannot get to within range of its focus, it will get as close to an attack position as possible
def test_Scenario58():
    s = init_test()

    s.figures[29] = 'C'
    s.figures[12] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 2

    assert_answers(s,{(25, ), (10, ), (18, )})

# Even if the monster cannot get to within range of its focus, it will get as close to the nearest attack position as possible
def test_Scenario59():
    s = init_test()

    s.figures[30] = 'C'

    s.contents[9] = 'X'
    s.contents[17] = 'X'
    s.contents[24] = 'X'
    s.contents[32] = 'X'
    s.contents[39] = 'X'
    s.contents[47] = 'X'

    s.figures[25] = 'A'

    s.ACTION_MOVE = 3
    s.ACTION_RANGE = 3

    assert_answers(s,{(3, )})

# When using a ranged attack, the monster will step away from its target to avoid disadvantage
def test_Scenario60():
    s = init_test()

    s.figures[30] = 'C'

    s.contents[23] = 'O'
    s.contents[31] = 'O'
    s.contents[38] = 'O'
    s.contents[46] = 'O'
    s.contents[36] = 'O'
    s.contents[44] = 'O'
    s.contents[51] = 'O'
    s.contents[59] = 'O'

    s.figures[37] = 'A'

    s.ACTION_MOVE = 3
    s.ACTION_RANGE = 4

    assert_answers(s,{(45, 30)})

# When using a ranged attack while muddled, the monster will not step away from its target
def test_Scenario61():
    s = init_test()

    s.figures[30] = 'C'

    s.contents[23] = 'O'
    s.contents[31] = 'O'
    s.contents[38] = 'O'
    s.contents[46] = 'O'
    s.contents[36] = 'O'
    s.contents[44] = 'O'
    s.contents[51] = 'O'
    s.contents[59] = 'O'

    s.figures[37] = 'A'

    s.ACTION_MOVE = 3
    s.ACTION_RANGE = 4
    s.MUDDLED = True

    assert_answers(s,{(37, 30)})

# When using a ranged attack, the monster will not step onto a trap to avoid disadvantage
def test_Scenario62():
    s = init_test()

    s.figures[30] = 'C'

    s.contents[23] = 'O'
    s.contents[31] = 'O'
    s.contents[38] = 'O'
    s.contents[46] = 'O'
    s.contents[36] = 'O'
    s.contents[44] = 'O'
    s.contents[51] = 'O'
    s.contents[59] = 'O'

    s.contents[45] = 'T'

    s.figures[37] = 'A'

    s.ACTION_MOVE = 3
    s.ACTION_RANGE = 4

    assert_answers(s,{(37, 30)})

# The monster will move the additional step to engage both its focus and an extra target
def test_Scenario63():
    s = init_test()

    s.figures[16] = 'C'
    s.initiatives[16] = 20
    s.figures[22] = 'C'
    s.initiatives[22] = 10

    s.figures[18] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_TARGET = 2

    assert_answers(s,{(23, 16, 22)})

# Online test question #8
def test_Scenario64():
    s = init_test()

    s.figures[16] = 'C'
    s.initiatives[16] = 10
    s.figures[31] = 'C'
    s.initiatives[31] = 20
    s.figures[35] = 'C'
    s.initiatives[35] = 30

    s.contents[22] = 'T'

    s.figures[24] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 2
    s.ACTION_TARGET = 3

    assert_answers(s,{(18, 16, 31)})

# Online test question #9
def test_Scenario65():
    s = init_test()

    s.figures[16] = 'C'
    s.initiatives[16] = 10
    s.figures[31] = 'C'
    s.initiatives[31] = 20
    s.figures[35] = 'C'
    s.initiatives[35] = 30

    s.contents[22] = 'T'

    s.figures[24] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 2
    s.ACTION_TARGET = 3
    s.MUDDLED = True

    assert_answers(s,{(30, 16, 31, 35)})

# Online test question #10
def test_Scenario66():
    s = init_test()

    s.figures[16] = 'C'
    s.initiatives[16] = 10
    s.figures[31] = 'C'
    s.initiatives[31] = 20
    s.figures[35] = 'C'
    s.initiatives[35] = 30

    s.contents[22] = 'T'

    s.figures[24] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 2
    s.ACTION_TARGET = 3
    s.FLYING = True

    assert_answers(s,{(22, 16, 31, 35)})

# Online test question #11
def test_Scenario67():
    s = init_test()

    s.figures[15] = 'C'
    s.initiatives[15] = 20
    s.figures[36] = 'C'
    s.initiatives[36] = 10

    s.contents[23] = 'O'
    s.contents[29] = 'O'

    s.contents[30] = 'T'

    s.figures[22] = 'A'

    s.ACTION_MOVE = 1
    s.ACTION_RANGE = 2

    assert_answers(s,{(22, 15)})

# Online test question #12
def test_Scenario68():
    s = init_test()

    s.figures[15] = 'C'
    s.initiatives[15] = 40
    s.figures[22] = 'C'
    s.initiatives[22] = 10
    s.figures[23] = 'C'
    s.initiatives[23] = 30
    s.figures[24] = 'C'
    s.initiatives[24] = 20

    s.figures[17] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 2
    s.ACTION_TARGET = 2

    assert_answers(s,{(9, 23, 24), (10, 23, 24)})

# Online test question #14
def test_Scenario69():
    s = init_test()

    s.figures[17] = 'C'
    s.initiatives[17] = 20
    s.figures[29] = 'C'
    s.initiatives[29] = 50
    s.figures[46] = 'C'
    s.initiatives[46] = 10

    s.figures[38] = 'M'

    s.contents[37] = 'T'

    s.contents[23] = 'O'

    s.figures[30] = 'A'

    s.ACTION_MOVE = 1
    s.ACTION_RANGE = 2
    s.ACTION_TARGET = 2

    assert_answers(s,{(31, 17, 29)})

# The monster prioritizes additional targets based on their rank as a focus. Here C30 is preferred because it is in closer proximity
def test_Scenario70():
    s = init_test()

    s.figures[9] = 'C'
    s.initiatives[9] = 10
    s.figures[47] = 'C'
    s.initiatives[47] = 30
    s.figures[50] = 'C'
    s.initiatives[50] = 20

    s.figures[24] = 'A'

    s.ACTION_MOVE = 3
    s.ACTION_RANGE = 4
    s.ACTION_TARGET = 2

    assert_answers(s,{(24, 9, 47)})

# The monster prioritizes additional targets based on their rank as a focus. Here C20 is preferred because of initiative
def test_Scenario71():
    s = init_test()

    s.figures[17] = 'C'
    s.initiatives[17] = 10
    s.figures[62] = 'C'
    s.initiatives[62] = 20
    s.figures[57] = 'C'
    s.initiatives[57] = 30

    s.figures[24] = 'A'

    s.ACTION_MOVE = 3
    s.ACTION_RANGE = 3
    s.ACTION_TARGET = 2

    assert_answers(s,{(39, 17, 62)})

# The monster prioritizes additional targets based on their rank as a focus. Here C30 is preferred because the path to attacking it is shorter
def test_Scenario72():
    s = init_test()

    s.figures[17] = 'C'
    s.initiatives[17] = 10
    s.figures[62] = 'C'
    s.initiatives[62] = 20
    s.figures[57] = 'C'
    s.initiatives[57] = 30

    s.contents[32] = 'O'

    s.figures[24] = 'A'

    s.ACTION_MOVE = 3
    s.ACTION_RANGE = 3
    s.ACTION_TARGET = 2

    assert_answers(s,{(37, 17, 57)})

# The monster prioritizes additional targets based on their rank as a focus. Here it is a tie, so the players pick
def test_Scenario73():
    s = init_test()

    s.figures[17] = 'C'
    s.initiatives[17] = 10
    s.figures[62] = 'C'
    s.initiatives[62] = 99
    s.figures[57] = 'C'
    s.initiatives[57] = 99

    s.figures[24] = 'A'

    s.ACTION_MOVE = 3
    s.ACTION_RANGE = 3
    s.ACTION_TARGET = 2

    assert_answers(s,{(37, 17, 57), (39, 17, 62)})

# The monster only attacks additional targets if it can do so while still attacking its focus
def test_Scenario74():
    s = init_test()

    s.figures[9] = 'C'
    s.initiatives[9] = 10

    s.figures[29] = 'C'
    s.initiatives[29] = 20

    s.figures[32] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_TARGET = 2

    assert_answers(s,{(17, 9)})

# The monster chooses extra targets based on their priority as a focus. On ties, players choose
def test_Scenario75():
    s = init_test()

    s.figures[16] = 'C'
    s.initiatives[16] = 10
    s.figures[17] = 'C'
    s.initiatives[17] = 30
    s.figures[24] = 'C'
    s.initiatives[24] = 10
    s.figures[31] = 'C'
    s.initiatives[31] = 20
    s.figures[30] = 'C'
    s.initiatives[30] = 40
    s.figures[22] = 'C'
    s.initiatives[22] = 30

    s.figures[23] = 'A'

    s.ACTION_MOVE = 1
    s.ACTION_TARGET = 4

    assert_answers(s,{(23, 16, 22, 24, 31), (23, 16, 17, 24, 31)})

# The monster cannot reach any focus, so it does not move
def test_Scenario76():
    s = init_test()

    s.figures[30] = 'A'

    s.ACTION_MOVE = 1

    assert_answers(s,{(30, )})

# The monster cannot reach any focus, so it does not move
def test_Scenario77():
    s = init_test()

    s.figures[9] = 'C'

    s.contents[22] = 'O'
    s.contents[23] = 'O'
    s.contents[24] = 'O'
    s.contents[29] = 'O'
    s.contents[32] = 'O'
    s.contents[35] = 'O'
    s.contents[39] = 'O'
    s.contents[43] = 'O'
    s.contents[46] = 'O'
    s.contents[50] = 'O'
    s.contents[51] = 'O'
    s.contents[52] = 'O'

    s.figures[37] = 'A'

    s.ACTION_MOVE = 2

    assert_answers(s,{(37, )})

# The monster will not step on a trap to attack its focus if it has a trap-free path to attack on future tur
def test_Scenario78():
    s = init_test()

    s.figures[28] = 'C'

    s.contents[29] = 'T'

    s.figures[32] = 'A'

    s.ACTION_MOVE = 3

    assert_answers(s,{(22, ), (36, )})

# The monster moves in close to attack additional targets using its AoE
def test_Scenario79():
    s = init_test()

    s.figures[16] = 'C'
    s.figures[22] = 'C'

    s.figures[18] = 'A'

    s.aoe[25] = True
    s.aoe[31] = True
    s.aoe[32] = True

    s.ACTION_MOVE = 2

    assert_answers(s,{(23, 16, 22)})

# The monster moves in close to attack an additional target using its AoE
def test_Scenario80():
    s = init_test()

    s.figures[16] = 'C'
    s.figures[22] = 'C'

    s.figures[18] = 'A'

    s.aoe[31] = True
    s.aoe[37] = True

    s.ACTION_MOVE = 2

    assert_answers(s,{(9, 16, 22)})

# When deciding how to use its AoE, the monster prioritizes targets based on their ranking as a focus. The monster's first priority is to attack its focus, C30. After that, the next highest priority is C10
def test_Scenario81():
    s = init_test()

    s.figures[16] = 'C'
    s.initiatives[16] = 30
    s.figures[22] = 'C'
    s.initiatives[22] = 20
    s.figures[8] = 'C'
    s.initiatives[8] = 10

    s.figures[18] = 'A'

    s.aoe[31] = True
    s.aoe[37] = True

    s.ACTION_MOVE = 2

    assert_answers(s,{(23, 8, 16)})

# The monster favors C10 over C20 as its secondary target. Even with an AoE and an added target, the monster is unable to attack all three characters. From one position the monster can use its AoE to attack two targets. From another, the monster can use its additional attack. The player can choose where the monster moves
def test_Scenario82():
    s = init_test()

    s.figures[16] = 'C'
    s.initiatives[16] = 30
    s.figures[22] = 'C'
    s.initiatives[22] = 10
    s.figures[29] = 'C'
    s.initiatives[29] = 20

    s.figures[18] = 'A'

    s.aoe[31] = True
    s.aoe[37] = True

    s.ACTION_MOVE = 2
    s.ACTION_TARGET = 2

    assert_answers(s,{(23, 16, 22), (9, 16, 22)})

# The monster moves to a position where it can attack all the characters, using both its AoE and its extra attack
def test_Scenario83():
    s = init_test()

    s.figures[16] = 'C'
    s.figures[17] = 'C'
    s.figures[22] = 'C'

    s.figures[18] = 'A'

    s.aoe[31] = True
    s.aoe[37] = True

    s.ACTION_MOVE = 2
    s.ACTION_TARGET = 2

    assert_answers(s,{(9, 16, 17, 22)})

# The path to melee range of C10 is shorter than the path to C20. However, the monster can attack C20 over the obstacle with its melee AoE. Thus, the path to an attack position on C20 is shorter. The monster focuses on C20
def test_Scenario84():
    s = init_test()

    s.figures[15] = 'C'
    s.initiatives[15] = 20
    s.figures[51] = 'C'
    s.initiatives[51] = 10

    s.contents[9] = 'O'
    s.contents[16] = 'O'
    s.contents[23] = 'O'

    s.figures[19] = 'A'

    s.aoe[31] = True
    s.aoe[37] = True

    s.ACTION_MOVE = 3

    assert_answers(s,{(17, 15)})

# AoE melee attacks do not require adjacency, nor do they test range. The monster attacks from outside the room. It does not need to step into the room, as would be required to use a non-AoE melee attack
def test_Scenario85():
    s = init_test()

    s.figures[36] = 'C'

    s.contents[0] = 'X'
    s.contents[1] = 'X'
    s.contents[2] = 'X'
    s.contents[16] = 'X'
    s.contents[30] = 'X'
    s.contents[58] = 'X'
    s.contents[72] = 'X'
    s.contents[84] = 'X'
    s.contents[85] = 'X'
    s.contents[86] = 'X'
    s.walls[8][1] = True
    s.walls[22][1] = True
    s.walls[36][1] = True
    s.walls[50][1] = True
    s.walls[64][1] = True
    s.walls[78][1] = True

    s.figures[44] = 'M'
    s.figures[31] = 'A'

    s.aoe[18] = True
    s.aoe[25] = True
    s.aoe[32] = True

    s.ACTION_MOVE = 3

    assert_answers(s,{(37, 36)})

# The mirrored image of an AoE pattern can be used. The players choose which group of characters the monster attacks. If attacking the second group, the monster uses the mirrored version of its AoE pattern
def test_Scenario86():
    s = init_test()

    s.figures[18] = 'C'
    s.figures[23] = 'C'
    s.figures[24] = 'C'

    s.figures[51] = 'C'
    s.figures[52] = 'C'
    s.figures[60] = 'C'

    s.figures[36] = 'A'

    s.aoe[20] = True
    s.aoe[25] = True
    s.aoe[26] = True

    s.ACTION_MOVE = 2

    assert_answers(s,{(22, 18, 23, 24), (50, 51, 52, 60)})

# The monster rotates its ranged AoE pattern as neccessary to attack the maximum number of charcters
def test_Scenario87():
    s = init_test()

    s.figures[15] = 'C'
    s.figures[16] = 'C'
    s.figures[17] = 'C'

    s.figures[60] = 'C'
    s.figures[67] = 'C'
    s.figures[75] = 'C'

    s.figures[37] = 'A'

    s.aoe[18] = True
    s.aoe[24] = True
    s.aoe[31] = True

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 3

    assert_answers(s,{(37, 15, 16, 17), (37, 60, 67, 75)})

# Traps do not block ranged attacks. The monster stands still and attacks the character
def test_Scenario88():
    s = init_test()

    s.figures[10] = 'C'

    s.contents[22] = 'T'
    s.contents[23] = 'T'
    s.contents[24] = 'T'
    s.contents[25] = 'T'
    s.contents[26] = 'T'

    s.figures[38] = 'A'

    s.ACTION_MOVE = 3
    s.ACTION_RANGE = 4

    assert_answers(s,{(38, 10)})

# The monster focuses on the character it has the shortest path to an attack location for, avoiding traps if possible. The monster moves towards C20
def test_Scenario89():
    s = init_test()

    s.figures[17] = 'C'
    s.initiatives[17] = 10
    s.figures[53] = 'C'
    s.initiatives[53] = 20

    s.contents[22] = 'T'
    s.contents[23] = 'T'
    s.contents[24] = 'T'
    s.contents[25] = 'T'
    s.contents[26] = 'T'

    s.figures[31] = 'A'

    s.ACTION_MOVE = 1

    assert_answers(s,{(38, )})

# Traps do not block proximity. With both characters at equal pathing distance, the monster focuses on the character in closer proximity, C20
def test_Scenario90():
    s = init_test()

    s.figures[17] = 'C'
    s.initiatives[17] = 20
    s.figures[76] = 'C'
    s.initiatives[76] = 10

    s.contents[22] = 'T'
    s.contents[23] = 'T'
    s.contents[24] = 'T'
    s.contents[25] = 'T'
    s.contents[26] = 'T'

    s.figures[31] = 'A'

    s.ACTION_MOVE = 1

    assert_answers(s,{(30, )})

# Walls do block proximity. With both characters at equal pathing distance and proximity, the monster focuses on the character with the lower initiative, C10
def test_Scenario91():
    s = init_test()

    s.figures[17] = 'C'
    s.initiatives[17] = 20
    s.figures[76] = 'C'
    s.initiatives[76] = 10

    s.contents[22] = 'X'
    s.contents[23] = 'X'
    s.contents[24] = 'X'
    s.contents[25] = 'X'
    s.contents[26] = 'X'

    s.figures[31] = 'A'

    s.ACTION_MOVE = 1

    assert_answers(s,{(38, )})

# The range of AoE attacks is not affected by walls. The monster attacks the character without moving by placing its AoE on the other side of the thin wall
def test_Scenario92():
    s = init_test()

    s.figures[29] = 'C'

    s.contents[9] = 'X'
    s.contents[23] = 'X'
    s.contents[51] = 'X'
    s.contents[65] = 'X'
    s.walls[16][1] = True
    s.walls[30][1] = True
    s.walls[44][1] = True
    s.walls[58][1] = True

    s.aoe[24] = True
    s.aoe[25] = True
    s.aoe[18] = True
    s.aoe[32] = True

    s.figures[32] = 'A'

    s.ACTION_MOVE = 1
    s.ACTION_RANGE = 2

    assert_answers(s,{(32, 29)})

# Online test question #15
def test_Scenario93():
    s = init_test()

    s.figures[11] = 'C'
    s.initiatives[11] = 35
    s.figures[33] = 'C'
    s.initiatives[33] = 99
    s.figures[39] = 'C'
    s.initiatives[39] = 100
    s.figures[38] = 'C'
    s.initiatives[38] = 101

    s.contents[10] = 'O'
    s.contents[18] = 'O'

    s.contents[16] = 'T'

    s.figures[15] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 3
    s.ACTION_TARGET = 3

    assert_answers(s,{(23, 11, 33, 38)})

# Online test question #16
def test_Scenario94():
    s = init_test()

    s.figures[25] = 'C'
    s.initiatives[25] = 30
    s.figures[32] = 'C'
    s.initiatives[32] = 20
    s.figures[39] = 'C'
    s.initiatives[39] = 40
    s.figures[46] = 'C'
    s.initiatives[46] = 10

    s.figures[22] = 'A'

    s.ACTION_MOVE = 4
    s.ACTION_TARGET = 3

    assert_answers(s,{(38, 32, 39, 46)})

# Online test question #17
def test_Scenario95():
    s = init_test()

    s.figures[25] = 'C'
    s.initiatives[25] = 20
    s.figures[32] = 'C'
    s.initiatives[32] = 40
    s.figures[39] = 'C'
    s.initiatives[39] = 30
    s.figures[46] = 'C'
    s.initiatives[46] = 10

    s.figures[22] = 'A'

    s.ACTION_MOVE = 4
    s.ACTION_TARGET = 3

    assert_answers(s,{(24, 25, 32)})

# Online test question #18
def test_Scenario96():
    s = init_test()

    s.figures[25] = 'C'
    s.initiatives[25] = 40
    s.figures[32] = 'C'
    s.initiatives[32] = 20
    s.figures[39] = 'C'
    s.initiatives[39] = 10
    s.figures[46] = 'C'
    s.initiatives[46] = 30

    s.figures[22] = 'A'

    s.aoe[17] = True
    s.aoe[9] = True

    s.ACTION_MOVE = 4

    assert_answers(s,{(24, 32, 39)})

# Online test question #19
def test_Scenario97():
    s = init_test()

    s.figures[25] = 'C'
    s.initiatives[25] = 30
    s.figures[32] = 'C'
    s.initiatives[32] = 20
    s.figures[39] = 'C'
    s.initiatives[39] = 40
    s.figures[46] = 'C'
    s.initiatives[46] = 10

    s.figures[22] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_TARGET = 3

    assert_answers(s,{(38, 32, 39, 46)})

# Difficult terrain requires two movement points to enter. The monster moves only three steps towards the character
def test_Scenario98():
    s = init_test()

    s.figures[52] = 'C'

    s.contents[24] = 'D'
    s.contents[23] = 'D'

    s.contents[29] = 'X'
    s.contents[30] = 'X'
    s.contents[32] = 'X'
    s.contents[33] = 'X'
    s.contents[34] = 'X'

    s.figures[10] = 'A'

    s.ACTION_MOVE = 4

    assert_answers(s,{(31, )})

# Difficult terrain requires two movement points to enter. The monster moves only two steps towards the character
def test_Scenario99():
    s = init_test()

    s.figures[52] = 'C'

    s.contents[10] = 'D'
    s.contents[24] = 'D'
    s.contents[24] = 'D'
    s.contents[23] = 'D'
    s.contents[31] = 'D'

    s.contents[29] = 'X'
    s.contents[30] = 'X'
    s.contents[32] = 'X'
    s.contents[33] = 'X'
    s.contents[34] = 'X'

    s.figures[10] = 'A'

    s.ACTION_MOVE = 4

    assert_answers(s,{(23, ), (24, )})

# The path through the difficult terrain and the path around the difficult terrain require equal movement. The players choose
def test_Scenario100():
    s = init_test()

    s.figures[52] = 'C'

    s.contents[17] = 'D'
    s.contents[18] = 'D'
    s.contents[24] = 'D'
    s.contents[23] = 'D'
    s.contents[31] = 'D'
    s.contents[37] = 'D'
    s.contents[38] = 'D'

    s.contents[29] = 'X'
    s.contents[30] = 'X'
    s.contents[32] = 'X'
    s.contents[33] = 'X'
    s.contents[34] = 'X'

    s.figures[10] = 'A'

    s.ACTION_MOVE = 4

    assert_answers(s,{(21, ), (23, ), (24, )})

# The path around the difficult terrain is shorter than the path through the difficult terrain. The moster moves around it
def test_Scenario101():
    s = init_test()

    s.figures[52] = 'C'

    s.contents[17] = 'D'
    s.contents[18] = 'D'
    s.contents[24] = 'D'
    s.contents[23] = 'D'
    s.contents[31] = 'D'
    s.contents[37] = 'D'
    s.contents[38] = 'D'

    s.contents[30] = 'X'
    s.contents[32] = 'X'
    s.contents[33] = 'X'
    s.contents[34] = 'X'

    s.figures[10] = 'A'

    s.ACTION_MOVE = 4

    assert_answers(s,{(29, )})

# Flying monsters ignore the effects of difficult terrain. The monster moves a full four steps towards the character
def test_Scenario102():
    s = init_test()

    s.figures[52] = 'C'

    s.contents[24] = 'D'
    s.contents[23] = 'D'
    s.contents[31] = 'D'

    s.contents[29] = 'X'
    s.contents[30] = 'X'
    s.contents[32] = 'X'
    s.contents[33] = 'X'
    s.contents[34] = 'X'

    s.figures[10] = 'A'

    s.ACTION_MOVE = 4
    s.FLYING = True

    assert_answers(s,{(37, ), (38, )})

# Jumping monsters ignore the effects of difficult terrain, except on the last hex of movement. The monster moves a full four steps towards the character
def test_Scenario103():
    s = init_test()

    s.figures[52] = 'C'

    s.contents[24] = 'D'
    s.contents[23] = 'D'
    s.contents[31] = 'D'

    s.contents[29] = 'X'
    s.contents[30] = 'X'
    s.contents[32] = 'X'
    s.contents[33] = 'X'
    s.contents[34] = 'X'

    s.figures[10] = 'A'

    s.ACTION_MOVE = 4
    s.JUMPING = True

    assert_answers(s,{(37, ), (38, )})

# In Gloomhaven, jumping monsters ignore the effects of difficult terrain, except on the last hex of movement. The monster moves only three steps towards the character
def test_Scenario104():
    s = init_test()

    s.figures[52] = 'C'

    s.contents[17] = 'D'
    s.contents[18] = 'D'
    s.contents[24] = 'D'
    s.contents[23] = 'D'
    s.contents[37] = 'D'
    s.contents[38] = 'D'

    s.contents[45] = 'D'
    s.contents[46] = 'D'
    s.contents[51] = 'D'

    s.contents[29] = 'X'
    s.contents[30] = 'X'
    s.contents[32] = 'X'
    s.contents[33] = 'X'
    s.contents[34] = 'X'

    s.figures[10] = 'A'

    s.ACTION_MOVE = 4
    s.JUMPING = True

    assert_answers(s,{(31, )})

# The monster does not avoid disadvantage when it cannot attack the character. The monster stops adjacent to the character
def test_Scenario105():
    s = init_test()

    s.figures[37] = 'C'

    s.walls[30][0] = True
    s.walls[30][5] = True
    s.walls[37][0] = True
    s.walls[37][1] = True
    s.walls[31][5] = True
    s.walls[44][1] = True

    s.figures[32] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 2

    assert_answers(s,{(45, ), (30, )})

# There are two destinations that are equally valid assuming infinite movemnet for the jumping monster. THe players can choose either as the monster's destination. Because a jumping monster cannot end its movement on an obstacle, the monster will path around the obsticles. For one of the two destinations, the monster makes less progress towards the destination because the second step of movemnet does not take the monster closer to the destination
def test_Scenario106():
    s = init_test()

    s.figures[37] = 'C'

    s.contents[31] = 'O'
    s.contents[38] = 'O'

    s.figures[25] = 'A'

    s.ACTION_MOVE = 2
    s.JUMPING = True

    assert_answers(s,{(23, ), (32, )})

# A monster being on an obstacle does not allow its allies to move through it. The monster is blocked by the wall of obsticles. The monster will not move
def test_Scenario107():
    s = init_test()

    s.figures[37] = 'C'

    s.contents[21] = 'O'
    s.contents[22] = 'O'
    s.contents[23] = 'O'
    s.contents[24] = 'O'
    s.contents[25] = 'O'
    s.contents[26] = 'O'
    s.contents[27] = 'O'

    s.figures[24] = 'M'

    s.figures[17] = 'A'

    s.ACTION_MOVE = 2

    assert_answers(s,{(17, )})

# The flying monster will path through characters to reach an optimal attack position
def test_Scenario108():
    s = init_test()

    s.figures[23] = 'C'
    s.initiatives[23] = 10
    s.figures[24] = 'C'
    s.initiatives[24] = 20
    s.figures[32] = 'C'
    s.initiatives[32] = 30
    s.figures[30] = 'C'
    s.initiatives[30] = 40

    s.figures[10] = 'A'

    s.ACTION_MOVE = 3
    s.ACTION_TARGET = 4
    s.FLYING = True

    assert_answers(s,{(31, 23, 24, 30, 32)})

# The monster will use its extra attack to target its focus, using its aoe on secondary targets, because that targets the most characters
def test_Scenario109():
    s = init_test()

    s.figures[15] = 'C'
    s.initiatives[15] = 10
    s.figures[39] = 'C'
    s.initiatives[39] = 20
    s.figures[46] = 'C'
    s.initiatives[46] = 30

    s.figures[17] = 'A'

    s.aoe[24] = True
    s.aoe[25] = True

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 3
    s.ACTION_TARGET = 2

    assert_answers(s,{(17, 15, 39, 46)})

# A monster without an attack will move as if it had a melee attack
def test_Scenario110():
    s = init_test()

    s.figures[15] = 'C'

    s.figures[18] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 3
    s.ACTION_TARGET = 0

    assert_answers(s,{(16, )})

# The monster will step away to avoid disadvantage when making a range aoe attack
def test_Scenario111():
    s = init_test()

    s.figures[15] = 'C'

    s.figures[16] = 'A'

    s.aoe[24] = True
    s.aoe[25] = True

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 1

    assert_answers(s,{(17, 15), (23, 15), (9, 15)})

# The monster will avoid the trap to attack the character
def test_Scenario112():
    s = init_test()

    s.figures[15] = 'C'

    s.contents[16] = 'T'

    s.figures[18] = 'A'

    s.ACTION_MOVE = 3

    assert_answers(s,{(22, 15), (8, 15)})

# The jumping monster will avoid the trap to attack the character
def test_Scenario113():
    s = init_test()

    s.figures[15] = 'C'

    s.contents[16] = 'T'

    s.figures[18] = 'A'

    s.ACTION_MOVE = 3
    s.JUMPING = True

    assert_answers(s,{(22, 15), (8, 15)})

# The flying monster will ignore the trap to attack the character
def test_Scenario114():
    s = init_test()

    s.figures[15] = 'C'

    s.contents[16] = 'T'

    s.figures[18] = 'A'

    s.ACTION_MOVE = 3
    s.FLYING = True

    assert_answers(s,{(16, 15)})

# With no other option, the monster will move onto the trap to attack the character
def test_Scenario115():
    s = init_test()

    s.figures[15] = 'C'

    s.contents[16] = 'T'
    s.contents[8] = 'T'
    s.contents[7] = 'T'
    s.contents[14] = 'T'
    s.contents[21] = 'T'
    s.contents[22] = 'T'

    s.figures[18] = 'A'

    s.ACTION_MOVE = 3

    assert_answers(s,{(16, 15)})

# AoE attacks require line of site. The monster will move around the wall
def test_Scenario116():
    s = init_test()

    s.figures[31] = 'C'

    s.contents[24] = 'X'
    s.contents[38] = 'X'
    s.walls[31][1] = True

    s.figures[32] = 'A'

    s.aoe[25] = True

    s.ACTION_MOVE = 3

    assert_answers(s,{(17, ), (45, )})

# The closest character with the lowest initiative is the monster's focus. The monster will place its AoE to attack its focus
def test_Scenario117():
    s = init_test()

    s.figures[16] = 'C'
    s.initiatives[16] = 10
    s.figures[17] = 'C'
    s.initiatives[17] = 20
    s.figures[18] = 'C'
    s.initiatives[18] = 30

    s.figures[58] = 'C'
    s.initiatives[58] = 70
    s.figures[59] = 'C'
    s.initiatives[59] = 10
    s.figures[60] = 'C'
    s.initiatives[60] = 10

    s.figures[35] = 'A'

    s.aoe[18] = True
    s.aoe[24] = True
    s.aoe[31] = True

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 3

    assert_answers(s,{(35, 16, 17, 18)})

# The closest character with the lowest initiative is the monster's focus. The monster will place its AoE to attack its focus, even if other placements hit more targets
def test_Scenario118():
    s = init_test()

    s.figures[16] = 'C'
    s.initiatives[16] = 10

    s.figures[58] = 'C'
    s.initiatives[58] = 70
    s.figures[59] = 'C'
    s.initiatives[59] = 10
    s.figures[60] = 'C'
    s.initiatives[60] = 10

    s.figures[35] = 'A'

    s.aoe[18] = True
    s.aoe[24] = True
    s.aoe[31] = True

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 3

    assert_answers(s,{(35, 16)})

# There are two equally good focuses, so the players can choose which group the monster attacks. This is true even though choosing one of the focuses allows the monster to attack more targets
def test_Scenario119():
    s = init_test()

    s.figures[16] = 'C'
    s.initiatives[16] = 10
    s.figures[17] = 'C'
    s.initiatives[17] = 20
    s.figures[18] = 'C'
    s.initiatives[18] = 30

    s.figures[58] = 'C'
    s.initiatives[58] = 10

    s.figures[35] = 'A'

    s.aoe[18] = True
    s.aoe[24] = True
    s.aoe[31] = True

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 3

    assert_answers(s,{(35, 16, 17, 18), (35, 58)})

# There are two equally good focuses, so the players can choose which group the monster attacks. This is true even though choosing one of the focuses allows the monster to attack more favorable targets
def test_Scenario120():
    s = init_test()

    s.figures[16] = 'C'
    s.initiatives[16] = 10
    s.figures[17] = 'C'
    s.initiatives[17] = 20
    s.figures[18] = 'C'
    s.initiatives[18] = 30

    s.figures[58] = 'C'
    s.initiatives[58] = 10
    s.figures[59] = 'C'
    s.initiatives[59] = 80
    s.figures[60] = 'C'
    s.initiatives[60] = 90

    s.figures[35] = 'A'

    s.aoe[18] = True
    s.aoe[24] = True
    s.aoe[31] = True

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 3

    assert_answers(s,{(35, 16, 17, 18), (35, 58, 59, 60)})

# The monster will place its AoE to hit its focus and the most favorable set of additional targets
def test_Scenario121():
    s = init_test()

    s.figures[58] = 'C'
    s.initiatives[58] = 10
    s.figures[59] = 'C'
    s.initiatives[59] = 20
    s.figures[60] = 'C'
    s.initiatives[60] = 30
    s.figures[64] = 'C'
    s.initiatives[64] = 40
    s.figures[71] = 'C'
    s.initiatives[71] = 50

    s.figures[35] = 'A'

    s.aoe[18] = True
    s.aoe[24] = True
    s.aoe[31] = True

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 3

    assert_answers(s,{(35, 58, 59, 60)})

# A monster with an AoE attack and a target count of zero will move as if it had a melee attack and not attack
def test_Scenario122():
    s = init_test()

    s.figures[59] = 'C'

    s.figures[36] = 'A'

    s.aoe[18] = True
    s.aoe[25] = True
    s.aoe[32] = True

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 3
    s.ACTION_TARGET = 0

    assert_answers(s,{(51, )})

# All of vertices of the monster's starting hex are touching walls, so the monster does not have line of sight to any other hex. It will step forward to gain los and attack the character
def test_Scenario123():
    s = init_test()

    s.figures[36] = 'C'

    s.contents[52] = 'X'
    s.contents[66] = 'X'
    s.contents[58] = 'X'

    s.figures[59] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 4

    assert_answers(s,{(51, 36, )})

# If a monster can attack its focus this turn, it will move to do so. That is true even when there is a more optimal attack location, if it cannot reach that more optimal location this turn
def test_Scenario124():
    s = init_test()

    s.figures[26] = 'C'
    s.figures[39] = 'C'

    s.contents[29] = 'O'
    s.contents[22] = 'O'
    s.contents[16] = 'O'
    s.contents[17] = 'O'
    s.contents[18] = 'O'
    s.contents[19] = 'O'
    s.contents[20] = 'O'
    s.contents[35] = 'O'
    s.contents[43] = 'O'
    s.contents[44] = 'O'
    s.contents[45] = 'O'
    s.contents[46] = 'O'
    s.contents[47] = 'O'
    s.contents[27] = 'O'
    s.contents[34] = 'O'
    s.contents[40] = 'O'
    s.contents[31] = 'O'
    s.contents[32] = 'O'

    s.figures[36] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_TARGET = 2

    assert_answers(s,{(38, 39, )})

# If a monster cannot attack its focus this turn, it will move towards the most optimal attack location. That is true even if there is a closer attack location that is less optimal
def test_Scenario125():
    s = init_test()

    s.figures[26] = 'C'
    s.figures[39] = 'C'

    s.contents[29] = 'O'
    s.contents[22] = 'O'
    s.contents[16] = 'O'
    s.contents[17] = 'O'
    s.contents[18] = 'O'
    s.contents[19] = 'O'
    s.contents[20] = 'O'
    s.contents[35] = 'O'
    s.contents[43] = 'O'
    s.contents[44] = 'O'
    s.contents[45] = 'O'
    s.contents[46] = 'O'
    s.contents[47] = 'O'
    s.contents[27] = 'O'
    s.contents[34] = 'O'
    s.contents[40] = 'O'
    s.contents[31] = 'O'
    s.contents[32] = 'O'

    s.figures[36] = 'A'

    s.ACTION_MOVE = 1
    s.ACTION_TARGET = 2

    assert_answers(s,{(30, )})

# If the monster has multiple attack options that target its focus plus a maximum number of additional charcters, it will favor additional targets that are closest in proximty first, then it will favor targets that have lower initiative. In this case, C20 is favored over C30 due to initiative. Note that if secondary targets were instead ranked based on their quality as a focus, C30 would have been favored. That is because only two steps are required to attack C30 individually, while three steps are required to attack C20 due to the obstacle. See this ruling (https://boardgamegeek.com/article/29431623#29431623). Still looking for full clarity (https://boardgamegeek.com/article/29455803#29455803)
def test_Scenario126():
    s = init_test()

    s.figures[33] = 'C'
    s.initiatives[33] = 30
    s.figures[39] = 'C'
    s.initiatives[39] = 10
    s.figures[47] = 'C'
    s.initiatives[47] = 20

    s.contents[45] = 'O'

    s.figures[36] = 'A'

    s.aoe[25] = True
    s.aoe[26] = True

    s.ACTION_MOVE = 3

    assert_answers(s,{(32, 39, 47)})

# The players can choose either of the monster's two desintations, including the destination on difficult terrain, even though the monster can make less progress towards that destinatino. See ruling here (https://boardgamegeek.com/thread/2014493/monster-movement-question)
def test_Scenario127():
    s = init_test()

    s.figures[39] = 'C'

    s.contents[38] = 'D'

    s.figures[36] = 'A'

    s.ACTION_MOVE = 2

    assert_answers(s,{(31, ), (45, ), (37, )})

# The players can choose either of the monster's two desintations, even though the monster can only make progress towards one of them. See ruling here (https://boardgamegeek.com/thread/2014493/monster-movement-question)
def test_Scenario128():
    s = init_test()

    s.figures[39] = 'C'
    s.figures[31] = 'M'

    s.contents[38] = 'O'

    s.figures[37] = 'A'

    s.ACTION_MOVE = 1

    assert_answers(s,{(37, ), (45, )})

# The players can choose any of the monster's three desintations, even though the monster can only make progress towards two of them. See ruling here (https://boardgamegeek.com/thread/2014493/monster-movement-question)
def test_Scenario129():
    s = init_test()

    s.figures[40] = 'C'
    s.figures[31] = 'M'

    s.contents[38] = 'O'

    s.figures[37] = 'A'

    s.ACTION_MOVE = 1

    assert_answers(s,{(37, ), (45, )})

# With only a single destination, the monster takes the best path to that destination. The players cannot choose to have the monster take the path along which the monster cannot make progress. Compare to scenario #129
def test_Scenario130():
    s = init_test()

    s.figures[40] = 'C'
    s.figures[31] = 'M'

    s.contents[33] = 'O'
    s.contents[38] = 'O'
    s.contents[47] = 'O'

    s.figures[37] = 'A'

    s.ACTION_MOVE = 1

    assert_answers(s,{(45, )})

# Large number of walls and characters, high target attack, large range and move, and a large aoe to use when timing optimizations
def test_Scenario131():
    s = init_test()

    s.figures[8] = 'C'
    s.figures[17] = 'C'
    s.figures[23] = 'C'
    s.figures[26] = 'C'
    s.figures[40] = 'C'
    s.figures[46] = 'C'
    s.figures[51] = 'C'
    s.figures[54] = 'C'
    s.figures[57] = 'C'
    s.figures[58] = 'C'
    s.figures[68] = 'C'
    s.figures[80] = 'C'
    s.figures[90] = 'C'
    s.figures[92] = 'C'
    s.figures[94] = 'C'
    s.figures[102] = 'C'

    s.contents[9] = 'X'
    s.contents[25] = 'X'
    s.contents[30] = 'X'
    s.contents[38] = 'X'
    s.contents[44] = 'X'
    s.contents[47] = 'X'
    s.contents[50] = 'X'
    s.contents[53] = 'X'
    s.contents[64] = 'X'
    s.contents[65] = 'X'
    s.contents[75] = 'X'
    s.contents[76] = 'X'
    s.contents[78] = 'X'
    s.contents[88] = 'X'
    s.contents[89] = 'X'
    s.contents[93] = 'X'
    s.contents[99] = 'X'
    s.contents[104] = 'X'

    s.figures[37] = 'A'

    s.ACTION_MOVE = 7
    s.ACTION_RANGE = 7
    s.ACTION_TARGET = 5

    s.aoe[17] = True
    s.aoe[18] = True
    s.aoe[23] = True
    s.aoe[24] = True
    s.aoe[25] = True
    s.aoe[31] = True
    s.aoe[32] = True

    assert_answers(s,{(52, 17, 23, 26, 46, 51, 57, 58),(52, 17, 23, 40, 46, 51, 57, 58),(20, 8, 17, 23, 40, 46, 51, 58),})

# The monster will take a longer path to avoid traps. That is true even if it means not being able to attack its focus this turn
def test_Scenario132():
    s = init_test()

    s.figures[24] = 'C'

    s.contents[22] = 'T'

    s.contents[30] = 'O'
    s.contents[31] = 'O'
    s.contents[33] = 'O'

    s.contents[28] = 'O'
    s.contents[21] = 'O'
    s.contents[15] = 'O'
    s.contents[16] = 'O'
    s.contents[17] = 'O'
    s.contents[18] = 'O'
    s.contents[25] = 'O'
    s.contents[35] = 'O'
    s.contents[43] = 'O'
    s.contents[44] = 'O'
    s.contents[45] = 'O'
    s.contents[46] = 'O'
    s.contents[39] = 'O'

    s.figures[29] = 'A'

    s.ACTION_MOVE = 2

    assert_answers(s,{(37, )})

# The monster first uses proximity to rank secondary targets, before initiative. Because of the wall line between the monster and C10, C10 is two proximity steps away. Thus, the monster prefers C30 as its second target
def test_Scenario133():
    s = init_test()

    s.figures[38] = 'C'
    s.initiatives[38] = 10
    s.figures[44] = 'C'
    s.initiatives[44] = 30
    s.figures[45] = 'C'
    s.initiatives[45] = 20

    s.contents[59] = 'X'
    s.contents[73] = 'X'
    s.contents[31] = 'X'
    s.contents[17] = 'X'

    s.walls[23][1] = True
    s.walls[37][1] = True
    s.walls[51][1] = True
    s.walls[65][1] = True

    s.figures[30] = 'M'
    s.figures[36] = 'M'

    s.figures[37] = 'A'

    s.ACTION_MOVE = 1
    s.ACTION_RANGE = 2
    s.ACTION_TARGET = 2

    assert_answers(s,{(37, 44, 45)})

# Have clarification. Must measure range around thin wall. This answer is wrong. Waiting for clarification. See https://boardgamegeek.com/thread/2020826/question-about-measuring-range-aoe-attacks and https://boardgamegeek.com/thread/2020622/ranged-aoe-and-wall-hexe
def test_Scenario134():
    s = init_test()

    s.figures[47] = 'C'

    s.contents[59] = 'X'
    s.contents[73] = 'X'
    s.contents[31] = 'X'
    s.contents[17] = 'X'

    s.walls[23][1] = True
    s.walls[37][1] = True
    s.walls[51][1] = True
    s.walls[65][1] = True

    s.figures[36] = 'A'

    s.aoe[25] = True
    s.aoe[24] = True
    s.aoe[31] = True

    s.ACTION_MOVE = 0
    s.ACTION_RANGE = 2

    assert_answers(s,{(36, )})

# Have clarification. Cannot use wall as target point for aoe. This answer is wrong. Waiting for clarification. See https://boardgamegeek.com/thread/2020826/question-about-measuring-range-aoe-attacks and https://boardgamegeek.com/thread/2020622/ranged-aoe-and-wall-hexe
def test_Scenario135():
    s = init_test()

    s.figures[47] = 'C'

    s.contents[59] = 'X'
    s.contents[73] = 'X'
    s.contents[31] = 'X'
    s.contents[17] = 'X'
    s.contents[38] = 'X'

    s.walls[23][1] = True
    s.walls[51][1] = True
    s.walls[65][1] = True

    s.figures[36] = 'A'

    s.aoe[25] = True
    s.aoe[24] = True
    s.aoe[31] = True

    s.ACTION_MOVE = 0
    s.ACTION_RANGE = 2

    assert_answers(s,{(36, )})

# Have clarification. Cannot use wall as target point for aoe. This answer is wrong. Waiting for clarification. See https://boardgamegeek.com/thread/2020826/question-about-measuring-range-aoe-attacks and https://boardgamegeek.com/thread/2020622/ranged-aoe-and-wall-hexe
def test_Scenario136():
    s = init_test()

    s.figures[47] = 'C'

    s.contents[59] = 'X'
    s.contents[73] = 'X'
    s.contents[31] = 'X'
    s.contents[17] = 'X'
    s.contents[38] = 'X'
    s.contents[37] = 'X'

    s.walls[23][1] = True
    s.walls[51][1] = True
    s.walls[65][1] = True

    s.figures[36] = 'A'

    s.aoe[25] = True
    s.aoe[24] = True
    s.aoe[31] = True

    s.ACTION_MOVE = 0
    s.ACTION_RANGE = 2

    assert_answers(s,{(36, )})

# https://boardgamegeek.com/article/29498431#2949843
def test_Scenario137():
    s = init_test()

    s.figures[53] = 'C'
    s.initiatives[53] = 10
    s.figures[34] = 'C'
    s.initiatives[34] = 50
    s.figures[24] = 'C'
    s.initiatives[24] = 40
    s.figures[76] = 'C'
    s.initiatives[76] = 30
    s.figures[74] = 'C'
    s.initiatives[74] = 20

    s.figures[49] = 'A'

    s.ACTION_MOVE = 5
    s.ACTION_RANGE = 2
    s.ACTION_TARGET = 3

    assert_answers(s,{(67, 53, 74, 76)})

# Monsters are willing to move farther to avoid disadvantage against secondary targets
def test_Scenario138():
    s = init_test()

    s.figures[53] = 'C'
    s.initiatives[53] = 10
    s.figures[38] = 'C'
    s.initiatives[38] = 30
    s.figures[26] = 'C'
    s.initiatives[26] = 20

    s.figures[49] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 2
    s.ACTION_TARGET = 3

    assert_answers(s,{(40, 26, 38, 53)})

# Monsters are willing to move farther to avoid disadvantage against secondary targets; but this one is muddled
def test_Scenario139():
    s = init_test()

    s.figures[53] = 'C'
    s.initiatives[53] = 10
    s.figures[38] = 'C'
    s.initiatives[38] = 30
    s.figures[26] = 'C'
    s.initiatives[26] = 20

    s.figures[49] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 2
    s.ACTION_TARGET = 3
    s.MUDDLED = True

    assert_answers(s,{(39, 26, 38, 53)})

# Monsters are willing to move farther to avoid disadvantage against secondary targets; but this one is muddled
def test_Scenario140():
    s = init_test()

    s.figures[53] = 'C'
    s.initiatives[53] = 10
    s.figures[38] = 'C'
    s.initiatives[38] = 30
    s.figures[26] = 'C'
    s.initiatives[26] = 20

    s.figures[49] = 'A'

    s.ACTION_MOVE = 5
    s.ACTION_RANGE = 2
    s.ACTION_TARGET = 3

    assert_answers(s,{(39, 26, 38, 53)})

# Monster picks his secondary targets based on how far it must move to attack them, then proximity, then initiative. Here both groups can be attacked in five steps. It picks the left targets due to proximty. It ends up moving six steps to avoid disadvantage, even though it could have attacked the right targets without disadvantage in five moves. That is because targets are picked based on distance to attack. Only after picking targets does the monster adjust its destination based on avoiding disadvantage
def test_Scenario141():
    s = init_test()

    s.figures[53] = 'C'
    s.initiatives[53] = 10
    s.figures[32] = 'C'
    s.initiatives[32] = 30
    s.figures[26] = 'C'
    s.initiatives[26] = 20
    s.figures[81] = 'C'
    s.initiatives[81] = 30
    s.figures[82] = 'C'
    s.initiatives[82] = 20

    s.figures[49] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 2
    s.ACTION_TARGET = 3

    assert_answers(s,{(40, 26, 32, 53)})

# Tests a bug in the line-line collision detection causing all colinear line segments to report as colliding
def test_Scenario142():
    s = init_test()

    s.figures[32] = 'C'

    s.contents[23] = 'X'
    s.contents[24] = 'X'
    s.contents[25] = 'X'
    s.contents[33] = 'X'
    s.contents[39] = 'X'
    s.contents[47] = 'X'
    s.contents[51] = 'X'
    s.contents[53] = 'X'

    s.figures[52] = 'A'

    s.ACTION_MOVE = 0
    s.ACTION_RANGE = 3

    assert_answers(s,{(52, 32)})

# Monster does not suffer disadvantage against an adjacent target if the range to that target is two
def test_Scenario143():
    s = init_test()

    s.figures[32] = 'C'

    s.contents[23] = 'X'
    s.contents[24] = 'X'
    s.contents[25] = 'X'
    s.contents[51] = 'X'
    s.contents[52] = 'X'
    s.contents[53] = 'X'

    s.walls[31][1] = True
    s.walls[45][1] = True

    s.figures[31] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 2

    assert_answers(s,{(31, 32)})

# trap test
def test_Scenario144():
    s = init_test()

    s.figures[37] = 'C'

    s.contents[2] = 'X'
    s.contents[3] = 'X'
    s.contents[8] = 'X'
    s.contents[10] = 'X'
    s.contents[15] = 'X'
    s.contents[18] = 'X'
    s.contents[28] = 'X'
    s.contents[33] = 'X'
    s.contents[35] = 'X'
    s.contents[36] = 'X'
    s.contents[38] = 'X'
    s.contents[39] = 'X'
    s.contents[44] = 'X'
    s.contents[45] = 'X'

    s.contents[16] = 'T'
    s.contents[17] = 'T'
    s.contents[21] = 'T'
    s.contents[22] = 'T'
    s.contents[23] = 'T'
    s.contents[24] = 'T'
    s.contents[25] = 'T'
    s.contents[29] = 'T'
    s.contents[30] = 'T'
    s.contents[31] = 'T'
    s.contents[32] = 'T'

    s.walls[25][1] = True
    s.walls[25][2] = True
    s.walls[21][3] = True
    s.walls[21][4] = True

    s.figures[9] = 'A'

    s.ACTION_MOVE = 2

    assert_answers(s,{(22, ), (23, ), (24, )})

# The monster will choose to close the distance to its destination along a path that minimizes the number of traps it will trigger
def test_Scenario145():
    s = init_test()

    s.figures[34] = 'C'

    s.contents[28] = 'X'
    s.contents[21] = 'X'
    s.contents[15] = 'X'
    s.contents[16] = 'X'
    s.contents[17] = 'X'
    s.contents[18] = 'X'
    s.contents[19] = 'X'
    s.contents[20] = 'X'
    s.contents[27] = 'X'
    s.contents[35] = 'X'
    s.contents[43] = 'X'
    s.contents[44] = 'X'
    s.contents[45] = 'X'
    s.contents[46] = 'X'
    s.contents[47] = 'X'
    s.contents[48] = 'X'
    s.contents[31] = 'X'
    s.contents[32] = 'X'
    s.contents[41] = 'X'

    s.contents[23] = 'T'
    s.contents[25] = 'T'
    s.contents[39] = 'T'

    s.figures[29] = 'A'

    s.ACTION_MOVE = 3

    assert_answers(s,{(38, )})

# Monster values traps triggered on later turns equal to those triggered on this turn
def test_Scenario146():
    s = init_test()

    s.figures[32] = 'C'

    s.contents[8] = 'X'
    s.contents[9] = 'X'
    s.contents[10] = 'X'
    s.contents[11] = 'X'
    s.contents[19] = 'X'
    s.contents[23] = 'X'
    s.contents[24] = 'X'
    s.contents[15] = 'X'
    s.contents[21] = 'X'
    s.contents[28] = 'X'
    s.contents[35] = 'X'
    s.contents[43] = 'X'
    s.contents[50] = 'X'
    s.contents[31] = 'X'
    s.contents[37] = 'X'
    s.contents[38] = 'X'
    s.contents[39] = 'X'
    s.contents[51] = 'X'

    s.contents[25] = 'T'
    s.contents[18] = 'T'
    s.contents[36] = 'T'
    s.contents[44] = 'T'

    s.figures[30] = 'A'

    s.ACTION_MOVE = 3

    assert_answers(s,{(17, )})

# Tests los angles from vertices with walls
def test_Scenario147():
    s = init_test()

    s.figures[18] = 'C'

    s.walls[12][4] = 'T'
    s.walls[12][5] = 'T'

    s.figures[12] = 'A'

    s.ACTION_MOVE = 0
    s.ACTION_RANGE = 4

    assert_answers(s,{(12, )})

# Simple test of Frosthaven hex to hex (not vertex to vertex) line of sight
def test_Scenario148():
    s = init_test()

    s.figures[75] = 'C'

    s.walls[47][2] = 'T'
    s.walls[47][5] = 'T'

    s.figures[33] = 'A'

    s.ACTION_MOVE = 0
    s.ACTION_RANGE = 6

    assert_answers(s,{(33, )})

# Test Frosthaven hex-to-hex los algorithm for walls that are parallel to the sightline
def test_Scenario149():
    s = init_test()

    s.figures[11] = 'C'

    s.walls[33][4] = 'T'
    s.walls[33][5] = 'T'
    s.walls[32][2] = 'T'

    s.figures[53] = 'A'

    s.ACTION_MOVE = 0
    s.ACTION_RANGE = 6

    assert_answers(s,{(53, )})

# Line-of-sight test that is very close to fully blocked
def test_Scenario150():
    s = init_test()

    s.figures[31] = 'C'

    s.contents[32] = 'X'
    s.contents[52] = 'X'
    s.contents[61] = 'X'
    s.contents[66] = 'X'
    s.contents[88] = 'X'

    s.figures[89] = 'A'

    s.ACTION_MOVE = 0
    s.ACTION_RANGE = 9

    assert_answers(s,{(89, )})