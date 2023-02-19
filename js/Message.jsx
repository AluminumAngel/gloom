import React from 'react';

const STATE_HIDDEN = 0;
const STATE_VISIBLE = 1;
const STATE_FADING = 2;

export default class Message extends React.PureComponent {
  constructor( props ) {
    super( props );

    this.timeout = null;

    this.state = {
      state: STATE_HIDDEN,
      className: '',
      text: '',
    };
  }

  display( className, text ) {
    this.setState( {
      state: STATE_VISIBLE,
      className: className,
      text: text,
    } );

    clearTimeout( this.timeout );
    this.timeout = setTimeout( () => {
      this.setState( {
        state: STATE_FADING,
      } );
      this.timeout = setTimeout( () => {
        this.setState( {
          state: STATE_HIDDEN,
        } );
      }, 2000 );
    }, 3000 );
  }

  render() {
    if ( this.state.state === STATE_HIDDEN ) {
      return null;
    }

    var class_name = 'message-container';
    if ( this.state.state === STATE_FADING ) {
      class_name += ' fade';
    }

    return (
      <div className={class_name}>
        <div className={'message alert text-center ' + this.state.className}>
          {this.state.text}
        </div>
      </div>
    );
  }
}