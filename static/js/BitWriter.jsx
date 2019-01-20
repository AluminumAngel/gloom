export default class BitWriter {
  constructor() {
    this.byte_list = [];
    this.scratch_byte = 0;
    this.next_bit = 0;
  }

  result() {
    var bytes = btoa( String.fromCharCode.apply( null, new Uint8Array(
      this.byte_list
    ) ) );
    bytes = bytes.replace( /\+/g, '-' );
    bytes = bytes.replace( /\//g, '_' )
    bytes = bytes.replace( /\=+$/, '' );
    return bytes;
  }

  flush() {
    if ( this.next_bit !== 0 ) {
      this.byte_list.push( this.scratch_byte );
      this.scratch_byte = 0;
      this.next_bit = 0;
    }
  }

  writeBits( num_bits, value ) {
    if ( num_bits > 32 ) {
      throw 'too many bits written';
    }
    if ( value > ( 1 << num_bits ) - 1 ) {
      throw 'too few bits written';
    }
    if ( value < 0 ) {
      throw 'writing negative number'
    }

    while ( true ) {
      if ( this.next_bit + num_bits < 8 ) {
        this.scratch_byte |= value << this.next_bit;
        this.next_bit += num_bits;
        return;
      }
      else {
        var bits_to_write = 8 - this.next_bit;
        var mask = ( 1 << bits_to_write ) - 1;
        this.scratch_byte |= ( value & mask ) << this.next_bit;

        this.byte_list.push( this.scratch_byte );
        this.scratch_byte = 0;
        this.next_bit = 0;

        num_bits -= bits_to_write;
        value >>= bits_to_write;
      }
    }
  }
}