import React from 'react';
import * as BRUSH from './brushes';
import HexUtils from './HexUtils';
import FigureIcon from './FigureIcon';
import FigureSelectionHighlight from './FigureSelectionHighlight';
import FigureTransform from './FigureTransform';

export default function Figure( props ) {
  if ( props.figure === BRUSH.EMPTY && ( !props.displaySolution || !props.move ) ) {
    return null;
  }
  if ( props.dragSource ) {
    return null;
  }

  var className = '';
  var figure = props.figure;
  if ( figure === BRUSH.EMPTY ) {
    figure = props.activeFaction ? BRUSH.ACTIVE_CHARACTER : BRUSH.ACTIVE_MONSTER;
  }
  else if ( props.activeFigure ) {
    figure = props.activeFaction ? BRUSH.ACTIVE_CHARACTER : BRUSH.ACTIVE_MONSTER;
    if ( props.displaySolution && !props.move ) {
      className = 'previous-position';
    }
  }
  else if ( props.displaySolution && props.attack ) {
    className = 'attacked';
  }

  const [ x, y ] = HexUtils.getGridHexCenter( props.c, props.r );

  return (
    <FigureTransform rotate={props.rotate} x={x} y={y}>
      <FigureIcon
        x={x}
        y={y}
        className={className}
        figure={figure}
        flying={props.flying}
        initiative={props.initiative}
        activeFaction={props.activeFaction}
      />
      <FigureSelectionHighlight
        x={x}
        y={y}
        active={props.selected}
      />
    </FigureTransform>
  );
}