import React from 'react';
import * as C from './defines';
import * as BRUSH from './brushes';
import * as FIGURE_HIGHLIGHT from './figure_highlights';
import HexUtils from './HexUtils';
import FigureIcon from './FigureIcon';
import FigureSelectionHighlight from './FigureSelectionHighlight';
import FigureTargetHighlight from './FigureTargetHighlight';
import FigureTransform from './FigureTransform';

const Figure = React.memo( function( props ) {
  if ( props.figure === BRUSH.EMPTY ) {
    if ( !props.displaySolution ) return null;
    if ( !props.move && !props.destination ) return null;
  }
  if ( props.dragSource ) return null;

  var figure = props.figure;
  var className = '';
  if ( figure === BRUSH.EMPTY ) {
    if ( props.move ) {
      figure = props.activeFaction ? BRUSH.ACTIVE_CHARACTER : BRUSH.ACTIVE_MONSTER;
    }
    else {
      figure = props.activeFaction ? BRUSH.CHARACTER_DESTINATION : BRUSH.MONSTER_DESTINATION;
      className = 'ghost';
    }
  }
  else if ( props.activeFigure ) {
    figure = props.activeFaction ? BRUSH.ACTIVE_CHARACTER : BRUSH.ACTIVE_MONSTER;
    if ( props.displaySolution && !props.move ) {
      className = 'ghost';
    }
  }

  const [ x, y ] = HexUtils.getGridHexCenter( props.c, props.r );

  var targetHighlight = null;
  if ( props.displaySolution ) {
    var targetHighlightType = -1;
    if ( props.focus ) {
      if ( !props.activeFaction ) {
        targetHighlightType = FIGURE_HIGHLIGHT.MONSTER_FOCUS;
      }
      else {
        targetHighlightType = FIGURE_HIGHLIGHT.CHARACTER_FOCUS;
      }
      if ( props.attack ) {
        targetHighlightType += FIGURE_HIGHLIGHT.ATTACKED_MONSTER_FOCUS - FIGURE_HIGHLIGHT.MONSTER_FOCUS;
      }
    }
    else if ( props.attack ) {
      targetHighlightType = FIGURE_HIGHLIGHT.ATTACKED;
    }
    if ( targetHighlightType !== -1 ) {
      targetHighlight = (
        <FigureTargetHighlight
          id={props.id}
          x={x}
          y={y}
          type={targetHighlightType}
        />
      );
    }
  }

  var selectionHighlight = null;
  if ( props.selected ) {
    selectionHighlight = (
      <FigureSelectionHighlight
        x={x}
        y={y}
      />
    );
  }

  return (
    <React.Fragment>
      <FigureTransform rotate={props.rotate} x={x} y={y}>
        <FigureIcon
          x={x}
          y={y}
          className={className}
          figure={figure}
          flying={props.flying}
          teleport={props.teleport}
          initiative={props.initiative}
          activeFaction={props.activeFaction}
        />
      </FigureTransform>
      {targetHighlight}
      {selectionHighlight}
    </React.Fragment>
  );
} );
export default Figure;