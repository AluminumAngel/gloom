import React from 'react';
import * as C from './defines';
import * as AOE_BRUSH from './aoe_brushes';
import AOEHex from './AOEHex';

const AOE_CENTER = ( C.AOE_SIZE - 1 ) / 2;
const AOE_CENTER_ROW = ( C.AOE_HEIGHT - 1 ) / 2;
const AOE_CENTER_COLUMN = ( C.AOE_WIDTH - 1 ) / 2;

export default function AOEHexGrid( props ) {
  var hexes = [];

  if ( props.melee ) {
    hexes.push( <AOEHex
      key={AOE_CENTER}
      r={AOE_CENTER_ROW}
      c={AOE_CENTER_COLUMN}
      content={AOE_BRUSH.CENTER}
      index={AOE_CENTER}
      onClick={null}
    /> );
  }

  for ( var c = 0, index = 0; c < C.AOE_WIDTH; c++ ) {
    for ( var r = 0; r < C.AOE_HEIGHT; r++, index++ ) {
      if ( index !== AOE_CENTER || !props.melee ) {
        if ( C.AOE_GRID_SKIP_LIST.indexOf( index ) === -1 ) {
          if ( !props.grid[index] ) {
            hexes.push( <AOEHex
              key={index}
              r={r}
              c={c}
              content={AOE_BRUSH.EMPTY}
              index={index}
              onClick={props.onHexClick}
            /> );
          }
        }
      }
    }
  }

  for ( var c = 0, index = 0; c < C.AOE_WIDTH; c++ ) {
    for ( var r = 0; r < C.AOE_HEIGHT; r++, index++ ) {
      if ( index !== AOE_CENTER || !props.melee ) {
        if ( C.AOE_GRID_SKIP_LIST.indexOf( index ) === -1 ) {
          if ( props.grid[index] ) {
            hexes.push( <AOEHex
              key={index}
              r={r}
              c={c}
              content={AOE_BRUSH.SET}
              index={index}
              onClick={props.onHexClick}
            /> );
          }
        }
      }
    }
  }

  return <React.Fragment>{hexes}</React.Fragment>;
}