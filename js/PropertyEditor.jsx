import React from 'react';
import NumberSelector from './NumberSelector';

const MOVE_OPTIONS = [
  [ 0, 'none' ],
  [ 1, '1' ],
  [ 2, '2' ],
  [ 3, '3' ],
  [ 4, '4' ],
  [ 5, '5' ],
  [ 6, '6' ],
  [ 7, '7' ],
  [ 8, '8' ],
  [ 9, '9' ],
];

const RANGE_OPTIONS = [
  [ 0, 'melee' ],
  [ 1, '1' ],
  [ 2, '2' ],
  [ 3, '3' ],
  [ 4, '4' ],
  [ 5, '5' ],
  [ 6, '6' ],
  [ 7, '7' ],
  [ 8, '8' ],
  [ 9, '9' ],
];

const TARGET_OPTIONS = [
  [ 0, 'no attack' ],
  [ 1, '1' ],
  [ 2, '2' ],
  [ 3, '3' ],
  [ 4, '4' ],
  [ 5, '5' ],
  [ 6, 'all' ],
];

const FLYING_OPTIONS = [
  [ 0, 'none' ],
  [ 1, 'jump' ],
  [ 2, 'flying' ],
];

const TELEPORT_OPTIONS = [
  [ 0, 'no' ],
  [ 1, 'yes' ],
];

const MUDDLED_OPTIONS = [
  [ 0, 'no' ],
  [ 1, 'yes' ],
];

const INITIATIVE_OPTIONS = [
  [ 1, '1' ],
  [ 2, '2' ],
  [ 3, '3' ],
  [ 4, '4' ],
  [ 5, '5' ],
  [ 6, '6' ],
  [ 7, '7' ],
  [ 8, '8' ],
  [ 9, '9' ],
];

const PropertyEditor = React.memo( function( props ) {
  return (
    <React.Fragment>
      <NumberSelector
        label='Move'
        options={MOVE_OPTIONS}
        value={props.move}
        onChange={props.onMoveChange}
        tooltip={
          <React.Fragment>
            Set the movement distance of the current turn.
            <p/>
            If the current turn does not include a move, select none.
          </React.Fragment>
        }
      />
      <NumberSelector
        label='Range'
        options={RANGE_OPTIONS}
        value={props.range}
        onChange={props.onRangeChange}
        tooltip={
          <React.Fragment>
            Set the range of the current attack.
          </React.Fragment>
        }
      />
      <NumberSelector
        label='Target'
        options={TARGET_OPTIONS}
        value={props.target}
        onChange={props.onTargetChange}
        tooltip={
          <React.Fragment>
            Set the number of targets of the current attack.
            <p/>
            If the current turn does not include an attack, select no attack.
            <p/>
            In the case of an area of effect attack, targets beyond the first do not use the area of effect.
            <p/>
            A target setting of four or greater on a ranged area of effect attack is too complex to solve in a timely manner.
          </React.Fragment>
        }
      />
      <NumberSelector
        label='Trait'
        options={FLYING_OPTIONS}
        traitBehavior={true}
        value={props.flying}
        onChange={props.onFlyingChange}
        tooltip={
          <React.Fragment>
            Set the movement trait of the current move.
          </React.Fragment>
        }
      />
      <NumberSelector
        label='Teleport'
        options={TELEPORT_OPTIONS}
        value={props.teleport}
        onChange={props.onTeleportChange}
        tooltip={
          <React.Fragment>
            Set whether the active {props.activeFactionString} is teleporting.
          </React.Fragment>
        }
      />
      <NumberSelector
        label='Muddled'
        options={MUDDLED_OPTIONS}
        value={props.muddled}
        onChange={props.onMuddledChange}
        tooltip={
          <React.Fragment>
            Set whether the active {props.activeFactionString} is muddled.
          </React.Fragment>
        }
      />
      <NumberSelector
        label='Initiative'
        options={INITIATIVE_OPTIONS}
        value={props.initiative}
        disabled={props.initiative === -1}
        onChange={props.onInitiativeChange}
        tooltip={
          <React.Fragment>
            Set the initiative rank of the selected {props.inactiveFactionString}.
          </React.Fragment>
        }
      />
    </React.Fragment>
  );
} );
export default PropertyEditor;