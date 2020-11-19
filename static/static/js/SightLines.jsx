import React from 'react';
import SightLine from './SightLine';

const SightLines = React.memo( function( props ) {
  if ( !props.lines ) return null;

  var lines = [];
  props.lines.forEach( ( line ) => {
    lines.push(
      <SightLine
        key={line}
        className={props.className}
        line={line}
      />
    );
  } );
  return <React.Fragment>{lines}</React.Fragment>;
} );
export default SightLines;