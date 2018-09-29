import React from 'react';
import * as C from './defines';

export default function FigureTargetHighlightClip( props ) {
  const clip_points = [
    props.x, props.y + 2 * C.FIGURE_RADIUS,
    props.x, props.y - 2 * C.FIGURE_RADIUS,
    props.x - 2 * C.FIGURE_RADIUS, props.y - 2 * C.FIGURE_RADIUS,
    props.x - 2 * C.FIGURE_RADIUS, props.y + 2 * C.FIGURE_RADIUS,
  ].join( ',' );
  const angle = props.side ? 'rotate(60 ' : 'rotate(240 ';

  return (
    <clipPath id={props.id}>
      <polygon
        points={clip_points}
        transform={angle + props.x + ' ' + props.y + ')'}
      />
    </clipPath>    
  );  
}