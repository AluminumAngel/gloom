import React from 'react';
import HexUtils from './HexUtils';

const SpoilerHex = React.memo( function( props ) {
  return (
    <polygon
      className='spoiler'
      points={HexUtils.getGridHexPoints( props.c, props.r )}
      pointerEvents='none'
    />
  );
} );
export default SpoilerHex;