import React from 'react';
import * as C from './defines';
import BorderHex from './BorderHex';

export default function BorderGrid( props ) {
  var hexes = [];
  var index = 0;
  var c;
  var r
  for ( c = -1, r = 0; r < C.GRID_HEIGHT; r++, index++ ) {
    hexes.push( <BorderHex key={index} r={r} c={c}/> );
  }
  for ( c = C.GRID_WIDTH, r = 0; r < C.GRID_HEIGHT; r++, index++ ) {
    hexes.push( <BorderHex key={index} r={r} c={c}/> );
  }
  for ( c = 0, r = -1; c < C.GRID_WIDTH; c++, index++ ) {
    hexes.push( <BorderHex key={index} r={r} c={c}/> );
  }
  for ( c = -1, r = C.GRID_HEIGHT; c < C.GRID_WIDTH; c++, index++ ) {
    hexes.push( <BorderHex key={index} r={r} c={c}/> );
  }
  return <g mask='url(#edge-fade)'>{hexes}</g>;
}