import React from 'react';
import * as C from './defines';

export default class Wall extends React.PureComponent {
  handleClick = ( e ) => {
    this.props.onClick( true, this.props.index );
    e.preventDefault();
  };

  handleContextMenu = ( e ) => {
    this.props.onClick( false, this.props.index );
    e.preventDefault();
  };

  render() {
    return (
      <React.Fragment>
        <polyline
          className={this.props.wall ? 'wall' : 'no-wall'}
          points={getWallPoints( this.props.c, this.props.r, this.props.side )}
          pointerEvents='none'
        />
        <polygon
          points={getWallInteractivePoints( this.props.c, this.props.r, this.props.side )}
          visibility='hidden'
          pointerEvents={this.props.active ? 'all' : 'none'}
          onClick={this.handleClick}
          onContextMenu={this.handleContextMenu}
        />
      </React.Fragment>
    );
  }
}

function getWallPoints( column, row, wall ) {
  const x = 1.0 + 1.5 * column;
  var y = C.SQRT_3_OVER_2 + C.SQRT_3_OVER_2 * ( 2.0 * row + column % 2 );
  y = C.GRID_SCALED_HEIGHT / C.SCALE - y;

  var points_list = [];
  if ( wall === 0 )
  {
    points_list.push( [ C.SCALE * ( x - 0.5 ), C.SCALE * ( y - C.SQRT_3_OVER_2 ) ].join(',') );
    points_list.push( [ C.SCALE * ( x + 0.5 ), C.SCALE * ( y - C.SQRT_3_OVER_2 ) ].join(',') );
  }
  else if ( wall === 1 )
  {
    points_list.push( [ C.SCALE * ( x + 0.5 ), C.SCALE * ( y - C.SQRT_3_OVER_2 ) ].join(',') );
    points_list.push( [ C.SCALE * ( x + 1.0 ), C.SCALE * y ].join(',') );
  }
  else
  {
    points_list.push( [ C.SCALE * ( x + 1.0 ), C.SCALE * y ].join(',') );
    points_list.push( [ C.SCALE * ( x + 0.5 ), C.SCALE * ( y + C.SQRT_3_OVER_2 ) ].join(',') );
  }

  return points_list.join( ',' );
}

function getWallInteractivePoints( column, row, wall ) {
  const x = 1.0 + 1.5 * column;
  var y = C.SQRT_3_OVER_2 + C.SQRT_3_OVER_2 * ( 2.0 * row + column % 2 );
  y = C.GRID_SCALED_HEIGHT / C.SCALE - y;

  var points_list = [];
  if ( wall === 0 )
  {
    points_list.push( [ C.SCALE * ( x - 0.5 ), C.SCALE * ( y - C.SQRT_3_OVER_2 ) ].join(',') );
    points_list.push( [ C.SCALE * ( x ), C.SCALE * ( y ) ].join(',') );
    points_list.push( [ C.SCALE * ( x + 0.5 ), C.SCALE * ( y - C.SQRT_3_OVER_2 ) ].join(',') );
    points_list.push( [ C.SCALE * ( x ), C.SCALE * ( y - 2 * C.SQRT_3_OVER_2 ) ].join(',') );
  }
  else if ( wall === 1 )
  {
    points_list.push( [ C.SCALE * ( x + 0.5 ), C.SCALE * ( y - C.SQRT_3_OVER_2 ) ].join(',') );
    points_list.push( [ C.SCALE * ( x ), C.SCALE * ( y ) ].join(',') );
    points_list.push( [ C.SCALE * ( x + 1.0 ), C.SCALE * ( y ) ].join(',') );
    points_list.push( [ C.SCALE * ( x + 1.5 ), C.SCALE * ( y - C.SQRT_3_OVER_2 ) ].join(',') );
  }
  else
  {
    points_list.push( [ C.SCALE * ( x + 1.0 ), C.SCALE * y ].join(',') );
    points_list.push( [ C.SCALE * ( x ), C.SCALE * ( y ) ].join(',') );
    points_list.push( [ C.SCALE * ( x + 0.5 ), C.SCALE * ( y + C.SQRT_3_OVER_2 ) ].join(',') );
    points_list.push( [ C.SCALE * ( x + 1.5 ), C.SCALE * ( y + C.SQRT_3_OVER_2 ) ].join(',') );
  }

  return points_list.join( ',' );
}