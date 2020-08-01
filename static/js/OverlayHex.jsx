import React from 'react';
import HexUtils from './HexUtils';

const CLASS_NAMES = [
  'aoe-coverage',
  'reach',
  'sight',
];

const OverlayHex = React.memo( function( props ) {
  return (
    <polygon
      className={CLASS_NAMES[props.content]}
      points={HexUtils.getGridHexPoints( props.c, props.r )}
      pointerEvents='none'
    />
  );
} );
export default OverlayHex;