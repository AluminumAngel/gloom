import React from 'react';
import SightPoint from './SightPoint';

const SightPoints = React.memo( function( props ) {
  if ( !props.points ) return null;

  var points = [];
  props.points.forEach( ( point ) => {
    points.push(
      <SightPoint
        key={point}
        className={props.className}
        point={point}
      />
    );
  } );
  return <React.Fragment>{points}</React.Fragment>;
} );
export default SightPoints;