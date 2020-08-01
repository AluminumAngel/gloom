import React from 'react';
import * as C from './defines';

const FigureSelectionHighlight = React.memo( function( props ) {
  return (
    <circle
      className='selection-highlight'
      cx={props.x}
      cy={props.y}
      r={C.FIGURE_RADIUS + 1.5}
      pointerEvents='none'
    />
  );
} );
export default FigureSelectionHighlight;