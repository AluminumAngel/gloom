export const EMPTY = 0;

export const OBSTACLE = 1;
export const WALL = 2;
export const TRAP = 3;
export const HAZARDOUS_TERRAIN = 4;
export const DIFFICULT_TERRAIN = 5;
export const ICY_TERRAIN = 6;
export const FIRST_TERRAIN_BRUSH = OBSTACLE;
export const LAST_TERRAIN_BRUSH = ICY_TERRAIN;

export const CHARACTER = 7;
export const MONSTER = 8;
export const FIRST_FIGURE_BRUSH = CHARACTER;
export const LAST_FIGURE_BRUSH = MONSTER;

export const ACTIVE_CHARACTER = 9;
export const ACTIVE_MONSTER = 10;
export const CHARACTER_DESTINATION = 11;
export const MONSTER_DESTINATION = 12;
export const FIRST_ACTIVE_BRUSH = ACTIVE_CHARACTER;

export const ACTIVE_FIGURE = 13;
export const THIN_WALL = 14;
export const PROGRESS = 15;
export const FIRST_ACTION_BRUSH = ACTIVE_FIGURE;