import React from 'react';
import * as C from './defines';

const SIGHTLINE_ENDPOINT_RADIUS = 0.2 * C.SCALE;

const SightPoint = React.memo( function( props ) {
  return (
    <circle
      cx={C.SCALE * props.point[0]}
      cy={C.GRID_SCALED_HEIGHT - C.SCALE * props.point[1]}
      r={SIGHTLINE_ENDPOINT_RADIUS}
      className={props.className}
      pointerEvents='none'
    />
  );
} );
export default SightPoint;