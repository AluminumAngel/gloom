import React from 'react';
import * as C from './defines';
import AOEHex from './AOEHex';

export default function AOEHexGrid( props ) {
  const skip_list = [ 0, 1, 6, 7, 13, 14, 28, 35, 41, 42, 43, 48 ];
  var hexes = [];
  var index = 0;
  for ( var c = 0; c < C.AOE_WIDTH; c++ ) {
    for ( var r = 0; r < C.AOE_HEIGHT; r++, index++ ) {
      if ( skip_list.indexOf( index ) === -1 ) {
        hexes.push( <AOEHex
          key={index}
          r={r}
          c={c}
          content={props.grid[index]}
          index={index}
          melee={props.melee}
          onClick={props.onHexClick}
        /> );
      }
    }
  }
  return <g>{hexes}</g>;
}