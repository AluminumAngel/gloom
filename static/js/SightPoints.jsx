import React from 'react';
import SightPoint from './SightPoint';

export default function SightPoints( props ) {
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
}