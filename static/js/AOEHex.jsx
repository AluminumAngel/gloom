import React from 'react';
import * as C from './defines';
import HexUtils from './HexUtils';

const AOE_CENTER = ( C.AOE_SIZE - 1 ) / 2;

export default class AOEHex extends React.PureComponent {
  handleClick = ( e ) => {
    this.props.onClick( true, this.props.index );
    e.preventDefault();
  };

  handleContextMenu = ( e ) => {
    this.props.onClick( false, this.props.index );
    e.preventDefault();
  };

  render() {
    var className;
    if ( this.props.melee && this.props.index === AOE_CENTER ) {
      className = 'aoe-center';
    }
    else {
      className = this.props.content ? 'aoe-coverage' : 'empty';
    }
    return (
      <polygon
        className={className}
        points={HexUtils.getAOEHexPoints( this.props.c, this.props.r )}
        onClick={this.handleClick}
        onContextMenu={this.handleContextMenu}
      />
    );
  }
}
