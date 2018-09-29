import React from 'react';
import * as C from './defines';
import Wall from './Wall';

export default function WallGrid( props ) {
  var walls = [];
  var index = 0;
  for ( var c = 0; c < C.GRID_WIDTH; c++ ) {
    for ( var r = 0; r < C.GRID_HEIGHT; r++ ) {
      for ( var side = 0; side < 3; side++, index++ ) {
        walls.push( <Wall
          key={index}
          r={r}
          c={c}
          side={side}
          wall={props.walls[index]}
          index={index}
          active={props.activeWalls}
          onClick={props.onWallClick}
        /> );
      }
    }
  }
  return <React.Fragment>{walls}</React.Fragment>;
}