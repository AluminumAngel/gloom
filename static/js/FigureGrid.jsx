import React from 'react';
import * as C from './defines';
import Figure from './Figure';

export default function FigureGrid( props ) {
  var figures = [];
  var index = 0;
  for ( var c = 0; c < C.GRID_WIDTH; c++ ) {
    for ( var r = 0; r < C.GRID_HEIGHT; r++, index++ ) {
      figures.push( <Figure
        key={index}
        r={r}
        c={c}
        figure={props.figures[index]}
        initiative={props.initiatives[index]}
        displaySolution={props.displaySolution}
        move={props.moves[index]}
        attack={props.attacks[index]}
        flying={props.flying}
        selected={props.selection === index}
        rotate={props.rotate}
        dragSource={props.dragSourceIndex === index}
        activeFaction={props.activeFaction}
        activeFigure={props.activeFigureIndex === index}
      /> );
    }
  }
  return <g>{figures}</g>;
}