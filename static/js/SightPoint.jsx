import React from 'react';
import * as C from './defines';
import HexUtils from './HexUtils';

const SIGHTLINE_ENDPOINT_RADIUS = 0.2 * C.SCALE;

export default function SightPoint( props ) {
  const position = HexUtils.getGridHexPoint( props.point );
  return (
    <circle
      cx={position[0]}
      cy={position[1]}
      r={SIGHTLINE_ENDPOINT_RADIUS}
      className={props.className}
      pointerEvents='none'
    />
  );
}