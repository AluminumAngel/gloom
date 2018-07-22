import React from 'react';
import { UncontrolledTooltip } from 'reactstrap';
import axios from 'axios';
import * as C from './defines';
import * as BRUSH from './brushes';
import AOEHexGrid from './AOEHexGrid';
import BorderGrid from './BorderGrid';
import BrushPicker from './BrushPicker';
import DragFigure from './DragFigure';
import FigureGrid from './FigureGrid';
import HexGrid from './HexGrid';
import NumberSelector from './NumberSelector';
import OverlayHexGrid from './OverlayHexGrid';
import WallGrid from './WallGrid';

const DISPLAY_ALL_ACTIONS = -1;
const NULL_INDEX = -1;

const MAX_INITIATIVE = 9;

const ACTION_WAITING_ON_SOLUTION = 0;
const ACTION_WAITING_ON_VIEW = 1;
const ACTION_NO_ACTIVE_FIGURE = 2;
const ACTION_SCENARIO_TOO_COMPLEX = 3;
const ACTION_NO_REQUEST = 4;
const ACTION_REQUEST_SOLUTION = 5;
const ACTION_REQUEST_START_VIEWS = 6;
const ACTION_REQUEST_SOLUTION_VIEWS = 7;
const ACTION_NONE_REQUIRED = 8;
// const ACTION_NAMED = [
//   'ACTION_WAITING_ON_SOLUTION',
//   'ACTION_WAITING_ON_VIEW',
//   'ACTION_NO_ACTIVE_FIGURE',
//   'ACTION_SCENARIO_TOO_COMPLEX',
//   'ACTION_NO_REQUEST',
//   'ACTION_REQUEST_SOLUTION',
//   'ACTION_REQUEST_START_VIEWS',
//   'ACTION_REQUEST_SOLUTION_VIEWS',
//   'ACTION_NONE_REQUIRED',
// ];

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
];
const FLYING_OPTIONS = [
  [ 0, 'none' ],
  [ 1, 'jumping' ],
  [ 2, 'flying' ],
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
  [ MAX_INITIATIVE, '9' ],
];

const ORDINAL_SUFFIXES = [
  'th',
  'st',
  'nd',
  'rd',
  'th',
  'th',
  'th',
  'th',
  'th',
  'th',
  'th',
  'th',
  'th',
  'th',
];

const NUMBER_WORDS = [
  'one',
  'two',
  'three',
  'four',
  'five',
  'six',
  'seven',
  'eight',
  'nine',
  'ten',
  'eleven',
  'twelve',
];

const STATE_KEYS = [
  // tools state
  // 'brush',
  'rotate_grid',
  // 'show_movement',
  // 'show_reach',
  // 'show_sight',

  // scenario state
  'grid',
  'figures',
  'initiatives',
  'walls',
  'active_figure_index',
  'move',
  'range',
  'target',
  'flying',
  'muddled',
  'aoe_grid',
  'active_faction',
];

function isFigureAllowed( content ) {
  return content !== BRUSH.WALL;
}

function isFigureBrush( brush ) {
  return brush === BRUSH.MONSTER || brush === BRUSH.CHARACTER
}

function getOrdinalWord( value ) {
  if ( value < ORDINAL_SUFFIXES.length ) {
    return value + ORDINAL_SUFFIXES[value];
  }
  else {
    return value + ORDINAL_SUFFIXES[value % 10];
  }
}

function getNumberWord( value ) {
  if ( value <= NUMBER_WORDS.length ) {
    return NUMBER_WORDS[value - 1];
  }
  return value;
}

export default class MapEditor extends React.PureComponent {
  constructor( props ) {
    super( props );

    this.drag_ref = React.createRef();
    this.localStorageAvailable = this.isLocalStorageAvailable();

    this.state = {
      // app state
      solution_pending: false,
      views_pending: false,
      scenario_id: 1,
      drag_source_index: NULL_INDEX,
      selection: NULL_INDEX,

      // tools state
      brush: BRUSH.ACTIVE_FIGURE,
      rotate_grid: false,
      show_movement: !START_IN_LOS_MODE,
      show_reach: false,
      show_sight: START_IN_LOS_MODE,

      // scenario state
      grid: Array( C.GRID_SIZE ).fill( 0 ),
      figures: Array( C.GRID_SIZE ).fill( 0 ),
      initiatives: Array( C.GRID_SIZE ).fill( 1 ),
      walls: Array( 3 * C.GRID_SIZE ).fill( false ),
      active_figure_index: NULL_INDEX,
      move: 2,
      range: 0,
      target: 1,
      flying: 0,
      muddled: 0,
      aoe_grid: Array( C.AOE_SIZE ).fill( false ),
      active_faction: false,

      // dependent state
      scenario_too_complex: false,
      next_initiative: 1,
      target_count: 0,

      // solution state
      solution_scenario_id: 0,
      solution_actions: null,
      solution_actions_reach: null,
      solution_actions_sight: null,
      solution_start_reach: null,
      solution_start_sight: null,
      action_displayed: DISPLAY_ALL_ACTIONS,
      display_moves: Array( C.GRID_SIZE ).fill( false ),
      display_attacks: Array( C.GRID_SIZE ).fill( false ),
      display_aoe: Array( C.GRID_SIZE ).fill( false ),
      display_reach: Array( C.GRID_SIZE ).fill( false ),
      display_sight: Array( C.GRID_SIZE ).fill( false ),
    };
    this.restoreState( this.state );
    this.storeState( this.state );

    this.componentDidUpdate();

    if ( !DEVELOPMENT ) {
      gtag( 'event', 'screen_view', {
        screen_name: 'Map Editor',
        app_name: APP_NAME,
        app_version: APP_VERSION,
      } );
    }
  }

  storeState( state ) {
    if ( !this.localStorageAvailable ) return;

    STATE_KEYS.forEach( ( key ) => {
      if ( key in state ) {
        localStorage.setItem( key, JSON.stringify( state[key] ) );
      }
    } );
  }

  restoreState( state ) {
    if ( !this.localStorageAvailable ) return;

    var previous_version = localStorage.getItem( 'version' )
    if ( previous_version !== DATA_VERSION ) {
      localStorage.clear();
    }
    else {
      STATE_KEYS.forEach( ( key ) => {
        var value = localStorage.getItem( key );
        if ( value ) {
          state[key] = JSON.parse( value );
        }
      } );

      state['next_initiative'] = this.determineNextInitiative( state.figures, state.initiatives, state.active_faction );
      this.addDependentData( state );
    }
    
    localStorage.setItem( 'version', DATA_VERSION );
  }

  isLocalStorageAvailable() {
    // https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API/Using_the_Web_Storage_API
    try {
      var storage = window['localStorage'];
      const test_key = '__gloom_storage_test__';
      storage.setItem( test_key, test_key );
      storage.removeItem( test_key );
      return true;
    }
    catch ( e ) {
      return e instanceof DOMException && (
        e.code === 22 ||
        e.code === 1014 ||
        e.name === 'QuotaExceededError' ||
        e.name === 'NS_ERROR_DOM_QUOTA_REACHED'
      ) && storage.length !== 0;
    }
  }

  componentDidMount() {
    this.reactToUpdate();
  }

  componentDidUpdate() {
    this.reactToUpdate();
  }

  reactToUpdate() {
    setTimeout( () => {
      switch ( this.determineActionRequired() ) {
        case ACTION_WAITING_ON_SOLUTION:
        case ACTION_WAITING_ON_VIEW:
        case ACTION_NO_ACTIVE_FIGURE:
        case ACTION_SCENARIO_TOO_COMPLEX:
        case ACTION_NO_REQUEST:
        case ACTION_NONE_REQUIRED:
          return;

        case ACTION_REQUEST_SOLUTION:
          this.handleRequestSolution();
          return;

        case ACTION_REQUEST_START_VIEWS:
          this.handleRequestViewsForStart();
          return;

        case ACTION_REQUEST_SOLUTION_VIEWS:
          this.handleRequestViewsForActions();
          return;
      }
    }, 0 );
  }

  determineActionRequired() {
    if ( this.state.solution_pending ) {
      return ACTION_WAITING_ON_SOLUTION;
    }
    if ( this.state.views_pending ) {
      return ACTION_WAITING_ON_VIEW;
    }

    if ( this.state.active_figure_index === NULL_INDEX ) {
      return ACTION_NO_ACTIVE_FIGURE;
    }

    if ( this.state.scenario_id !== this.state.solution_scenario_id ) {
      if ( this.state.show_movement ) {
        if ( !this.state.scenario_too_complex ) {
          return ACTION_REQUEST_SOLUTION;
        }
        else {
          return ACTION_SCENARIO_TOO_COMPLEX;
        }
      }
      else if ( this.state.show_reach || this.state.show_sight ) {
        return ACTION_REQUEST_START_VIEWS;
      }
      else {
        return ACTION_NO_REQUEST;
      }
    }
    else {
      if ( this.state.show_movement ) {
        if ( !this.state.solution_actions ) {
          if ( !this.state.scenario_too_complex ) {
            return ACTION_REQUEST_SOLUTION;
          }
          else {
            return ACTION_SCENARIO_TOO_COMPLEX;
          }
        }
        else if ( ( this.state.show_reach && !this.state.solution_actions_reach ) || ( this.state.show_sight && !this.state.solution_actions_sight ) ) {
          return ACTION_REQUEST_SOLUTION_VIEWS;
        }
        else {
          return ACTION_NONE_REQUIRED;
        }
      }
      else {
        if ( ( this.state.show_reach && !this.state.solution_start_reach ) || ( this.state.show_sight && !this.state.solution_start_sight ) ) {
          return ACTION_REQUEST_START_VIEWS;
        }
        else {
          return ACTION_NONE_REQUIRED;
        }
      }
    }
  }

  handleWallClick = ( primary, index ) => {
    var walls = this.state.walls.slice();
    var wall = walls[index];
    if ( primary ) {
      wall = !wall; 
    }
    else {
      wall = false;
    }
    walls[index] = wall;
    this.setScenario( {
      walls: walls,
      selection: NULL_INDEX,
    } );
  };

  handleAOEHexClick = ( primary, index ) => {
    var aoe_grid = this.state.aoe_grid.slice();
    var aoe = aoe_grid[index];
    if ( primary ) {
      aoe = !aoe;
    }
    else {
      aoe = false;
    }
    aoe_grid[index] = aoe;
    this.setScenario( {
      aoe_grid: aoe_grid,
    } );
  };

  handleHexMouseDown = ( x, y, index, c, r ) => {
    if ( this.drag_ref.current.active ) return;
    if ( this.state.brush !== BRUSH.PROGRESS ) return;
    if ( this.state.figures[index] === BRUSH.EMPTY ) return;

    var figure = this.state.figures[index];
    if ( this.state.active_figure_index === index ) {
      figure += BRUSH.FIRST_ACTIVE_BRUSH - BRUSH.FIRST_FIGURE_BRUSH;
    }

    this.drag_ref.current.activate(
      x,
      y,
      index,
      c,
      r,
      figure,
      this.state.initiatives[index],
      this.state.flying,
      this.state.rotate_grid
    );
  };

  handleDragStart = ( index ) => {
    this.setState( {
      selection: NULL_INDEX,
      drag_source_index: index,
    } );
    this.drag_ref.current.suppress_clicks = true;
  };

  handleGridMouseUp = () => {
    this.handleHexMouseUp( NULL_INDEX );
    this.drag_ref.current.suppress_clicks = false;
  };

  handleGridMouseLeave = () => {
    this.handleHexMouseUp( NULL_INDEX );
    this.drag_ref.current.suppress_clicks = false;
  };

  handleHexMouseUp = ( index ) => {
    const dragging = this.drag_ref.current.state.dragging;
    this.drag_ref.current.deactivate();
    if ( !dragging ) return;

    const return_figure = index === this.state.drag_source_index
      || index === NULL_INDEX
      || !isFigureAllowed( this.state.grid[index] );
    if ( return_figure ) {
      const selection = this.state.figures[this.state.drag_source_index] === this.inactiveFactionBrush()
        ? this.state.drag_source_index
        : NULL_INDEX;
      this.setState( {
        selection: selection,
        drag_source_index: NULL_INDEX,
      } );
      return;
    }

    this.drag_ref.current.suppress_clicks = false;

    const figure = this.state.figures[this.state.drag_source_index];
    const initiative = this.state.initiatives[this.state.drag_source_index];

    var figures = this.state.figures.slice();
    var initiatives = this.state.initiatives.slice();

    figures[index] = figure;
    figures[this.state.drag_source_index] = BRUSH.EMPTY;
    initiatives[index] = initiative;

    const selection = figure === this.inactiveFactionBrush()
      ? index
      : NULL_INDEX;

    var active_figure_index = this.state.active_figure_index;
    if ( this.state.active_figure_index === this.state.drag_source_index ) {
      active_figure_index = index;
    }

    this.setScenario( {
      figures: figures,
      initiatives: initiatives,
      selection: selection,
      active_figure_index: active_figure_index,
      drag_source_index: NULL_INDEX,
    } );
  };

  determineNextInitiative( figures, initiatives, active_faction ) {
    var initiatives_used = Array( MAX_INITIATIVE ).fill( false );
    const inactive_faction_brush = active_faction ? BRUSH.MONSTER : BRUSH.CHARACTER;
    figures.forEach( ( figure, index ) => {
      if ( figure === inactive_faction_brush ) {
        initiatives_used[initiatives[index] - 1] = true;
      }
    } );
    var first_open_initiative;
    for ( first_open_initiative = 0; first_open_initiative < MAX_INITIATIVE; first_open_initiative++ ) {
      if ( !initiatives_used[first_open_initiative] ) break;
    }
    return Math.min( first_open_initiative + 1, MAX_INITIATIVE );
  }

  activeFactionBrush() {
    return this.state.active_faction ? BRUSH.CHARACTER : BRUSH.MONSTER;
  }

  inactiveFactionBrush() {
    return this.state.active_faction ? BRUSH.MONSTER : BRUSH.CHARACTER;
  }

  handleHexClick = ( primary, index ) => {
    if ( this.drag_ref.current.suppress_clicks ) {
      this.drag_ref.current.suppress_clicks = false;
      return;
    }

    const content = this.state.grid[index];
    const figure = this.state.figures[index];
    const initiative = this.state.initiatives[index];

    var grid = null;
    var figures = null;
    var initiatives = null;
    var active_figure_index = this.state.active_figure_index;
    var selection = this.state.selection;

    if ( this.state.brush === BRUSH.PROGRESS ) {
      if ( primary ) {
        if ( isFigureBrush( figure ) ) {
          if ( figure === this.activeFactionBrush() ) {
            if ( this.state.active_figure_index !== index ) {
              active_figure_index = index;
              selection = NULL_INDEX;
            }
            else {
              active_figure_index = NULL_INDEX;
              selection = NULL_INDEX;
            }
          }
          else {
            if ( selection !== index ) {
              selection = index;
            }
            else {
              selection = NULL_INDEX;
            }
          }
        }
        else if ( this.state.display_moves[index] && this.isDisplayingSolution() ) {
          initiatives = this.state.initiatives.slice();
          initiatives[index] = initiatives[active_figure_index];
          figures = this.state.figures.slice();
          figures[active_figure_index] = BRUSH.EMPTY;
          figures[index] = this.activeFactionBrush();
          active_figure_index = NULL_INDEX;
          selection = NULL_INDEX;
        }
      }
      else {
        if ( figure !== BRUSH.EMPTY ) {
          if ( index === active_figure_index ) {
            active_figure_index = NULL_INDEX;
          }
          figures = this.state.figures.slice();
          figures[index] = BRUSH.EMPTY;
          selection = NULL_INDEX;
        }
      }
    }
    else {
      if ( primary ) {
        if ( this.state.brush === BRUSH.ACTIVE_FIGURE ) {
          if ( figure === this.activeFactionBrush() && active_figure_index === index ) {
            figures = this.state.figures.slice();
            figures[index] = BRUSH.EMPTY;
            active_figure_index = NULL_INDEX;
            selection = NULL_INDEX;
          }
          else {
            if ( isFigureAllowed( this.state.grid[index] ) ) {
              figures = this.state.figures.slice();
              figures[index] = this.activeFactionBrush();
              initiatives = this.state.initiatives.slice();
              initiatives[index] = 1;
              if ( active_figure_index !== NULL_INDEX ) {
                figures[active_figure_index] = BRUSH.EMPTY;
              }
              active_figure_index = index;
              selection = NULL_INDEX;
            }
          }
        }
        else if ( isFigureBrush( this.state.brush ) ) {
          if ( figure === this.state.brush && active_figure_index !== index ) {
            if ( this.state.brush === this.inactiveFactionBrush() ) {
              if ( selection === index ) {
                selection = NULL_INDEX;
              }
              else {
                selection = index;
              }
            }
            else
            {
              figures = this.state.figures.slice();
              figures[index] = BRUSH.EMPTY;
              selection = NULL_INDEX;
            }
          }
          else {
            if ( isFigureAllowed( this.state.grid[index] ) ) {
              figures = this.state.figures.slice();
              figures[index] = this.state.brush;
              if ( active_figure_index === index ) {
                active_figure_index = NULL_INDEX;
              }
              if ( this.state.brush === this.inactiveFactionBrush() ) {
                initiatives = this.state.initiatives.slice();
                initiatives[index] = this.state.next_initiative;
                selection = index;
              }
              else {
                initiatives = this.state.initiatives.slice();
                initiatives[index] = 1;
                selection = NULL_INDEX;
              }
            }
          }
        }
        else {
          if ( content === this.state.brush ) {
            grid = this.state.grid.slice();
            grid[index] = BRUSH.EMPTY;
            selection = NULL_INDEX;
          }
          else {
            grid = this.state.grid.slice();
            grid[index] = this.state.brush;
            if ( figure !== BRUSH.EMPTY && !isFigureAllowed( this.state.brush ) ) {
              figures = this.state.figures.slice();
              figures[index] = BRUSH.EMPTY;
              if ( active_figure_index === index ) {
                active_figure_index = NULL_INDEX;
              }
            }
            selection = NULL_INDEX;
          }
        }
      }
      else {
        if ( isFigureBrush( this.state.brush ) || this.state.brush === BRUSH.ACTIVE_FIGURE ) {
          if ( figure !== BRUSH.EMPTY ) {
            figures = this.state.figures.slice();
            figures[index] = BRUSH.EMPTY;
            if ( active_figure_index === index ) {
              active_figure_index = NULL_INDEX;
            }
            selection = NULL_INDEX;
          }
        }
        else if ( content !== BRUSH.EMPTY ) {
          grid = this.state.grid.slice();
          grid[index] = BRUSH.EMPTY;
          selection = NULL_INDEX;
        }
      }
    }

    const scenario_changed = grid || figures || initiatives || active_figure_index != this.state.active_figure_index;
    if ( scenario_changed || selection != this.state.selection ) {
      if ( scenario_changed ) {

        // TODO: often don't need to do this
        const next_initiative = this.determineNextInitiative(
          figures ? figures : this.state.figures,
          initiatives ? initiatives : this.state.initiatives,
          this.state.active_faction
        );

        var scenario_update = {
          selection: selection,
          active_figure_index: active_figure_index,
          next_initiative: next_initiative,
        };
        if ( grid ) {
          scenario_update.grid = grid;
        }
        if ( figures ) {
          scenario_update.figures = figures;
        }
        if ( initiatives ) {
          scenario_update.initiatives = initiatives;
        }
        this.setScenario( scenario_update );
      }
      else {
        this.setState( {
          selection: selection,
        } );
      }
    }
  };

  handleBrushSelection = ( brush ) => {
    this.setToolsState( {
      brush: brush
    } );
  };

  handleMapClear = () => {
    this.setScenario( {
      selection: NULL_INDEX,

      grid: Array( C.GRID_SIZE ).fill( BRUSH.EMPTY ),
      figures: Array( C.GRID_SIZE ).fill( BRUSH.EMPTY ),
      initiatives: Array( C.GRID_SIZE ).fill( 1 ),
      walls: Array( 3 * C.GRID_SIZE ).fill( false ),
      active_figure_index: NULL_INDEX,

      next_initiative: 1,
    } );
  };

  handleAOEClear = () => {
    this.setScenario( {
      aoe_grid: Array( C.AOE_SIZE ).fill( false ),
    } );
  };

  handleRotateMapChanged = () => {
    this.setToolsState( {
      rotate_grid: !this.state.rotate_grid,
    } );
  };

  handleDisplayMovementChanged = () => {
    this.setReachSightDisplayed( !this.state.show_movement, this.state.show_reach, this.state.show_sight )
  };

  handleDisplayReachChanged = () => {
    this.setReachSightDisplayed( this.state.show_movement, !this.state.show_reach, false )
  };

  handleDisplaySightChanged = () => {
    this.setReachSightDisplayed( this.state.show_movement, false, !this.state.show_sight )
  };

  handleActiveFactionChanged = () => {
    var figures = this.state.figures;
    if ( this.state.active_figure_index !== NULL_INDEX ) {
      figures = figures.slice();
      figures[this.state.active_figure_index] = this.state.active_faction
        ? BRUSH.CHARACTER
        : BRUSH.MONSTER;
    }

    const active_faction = !this.state.active_faction;
    const next_initiative = this.determineNextInitiative( figures, this.state.initiatives, active_faction );

    this.setScenario( {
      figures: figures,
      active_figure_index: NULL_INDEX,
      selection: NULL_INDEX,
      next_initiative: next_initiative,
      active_faction: !this.state.active_faction,
    } );
  };

  handleMoveChange = ( value ) => {
    this.setScenario( {
      move: value,
    } );
  };

  handleRangeChange = ( value ) => {
    this.setScenario( {
      range: value,
    } );
  };

  handleTargetChange = ( value ) => {
    this.setScenario( {
      target: value,
    } );
  };

  handleFlyingChange = ( value ) => {
    this.setScenario( {
      flying: value,
    } );
  };

  handleMuddledChange = ( value ) => {
    this.setScenario( {
      muddled: value,
    } );
  };

  handleInitiativeChange = ( value ) => {
    if ( this.state.selection !== -1 ) {

      var initiatives = this.state.initiatives.slice();
      initiatives[this.state.selection] = value;

      var next_initiative = this.determineNextInitiative( this.state.figures, initiatives, this.state.active_faction );

      this.setScenario( {
        initiatives: initiatives,
        next_initiative: next_initiative,
      } );
    }
  };

  unpackSolution( solution ) {
    var solution_state;
    if ( this.state.solution_scenario_id !== solution.scenario_id ) {
      solution_state = {
        solution_scenario_id: solution.scenario_id,

        solution_actions: solution.actions.slice(),
        solution_actions_reach: solution.reach ? solution.reach.slice() : null,
        solution_actions_sight: solution.sight ? solution.sight.slice() : null,
        solution_start_reach: null,
        solution_start_sight: null,
      };
    }
    else {
      solution_state = {
        solution_actions: solution.actions.slice(),
        solution_actions_reach: solution.reach ? solution.reach.slice() : null,
        solution_actions_sight: solution.sight ? solution.sight.slice() : null,
      }
    }

    // if possible, use view data for the start views
    if ( solution.reach || solution.sight ) {
      for ( var index = 0; index < solution.actions.length; index++ ) {
        if ( solution.actions[index].move === this.state.active_figure_index ) {
          if ( solution.reach ) {
            solution_state['solution_start_reach'] = solution.reach[index].slice();
          }
          if ( solution.sight ) {
            solution_state['solution_start_sight'] = solution.sight[index].slice();
          }
          break;        
        }
      }
    }

    this.setDisplayedSolution( DISPLAY_ALL_ACTIONS, this.state.show_movement, this.state.show_reach, this.state.show_sight, solution_state );
  }

  unpackViewsForActions( views ) {
    if ( this.state.solution_scenario_id !== views.scenario_id ) {
      return;
    }

    var solution_state = {
      solution_actions_reach: views.reach ? views.reach.slice() : null,
      solution_actions_sight: views.sight ? views.sight.slice() : null,
    };
    this.setDisplayedSolution( this.state.action_displayed, this.state.show_movement, this.state.show_reach, this.state.show_sight, solution_state );
  }

  unpackViewsForStart( views ) {
    var solution_state;
    if ( this.state.solution_scenario_id !== views.scenario_id ) {
      solution_state = {
        solution_scenario_id: views.scenario_id,

        solution_actions: null,
        solution_actions_reach: null,
        solution_actions_sight: null,
        solution_start_reach: views.reach ? views.reach[0].slice() : null,
        solution_start_sight: views.sight ? views.sight[0].slice() : null,
      };
    }
    else {
      solution_state = {
        solution_start_reach: views.reach ? views.reach[0].slice() : null,
        solution_start_sight: views.sight ? views.sight[0].slice() : null,
      };
    }
    this.setDisplayedSolution( this.state.action_displayed, this.state.show_movement, this.state.show_reach, this.state.show_sight, solution_state );
  }

  setActionDisplayed( action_displayed ) {
    if ( action_displayed === this.state.action_displayed ) {
      return;
    }
    this.setDisplayedSolution( action_displayed, this.state.show_movement, this.state.show_reach, this.state.show_sight, null );
  }

  setReachSightDisplayed( show_movement, show_reach, show_sight ) {
    if ( show_movement === this.state.show_movement ) {
      if ( show_reach === this.state.show_reach ) {
        if ( show_sight === this.state.show_sight ) {
          return;
        }
      }
    }

    var action_displayed;
    if ( show_movement && !this.state.show_movement ) {
      action_displayed = DISPLAY_ALL_ACTIONS;
    } else {
      action_displayed = this.state.action_displayed;
    }

    this.setDisplayedSolution( action_displayed, show_movement, show_reach, show_sight, null );
  }

  setDisplayedSolution( action_displayed, show_movement, show_reach, show_sight, solution_state ) {
    var solution_actions = solution_state && solution_state.solution_actions ? solution_state.solution_actions : this.state.solution_actions;
    var solution_actions_reach = solution_state && solution_state.solution_actions_reach ? solution_state.solution_actions_reach : this.state.solution_actions_reach;
    var solution_actions_sight = solution_state && solution_state.solution_actions_sight ? solution_state.solution_actions_sight : this.state.solution_actions_sight;
    var solution_start_reach = solution_state && solution_state.solution_start_reach ? solution_state.solution_start_reach : this.state.solution_start_reach;
    var solution_start_sight = solution_state && solution_state.solution_start_sight ? solution_state.solution_start_sight : this.state.solution_start_sight;
    
    var moves = Array( C.GRID_SIZE ).fill( false );
    var attacks = Array( C.GRID_SIZE ).fill( false );
    var aoe = Array( C.GRID_SIZE ).fill( false );
    var reach = Array( C.GRID_SIZE ).fill( false );
    var sight = Array( C.GRID_SIZE ).fill( false );

    if ( show_movement ) {
      if ( solution_actions ) { 
        if ( action_displayed === DISPLAY_ALL_ACTIONS ) {
          for ( var index = 0; index < solution_actions.length; index++ ) {
            moves[solution_actions[index].move] = true;
            solution_actions[index].attacks.forEach( ( location ) => {
              attacks[location] = true;
            } );
            solution_actions[index].aoe.forEach( ( location ) => {
              aoe[location] = true;
            } );
            if ( show_reach && solution_actions_reach ) {
              solution_actions_reach[index].forEach( ( range ) => {
                for ( var location = range[0]; location < range[1]; location++ ) {
                  reach[location] = true;
                }
              } );
            }
            if ( show_sight && solution_actions_sight ) {
              solution_actions_sight[index].forEach( ( range ) => {
                for ( var location = range[0]; location < range[1]; location++ ) {
                  sight[location] = true;
                }
              } );
            }
          }
        }
        else {
          moves[solution_actions[action_displayed].move] = true;
          solution_actions[action_displayed].attacks.forEach( ( location ) => {
            attacks[location] = true;
          } );
          solution_actions[action_displayed].aoe.forEach( ( location ) => {
            aoe[location] = true;
          } );
          if ( show_reach && solution_actions_reach ) {
            solution_actions_reach[action_displayed].forEach( ( range ) => {
              for ( var location = range[0]; location < range[1]; location++ ) {
                reach[location] = true;
              }
            } );
          }
          if ( show_sight && solution_actions_sight ) {
            solution_actions_sight[action_displayed].forEach( ( range ) => {
              for ( var location = range[0]; location < range[1]; location++ ) {
                sight[location] = true;
              }
            } );
          }
        }
      }
    }
    else {
      if ( show_reach && solution_start_reach ) {
        solution_start_reach.forEach( ( range ) => {
          for ( var location = range[0]; location < range[1]; location++ ) {
            reach[location] = true;
          }
        } );
      }
      if ( show_sight && solution_start_sight ) {
        solution_start_sight.forEach( ( range ) => {
          for ( var location = range[0]; location < range[1]; location++ ) {
            sight[location] = true;
          }
        } );
      }
    }

    var display_state = {
      action_displayed: action_displayed,
      show_movement: show_movement,
      show_reach: show_reach,
      show_sight: show_sight,
      display_moves: moves,
      display_attacks: attacks,
      display_aoe: aoe,
      display_reach: reach,
      display_sight: sight,
    };
    this.setToolsState( Object.assign( display_state, solution_state ) );
  }

  getSolveViewLevel() {
    if ( this.state.show_sight ) {
      return 2;
    }
    else if ( this.state.show_reach ) {
      return 1;
    }
    else {
      return 0;
    }
  }

  packScenario() {
    var scenario = {
      scenario_id: this.state.scenario_id,
      solve_view: this.getSolveViewLevel(),

      active_figure: this.state.active_figure_index,
      move: this.state.move,
      range: this.state.range,
      target: this.state.target,
      flying: this.state.flying,
      muddled: this.state.muddled,
      aoe: [],

      width: C.GRID_WIDTH,
      height: C.GRID_HEIGHT,
      map: {},
    };

    this.state.aoe_grid.forEach( ( element, index ) => {
      if ( element ) {
        scenario.aoe.push( index );
      }
    } );

    function add_elements( map_layer, key, brush ) {
      scenario.map[key] = [];
      map_layer.forEach( ( element, index ) => {
        if ( element === brush ) {
          scenario.map[key].push( index );
        }
      } );
    }

    // TODO: currently sending active figure twice (in monster and active_figure)
    add_elements( this.state.figures, 'characters', BRUSH.CHARACTER );
    add_elements( this.state.figures, 'monsters', BRUSH.MONSTER  );
    add_elements( this.state.grid, 'walls', BRUSH.WALL );
    add_elements( this.state.grid, 'obsticles', BRUSH.OBSTICLE );
    add_elements( this.state.grid, 'traps', BRUSH.TRAP );
    add_elements( this.state.grid, 'hazardous', BRUSH.HAZARDOUS_TERRAIN );
    add_elements( this.state.grid, 'difficult', BRUSH.DIFFICULT_TERRAIN );

    const inactive_faction_brush = this.inactiveFactionBrush();
    scenario.map.initiatives = [];
    this.state.figures.forEach( ( figure, index ) => {
      if ( figure === inactive_faction_brush ) {
        scenario.map.initiatives.push( this.state.initiatives[index] );
      }
    } );

    scenario.map.thin_walls = [];
    this.state.walls.forEach( ( wall, index ) => {
      if ( wall ) {
        scenario.map.thin_walls.push( [ Math.trunc( index / 3 ), index % 3 ] );
      }
    } );

    return scenario;
  }

  // TODO: clean
  packScenarioForViews() {
    var scenario = {
      scenario_id: this.state.scenario_id,
      solve_view: this.getSolveViewLevel(),

      range: this.state.range,
      target: this.state.target,

      width: C.GRID_WIDTH,
      height: C.GRID_HEIGHT,
      map: {},
    };

    function add_elements( map_layer, key, brush ) {
      scenario.map[key] = [];
      map_layer.forEach( ( element, index ) => {
        if ( element === brush ) {
          scenario.map[key].push( index );
        }
      } );
    }

    add_elements( this.state.grid, 'walls', BRUSH.WALL );

    scenario.map.thin_walls = [];
    this.state.walls.forEach( ( wall, index ) => {
      if ( wall ) {
        scenario.map.thin_walls.push( [ Math.trunc( index / 3 ), index % 3 ] );
      }
    } );

    return scenario;
  }  

  // unpackscenario( scenario ) {
  //   var grid = Array( C.GRID_SIZE ).fill( 0 );
  //   var figures = Array( C.GRID_SIZE ).fill( 0 );
  //   var initiatives = Array( C.GRID_SIZE ).fill( 1 );
  //   var walls = Array( 3 * C.GRID_SIZE ).fill( false );
  //   var aoe_grid = Array( C.AOE_SIZE ).fill( false );

  //   function get_index( c, r ) {
  //     return r + c * C.GRID_HEIGHT;
  //   }

  //   // TODO: clean data
  //   // TODO: don't allow more than one active monster
  //   // TODO: validate characters on walls and obstables
  //   // TODO: validate thins vs standard walls

  //   var map = scenario.map;
  //   function add_elements( map_layer, key, brush ) {
  //     map[key].forEach( ( item ) => {
  //       map_layer[get_index( item[0], item[1] )] = brush;
  //     } );
  //   }

  //   add_elements( figures, 'characters', BRUSH.CHARACTER );
  //   add_elements( figures, 'monsters', BRUSH.MONSTER  );
  //   add_elements( grid, 'walls', BRUSH.WALL );
  //   add_elements( grid, 'obsticles', BRUSH.OBSTICLE );
  //   add_elements( grid, 'traps', BRUSH.TRAP );
  //   add_elements( grid, 'hazardous', BRUSH.HAZARDOUS_TERRAIN );
  //   add_elements( grid, 'difficult', BRUSH.DIFFICULT_TERRAIN );

  //   for ( var i = 0; i < map['initiatives'].length; i++ )
  //   {
  //     initiatives[get_index(map['characters'][i][0],map['characters'][i][1])] = map['initiatives'][i];
  //   }

  //   for ( var i = 0; i < map['thin_walls'][0].length; i++ )
  //   {
  //     walls[0+3*get_index(map['thin_walls'][0][i][0], map['thin_walls'][0][i][1])] = true;
  //   }
  //   for ( var i = 0; i < map['thin_walls'][1].length; i++ )
  //   {
  //     walls[1+3*get_index(map['thin_walls'][1][i][0], map['thin_walls'][1][i][1])] = true;
  //   }
  //   for ( var i = 0; i < map['thin_walls'][2].length; i++ )
  //   {
  //     walls[2+3*get_index(map['thin_walls'][2][i][0], map['thin_walls'][2][i][1])] = true;
  //   }

  //   for ( var i = 0; i < scenario.aoe.length; i++ )
  //   {
  //     aoe_grid[scenario.aoe[i]] = true;
  //   }

  //   const active_figure_index = get_index( scenario.active_figure[0], scenario.active_figure[1] );

  //   this.setScenario( {
  //     grid: grid,
  //     figures: figures,
  //     initiatives: initiatives,
  //     walls: walls,
  //     selection: NULL_INDEX,
  //     active_figure_index: active_figure_index,

  //     move: scenario.move,
  //     range: scenario.range,
  //     target: scenario.target,
  //     flying: scenario.flying,
  //     muddled: scenario.muddled,
  //     aoe_grid: aoe_grid,
  //   } );
  // }

  handleRequestSolution = () => {
    if ( !DEVELOPMENT ) {
      gtag( 'event', 'request', {
        event_category: 'Solution',
        event_label: this.state.active_faction ? 'characters' : 'monsters',
        value: this.state.target_count,
      } );
    }

    var scenario = this.packScenario();
    this.setState( {
      solution_pending: true,
    } );
    axios.put( URL_FOR.solve, scenario )
      .then( ( response ) => {
        this.setState( {
          solution_pending: false,
        } );
        this.unpackSolution( response.data );
      } )
      .catch( () => {
        this.setState( {
          solution_pending: false,
        } );
      } );
  };

  // TODO: clean
  handleRequestViewsForActions = () => {
    var viewpoints = [];
    for ( var i = 0; i < this.state.solution_actions.length; i++ ) {
      viewpoints.push( this.state.solution_actions[i]['move'] );
    }

    if ( !DEVELOPMENT ) {
      gtag( 'event', 'request', {
        event_category: 'SolutionViews',
        event_label: this.getSolveViewLevel() > 1 ? 'sight' : 'reach',
        value: viewpoints.length,
      } );
    }

    var views_request = this.packScenarioForViews();
    views_request['viewpoints'] = viewpoints;
    this.setState( {
      views_pending: true,
    } );
    axios.put( URL_FOR.views, views_request )
      .then( ( response ) => {
        this.setState( {
          views_pending: false,
        } );
        this.unpackViewsForActions( response.data );
      } )
      .catch( () => {
        this.setState( {
          views_pending: false,
        } );
      } );
  };

  // TODO: clean
  handleRequestViewsForStart = () => {
    var viewpoints = [ this.state.active_figure_index ];

    if ( !DEVELOPMENT ) {
      gtag( 'event', 'request', {
        event_category: 'StartViews',
        event_label: this.getSolveViewLevel() > 1 ? 'sight' : 'reach',
        value: viewpoints.length,
      } );
    }

    var views_request = this.packScenarioForViews();
    views_request['viewpoints'] = viewpoints;
    this.setState( {
      views_pending: true,
    } );
    axios.put( URL_FOR.views, views_request )
      .then( ( response ) => {
        // TODO: this is an extra setState()
        this.setState( {
          views_pending: false,
        } );
        this.unpackViewsForStart( response.data );
      } )
      .catch( () => {
        this.setState( {
          views_pending: false,
        } );
      } );
  };

  // handleRequestScenario = () => {
  //   axios.get( URL_FOR.scenario )
  //     .then( ( response ) => {
  //       this.unpackscenario( response.data );
  //     } )
  //     .catch( () => {
  //     } );
  // };

  handlePreviousAction = () => {
    var action_displayed = this.state.action_displayed;
    if ( this.state.solution_actions && this.state.solution_actions.length > 1 ) {
      if ( action_displayed === DISPLAY_ALL_ACTIONS ) {
        action_displayed = this.state.solution_actions.length - 1;
      }
      else if ( action_displayed === 0 ) {
        action_displayed = this.state.solution_actions.length - 1;
      }
      else {
        action_displayed -= 1;
      }
    }
    this.setActionDisplayed( action_displayed );
  };

  handleNextAction = () => {
    var action_displayed = this.state.action_displayed;
    if ( this.state.solution_actions && this.state.solution_actions.length > 1 ) {
      if ( action_displayed === DISPLAY_ALL_ACTIONS ) {
        action_displayed = 0;
      }
      else if ( action_displayed === this.state.solution_actions.length - 1 ) {
        action_displayed = 0;
      }
      else {
        action_displayed += 1;
      }
    }
    this.setActionDisplayed( action_displayed );
  };

  handleAllActions = () => {
    var action_displayed = this.state.action_displayed;
    if ( this.state.solution_actions && this.state.solution_actions.length > 1 ) {
      action_displayed = DISPLAY_ALL_ACTIONS;
    }
    this.setActionDisplayed( action_displayed );
  };

  addDependentData( scenario ) {
    scenario.target_count = 0;
    var inactive_faction_brush = this.inactiveFactionBrush();
    var figures = scenario.figures !== undefined ? scenario.figures : this.state.figures;
    figures.forEach( ( figure ) => {
      if ( figure === inactive_faction_brush ) {
        scenario.target_count++;
      }
    } );

    // TEMP (need to retime with new optimizations)
    // Determine if the scenario is too complex to request a solution.
    // If there are more than 20 characters.
    // If its a ranged aoe and the target count is above 3.
    scenario.scenario_too_complex = false;
    if ( scenario.target_count > 20 ) {
      scenario.scenario_too_complex = true;
    }
    else {
      var target = scenario.target !== undefined ? scenario.target : this.state.target;
      if ( target > 3 ) {
        var range = scenario.range !== undefined ? scenario.range : this.state.range;
        if ( range > 1 ) {
          var active_aoe = false;
          var aoe_grid = scenario.aoe_grid !== undefined ? scenario.aoe_grid : this.state.aoe_grid;
          for ( var index = 0; index < aoe_grid.length; index++ ) {
            if ( aoe_grid[index] ) {
              active_aoe = true;
              break;
            }
          }
          if ( active_aoe ) {
            scenario.scenario_too_complex = true;
          }
        }
      }
    }
  }

  setScenario( scenario ) {
    this.storeState( scenario );

    this.addDependentData( scenario );

    scenario.scenario_id = ( this.state.scenario_id + 1 ) % ( 256 * 256 * 256 );
    this.setState( scenario );
  }

  setToolsState( tools_state ) {
    this.storeState( tools_state );
    this.setState( tools_state );
  }

  isDisplayingSolution() {
    if ( this.state.drag_source_index !== NULL_INDEX ) {
      return false;
    }
    return this.state.scenario_id === this.state.solution_scenario_id;
  }

  render() {
    const display_solution = this.isDisplayingSolution();
    const solution_count = this.state.solution_actions ? this.state.solution_actions.length : 0;
    const multiple_actions = display_solution && solution_count > 1;

    const active_faction_string = this.state.active_faction ? 'character' : 'monster';
    const inactive_faction_string = this.state.active_faction ? 'monster' : 'character';

    const action = this.determineActionRequired();

    var display_move_solution = false;

    var status_label;
    switch ( action ) {
      case ACTION_WAITING_ON_SOLUTION:
      case ACTION_REQUEST_SOLUTION:
        status_label = <span><div className='mr-2 throbber'></div> Solving...</span>
        break;

      case ACTION_WAITING_ON_VIEW:
      case ACTION_REQUEST_START_VIEWS:
      case ACTION_REQUEST_SOLUTION_VIEWS:
        status_label = <span><div className='mr-2 throbber'></div> Calculating...</span>
        break;

      case ACTION_NO_ACTIVE_FIGURE:
      case ACTION_NO_REQUEST:
        status_label = null
        break;

      case ACTION_SCENARIO_TOO_COMPLEX:
        status_label = <span>Too complex. Reduce the target count, area of effect, or {faction_string}.</span>
        break;

      case ACTION_NONE_REQUIRED:
        var status_message;
        if ( this.state.show_movement ) {
          display_move_solution = true;
          if ( this.state.solution_actions ) {
            if ( this.state.solution_actions.length === 1 ) {
              if ( this.state.solution_actions[0].attacks.length === 0 && this.state.solution_actions[0].move === this.state.active_figure_index ) {
                status_message = 'The ' + active_faction_string + ' takes no action.';
              }
              else {
                status_message = 'Showing the only movement option.';
              }
            }
            else if ( this.state.action_displayed === DISPLAY_ALL_ACTIONS ) {
              status_message = 'Showing ' + getNumberWord( solution_count ) + ' movement options.';
            }
            else {
              status_message = 'Showing the ' + getOrdinalWord( this.state.action_displayed + 1 ) + ' of ' + getNumberWord( solution_count ) + ' movement options.';
              if ( this.state.solution_actions[this.state.action_displayed].move === this.state.active_figure_index && this.state.solution_actions[this.state.action_displayed].attacks.length === 0 ) {
                status_message += ' No action taken.';
              }
            }
          }
        }
        else if ( this.state.show_reach ) {
          status_message = 'Showing range.';
        }
        else if ( this.state.show_sight ) {
          status_message = 'Showing line of sight.';
        }
        else {
          status_message = '';
        }
        status_label = <span>{status_message}</span>
        break;
    }    

    const x_margin = C.GRID_MARGIN + ( this.state.rotate_grid ? 0 : C.GRID_DELTA );
    const y_margin = C.GRID_MARGIN + ( this.state.rotate_grid ? C.GRID_DELTA : 0 );
    const view_box = ( -x_margin ) + ' ' + ( -y_margin ) + ' ' + ( C.GRID_EXTENT ) + ' ' + ( C.GRID_EXTENT );

    const x_fade_margin = C.GRID_MARGIN + C.GRID_DELTA;
    const y_fade_margin = C.GRID_MARGIN;

    var class_name = 'container-fluid';
    if ( this.drag_ref.current && this.drag_ref.current.active ) {
      class_name += ' grabbing';
    }

    return (
      <div className={class_name}>
        <div className='d-flex'>
          <div className='mt-5'>

              <BrushPicker
                flying={this.state.flying}
                initiative={this.state.next_initiative}
                selection={this.state.brush}
                activeFaction={this.state.active_faction}
                onSelection={this.handleBrushSelection}
              />

              <NumberSelector
                label='Move'
                options={MOVE_OPTIONS}
                value={this.state.move}
                onChange={this.handleMoveChange}
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
                value={this.state.range}
                onChange={this.handleRangeChange}
                tooltip={
                  <React.Fragment>
                    Set the range of the current attack.
                  </React.Fragment>
                }
              />
              <NumberSelector
                label='Target'
                options={TARGET_OPTIONS}
                value={this.state.target}
                onChange={this.handleTargetChange}
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
                value={this.state.flying}
                onChange={this.handleFlyingChange}
                tooltip={
                  <React.Fragment>
                    Set the movement trait of the current move.
                  </React.Fragment>
                }
              />
              <NumberSelector
                label='Muddled'
                options={MUDDLED_OPTIONS}
                value={this.state.muddled}
                onChange={this.handleMuddledChange}
                tooltip={
                  <React.Fragment>
                    Set whether the active {active_faction_string} is muddled.
                  </React.Fragment>
                }
              />
              <NumberSelector
                label='Initiative'
                options={INITIATIVE_OPTIONS}
                value={this.state.selection == -1 ? 1 : this.state.initiatives[this.state.selection]}
                disabled={this.state.selection == -1}
                onChange={this.handleInitiativeChange}
                tooltip={
                  <React.Fragment>
                    Set the initiative rank of the selected {inactive_faction_string}.
                  </React.Fragment>
                }
              />
          </div>

          <div className='mx-3 mt-2 d-flex flex-column'>
            <div className='mb-2 d-flex'>
              <span className='mr-auto ml-4 col-form-label-sm text-muted'>
                {status_label}
              </span>
              <div className='btn-group mr-4'>
                <button
                  type='button'
                  className='px-3 btn btn-sm btn-dark'
                  id='previous-action-button'
                  disabled={!multiple_actions || !display_move_solution}
                  onClick={this.handlePreviousAction}
                >
                  &lt;&lt;
                </button>
                <UncontrolledTooltip
                  placement='bottom'
                  delay={C.TOOLTIP_DELAY}
                  target='previous-action-button'
                >
                  Show the previous movement option.
                </UncontrolledTooltip>
                <button
                  type='button'
                  className='px-3 btn btn-sm btn-dark'
                  id='all-actions-button'
                  disabled={!multiple_actions || !display_move_solution}
                  onClick={this.handleAllActions}
                >
                  Show All Options
                </button>
                <UncontrolledTooltip
                  placement='bottom'
                  delay={C.TOOLTIP_DELAY}
                  target='all-actions-button'
                >
                  Show all movement options.
                </UncontrolledTooltip>
                <button
                  type='button'
                  className='px-3 btn btn-sm btn-dark'
                  id='next-action-button'
                  disabled={!multiple_actions || !display_move_solution}
                  onClick={this.handleNextAction}
                >
                  &gt;&gt;
                </button>
                <UncontrolledTooltip
                  placement='bottom'
                  delay={C.TOOLTIP_DELAY}
                  target='next-action-button'
                >
                  Show the next movement option.
                </UncontrolledTooltip>
              </div>
            </div>

            <svg
              id='grid_svg'
              width={C.GRID_EXTENT}
              height={C.GRID_EXTENT}
              viewBox={view_box}
              onMouseUp={this.handleGridMouseUp}
              onMouseLeave={this.handleGridMouseLeave}
            >
              <defs>
                <linearGradient id='fadeGrad' y2='1' x2='0'>
                  <stop offset='0' stopColor='black'/>
                  <stop offset='1' stopColor='white'/>
                </linearGradient>
                <linearGradient id='fadeGradR' y2='1' x2='0'>
                  <stop offset='0' stopColor='white'/>
                  <stop offset='1' stopColor='black'/>
                </linearGradient>
                <linearGradient id='fadeGradH' y2='0' x2='1'>
                  <stop offset='0' stopColor='black'/>
                  <stop offset='1' stopColor='white'/>
                </linearGradient>
                <linearGradient id='fadeGradHR' y2='0' x2='1'>
                  <stop offset='0' stopColor='white'/>
                  <stop offset='1' stopColor='black'/>
                </linearGradient>
                <mask id='edge_fade' maskContentUnits='userSpaceOnUse'>
                  <rect x={-x_fade_margin} y={-y_fade_margin} width={x_fade_margin} height={C.GRID_SCALED_HEIGHT + 2 * y_fade_margin} fill='url(#fadeGradH)'/>
                  <rect x={C.GRID_SCALED_WIDTH} y={-y_fade_margin} width={x_fade_margin} height={C.GRID_SCALED_HEIGHT + 2 * y_fade_margin} fill='url(#fadeGradHR)'/>
                  <rect x={0} y={-y_fade_margin} width={C.GRID_SCALED_WIDTH} height={y_fade_margin} fill='url(#fadeGrad)'/>
                  <rect x={0} y={C.GRID_SCALED_HEIGHT} width={C.GRID_SCALED_WIDTH} height={y_fade_margin} fill='url(#fadeGradR)'/>
                  <rect x={0} y={0} width={C.GRID_SCALED_WIDTH} height={C.GRID_SCALED_HEIGHT} fill='white'/>
                </mask>
              </defs>

              <g transform={this.state.rotate_grid ? C.GRID_TRANSFORM : ''}>
                <HexGrid
                  grid={this.state.grid}
                  activeHexes={this.state.brush != BRUSH.THIN_WALL}
                  onHexClick={this.handleHexClick}
                  onHexMouseDown={this.handleHexMouseDown}
                  onHexMouseUp={this.handleHexMouseUp}
                />
                <BorderGrid/>
                <WallGrid
                  walls={this.state.walls}
                  activeWalls={this.state.brush == BRUSH.THIN_WALL}
                  onWallClick={this.handleWallClick}
                />
                <OverlayHexGrid
                  displaySolution={display_solution}
                  showReach={this.state.show_reach}
                  showSight={this.state.show_sight}
                  aoe={this.state.display_aoe}
                  reach={this.state.display_reach}
                  sight={this.state.display_sight}
                />
                <FigureGrid
                  figures={this.state.figures}
                  initiatives={this.state.initiatives}
                  displaySolution={display_move_solution}
                  moves={this.state.display_moves}
                  attacks={this.state.display_attacks}
                  flying={this.state.flying}
                  selection={this.state.selection}
                  rotate={this.state.rotate_grid}
                  dragSourceIndex={this.state.drag_source_index}
                  activeFaction={this.state.active_faction}
                  activeFigureIndex={this.state.active_figure_index}
                />
                <DragFigure
                  ref={this.drag_ref}
                  activeFaction={this.state.active_faction}
                  onDragStart={this.handleDragStart}
                />
              </g>        
            </svg>
            <div className='mt-2 d-flex'>
              <button
                type='button'
                className={'px-4 ml-4 btn btn-sm btn-dark' + ( this.state.active_faction ? ' active' : '' )}
                id='switch-aggressors-button'
                onClick={this.handleActiveFactionChanged}
              >
                Switch Active Faction
              </button>
              <UncontrolledTooltip placement='top' delay={C.TOOLTIP_DELAY} target='switch-aggressors-button'>
                When set, the characters become the active faction. Use to determine the attack of an allied summon.
              </UncontrolledTooltip>
              <button
                type='button'
                className={'px-4 mx-3 btn btn-sm btn-dark' + ( this.state.rotate_grid ? ' active' : '' )}
                onClick={this.handleRotateMapChanged}
              >
                Rotate Board
              </button>
              <button
                type='button'
                className='mr-4 btn btn-sm btn-dark btn-block'
                onClick={this.handleMapClear}
              >
                Clear Board
              </button>
            </div>
          </div>

          <div className='mt-5 d-flex flex-column'>
            <svg width={C.AOE_EXTENT} height={C.AOE_EXTENT} viewBox={C.AOE_VIEWBOX}>
              <g transform={C.AOE_TRANSFORM}>
                <AOEHexGrid
                  grid={this.state.aoe_grid}
                  melee={this.state.range == 0}
                  onHexClick={this.handleAOEHexClick}
                />
              </g>
            </svg>
            <div className='mt-2 mx-4'>
              <button
                type='button'
                className='btn btn-sm btn-dark btn-block'
                onClick={this.handleAOEClear}
              >
                Clear Area of Effect
              </button>
            </div>
           <div className='w-75 mt-auto mb-5 btn-group-vertical'>
              <button
                type='button'
                className={'btn btn-sm btn-dark btn-block text-left' + ( this.state.show_movement ? ' active' : '' )}
                id='show-movement-button'
                onClick={this.handleDisplayMovementChanged}
              >
                Show Movement
              </button>
              <UncontrolledTooltip placement='left' delay={C.TOOLTIP_DELAY} target='show-movement-button'>
                <div className='text-left'>
                  Show the movement options for the active {active_faction_string}.
                  <p/>
                  Unset to test range or line of sight from the active {active_faction_string}'s initial location.
                </div>
              </UncontrolledTooltip>
              <button
                type='button'
                className={'btn btn-sm btn-dark btn-block text-left' + ( this.state.show_reach ? ' active' : '' )}
                id='show-reach-button'
                onClick={this.handleDisplayReachChanged}
              >
                Show Range
              </button>
              <UncontrolledTooltip placement='left' delay={C.TOOLTIP_DELAY} target='show-reach-button'>
                <div className='text-left'>
                  Show the range of the active {active_faction_string}'s attack.
                  <p/>
                  For a ranged area of effect attack, only a single hex of the area needs to be within the attack's range, though all targets must be within line of sight.
                </div>
              </UncontrolledTooltip>
              <button
                type='button'
                className={'btn btn-sm btn-dark btn-block text-left' + ( this.state.show_sight ? ' active' : '' )}
                id='show-sight-button'
                onClick={this.handleDisplaySightChanged}
              >
                Show Line of Sight
              </button>
              <UncontrolledTooltip placement='left' delay={C.TOOLTIP_DELAY} target='show-sight-button'>
                <div className='text-left'>
                  Show the active {active_faction_string}'s line of sight.
                </div>
              </UncontrolledTooltip>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
