import React from 'react';
import * as C from './defines';

export default function FigureSelectionHighlight( props ) {
  return (
    <circle
      className='selection-highlight'
      cx={props.x}
      cy={props.y}
      r={C.FIGURE_RADIUS + 1.5}
      pointerEvents='none'
    />
  );
}
