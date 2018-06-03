import React from 'react';
import { UncontrolledTooltip } from 'reactstrap';
import * as C from './defines';

export default function NumberSelector( props ) {
  var options = [];
  props.options.forEach( ( option ) => {
    var class_name = 'btn btn-sm btn-dark';
    if ( option[0] === props.value && !props.disabled ) {
      class_name += ' active';
    }
    options.push(
      <button
        key={option[0]}
        type='button'
        className={class_name}
        onClick={function() { props.onChange( option[0] ); }}
        disabled={props.disabled}
      >
        {option[1]}
      </button>
    );
  } );
  var class_name = 'my-2 mr-auto col-form-label-sm';
  if ( props.disabled ) {
    class_name += ' text-muted';
  }
  return (
      <div className='d-flex'>
        <label className={class_name}>
          {props.label}
        </label>
        <div className='my-2 ml-4 btn-group' id={props.label}>
          {options}
        </div>
        <UncontrolledTooltip
          placement='right'
          delay={C.TOOLTIP_DELAY}
          target={props.label}
        >
          <div className='text-left'>
            {props.tooltip}
          </div>
        </UncontrolledTooltip>
      </div>
  );
}