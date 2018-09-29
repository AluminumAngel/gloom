import React from 'react';
import * as C from './defines';
import OverlayHex from './OverlayHex';

export default function OverlayHexGrid( props ) {
  if ( !props.show || !props.grid ) return null;

  var hexes = [];
  for ( var c = 0, index = 0; c < C.GRID_WIDTH; c++ ) {
    for ( var r = 0; r < C.GRID_HEIGHT; r++, index++ ) {
      if ( props.grid[index] ) {
        hexes.push( <OverlayHex
          key={index}
          r={r}
          c={c}
          content={props.content}
        /> );
      }
    }
  }
  return <React.Fragment>{hexes}</React.Fragment>;
}