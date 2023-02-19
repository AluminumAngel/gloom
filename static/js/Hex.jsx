import React from 'react';
import HexUtils from './HexUtils';

const CLASS_NAMES = [
  'empty',
  'obstacle',
  'wall',
  'trap',
  'hazardous-terrain',
  'difficult-terrain',
  'icy-terrain',
];

export default class Hex extends React.PureComponent {
  handleClick = ( e ) => {
    this.props.onClick( true, this.props.index );
    e.preventDefault();
  };

  handleContextMenu = ( e ) => {
    this.props.onClick( false, this.props.index );
    e.preventDefault();
  };

  handleMouseDown = ( e ) => {
    this.props.onMouseDown(
      e.pageX,
      e.pageY,
      this.props.index,
      this.props.c,
      this.props.r
    );
  };

  handleMouseUp = ( e ) => {
    this.props.onMouseUp( this.props.index );
    e.stopPropagation();
  };

  render() {
    return (
      <polygon
        className={CLASS_NAMES[this.props.content]}
        points={HexUtils.getGridHexPoints( this.props.c, this.props.r )}
        pointerEvents={this.props.active ? 'all' : 'none'}
        onMouseDown={this.handleMouseDown}
        onMouseUp={this.handleMouseUp}
        onClick={this.handleClick}
        onContextMenu={this.handleContextMenu}
      />
    );
  }
}