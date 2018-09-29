import React from 'react';
import { UncontrolledTooltip } from 'reactstrap';
import * as C from './defines';

const FIGURE_ICON_EXTENT = 2 * C.SCALE + 2;
const FIGURE_ICON_VIEWBOX = ( FIGURE_ICON_EXTENT / -2.0 ) + ' ' + ( FIGURE_ICON_EXTENT / -2.0 ) + ' ' + FIGURE_ICON_EXTENT + ' ' + FIGURE_ICON_EXTENT;

export default class BrushButton extends React.PureComponent {
  // WORKAROUND
  // https://github.com/reactstrap/reactstrap/issues/1004
  // Tracking hover state is a partial workaround for the above issue.
  // Without, you could get multiple tooltips would display if you touch then move
  // your touch off the button before releasing.
  // Issue presists on the Switch Active Faction button.

  constructor( props ) {
    super( props );

    this.state = {
      hover: false,
    };
  }

  handleMouseEnter = () => {
    this.setState( {
      hover: true,
    } );
  };

  handleMouseLeave = () => {
    this.setState( {
      hover: false,
    } );
  };

  handleClick = () => {
    this.props.onClick( this.props.brush );
  };

  render() {
    var tooltip = this.state.hover ? (
      <UncontrolledTooltip
        placement={this.props.tooltipPlacement ? this.props.tooltipPlacement : 'right'}
        delay={C.TOOLTIP_DELAY}
        target={'brush-tooltip-' + this.props.brush}
      >
        <div className='text-left'>
          {this.props.tooltip}
        </div>
      </UncontrolledTooltip>
    ) : null;

    return (
      <React.Fragment>
        <button
          type='button'
          id={'brush-tooltip-' + this.props.brush}
          className={'py-0 btn btn-sm btn-dark' + ( this.props.brush === this.props.selection ? ' active' : '' )}
          onClick={this.handleClick}
          onMouseEnter={this.handleMouseEnter}
          onMouseLeave={this.handleMouseLeave}
        >
          <div className='d-flex justify-content-end align-items-center'>
            <div>{this.props.text}</div>
            <svg
              viewBox={FIGURE_ICON_VIEWBOX}
              className='ml-3 mr-1'
              width={FIGURE_ICON_EXTENT}
              height={FIGURE_ICON_EXTENT}
            >
              {this.props.icon}
            </svg>
          </div>
        </button>
        {tooltip}
      </React.Fragment>
    );
  }
}