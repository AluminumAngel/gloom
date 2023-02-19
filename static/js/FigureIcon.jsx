import React from 'react';
import * as C from './defines';
import * as BRUSH from './brushes';

const FONT_SIZE = 0.7 * C.SCALE;

const CLASS_NAMES = [
  'character ',
  'monster ',
  'active-character ',
  'active-monster ',
  'active-character ',
  'active-monster ',
];

const ACTIVE_MONSTER_TEXT = [
  'M',
  'J',
  'F',
  'T',
  'U',
];

const ACTIVE_CHARACTER_TEXT = [
  'C',
  'J',
  'F',
  'T',
  'U',
];

function getTextIndex( flying, teleport ) {
  if ( teleport ) {
    if ( flying === 2 ) {
      return 4;
    }
    return 3;
  }
  return flying;
}

const FigureIcon = React.memo( function( props ) {
  const className = CLASS_NAMES[props.figure - BRUSH.FIRST_FIGURE_BRUSH] + props.className;
  var text;
  if ( props.figure === BRUSH.ACTIVE_MONSTER ) {
    text = ACTIVE_MONSTER_TEXT[getTextIndex( props.flying, props.teleport )];
  }
  else if ( props.figure === BRUSH.ACTIVE_CHARACTER ) {
    text = ACTIVE_CHARACTER_TEXT[getTextIndex( props.flying, props.teleport )];
  }
  else if ( props.figure === BRUSH.MONSTER_DESTINATION || props.figure === BRUSH.CHARACTER_DESTINATION ) {
    text = '\u2715';
  }
  else if ( props.activeFaction ) {
    if ( props.figure === BRUSH.MONSTER ) {
      text = props.initiative;
    }
    else {
      text = 'C';
    }
  }
  else {
    if ( props.figure === BRUSH.CHARACTER ) {
      text = props.initiative;
    }
    else {
      text = 'M';
    }
  }

  return (
    <React.Fragment>
      <circle
        className={className}
        cx={props.x}
        cy={props.y}
        r={C.FIGURE_RADIUS}
        pointerEvents='none'
      />
      <text
        className={className}
        x={props.x}
        y={props.y + 4.5}
        fontSize={FONT_SIZE}
        pointerEvents='none'
      >
        {text}
      </text>
    </React.Fragment>
  );
} );
export default FigureIcon;