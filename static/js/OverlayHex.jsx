import React from 'react';
import HexUtils from './HexUtils';

export default function OverlayHex( props ) {
  return (
    <polygon
      className='aoe'
      points={HexUtils.getGridHexPoints( props.c, props.r )}
      pointerEvents='none'
    />
  );
}