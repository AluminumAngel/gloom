import * as C from './defines';

const NUM_GRID_POINTS = 6 * C.GRID_SIZE;

export default class HexUtils {

  static getHexPoints( x, y ) {
    return [
      C.SCALE * ( x - 1.0 ), C.SCALE * y,
      C.SCALE * ( x - 0.5 ), C.SCALE * ( y - C.SQRT_3_OVER_2 ),
      C.SCALE * ( x + 0.5 ), C.SCALE * ( y - C.SQRT_3_OVER_2 ),
      C.SCALE * ( x + 1.0 ), C.SCALE * y,
      C.SCALE * ( x + 0.5 ), C.SCALE * ( y + C.SQRT_3_OVER_2 ),
      C.SCALE * ( x - 0.5 ), C.SCALE * ( y + C.SQRT_3_OVER_2 ),
    ].join( ',' );
  }

  static getGridHexCenter( column, row ) {
    const x = 1.0 + 1.5 * column;
    const y = C.GRID_SCALED_HEIGHT / C.SCALE - C.SQRT_3_OVER_2 * ( 2 * row + column % 2 + 1 );
    return [ C.SCALE * x, C.SCALE * y ];
  }

  static getGridHexPoints( column, row ) {
    const x = 1.0 + 1.5 * column;
    const y = C.GRID_SCALED_HEIGHT / C.SCALE - C.SQRT_3_OVER_2 * ( 2 * row + column % 2 + 1 );
    return this.getHexPoints( x, y );
  }

  static getAOEHexPoints( column, row ) {
    const x = 1.0 + 1.5 * column;
    const y = C.SQRT_3_OVER_2 * ( 2 * row + column % 2 );
    return this.getHexPoints( x, y );
  }

  static getGridHexPoint( point ) {
    const hex = Math.floor( point / 6 );
    const vertex = point % 6;
    const row = hex % C.GRID_HEIGHT;
    const column = Math.floor( hex / C.GRID_HEIGHT );
    const x = 1.0 + 1.5 * column;
    const y = C.GRID_SCALED_HEIGHT / C.SCALE - C.SQRT_3_OVER_2 * ( 2 * row + column % 2 + 1 );
    switch ( vertex ) {
      case 0:
        return [ C.SCALE * ( x + 1.0 ), C.SCALE * y ];
      case 1:
        return [ C.SCALE * ( x + 0.5 ), C.SCALE * ( y - C.SQRT_3_OVER_2 ) ];
      case 2:
        return [ C.SCALE * ( x - 0.5 ), C.SCALE * ( y - C.SQRT_3_OVER_2 ) ];
      case 3:
        return [ C.SCALE * ( x - 1.0 ), C.SCALE * y ];
      case 4:
        return [ C.SCALE * ( x - 0.5 ), C.SCALE * ( y + C.SQRT_3_OVER_2 ) ];
      default:
        return [ C.SCALE * ( x + 0.5 ), C.SCALE * ( y + C.SQRT_3_OVER_2 ) ];
    }
  }

  static getLinePoints( line ) {
    return [ Math.floor( line / NUM_GRID_POINTS ), line % NUM_GRID_POINTS ];
  }

}