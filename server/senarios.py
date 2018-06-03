# TODO should be a member function
def init( s, width, height, aoe_width, aoe_height ):
  s.MAP_WIDTH = width
  s.MAP_HEIGHT = height
  s.MAP_SIZE = s.MAP_WIDTH * s.MAP_HEIGHT
  s.MAP_CENTER = ( s.MAP_SIZE - 1 ) / 2;

  s.AOE_WIDTH = aoe_width
  s.AOE_HEIGHT = aoe_height
  s.AOE_SIZE = s.AOE_WIDTH * s.AOE_HEIGHT
  s.AOE_CENTER = ( s.AOE_SIZE - 1 ) / 2;
  if s.AOE_WIDTH != 7 or s.AOE_HEIGHT != 7:
    exit()
  if int( s.AOE_CENTER ) - s.AOE_CENTER != 0:
    exit( 'aoe has no center' )

  s.walls = [ [ False ] * 6 for _ in range( s.MAP_SIZE ) ]
  s.contents = [ ' ' ] * s.MAP_SIZE
  s.figures = [ ' ' ] * s.MAP_SIZE
  s.initiatives = [ 0 ] * s.MAP_SIZE
  s.aoe = [ False ] * s.AOE_SIZE
  s.message = ''

  s.ACTION_MOVE = 0
  s.ACTION_RANGE = 0
  s.ACTION_TARGET = 1
  s.FLYING = False
  s.JUMPING = False
  s.MUDDLED = False

# TODO should be a member function?
def init_from_test_senario( s, senario_index ):
  init( s, 16, 7, 7, 7 )

  # C : charcter
  # M : monster
  # A : active monster
  # O : obstacle
  # X : wall
  # T : trap
  # H : hazardous
  # D : difficult

  #######################################
  # 1 - simple test

  if senario_index == 1:
    s.message = 'Move towards the character and offer all valid options for the players to choose among.'

    s.figures[60] = 'C'
    s.figures[37] = 'M'
    s.figures[38] = 'M'
    s.figures[39] = 'A'

    s.ACTION_MOVE = 1

    s.correct_answer = { ( 46, ), ( 47, ) }

  #######################################
  # 2 - online test question #1

  elif senario_index == 2:
    s.message = 'Online test question #1. Shorten the path to the destination'

    s.figures[35] = 'C'
    s.figures[36] = 'M'
    s.figures[37] = 'M'
    s.figures[38] = 'A'

    s.ACTION_MOVE = 1

    s.correct_answer = { ( 45, ), ( 31, ) }

  #######################################
  # 3 - online test question #2

  elif senario_index == 3:
    s.message = 'Online test question #2. The monster cannot shorten the path to the destination, so it stays put.'

    s.figures[35] = 'C'
    s.figures[37] = 'M'
    s.figures[38] = 'M'
    s.figures[39] = 'A'

    s.ACTION_MOVE = 1

    s.correct_answer = { ( 39, ) }

  #######################################
  # 4 - online test question #6

  elif senario_index == 4:
    s.message = 'Online test question #6. The monster cannot attack the character from the near edge, so it begins the long trek around to the far edge.'

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

    s.correct_answer = { ( 34, ), ( 20, ) }

  #######################################
  # 5 - The monster will not move farther than it needs to to minimize
  # the path distance to its destination. 

  elif senario_index == 5:
    s.message = 'When shortening the path to its destination, the monster will move the minimum amount. Players cannot choose a move that puts the monster equally close to its destination, but uses more movement.'
    
    s.figures[35] = 'C'
    s.figures[30] = 'M'
    s.figures[36] = 'M'
    s.figures[37] = 'M'
    s.figures[44] = 'M'
    s.figures[38] = 'A'

    s.ACTION_MOVE = 2

    s.correct_answer = { ( 45, ), ( 31, ) }

  #######################################
  # 6 - online test question #3; test breaking focus ties with proximity

  elif senario_index == 6:
    s.message = 'When choosing focus, proximity breaks ties in path delta_length. C20 is in closer proximity.'

    s.figures[50] = 'C'
    s.initiatives[50] = 10

    s.figures[29] = 'C'
    s.initiatives[29] = 20

    s.contents[30] = 'O'
    s.figures[31] = 'A'

    s.ACTION_MOVE = 2

    s.correct_answer = { ( 36, 29 ), ( 22, 29 ) }

  #######################################
  # 7 - like 6, but test that proximity is blocked by s.walls

  elif senario_index == 7:
    s.message = 'When choosing focus, proximity breaks ties in path delta_length, but s.walls must be pathed around when testing proximity. Proximity is equal here, so initiative breaks the tie.'
    
    s.figures[50] = 'C'
    s.initiatives[50] = 10

    s.figures[29] = 'C'
    s.initiatives[29] = 20
    
    s.contents[30] = 'X'
    s.figures[31] = 'A'

    s.ACTION_MOVE = 2

    s.correct_answer = { ( 44, 50 ) }

  #######################################
  # 8 - test breaking focus ties with s.initiatives

  elif senario_index == 8:
    s.message = 'Given equal path distance and proximity, lowest initiative breaks the focus tie.'

    s.figures[9] = 'C'
    s.initiatives[9] = 10

    s.figures[29] = 'C'
    s.initiatives[29] = 20
    
    s.figures[32] = 'A'

    s.ACTION_MOVE = 2

    s.correct_answer = { ( 17, 9 ) }

  #######################################
  # 9 - test tied focus

  elif senario_index == 9:
    s.message = 'Given equal path distance, proximity, and initiative; players choose the focu'

    s.figures[9] = 'C'
    s.initiatives[9] = 99

    s.figures[29] = 'C'
    s.initiatives[29] = 99
    
    s.figures[32] = 'A'

    s.ACTION_MOVE = 2

    s.correct_answer = { ( 17, 9 ), ( 30, 29 ) }

  #######################################
  # online test question #4

  elif senario_index == 10:
    s.message = 'Online test question #4. The monster has a valid path to its destination that does not go through a trap. Even though the monster cannot shorten its path to the destination, it will not go through the trap.'

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

    s.correct_answer = { ( 79, ) }

  #######################################
  # in comments of online test question #4; monster shortens
  # distance to focus, even if it means moving off of shortest path 

  elif senario_index == 11:
    s.message = 'The monster will shorten its distance to focus, even if it means moving off the shortest path.'

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

    s.correct_answer = { ( 94, ) }

  #######################################
  # in comments of online test question #4; monster can't
  # shorten distance in only one move, so it stays put

  elif senario_index == 12:
    s.message = 'The monster cannot shorten its path to the destination, so it stays put.'
    
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

    s.correct_answer = { ( 79, ) }

  #######################################
  #

  elif senario_index == 13:
    s.message = 'The players do not choose between equally close destination Rather, the monster moves to the location that most shortens its path to any of the valid destination'

    s.figures[33] = 'A'

    s.figures[24] = 'M'

    s.contents[30] = 'O'
    s.contents[31] = 'O'

    s.figures[29] = 'C'

    s.ACTION_MOVE = 2

    s.correct_answer = { ( 38, ) }

  #######################################
  # online test question #5; moving over traps

  elif senario_index == 14:
    s.message = 'Online test question #5.'

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

    s.correct_answer = { ( 11, ) }

  #######################################
  # test that shortest path chooses focus

  elif senario_index == 15:
    s.message = 'The monster moves towards the character to which it has the stortest path, C20.'
    
    s.figures[17] = 'C'
    s.initiatives[17] = 10

    s.figures[51] = 'C'
    s.initiatives[51] = 20

    s.contents[24] = 'O'
    s.contents[18] = 'O'
    s.contents[31] = 'O'
    
    s.figures[32] = 'A'

    s.ACTION_MOVE = 2

    s.correct_answer = { ( 45, 51 ) }

  #######################################
  # test that shortest path to a legal attack chooses the focus;
  # not the shortest path to the focus itsenario

  elif senario_index == 16:
    s.message = 'The monster chooses its focus based on the shortest path to an attack position, not the shortest path to a character\'s position. The monster moves towards C20.'

    s.figures[9] = 'C'
    s.initiatives[9] = 10

    s.figures[58] = 'C'
    s.initiatives[58] = 20

    s.contents[16] = 'O'
    s.contents[23]= 'O'
    s.contents[3] = 'O'
    s.contents[8] = 'O'
    s.contents[10] = 'O'

    s.figures[17] = 'M'
    
    s.figures[32] = 'A'

    s.ACTION_MOVE = 2

    s.correct_answer = { ( 45, ) }

  #######################################
  # 17

  elif senario_index == 17:
    s.message = 'The monster will choose its destination without consideration for which destination it can most shorten its path to. The destination is chosen based only on which destination is closest. The monster moves as far as it can down the west side of the obsticle.'

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

    s.correct_answer = { ( 25, ) }

  #######################################
  # 18

  elif senario_index == 18:
    s.message = 'The monster will path around traps if at all possible.'

    s.figures[28] = 'C'

    s.contents[31] = 'T'
    s.contents[24] = 'T'
    s.contents[25] = 'T'
    s.contents[38] = 'T'
    s.contents[39] = 'T'

    s.figures[32] = 'A'

    s.ACTION_MOVE = 2

    s.correct_answer = { ( 40, ), ( 26, ) }

  #######################################
  # 19

  elif senario_index == 19:
    s.message = 'The monster will move through traps if that is its only option.'

    s.figures[28] = 'C'

    s.contents[31] = 'T'
    s.contents[33] = 'T'
    s.contents[24] = 'T'
    s.contents[25] = 'T'
    s.contents[38] = 'T'
    s.contents[39] = 'T'

    s.figures[32] = 'A'

    s.ACTION_MOVE = 2

    s.correct_answer = { ( 30, ) }

  #######################################
  # 20

  elif senario_index == 20:
    s.message = 'The monster will move through the minimium number of traps possible.'

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

    s.correct_answer = { ( 20, ) }

  #######################################
  # 21

  elif senario_index == 21:
    s.message = 'Monsters will fly over trap'

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

    s.correct_answer = { ( 29, 28 ) }

  #######################################
  # 22

  elif senario_index == 22:
    s.message = 'Monsters will jump over trap'

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

    s.correct_answer = { ( 29, 28 ) }

  #######################################
  # 23

  elif senario_index == 23:
    s.message = 'Monsters will jump over traps, but not land of them if possible.'

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

    s.correct_answer = { ( 22, ), ( 36, ) }

  #######################################
  # 21

  elif senario_index == 24:
    s.message = 'The monster will focus on a character that does not require it to move through a trap or hazardous terrain, if possible.'

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

    s.correct_answer = { ( 38, ) }

  #######################################
  # 22

  elif senario_index == 25:
    s.message = 'Online test question #13.'

    s.figures[16] = 'C'
    s.initiatives[16] = 30
    s.figures[30] = 'C'
    s.initiatives[30  ] = 20
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

    s.correct_answer = { ( 46, ) }

  #######################################
  # 23

  elif senario_index == 26:
    s.message = 'Online test question #20.'

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

    s.correct_answer = { ( 39, ) }

  #######################################
  # thin s.walls

  elif senario_index == 27:
    s.message = 'Thin s.walls block movement. The monster must go around the wall.'

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

    s.correct_answer = { ( 16, ) }

  #######################################
  # thin s.walls

  elif senario_index == 28:
    s.message = 'Thin s.walls block melee. The monster moves through the doorway.'

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

    s.correct_answer = { ( 36, ) }

  #######################################
  # thin s.walls

  elif senario_index == 29:
    s.message = 'Range follows proximity pathing, even melee attack A melee attack cannot be performed around a thin wall. The monster moves through the door to engage from behind.'

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

    s.correct_answer = { ( 43, 36 ) }

  #######################################
  # thin s.walls

  elif senario_index == 30:
    s.message = 'Range follows proximity pathing, even melee attack A melee attack cannot be performed around a doorway. The monster chooses the focus with the shorter path to an attack location.'

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

    s.correct_answer = { ( 38, 46 ) }

  #######################################
  # basic test

  elif senario_index == 31:
    s.message = 'The monster will not move if it can attack without disadvantage from its position.'

    s.figures[36] = 'C'
    s.figures[30] = 'A'

    s.ACTION_MOVE = 1

    s.correct_answer = { ( 30, 36 ) }

  #######################################
  # ranged

  elif senario_index == 32:
    s.message = 'The monster will not move if in range and line of sight of its focu'

    s.figures[29] = 'C'

    s.figures[25] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 4

    s.correct_answer = { ( 25, 29 ) }

  #######################################
  # ranged

  elif senario_index == 33:
    s.message = 'The monster will make the minimum move to get within range and line of sight.'

    s.figures[29] = 'C'

    s.contents[3] = 'X'
    s.contents[17] = 'X'
    s.contents[31] = 'X'
    s.walls[9][1] = True
    s.walls[23][1] = True

    s.figures[26] = 'A'

    s.ACTION_MOVE = 4
    s.ACTION_RANGE = 5

    s.correct_answer = { ( 39, 29 ), ( 40, 29 ) }

  #######################################
  # ranged

  elif senario_index in [ 34, 35, 36, 37, 38, 39, 40, 41, 42, 43 ]:
    s.message = 'Doorway line of sight. Use \'-l\' to draw visible hexe'

    character = [ 15, 21, 22, 28, 29, 35, 36, 42, 43, 44 ][senario_index - 34]
    s.figures[character] = 'C'

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

    s.correct_answer = [
      { ( 44, character ) },
      { ( 44, character ), ( 45, character ) },
      { ( 44, character ) },
      { ( 37, character ) },
      { ( 44, character ), ( 45, character ) },
      { ( 40, character ), ( 34, character ), ( 37, character ), ( 38, character ), ( 39, character )},
      { ( 32, character ), ( 33, character ), ( 26, character ) },
      { ( 32, character ), ( 33, character ), ( 26, character ) },
      { ( 18, character ), ( 11, character ), ( 5, character ) },
      { ( 3, character ) },
    ][senario_index - 34]

  #######################################
  # ranged

  elif senario_index in [ 44, 45, 46, 47, 48, 49, 50, 51, 52, 53 ]:
    s.message = 'Doorway line of sight. Use \'-l\' to draw visible hexe'

    character = [ 7, 15, 21, 8, 16, 22, 9, 17, 23, 31 ][senario_index - 44]
    s.figures[character] = 'C'

    s.contents[34] = 'X'
    s.contents[33] = 'X'
    s.contents[32] = 'X'
    s.contents[30] = 'X'
    s.contents[29] = 'X'
    s.contents[28] = 'X'

    s.figures[35] = 'A'

    s.ACTION_MOVE = 6
    s.ACTION_RANGE = 7

    s.correct_answer = [
      { ( 38, character ), ( 31, character ) },
      { ( 38, character ), ( 31, character ) },
      { ( 31, character ) },
      { ( 37, character ) },
      { ( 37, character ) },
      { ( 38, character ), ( 31, character ) },
      { ( 44, character ), ( 37, character ) },
      { ( 50, character ), ( 44, character ), ( 37, character ) },
      { ( 50, character ), ( 44, character ), ( 37, character ) },
      { ( 35, character ) },
    ][senario_index - 44]

  #######################################
  # https://boardgamegeek.com/image/3932301/codenamegreyfox

  elif senario_index == 54:
    s.message = 'The "V" terrain piece represents an unintuitive line of sight example. The monster does not have line of sight to the character from its initial position.'

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
    s.walls[76][1] = True

    s.figures[43] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 7

    s.correct_answer = { ( 49, 76 ), ( 50, 76 ) }

  #######################################
  # https://boardgamegeek.com/image/3932321/codenamegreyfox

  elif senario_index == 55:
    s.message = 'The monster cannot trace line of sight from the vertex coincident with the tip of the thin wall. The monster must step out to attack.'

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

    s.correct_answer = { ( 43, 65 ) }

  #######################################
  # ranged

  elif senario_index == 56:
    s.message = 'Range is measured by pathing around walls. The character is not within range of the monster\'s initial position. The monster steps forward.'

    s.figures[36] = 'C'

    s.contents[16] = 'X'
    s.contents[30] = 'X'
    s.walls[22][1] = True
    s.walls[36][1] = True

    s.figures[39] = 'A'

    s.ACTION_MOVE = 1
    s.ACTION_RANGE = 3

    s.correct_answer = { ( 38, 36 ), ( 46, 36 ) }

  #######################################
  # online test question #7

  elif senario_index == 57:
    s.message = 'Online test question #7. The monster\'s only attack position is over the obsticle north of the character. With no other options, the monster will move through the trap.'

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

    s.correct_answer = { ( 94, ) }

  #######################################
  # ranged

  elif senario_index == 58:
    s.message = 'Even if the cannot get to within range of its focus, it will get as close to an attack position as possible.'

    s.figures[29] = 'C'
    s.figures[12] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 2

    s.correct_answer = { ( 25, ), ( 10, ), ( 18, ) }

  #######################################

  #######################################
  # ranged

  elif senario_index == 59:
    s.message = 'Even if the cannot get to within range of its focus, it will get as close to the nearest attack position as possible.'

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

    s.correct_answer = { ( 3, ) }

  #######################################
  # ranged

  elif senario_index == 60:
    s.message = 'When using a ranged attack, the monster will step away from its target to avoid disadvantage.'

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

    s.correct_answer = { ( 45, 30 ) }

  #######################################
  # ranged

  elif senario_index == 61:
    s.message = 'When using a ranged attack while muddled, the monster will not step away from its target.'

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

    s.correct_answer = { ( 37, 30 ) }

  #######################################
  # ranged

  elif senario_index == 62:
    s.message = 'When using a ranged attack, the monster will not step onto a trap to avoid disadvantage.'

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

    s.correct_answer = { ( 37, 30 ) }

  #######################################
  # plus attack

  elif senario_index == 63:
    s.message = 'The monster will move the additional step to engage both its focus and an extra target.'

    s.figures[16] = 'C'
    s.initiatives[16] = 20
    s.figures[22] = 'C'
    s.initiatives[22] = 10

    s.figures[18] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_TARGET = 2

    s.correct_answer = { ( 23, 16, 22 ) }

  #######################################
  # plus attack

  elif senario_index == 64:
    s.message = 'Online test question #8.'

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

    s.correct_answer = { ( 18, 16, 31 ) }

  #######################################
  # plus attack

  elif senario_index == 65:
    s.message = 'Online test question #9.'

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

    s.correct_answer = { ( 30, 16, 31, 35 ) }

  #######################################
  # plus attack

  elif senario_index == 66:
    s.message = 'Online test question #10.'

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

    s.correct_answer = { ( 22, 16, 31, 35 ) }

  #######################################
  #

  elif senario_index == 67:
    s.message = 'Online test question #11.'

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

    s.correct_answer = { ( 22, 15 ) }

  #######################################
  #

  elif senario_index == 68:
    s.message = 'Online test question #12.'

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

    s.correct_answer = { ( 9, 23, 24 ), ( 10, 23, 24 ) }

  #######################################
  #

  elif senario_index == 69:
    s.message = 'Online test question #14.'

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

    s.correct_answer = { ( 31, 17, 29 ) }
  
  #######################################
  #

  elif senario_index == 70:
    s.message = 'The monster prioritizes additional targets based on their rank as a focu Here C30 is preferred because it is in closer proximity.'

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

    s.correct_answer = { ( 24, 9, 47 ) }

  #######################################
  #

  elif senario_index == 71:
    s.message = 'The monster prioritizes additional targets based on their rank as a focu Here C20 is preferred because of initiative.'

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

    s.correct_answer = { ( 39, 17, 62 ) }

  #######################################
  #

  elif senario_index == 72:
    s.message = 'The monster prioritizes additional targets based on their rank as a focu Here C30 is preferred because the path to attacking it is shorter.'

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

    s.correct_answer = { ( 37, 17, 57 ) }

  #######################################
  #

  elif senario_index == 73:
    s.message = 'The monster prioritizes additional targets based on their rank as a focu Here it is a tie, so the players pick.'

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

    s.correct_answer = { ( 37, 17, 57 ), ( 39, 17, 62 ) }

  #######################################
  #

  elif senario_index == 74:
    s.message = 'The monster only attacks additional targets if it can do so while still attacking its focus.'

    s.figures[9] = 'C'
    s.initiatives[9] = 10

    s.figures[29] = 'C'
    s.initiatives[29] = 20
    
    s.figures[32] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_TARGET = 2

    s.correct_answer = { ( 17, 9 ) }

  #######################################
  #

  elif senario_index == 75:
    s.message = 'The monster chooses extra targets based on their priority as a focu On ties, players choose.'

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

    s.correct_answer = { ( 23, 16, 22, 24, 31 ), ( 23, 16, 17, 24, 31 ) }

  #######################################
  #

  elif senario_index == 76:
    s.message = 'The monster cannot reach any focus, so it does not move.'

    s.figures[30] = 'A'

    s.ACTION_MOVE = 1

    s.correct_answer = { ( 30, ) }

  #######################################
  #

  elif senario_index == 77:
    s.message = 'The monster cannot reach any focus, so it does not move.'

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

    s.correct_answer = { ( 37, ) }

  #######################################
  #

  elif senario_index == 78:
    s.message = 'The monster will not step on a trap to attack its focus if it has a trap-free path to attack on future turn'

    s.figures[28] = 'C'

    s.contents[29] = 'T'

    s.figures[32] = 'A'

    s.ACTION_MOVE = 3

    s.correct_answer = { ( 22, ), ( 36, ) }

  #######################################
  #

  elif senario_index == 79:
    s.message = 'The monster moves in close to attack additional targets using its AoE.'

    s.figures[16] = 'C'
    s.figures[22] = 'C'

    s.figures[18] = 'A'

    s.aoe[25] = True
    s.aoe[31] = True
    s.aoe[32] = True

    s.ACTION_MOVE = 2

    s.correct_answer = { ( 23, 16, 22 ) }

  #######################################
  #

  elif senario_index == 80:
    s.message = 'The monster moves in close to attack an additional target using its AoE.'

    s.figures[16] = 'C'
    s.figures[22] = 'C'

    s.figures[18] = 'A'

    s.aoe[31] = True
    s.aoe[37] = True

    s.ACTION_MOVE = 2

    s.correct_answer = { ( 9, 16, 22 ) }

  #######################################
  #

  elif senario_index == 81:
    s.message = 'When deciding how to use its AoE, the monster prioritizes targets based on their ranking as a focu The monster\'s first priority is to attack its focus, C30. After that, the next highest priority is C10.'

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

    s.correct_answer = { ( 23, 8, 16 ) }

  #######################################
  #

  elif senario_index == 82:
    s.message = 'The monster favors C10 over C20 as its secondary target. Even with an AoE and an added target, the monster is unable to attack all three characters. From one position the monster can use its AoE to attack two targets. From another, the monster can use its additional attack. The player can choose where the monster moves.'

    s.figures[16] = 'C'
    s.initiatives[16] = 30
    s.figures[22] = 'C'
    s.initiatives[22] = 10
    s.figures[15] = 'C'
    s.initiatives[15] = 20

    s.figures[18] = 'A'

    s.aoe[31] = True
    s.aoe[37] = True

    s.ACTION_MOVE = 2
    s.ACTION_TARGET = 2

    s.correct_answer = { ( 23, 16, 22 ), ( 9, 16, 22 ) }

  #######################################
  #

  elif senario_index == 83:
    s.message = 'The monster moves to a position where it can attack all the characters, using both its AoE and its extra attack.'

    s.figures[16] = 'C'
    s.figures[17] = 'C'
    s.figures[22] = 'C'

    s.figures[18] = 'A'

    s.aoe[31] = True
    s.aoe[37] = True

    s.ACTION_MOVE = 2
    s.ACTION_TARGET = 2

    s.correct_answer = { ( 9, 16, 17, 22 ) }

  #######################################
  #

  elif senario_index == 84:
    s.message = 'The path to melee range of C10 is shorter than the path to C20. However, the monster can attack C20 over the obsticle with its melee AoE. Thus, the path to an attack position on C20 is shorter. The monster focuses on C20.'

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

    s.correct_answer = { ( 17, 15 ) }

  #######################################
  # thin s.walls and AoE

  elif senario_index == 85:
    s.message = 'AoE melee attacks do not require adjacency, nor do they test range. The monster attacks from outside the room. It does not need to step into the room, as would be required to use a non-AoE melee attack.'

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

    s.correct_answer = { ( 37, 36 ) }

  #######################################
  #

  elif senario_index == 86:
    s.message = 'The mirrored image of an AoE pattern can be used. The players choose which group of characters the monster attacks. If attacking the second group, the monster uses the mirrored version of its AoE pattern.'

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

    s.correct_answer = { ( 22, 18, 23, 24), ( 50, 51, 52, 60 ) }

  #######################################
  #

  elif senario_index == 87:
    s.message = 'The monster rotates its ranged AoE pattern as neccessary to attack the maximum number of charcters.'

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

    s.correct_answer = { ( 37, 15, 16, 17 ), ( 37, 60, 67, 75 ) }

  #######################################
  #

  elif senario_index == 88:
    s.message = 'Traps do not block ranged attacks. The monster stands still and attacks the character.'

    s.figures[10] = 'C'

    s.contents[22] = 'T'
    s.contents[23] = 'T'
    s.contents[24] = 'T'
    s.contents[25] = 'T'
    s.contents[26] = 'T'

    s.figures[38] = 'A'

    s.ACTION_MOVE = 3
    s.ACTION_RANGE = 4

    s.correct_answer = { ( 38, 10 ) }

  #######################################
  #

  elif senario_index == 89:
    s.message = 'The monster focuses on the character it has the shortest path to an attack location for, avoiding traps if possible. The monster moves towards C20.'

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

    s.correct_answer = { ( 38, ) }

  #######################################
  #

  elif senario_index == 90:
    s.message = 'Traps do not block proximity. With both characters at equal pathing distance, the monster focuses on the character in closer proximity, C20.'

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

    s.correct_answer = { ( 30, ) }
    
  #######################################
  #

  elif senario_index == 91:
    s.message = 'Walls do block proximity. With both characters at equal pathing distance and proximity, the monster focuses on the character with the lower initiative, C10.'

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

    s.correct_answer = { ( 38, ) }
    
  #######################################
  #

  elif senario_index == 92:
    s.message = 'The range of AoE attacks is not affected by walls. The monster attacks the character without moving by placing its AoE on the other side of the thin wall.'

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

    s.correct_answer = { ( 32, 29 ) }
    
  #######################################
  #

  elif senario_index == 93:
    s.message = 'Online test question #15.'

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

    s.correct_answer = { ( 23, 11, 33, 38 ) }
    
  #######################################
  #

  elif senario_index == 94:
    s.message = 'Online test question #16.'

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

    s.correct_answer = { ( 38, 32, 39, 46 ) }
    
  #######################################
  #

  elif senario_index == 95:
    s.message = 'Online test question #17.'

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

    s.correct_answer = { ( 24, 25, 32 ) }

  #######################################
  #

  elif senario_index == 96:
    s.message = 'Online test question #18.'

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

    s.correct_answer = { ( 38, 25, 32 ) }

  #######################################
  #

  elif senario_index == 97:
    s.message = 'Online test question #19.'

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

    s.correct_answer = { ( 33, 25, 32, 39 ) }

  #######################################
  #

  elif senario_index == 98:
    s.message = 'Difficult terrain requires two movement points to enter. The monster moves only three steps towards the character.'

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

    s.correct_answer = { ( 31, ) }

  #######################################
  #

  elif senario_index == 99:
    s.message = 'Difficult terrain requires two movement points to enter. The monster moves only two steps towards the character.'

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

    s.correct_answer = { ( 23, ), ( 24, ) }

  #######################################
  #

  elif senario_index == 100:
    s.message = 'The path through the difficult terrain and the path around the difficult terrain require equal movement. The players choose.'

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

    s.correct_answer = { ( 21, ), ( 23, ), ( 24, ) }

  #######################################
  #

  elif senario_index == 101:
    s.message = 'The path around the difficult terrain is shorter than the path through the difficult terrain. The moster moves around it.'

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

    s.correct_answer = { ( 29, ) }

  #######################################
  #

  elif senario_index == 102:
    s.message = 'Flying monsters ignore the effects of difficult terrain. The monster moves a full four steps towards the character.'

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

    s.correct_answer = { ( 37, ), ( 38, ) }

  #######################################
  #

  elif senario_index == 103:
    s.message = 'Jumping monsters ignore the effects of difficult terrain, except on the last hex of movement. The monster moves a full four steps towards the character.'

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

    s.correct_answer = { ( 37, ), ( 38, ) }

  #######################################
  #

  elif senario_index == 104:
    s.message = 'Jumping monsters ignore the effects of difficult terrain, except on the last hex of movement. The monster moves only three steps towards the character.'

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

    s.correct_answer = { ( 31, ) }

  #######################################
  #

  elif senario_index == 105:
    s.message = 'The monster does not avoid disadvantage when it cannot attack the character. The monster stops adjacent to the character.'

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

    s.correct_answer = { ( 45, ), ( 30, ) }

  #######################################
  #

  elif senario_index == 106:
    s.message = 'A jumping monster cannot end its movement on an obsticle. The monster with path around the obsticle.'

    s.figures[37] = 'C'

    s.contents[31] = 'O'
    s.contents[38] = 'O'

    s.figures[25] = 'A'

    s.ACTION_MOVE = 2
    s.JUMPING = True

    s.correct_answer = { ( 23, ) }

  #######################################
  #

  elif senario_index == 107:
    s.message = 'A monster being on an obsticle does not allow its allies to move through it. The monster is blocked by the wall of obsticles. The monster will not move.'

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

    s.correct_answer = { ( 17, ) }

  #######################################
  #

  elif senario_index == 108:
    s.message = 'The flying monster will path through characters to reach an optimal attack position.'

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

    s.correct_answer = { ( 31, 23, 24, 30, 32 ) }

  #######################################
  #

  elif senario_index == 109:
    s.message = 'The monster will use its extra attack to target its focus, using its aoe on secondary targets, because that targets the most characters.'

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

    s.correct_answer = { ( 17, 15, 39, 46 ) }

  #######################################
  #

  elif senario_index == 110:
    s.message = 'A monster without an attack will move as if it had a melee attack.'

    s.figures[15] = 'C'

    s.figures[18] = 'A'

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 3
    s.ACTION_TARGET = 0

    s.correct_answer = { ( 16, ) }

  #######################################
  #

  elif senario_index == 111:
    s.message = 'The monster will step away to avoid disadvantage when making a range aoe attack.'

    s.figures[15] = 'C'

    s.figures[16] = 'A'

    s.aoe[24] = True
    s.aoe[25] = True

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 1

    s.correct_answer = { ( 17, 15 ), ( 23, 15 ), ( 9, 15 ) }

  #######################################
  #

  elif senario_index == 112:
    s.message = 'The monster will avoid the trap to attack the character.'

    s.figures[15] = 'C'

    s.contents[16] = 'T'

    s.figures[18] = 'A'

    s.ACTION_MOVE = 3

    s.correct_answer = { ( 22, 15 ), ( 8, 15 ) }

  #######################################
  #

  elif senario_index == 113:
    s.message = 'The jumping monster will avoid the trap to attack the character.'

    s.figures[15] = 'C'

    s.contents[16] = 'T'

    s.figures[18] = 'A'

    s.ACTION_MOVE = 3
    s.JUMPING = True

    s.correct_answer = { ( 22, 15 ), ( 8, 15 ) }

  #######################################
  #

  elif senario_index == 114:
    s.message = 'The flying monster will ignore the trap to attack the character.'

    s.figures[15] = 'C'

    s.contents[16] = 'T'

    s.figures[18] = 'A'

    s.ACTION_MOVE = 3
    s.FLYING = True

    s.correct_answer = { ( 16, 15 ) }

  #######################################
  #

  elif senario_index == 115:
    s.message = 'With no other option, the monster will move onto the trap to attack the character.'

    s.figures[15] = 'C'

    s.contents[16] = 'T'
    s.contents[8] = 'T'
    s.contents[7] = 'T'
    s.contents[14] = 'T'
    s.contents[21] = 'T'
    s.contents[22] = 'T'

    s.figures[18] = 'A'

    s.ACTION_MOVE = 3

    s.correct_answer = { ( 16, 15 ) }

  #######################################
  #

  elif senario_index == 116:
    s.message = 'AoE attacks require line of site. The monster will move around the wall.'

    s.figures[31] = 'C'

    s.contents[24] = 'X'
    s.contents[38] = 'X'
    s.walls[31][1] = True

    s.figures[32] = 'A'

    s.aoe[25] = True

    s.ACTION_MOVE = 3

    s.correct_answer = { ( 17, ), ( 45, ) }

  #######################################
  #

  elif senario_index == 117:
    s.message = 'The closest character with the lowest initiative is the monster\'s focus. The monster will place its AoE to attack its focus.'

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

    s.correct_answer = { ( 35, 16, 17, 18 ) }

  #######################################
  #

  elif senario_index == 118:
    s.message = 'The closest character with the lowest initiative is the monster\'s focus. The monster will place its AoE to attack its focus, even if other placements hit more targets.'

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

    s.correct_answer = { ( 35, 16 ) }

  #######################################
  #

  elif senario_index == 119:
    s.message = 'There are two equally good focuses, so the players can choose which group the monster attacks. This is true even though choosing one of the focuses allows the monster to attack more targets.'

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

    s.correct_answer = { ( 35, 16, 17, 18 ), ( 35, 58 ) }

  #######################################
  #

  elif senario_index == 120:
    s.message = 'There are two equally good focuses, so the players can choose which group the monster attacks. This is true even though choosing one of the focuses allows the monster to attack more favorable targets.'

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

    s.correct_answer = { ( 35, 16, 17, 18 ), ( 35, 58, 59, 60 ) }

  #######################################
  #

  elif senario_index == 121:
    s.message = 'The monster will place its AoE to hit its focus and the most favorable set of additional targets.'

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

    s.correct_answer = { ( 35, 58, 59, 60 ) }

  #######################################
  #

  elif senario_index == 122:
    s.message = 'A monster with an AoE attack and a target count of zero will move as if it had a melee attack and not attack.'

    s.figures[59] = 'C'

    s.figures[36] = 'A'

    s.aoe[18] = True
    s.aoe[25] = True
    s.aoe[32] = True

    s.ACTION_MOVE = 2
    s.ACTION_RANGE = 3
    s.ACTION_TARGET = 0

    s.correct_answer = { ( 51, ) }

  #######################################
  #

  # elif senario_index == 123:
  #   s.message = ''

  #   s.figures[59] = 'C'

  #   s.figures[36] = 'A'

  #   s.aoe[31] = True
  #   s.aoe[24] = True
  #   s.aoe[23] = True

  #   s.ACTION_MOVE = 2
  #   s.ACTION_RANGE = 3

  #   s.correct_answer = { ( 51, ) }

  #######################################

  else:
    s.valid = False

  for content in s.contents:
    if content not in [ ' ', 'O', 'X', 'T', 'H', 'D' ]:
      exit( 'invalid content \'%s\'' % content )
  for figure in s.figures:
    if figure not in [ ' ', 'C', 'A', 'M' ]:
      exit( 'invalid figure \'%s\'' % figure )