import React from 'react';
import * as C from './defines';
import * as BRUSH from './brushes';
import HexUtils from './HexUtils';
import BrushButton from './BrushButton';
import FigureIcon from './FigureIcon';

const PLAY_SCENARIO_ICON_TRANSFORM = 'scale(' + ( C.SCALE * 0.00684 ) + ') translate(' + ( C.SCALE * -6.84 ) + ' ' + ( C.SCALE * -6.84 ) + ')';
const BASE_HEX_POINTS = HexUtils.getHexPoints( 0, 0 );
const BASE_WALL_POINTS = getButtonWallPoints();

function getButtonWallPoints() {
  const x = -0.75;
  const y = C.SQRT_3_OVER_2 / 2.0;

  var points_list = [];
  points_list.push( [ C.SCALE * ( x + 1.0 ), C.SCALE * ( y - C.SQRT_3_OVER_2 ) ].join(',') );
  points_list.push( [ C.SCALE * ( x + 0.5 ), C.SCALE * y ].join(',') );
  return points_list.join( ',' );
}

const BrushPicker = React.memo( function( props ) {
  return (
    <div className='d-flex'>
      <div className='w-75 mb-3 ml-auto btn-group-vertical'>
        <BrushButton
          brush={BRUSH.PROGRESS}
          selection={props.selection}
          onClick={props.onSelection}
          text='Play Scenario'
          icon={
            <g transform={PLAY_SCENARIO_ICON_TRANSFORM}>
              <path className='play-scenario-fill' d='M145.9541,208.4209c-0.5332,0 -1.04589,0 -2.1123,-0.51269c-1.0459,-0.53321 -2.0918,-1.57911 -3.1377,-2.625l-19.42089,-45.15821l-23.625,22.0459c-0.53321,1.0459 -1.57911,1.5791 -3.15821,1.5791c-0.5332,0 -1.5791,0 -2.09179,-0.5332c-1.57911,-0.5127 -3.15821,-2.625 -3.15821,-4.7168v-115.5c0,-2.09179 1.0459,-4.2041 3.15821,-4.71679c0.51269,-0.53321 1.55859,-0.53321 2.09179,-0.53321c1.0459,0 2.625,0.53321 3.6709,1.5791l84,78.75c1.5791,1.57911 2.11231,3.6709 1.5791,5.7627c-0.5332,2.1123 -2.625,3.1582 -4.71679,3.69141l-33.07911,3.13769l20.4668,44.625c0.5332,1.0459 0.5332,2.625 0,4.2041c-0.51269,1.0459 -1.5791,2.625 -2.625,3.15821l-15.2168,6.80859c-1.04589,-1.0459 -2.1123,-1.0459 -2.625,-1.0459z'/>
              <path className='play-scenario-stroke' d='M94.5,63l84,78.75l-40.4209,3.6709l23.625,51.4541l-15.2373,6.8291l-22.55859,-51.9873l-29.40821,26.7832v-115.5M94.5,52.5c-1.5791,0 -2.625,0.53321 -4.2041,1.0459c-3.6709,1.5791 -6.2959,5.25 -6.2959,9.4541v115.5c0,4.2041 2.625,7.875 6.2959,9.4541c1.5791,1.0459 3.1582,1.0459 4.2041,1.0459c2.625,0 5.25,-1.0459 7.3418,-2.625l17.8623,-16.7959l16.2627,38.32911c1.06641,2.625 3.1582,4.71679 5.7832,5.76269c1.0459,0.5332 2.625,0.5332 3.6709,0.5332c1.5791,0 2.625,-0.5332 4.2041,-1.04589l15.2168,-6.82911c2.625,-1.04589 4.7373,-3.1582 5.7832,-5.7832c1.0459,-2.625 1.0459,-5.76269 0,-7.875l-17.3291,-37.7959l25.73731,-2.09179c4.18359,-0.53321 7.875,-3.15821 8.92089,-6.82911c1.57911,-3.67089 0.5127,-8.4082 -2.625,-11.0332l-84,-78.75c-1.5791,-2.625 -4.2041,-3.6709 -6.8291,-3.6709z'/>
            </g>
          }
          tooltipPlacement='right-start'
          tooltip={props.activeFaction
            ?
              <React.Fragment>
                Left-click a character to activate or deactivate it.
                <p/>
                Left-click a movement option to have the active character perform that move.
                <p/>
                Left-click a monster to select it. While selected, the initiative order of a monster can be set.
                <p/>
                Drag-and-drop any figure to move it.
                <p/>
                Right-click any figure to remove it.
              </React.Fragment>
            :
              <React.Fragment>
                Left-click a monster to activate or deactivate it.
                <p/>
                Left-click a movement option to have the active monster perform that move.
                <p/>
                Left-click a character to select it. While selected, the initiative order of a character can be set.
                <p/>
                Drag-and-drop a figure to move it.
                <p/>
                Right-click any figure to remove it.
              </React.Fragment>
          }
        />
        <BrushButton
          brush={BRUSH.ACTIVE_FIGURE}
          selection={props.selection}
          onClick={props.onSelection}
          text={props.activeFaction ? 'Active Character' : 'Active Monster'}
          icon={
            <FigureIcon
              x='0'
              y='0'
              figure={props.activeFaction ? BRUSH.ACTIVE_CHARACTER : BRUSH.ACTIVE_MONSTER}
              flying={props.flying}
              teleport={props.teleport}
              initiative={props.initiative}
              activeFaction={props.activeFaction}
            />
          }
          tooltip={props.activeFaction
            ?
              <React.Fragment>
                Left-click the board to add or remove the active character.
                <p/>
                Right-click any figure to remove it.
              </React.Fragment>
            :
              <React.Fragment>
                Left-click the board to add or remove the active monster.
                <p/>
                Right-click any figure to remove it.
              </React.Fragment>
          }
        />
        <BrushButton
          brush={BRUSH.CHARACTER}
          selection={props.selection}
          onClick={props.onSelection}
          text='Character'
          icon={
            <FigureIcon
              x='0'
              y='0'
              figure={BRUSH.CHARACTER}
              flying={props.flying}
              initiative={props.initiative}
              activeFaction={props.activeFaction}
            />
          }
          tooltip={props.activeFaction
            ?
              <React.Fragment>
                Left-click the board to add or remove a character.
                <p/>
                Right-click any figure to remove it.
              </React.Fragment>
            :
              <React.Fragment>
                Left-click the board to add a character.
                <p/>
                Left-click a character to select it. While selected, the initiative order of a character can be set. 
                <p/>
                Right-click any figure to remove it.
              </React.Fragment>
          }
        />
        <BrushButton
          brush={BRUSH.MONSTER}
          selection={props.selection}
          onClick={props.onSelection}
          text='Monster'
          icon={
            <FigureIcon
              x='0'
              y='0'
              figure={BRUSH.MONSTER}
              flying={props.flying}
              initiative={props.initiative}
              activeFaction={props.activeFaction}
            />
          }
          tooltip={props.activeFaction
            ?
              <React.Fragment>
                Left-click the board to add a monster.
                <p/>
                Left-click a monster to select it. While selected, the initiative order of a monster can be set. 
                <p/>
                Right-click any figure to remove it.
              </React.Fragment>
            :
              <React.Fragment>
                Left-click the board to add or remove a monster.
                <p/>
                Right-click any figure to remove it.
              </React.Fragment>
          }
        />
        <BrushButton
          brush={BRUSH.WALL}
          selection={props.selection}
          onClick={props.onSelection}
          text='Wall'
          icon={
            <polygon
              className='wall'
              points={BASE_HEX_POINTS}
              pointerEvents='none'
            />
          }
          tooltip={
            <React.Fragment>
              Left-click the board to add or remove a wall.
              <p/>
              Right-click any overlay tile to remove it.
            </React.Fragment>
          }
        />
        <BrushButton
          brush={BRUSH.OBSTACLE}
          selection={props.selection}
          onClick={props.onSelection}
          text='Obstacle'
          icon={
            <polygon
              className='obstacle'
              points={BASE_HEX_POINTS}
              pointerEvents='none'
            />
          }
          tooltip={
            <React.Fragment>
              Left-click the board to add or remove an obstacle.
              <p/>
              Right-click any overlay tile to remove it.
            </React.Fragment>
          }
        />
        <BrushButton
          brush={BRUSH.TRAP}
          selection={props.selection}
          onClick={props.onSelection}
          text='Trap'
          icon={
            <polygon
              className='trap'
              points={BASE_HEX_POINTS}
              pointerEvents='none'
            />
          }
          tooltip={
            <React.Fragment>
              Left-click the board to add or remove a trap.
              <p/>
              Right-click any overlay tile to remove it.
            </React.Fragment>
          }
        />
        <BrushButton
          brush={BRUSH.HAZARDOUS_TERRAIN}
          selection={props.selection}
          onClick={props.onSelection}
          text='Hazardous Terrain'
          icon={
            <polygon
              className='hazardous-terrain'
              points={BASE_HEX_POINTS}
              pointerEvents='none'
            />
          }
          tooltip={
            <React.Fragment>
              Left-click the board to add or remove hazardous terrain.
              <p/>
              Right-click any overlay tile to remove it.
            </React.Fragment>
          }
        />
        <BrushButton
          brush={BRUSH.DIFFICULT_TERRAIN}
          selection={props.selection}
          onClick={props.onSelection}
          text='Difficult Terrain'
          icon={
            <polygon
              className='difficult-terrain'
              points={BASE_HEX_POINTS}
              pointerEvents='none'
            />
          }
          tooltip={
            <React.Fragment>
              Left-click the board to add or remove difficult terrain.
              <p/>
              Right-click any overlay tile to remove it.
            </React.Fragment>
          }
        />
        <BrushButton
          brush={BRUSH.ICY_TERRAIN}
          selection={props.selection}
          onClick={props.onSelection}
          text='Icy Terrain'
          icon={
            <polygon
              className='icy-terrain'
              points={BASE_HEX_POINTS}
              pointerEvents='none'
            />
          }
          tooltip={
            <React.Fragment>
              Left-click the board to add or remove icy terrain.
              <p/>
              Right-click any overlay tile to remove it.
            </React.Fragment>
          }
        />
        <BrushButton
          brush={BRUSH.THIN_WALL}
          selection={props.selection}
          onClick={props.onSelection}
          text='Wall Line'
          icon={
            <polyline
              className='wall'
              points={BASE_WALL_POINTS}
              pointerEvents='none'
            />
          }
          tooltip={
            <React.Fragment>
              Left-click the board to add or remove a thin wall.
              <p/>
              Right-click a thin wall to remove it.
            </React.Fragment>
          }
        />
      </div>
    </div>
  );
} );
export default BrushPicker;