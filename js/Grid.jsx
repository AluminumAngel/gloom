import React from 'react';
import * as C from './defines';
import * as BRUSH from './brushes';
import * as OVERLAY_BRUSH from './overlay_brushes';
import BorderGrid from './BorderGrid';
import DragFigure from './DragFigure';
import FigureGrid from './FigureGrid';
import HexGrid from './HexGrid';
import OverlayHexGrid from './OverlayHexGrid';
import SightLines from './SightLines';
import SightPoints from './SightPoints';
import DebugLines from './DebugLines';
import WallGrid from './WallGrid';

const VIEW_BOX_SANDARD = -( C.GRID_MARGIN + C.GRID_DELTA ) + ' ' + -C.GRID_MARGIN + ' ' + ( C.GRID_EXTENT ) + ' ' + ( C.GRID_EXTENT );
const VIEW_BOX_ROTATED = -C.GRID_MARGIN + ' ' + -( C.GRID_MARGIN + C.GRID_DELTA ) + ' ' + ( C.GRID_EXTENT ) + ' ' + ( C.GRID_EXTENT );

const GridDefs = React.memo( function( props ) {
  const x_fade_margin = C.GRID_MARGIN + C.GRID_DELTA;
  const y_fade_margin = C.GRID_MARGIN;
  return (
    <defs>
      <linearGradient id='fade-gradient-top' y2='1' x2='0'>
        <stop offset='0' stopColor='black'/>
        <stop offset='1' stopColor='white'/>
      </linearGradient>
      <linearGradient id='fade-gradient-bottom' y2='1' x2='0'>
        <stop offset='0' stopColor='white'/>
        <stop offset='1' stopColor='black'/>
      </linearGradient>
      <linearGradient id='fade-gradient-left' y2='0' x2='1'>
        <stop offset='0' stopColor='black'/>
        <stop offset='1' stopColor='white'/>
      </linearGradient>
      <linearGradient id='fade-gradient-right' y2='0' x2='1'>
        <stop offset='0' stopColor='white'/>
        <stop offset='1' stopColor='black'/>
      </linearGradient>
      <mask id='edge-fade' maskContentUnits='userSpaceOnUse'>
        <rect x={-x_fade_margin} y={-y_fade_margin} width={x_fade_margin} height={C.GRID_SCALED_HEIGHT + 2 * y_fade_margin} fill='url(#fade-gradient-left)'/>
        <rect x={C.GRID_SCALED_WIDTH} y={-y_fade_margin} width={x_fade_margin} height={C.GRID_SCALED_HEIGHT + 2 * y_fade_margin} fill='url(#fade-gradient-right)'/>
        <rect x={0} y={-y_fade_margin} width={C.GRID_SCALED_WIDTH} height={y_fade_margin} fill='url(#fade-gradient-top)'/>
        <rect x={0} y={C.GRID_SCALED_HEIGHT} width={C.GRID_SCALED_WIDTH} height={y_fade_margin} fill='url(#fade-gradient-bottom)'/>
        <rect x={0} y={0} width={C.GRID_SCALED_WIDTH} height={C.GRID_SCALED_HEIGHT} fill='white'/>
      </mask>
    </defs>
  );
} );

// Use to hide the grid when viewing debug plots.
// const Grid = React.memo( function( props ) {
//   return (
//     <svg
//       id='grid_svg'
//       width={C.GRID_EXTENT}
//       height={C.GRID_EXTENT}
//       viewBox={props.rotateGrid ? VIEW_BOX_ROTATED : VIEW_BOX_SANDARD}
//       onMouseUp={props.onGridMouseUp}
//       onMouseLeave={props.onGridMouseLeave}
//     >
//       <GridDefs/>
//       <g transform={props.rotateGrid ? C.GRID_TRANSFORM : ''}>
//         <DebugLines
//           lines={props.displaySolution ? props.debugLines : null}
//         />
//       </g>
//     </svg>
//   );
// } );

const Grid = React.memo( function( props ) {
  return (
    <svg
      id='grid_svg'
      width={C.GRID_EXTENT}
      height={C.GRID_EXTENT}
      viewBox={props.rotateGrid ? VIEW_BOX_ROTATED : VIEW_BOX_SANDARD}
      onMouseUp={props.onGridMouseUp}
      onMouseLeave={props.onGridMouseLeave}
    >
      <GridDefs/>
      <g transform={props.rotateGrid ? C.GRID_TRANSFORM : ''}>
        <HexGrid
          grid={props.grid}
          activeHexes={props.activeHexes}
          onHexClick={props.onHexClick}
          onHexMouseDown={props.onHexMouseDown}
          onHexMouseUp={props.onHexMouseUp}
        />
        <BorderGrid/>
        <WallGrid
          walls={props.walls}
          activeWalls={!props.activeHexes}
          onWallClick={props.onWallClick}
        />
        <OverlayHexGrid
          show={props.displaySolution}
          grid={props.aoe}
          content={OVERLAY_BRUSH.AOE}
        />
        <OverlayHexGrid
          show={props.displaySolution}
          grid={props.reach}
          content={OVERLAY_BRUSH.REACH}
        />
        <OverlayHexGrid
          show={props.displaySolution}
          grid={props.sight}
          content={OVERLAY_BRUSH.SIGHT}
        />
        <FigureGrid
          figures={props.figures}
          initiatives={props.initiatives}
          displaySolution={props.displayMoveSolution}
          moves={props.moves}
          destinations={props.destinations}
          attacks={props.attacks}
          focuses={props.focuses}
          flying={props.flying}
          teleport={props.teleport}
          selection={props.selection}
          rotate={props.rotate}
          dragSourceIndex={props.dragSourceIndex}
          activeFaction={props.activeFaction}
          activeFigureIndex={props.activeFigureIndex}
        />
        <SightLines
          lines={props.displaySolution ? props.sightlineLines : null}
          className='unblocked'
        />
        <SightPoints
          points={props.displaySolution ? props.sightlinePoints : null}
          className='unblocked'
        />
        <DebugLines
          lines={props.displaySolution ? props.debugLines : null}
        />
        <DragFigure
          ref={props.dragRef}
          activeFaction={props.active_faction}
          onDragStart={props.onDragStart}
        />
      </g>
    </svg>
  );
} );
export default Grid;