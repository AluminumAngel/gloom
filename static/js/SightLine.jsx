import React from 'react';
import HexUtils from './HexUtils';

export default function SightLine( props ) {
  const points = HexUtils.getLinePoints( props.line );
  const position_a = HexUtils.getGridHexPoint( points[0] );
  const position_b = HexUtils.getGridHexPoint( points[1] );
  return (
    <line
      x1={position_a[0]}
      y1={position_a[1]}
      x2={position_b[0]}
      y2={position_b[1]}
      className={props.className}
      pointerEvents='none'
    />
  );
}