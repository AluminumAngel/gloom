import * as C from './defines';

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

}