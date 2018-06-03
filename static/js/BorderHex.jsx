import React from 'react';
import HexUtils from './HexUtils';

export default function BorderHex( props ) {
  return (
    <polygon
      className='empty'
      points={HexUtils.getGridHexPoints( props.c, props.r )}
      pointerEvents='none'
    />
  );
}