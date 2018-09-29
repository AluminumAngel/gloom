import React from 'react';
import * as C from './defines';
import Hex from './Hex';

export default function HexGrid( props ) {
  var hexes = [];
  for ( var c = 0, index = 0; c < C.GRID_WIDTH; c++ ) {
    for ( var r = 0; r < C.GRID_HEIGHT; r++, index++ ) {
      hexes.push( <Hex
        key={index}
        r={r}
        c={c}
        content={props.grid[index]}
        index={index}
        active={props.activeHexes}
        onClick={props.onHexClick}
        onMouseDown={props.onHexMouseDown}
        onMouseUp={props.onHexMouseUp}
      /> );
    }
  }
  return <React.Fragment>{hexes}</React.Fragment>;
}