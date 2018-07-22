import React from 'react';
import * as C from './defines';
import OverlayHex from './OverlayHex';

export default function OverlayHexGrid( props ) {
  if ( !props.displaySolution ) {
    return null;
  }
  var hexes = [];
  for ( var c = 0, index = 0; c < C.GRID_WIDTH; c++ ) {
    for ( var r = 0; r < C.GRID_HEIGHT; r++, index++ ) {
      if ( props.aoe[index] ) {
        hexes.push( <OverlayHex
          key={index}
          r={r}
          c={c}
          content={0}
        /> );
      }
    }
  }
  for ( var c = 0, index = 0; c < C.GRID_WIDTH; c++ ) {
    for ( var r = 0; r < C.GRID_HEIGHT; r++, index++ ) {
      if ( props.reach[index] ) {
        hexes.push( <OverlayHex
          key={index + C.GRID_SIZE}
          r={r}
          c={c}
          content={1}
        /> );
      }
    }
  }
  for ( var c = 0, index = 0; c < C.GRID_WIDTH; c++ ) {
    for ( var r = 0; r < C.GRID_HEIGHT; r++, index++ ) {
      if ( props.sight[index] ) {
        hexes.push( <OverlayHex
          key={index + 2 * C.GRID_SIZE}
          r={r}
          c={c}
          content={2}
        /> );
      }
    }
  }
  return <g>{hexes}</g>;
}