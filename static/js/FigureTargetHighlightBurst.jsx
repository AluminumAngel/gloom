import React from 'react';
import * as C from './defines';

const CLASS_NAMES = [
  'attacked',
  'monster-focus',
  'character-focus',
  'monster-focus',
  'character-focus',
];

const HALF_TRIANGLE_WIDTH = 0.2 * C.FIGURE_RADIUS;
const TRIANGLE_BASE_HEIGHT = C.FIGURE_RADIUS + 1;
const TRIANGLE_TOP_HEIGHT = 1.5 * C.FIGURE_RADIUS;

export default function FigureTargetHighlightBurst( props ) {
  const triangle_points = [
    props.x - HALF_TRIANGLE_WIDTH, props.y - TRIANGLE_BASE_HEIGHT,
    props.x, props.y - TRIANGLE_TOP_HEIGHT,
    props.x + HALF_TRIANGLE_WIDTH, props.y - TRIANGLE_BASE_HEIGHT,
  ].join( ',' );

  var triangles = [];
  for ( var index = 0; index < 6; index++ ) {
    var angle = 30 + 60 * index;
    triangles.push(
      <polygon
        className={CLASS_NAMES[props.type]}
        key={index}
        points={triangle_points}
        pointerEvents='none'
        transform={'rotate(' + angle + ' ' + props.x + ' ' + props.y + ')'}
      />
    );
  }

  const circle = (
    <circle
      className={CLASS_NAMES[props.type]}
      cx={props.x}
      cy={props.y}
      r={C.FIGURE_RADIUS}
      pointerEvents='none'
    />
  );

  return (
    <g clipPath={props.clipPath}>
      {circle}
      {triangles}
    </g>
  );
}