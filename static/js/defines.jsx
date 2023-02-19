function bitsRequired( value ){
  return Math.ceil( Math.log( value + 1 ) / Math.log( 2 ) );
}

export const SCALE = 19;
export const SQRT_3_OVER_2 = Math.sqrt( 3.0 ) / 2.0;

// export const GRID_HEIGHT = 7; // for creating test scenarios
export const GRID_HEIGHT = 25;
export const GRID_WIDTH = Math.round( Math.sqrt( 3.0 ) / 1.5 * GRID_HEIGHT );
export const GRID_SCALED_WIDTH = SCALE * ( 0.5 + GRID_WIDTH * 1.5 );
export const GRID_SCALED_HEIGHT = SCALE * ( SQRT_3_OVER_2 + 2.0 * GRID_HEIGHT * SQRT_3_OVER_2 );
export const GRID_SIZE = GRID_HEIGHT * GRID_WIDTH;
export const GRID_SIZE_BITS = bitsRequired( GRID_SIZE + 1 );
export const GRID_MARGIN = 10;
export const GRID_EXTENT = Math.max( GRID_SCALED_WIDTH, GRID_SCALED_HEIGHT ) + 2 * GRID_MARGIN;
export const GRID_DELTA = Math.abs( GRID_SCALED_WIDTH - GRID_SCALED_HEIGHT ) / 2.0;
export const GRID_TRANSFORM = 'translate(' + ( GRID_SCALED_HEIGHT / 2.0 ) + ' ' + ( GRID_SCALED_WIDTH / 2.0 ) + ') rotate(90) translate(-' + ( GRID_SCALED_WIDTH / 2.0 ) + ' -' + ( GRID_SCALED_HEIGHT / 2.0 ) + ')';

export const GRID_HEIGHT_V0 = 20;
export const GRID_WIDTH_V0 = Math.round( Math.sqrt( 3.0 ) / 1.5 * GRID_HEIGHT_V0 );
export const GRID_SIZE_V0 = GRID_HEIGHT_V0 * GRID_WIDTH_V0;
export const GRID_SIZE_BITS_V0 = bitsRequired( GRID_SIZE_V0 + 1 );
export const ROW_ADJUST = ~~( ( GRID_HEIGHT - GRID_HEIGHT_V0 ) / 2 ) + 1;
export const COLUMN_ADJUST = ~~( ( GRID_WIDTH - GRID_WIDTH_V0 ) / 4 ) * 2 + 1;

export const AOE_HEIGHT = 7;
export const AOE_WIDTH = 7;
export const AOE_SIZE = AOE_HEIGHT * AOE_WIDTH;
export const AOE_SIZE_BITS = bitsRequired( AOE_SIZE );
export const AOE_MARGIN = 3;
export const AOE_SCALED_WIDTH = SCALE * ( 0.5 + AOE_WIDTH * 1.5 );
export const AOE_SCALED_HEIGHT = SCALE * ( 2.0 * AOE_HEIGHT * SQRT_3_OVER_2 );
export const AOE_EXTENT = Math.max( AOE_SCALED_WIDTH, AOE_SCALED_HEIGHT ) + 2 * AOE_MARGIN;
export const AOE_TRANSFORM = 'translate(' + ( AOE_SCALED_HEIGHT / 2.0 ) + ' ' + ( AOE_SCALED_WIDTH / 2.0 ) + ') rotate(90) translate(-' + ( AOE_SCALED_WIDTH / 2.0 ) + ' -' + ( AOE_SCALED_HEIGHT / 2.0 ) + ')';
export const AOE_VIEWBOX = ( -AOE_MARGIN ) + ' ' + ( -AOE_MARGIN - Math.abs( AOE_SCALED_WIDTH - AOE_SCALED_HEIGHT ) / 2.0 ) + ' ' + ( AOE_EXTENT ) + ' ' + ( AOE_EXTENT );
export const AOE_GRID_SKIP_LIST = [ 0, 1, 6, 7, 13, 14, 28, 35, 41, 42, 43, 48 ];

export const FIGURE_RADIUS = 0.6 * SCALE;

export const TOOLTIP_DELAY = {
  show: 500,
  hide: 0,
};