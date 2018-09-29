import React from 'react';
import * as C from './defines';
import * as FIGURE_HIGHLIGHT from './figure_highlights';
import FigureTargetHighlightBurst from './FigureTargetHighlightBurst';
import FigureTargetHighlightClip from './FigureTargetHighlightClip';

export default function FigureTargetHighlight( props ) {
  if ( props.type < FIGURE_HIGHLIGHT.ATTACKED_MONSTER_FOCUS ) {
    return (
      <FigureTargetHighlightBurst
        x={props.x}
        y={props.y}
        type={props.type}
        clipPath={null}
      />
    );
  }
  else {
    return (
      <React.Fragment>
        <FigureTargetHighlightClip
          id={'focus-clip-' + props.id}
          x={props.x}
          y={props.y}
          side={true}
        />
        <FigureTargetHighlightBurst
          x={props.x}
          y={props.y}
          type={props.type}
          clipPath={'url(#focus-clip-' + props.id + ')'}
        />
        <FigureTargetHighlightClip
          id={'attacked-clip-' + props.id}
          x={props.x}
          y={props.y}
          side={false}
        />
        <FigureTargetHighlightBurst
          x={props.x}
          y={props.y}
          type={FIGURE_HIGHLIGHT.ATTACKED}
          clipPath={'url(#attacked-clip-' + props.id + ')'}
        />
      </React.Fragment>
    );
  }
}