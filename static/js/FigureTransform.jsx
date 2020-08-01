import React from 'react';

const FigureTransform = React.memo( function( props ) {
  return (
    <g transform={props.rotate ? 'rotate(-90 ' + props.x + ' ' + props.y + ')' : ''}>
      {props.children}
    </g>
  );
} );
export default FigureTransform;