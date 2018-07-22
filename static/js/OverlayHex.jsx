import React from 'react';
import HexUtils from './HexUtils';

const CLASS_NAMES = [
  'aoe-coverage',
  'reach',
  'sight',
];

export default function OverlayHex( props ) {
  return (
    <polygon
      className={CLASS_NAMES[props.content]}
      points={HexUtils.getGridHexPoints( props.c, props.r )}
      pointerEvents='none'
    />
  );
}