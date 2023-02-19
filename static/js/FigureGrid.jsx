import React from 'react';
import * as C from './defines';
import Figure from './Figure';

const FigureGrid = React.memo( function( props ) {
  var figures = [];
  for ( var c = 0, index = 0; c < C.GRID_WIDTH; c++ ) {
    for ( var r = 0; r < C.GRID_HEIGHT; r++, index++ ) {
      figures.push( <Figure
        key={index}
        id={index}
        r={r}
        c={c}
        figure={props.figures[index]}
        initiative={props.initiatives[index]}
        displaySolution={props.displaySolution}
        move={props.moves[index]}
        destination={props.destinations && props.destinations[index]}
        attack={props.attacks[index]}
        focus={props.focuses && props.focuses[index]}
        flying={props.flying}
        teleport={props.teleport}
        selected={props.selection === index}
        rotate={props.rotate}
        dragSource={props.dragSourceIndex === index}
        activeFaction={props.activeFaction}
        activeFigure={props.activeFigureIndex === index}
      /> );
    }
  }
  return <React.Fragment>{figures}</React.Fragment>;
} );
export default FigureGrid;