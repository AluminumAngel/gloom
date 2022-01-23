import React from 'react';
import * as C from './defines';

const SightLine = React.memo( function( props ) {
  return (
    <line
      x1={C.SCALE * props.line[0][0]}
      y1={C.GRID_SCALED_HEIGHT - C.SCALE * props.line[0][1]}
      x2={C.SCALE * props.line[1][0]}
      y2={C.GRID_SCALED_HEIGHT - C.SCALE * props.line[1][1]}
      className={props.className}
      pointerEvents='none'
    />
  );
} );
export default SightLine;