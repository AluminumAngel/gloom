import React from 'react';
import * as C from './defines';
import * as BRUSH from './brushes';
import HexUtils from './HexUtils';
import FigureIcon from './FigureIcon';
import FigureTransform from './FigureTransform';

export default class DragFigure extends React.PureComponent {
  constructor( props ) {
    super( props );

    this.suppress_clicks = false;
    this.reset();
    this.state = {
      dragging: false,
      x: 0,
      y: 0,
      figure: BRUSH.EMPTY,
      initiative: 1,
      flying: 0,
      rotated: false,
    };
  }

  reset() {
    this.active = false;
    this.mouse_x = 0;
    this.mouse_y = 0;
    this.initial_mouse_x = 0;
    this.initial_mouse_y = 0;
    this.source_index = C.NULL_INDEX;
  }

  activate( mouse_x, mouse_y, source_index, c, r, figure, initiative, flying, teleport, rotated ) {
    this.active = true;
    this.mouse_x = this.initial_mouse_x = mouse_x;
    this.mouse_y = this.initial_mouse_y = mouse_y;
    this.source_index = source_index;

    const center = HexUtils.getGridHexCenter( c, r );
    this.setState( {
      x: center[0],
      y: center[1],
      figure: figure,
      initiative: initiative,
      flying: flying,
      teleport: teleport,
      rotated: rotated,
    } )

    document.addEventListener( 'mousemove', this.handleMouseMove );
  }

  deactivate() {
    if ( !this.active ) return;

    document.removeEventListener( 'mousemove', this.handleMouseMove );

    this.reset();
    this.setState( {
      dragging: false,
      x: 0,
      y: 0,
      figure: BRUSH.EMPTY,
      initiative: 1,
      flying: 0,
      teleport: 0,
      rotated: false,
    } );
  }

  handleMouseMove = ( e ) => {
    const page_x = e.pageX;
    const page_y = e.pageY;

    if ( !this.state.dragging ) {
      if ( page_x === this.initial_mouse_x && page_y === this.initial_mouse_y ) {
        return;
      }
      this.props.onDragStart( this.source_index );
    }

    const delta_x = this.mouse_x - page_x;
    const delta_y = this.mouse_y - page_y;

    var step_x;
    var step_y;
    if ( this.state.rotated ) {
      step_x = delta_y;
      step_y = -delta_x;
    }
    else {
      step_x = delta_x;
      step_y = delta_y;
    }

    this.mouse_x = page_x;
    this.mouse_y = page_y;

    this.setState( {
      dragging: true,
      x: this.state.x - step_x,
      y: this.state.y - step_y,
    } );
  }

  render() {
    if ( !this.state.dragging ) return null;

    return (
      <FigureTransform rotate={this.state.rotated} x={this.state.x} y={this.state.y}>
        <FigureIcon
          x={this.state.x}
          y={this.state.y}
          figure={this.state.figure}
          flying={this.state.flying}
          teleport={this.state.teleport}
          initiative={this.state.initiative}
          activeFaction={this.props.activeFaction}
        />
      </FigureTransform>
    );
  }
}