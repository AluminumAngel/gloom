import React from 'react';
import * as C from './defines';
import OverlayHex from './OverlayHex';

export default function OverlayHexGrid( props ) {
  if ( !props.displaySolution ) {
    return null;
  }
  var hexes = [];
  var index = 0;
  for ( var c = 0; c < C.GRID_WIDTH; c++ ) {
    for ( var r = 0; r < C.GRID_HEIGHT; r++, index++ ) {
      if ( props.aoe[index] ) {
        hexes.push( <OverlayHex
          key={index}
          r={r}
          c={c}
        /> );
      }
    }
  }
  return <g>{hexes}</g>;
}