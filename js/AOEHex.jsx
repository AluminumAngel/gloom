import React from 'react';
import HexUtils from './HexUtils';

const CLASS_NAMES = [
  'empty',
  'aoe-coverage',
  'aoe-center',
];

export default class AOEHex extends React.PureComponent {
  handleClick = ( e ) => {
    if ( this.props.onClick ) {
      this.props.onClick( true, this.props.index );
    }
    e.preventDefault();
  };

  handleContextMenu = ( e ) => {
    if ( this.props.onClick ) {
      this.props.onClick( false, this.props.index );
    }
    e.preventDefault();
  };

  render() {
    return (
      <polygon
        className={CLASS_NAMES[this.props.content]}
        points={HexUtils.getAOEHexPoints( this.props.c, this.props.r )}
        onClick={this.handleClick}
        onContextMenu={this.handleContextMenu}
      />
    );
  }
}
