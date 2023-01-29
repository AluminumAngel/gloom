import React from 'react';
import * as C from './defines';
import SpoilerHex from './SpoilerHex';

const SpoilerHexGrid = React.memo( function( props ) {
  if ( !props.grid ) return null;

  var hexes = [];
  for ( var c = 0, index = 0; c < C.GRID_WIDTH; c++ ) {
    for ( var r = 0; r < C.GRID_HEIGHT; r++, index++ ) {
      if ( props.grid[index] ) {
        hexes.push( <SpoilerHex
          key={index}
          r={r}
          c={c}
        /> );
      }
    }
  }
  return <React.Fragment>{hexes}</React.Fragment>;
} );
export default SpoilerHexGrid;