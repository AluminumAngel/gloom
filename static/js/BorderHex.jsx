import React from 'react';
import HexUtils from './HexUtils';

const BorderHex = React.memo( function( props ) {
  return (
    <polygon
      className='empty'
      points={HexUtils.getGridHexPoints( props.c, props.r )}
      pointerEvents='none'
    />
  );
} );
export default BorderHex;