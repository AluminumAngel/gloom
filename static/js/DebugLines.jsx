import React from 'react';
import * as C from './defines';

const DEBUG_CLASS_NAMES = [
  'debug',
  'debug_r',
  'debug_g',
  'debug_b',
  'debug_o',
];

const DEBUG_POINT_RADIUS = 0.2 * C.SCALE;

const DebugLines = React.memo( function( props ) {
  if ( !props.lines ) return null;

  var lines = [];
  props.lines.forEach( ( line, index ) => {
    if ( line[1].length === 2 )
    {
      lines.push(
        <line
          key={index}
          x1={C.SCALE * line[1][0][0]}
          y1={C.GRID_SCALED_HEIGHT - C.SCALE * line[1][0][1]}
          x2={C.SCALE * line[1][1][0]}
          y2={C.GRID_SCALED_HEIGHT - C.SCALE * line[1][1][1]}
          className={DEBUG_CLASS_NAMES[line[0]]}
          pointerEvents='none'
        />
      );
    }
    else
    {
      var class_index = line[0]
      var radius = DEBUG_POINT_RADIUS;
      if ( class_index > DEBUG_CLASS_NAMES.length ) {
        class_index -= DEBUG_CLASS_NAMES.length;
        radius /= 4;
      }
      lines.push(
        <circle
          key={index}
          cx={C.SCALE * line[1][0][0]}
          cy={C.GRID_SCALED_HEIGHT - C.SCALE * line[1][0][1]}
          r={radius}
          className={DEBUG_CLASS_NAMES[class_index]}
          pointerEvents='none'
        />
      );
    }
  } );
  return <React.Fragment>{lines}</React.Fragment>;
} );
export default DebugLines;