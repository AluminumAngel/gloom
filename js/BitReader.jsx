export default class BitReader {
  constructor( encoded_bytes ) {
    var bytes = encoded_bytes;

    bytes += "=".repeat( ( 4 - bytes.length % 4 ) % 4 );
    bytes = bytes.replace( /-/g, '+' );
    bytes = bytes.replace( /_/g, '/' );
    try {
      bytes = atob( bytes );
    }
    catch ( e ) {
      throw 'bad scenario URL';
    }
    this.byte_list = new Uint8Array( bytes.split( '' ).map( function( char ) {
      return char.charCodeAt( 0 );
    } ) );

    this.current_byte = 0;
    this.next_byte = 0;
    this.next_bit = 8;
  }

  readBits( num_bits ) {
    var value = 0;
    var bits_read = 0;
    while ( true ) {
      if ( this.next_bit === 8 ) {
        if ( this.next_byte === this.byte_list.length ) {
          throw 'bad scenario URL';
        }
        this.current_byte = this.byte_list[this.next_byte++];
        this.next_bit = 0;
      }

      var bits_to_read = Math.min( 8 - this.next_bit, num_bits );
      var mask = ( ( 1 << bits_to_read ) - 1 ) << this.next_bit;
      value += ( this.current_byte & mask ) >> this.next_bit << bits_read;
      this.next_bit += bits_to_read;
      num_bits -= bits_to_read;

      if ( num_bits === 0 ) {
        return value;
      }

      bits_read += bits_to_read;
    }
  }
}