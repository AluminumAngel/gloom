import React from 'react';

export default function FigureTransform( props ) {
  return (
    <g transform={props.rotate ? 'rotate(-90 ' + props.x + ' ' + props.y + ')' : ''}>
      {props.children}
    </g>
  );
}