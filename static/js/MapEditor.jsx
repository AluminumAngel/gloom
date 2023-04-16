import React from 'react';
import { UncontrolledTooltip } from 'reactstrap';
import { UncontrolledDropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap';
import axios from 'axios';
import * as C from './defines';
import * as BRUSH from './brushes';
import HexUtils from './HexUtils';
import AOEHexGrid from './AOEHexGrid';
import BitReader from './BitReader';
import BitWriter from './BitWriter';
import BrushPicker from './BrushPicker';
import Grid from './Grid';
import Message from './Message';
import PropertyEditor from './PropertyEditor';

// BUGS:
// - setToolsState may be unneccessary

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

const COMPLEXITY_AOE = 0;
const COMPLEXITY_ENEMIES = 1;

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

const GAME_RULES_FROST = 0;
const GAME_RULES_GLOOM = 1;
const GAME_RULES_JOTL = 2;
const GAME_RULES_OPTIONS = [
  [ GAME_RULES_FROST, 'Frosthaven' ],
  [ GAME_RULES_GLOOM, 'Gloomhaven' ],
  [ GAME_RULES_JOTL, 'Jaws of the Lion' ],
];

const STATE_KEYS = [
  // tools state
  // 'brush',
  'rotate_grid',
  // 'show_focus',
  // 'show_destination',
  // 'show_sightline',
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
  'teleport',
  'muddled',
  'game_rules',
  'aoe_grid',
  'active_faction',
];

const SIMPLE_STATE_KEYS = [
  'move',
  'range',
  'target',
  'flying',
  'muddled',
  'active_faction',
  'rotate_grid',
];

const SIMPLE_STATE_PROPERTIES = {
  move: {
    bits: 4,
    min: 0,
    max: 9,
  },
  range: {
    bits: 4,
    min: 0,
    max: 9,
  },
  target: {
    bits: 3,
    min: 0,
    max: 6, // make sure this change is safe for URLs
  },
  flying: {
    bits: 2,
    min: 0,
    max: 2,
  },
  teleport: {
    bits: 1,
    min: 0,
    max: 1,
  },
  muddled: {
    bits: 1,
    min: 0,
    max: 1,
  },
  jotl: {
    bits: 1,
    min: 0,
    max: 1,
  },
  game_rules: {
    bits: 2,
    min: 0,
    max: 2,
  },
  active_faction: {
    bits: 1,
    min: 0,
    max: 1,
  },
  rotate_grid: {
    bits: 1,
    min: 0,
    max: 1,
  },
};

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
    this.copy_ref = React.createRef();
    this.message_ref = React.createRef();
    this.local_storage_available = this.isLocalStorageAvailable();

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
      show_focus: false,
      show_destination: false,
      show_sightline: false,
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
      teleport: 0,
      muddled: 0,
      game_rules: 0,
      // debug_toggle: 0,
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
      display_focuses: Array( C.GRID_SIZE ).fill( false ),
      display_destinations: Array( C.GRID_SIZE ).fill( false ),
      display_sightline_lines: Array(),
      display_sightline_points: Array(),
      display_debug_lines: Array(),
      display_reach: Array( C.GRID_SIZE ).fill( false ),
      display_sight: Array( C.GRID_SIZE ).fill( false ),
    };

    var starting_scenario;
    if ( START_IN_LOS_MODE ) {
      starting_scenario = location.pathname.slice( 1 + URL_FOR.los.length );
    }
    else {
      starting_scenario = location.pathname.slice( 1 );
    }
    if ( starting_scenario !== '' ) {
      this.loadStateFromURL( starting_scenario, this.state );
    }
    else {
      this.restoreState( this.state );
    }
    // function rand( n ) {
    //   return Math.floor( Math.random() * n );
    // }
    // for ( var i = 0; i < C.GRID_SIZE; i++ ) {
    //   this.state.grid[i] = BRUSH.FIRST_TERRAIN_BRUSH + rand( BRUSH.LAST_TERRAIN_BRUSH - BRUSH.FIRST_TERRAIN_BRUSH + 1 );
    //   this.state.figures[i] = BRUSH.FIRST_FIGURE_BRUSH + rand( BRUSH.LAST_FIGURE_BRUSH - BRUSH.FIRST_FIGURE_BRUSH + 1 );
    //   this.state.initiatives[i] = 1 + rand( MAX_INITIATIVE );
    //   this.state.walls[3 * i + 0] = true;
    //   this.state.walls[3 * i + 1] = true;
    //   this.state.walls[3 * i + 2] = true;
    // }
    // for ( var i = 0; i < C.AOE_SIZE; i++ ) {
    //   this.state.aoe_grid[i] = true;
    // }
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
    if ( !this.local_storage_available ) return;

    STATE_KEYS.forEach( ( key ) => {
      if ( key in state ) {
        localStorage.setItem( key, JSON.stringify( state[key] ) );
      }
    } );
    localStorage.setItem( 'version', DATA_VERSION );
  }

  restoreState( state ) {
    if ( !this.local_storage_available ) return;

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
      this.state.teleport,
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

  handleShareScenario = () => {

    // build grid mapping
    var grid_mapping = {};
    function addEntry( location ) {
      if ( !( location in grid_mapping ) )  {
        grid_mapping[location] = {
          content: BRUSH.EMPTY,
          figure: BRUSH.EMPTY,
          walls: [ false, false, false ],
          initiative: 1,
        };
      }
    }
    this.state.grid.forEach( ( element, location ) => {
      if ( element != BRUSH.EMPTY ) {
        addEntry( location );
        grid_mapping[location].content = element;
      }
    } );
    this.state.figures.forEach( ( element, location ) => {
      if ( element != BRUSH.EMPTY ) {
        addEntry( location );
        grid_mapping[location].figure = element;
        grid_mapping[location].initiative = this.state.initiatives[location];
      }
    } );
    this.state.walls.forEach( ( element, index ) => {
      if ( element ) {
        var location = Math.floor( index / 3 );
        var wall_index = index - 3 * location;
        addEntry( location );
        grid_mapping[location].walls[wall_index] = true;
      }
    } );

    var bit_writer = new BitWriter();

    // write data version
    bit_writer.writeBits( 4, DATA_VERSION_MAJOR );
    bit_writer.writeBits( 3, DATA_VERSION_MINOR );
    bit_writer.writeBits( 3, DATA_VERSION_BUILD );

    // write simple keys
    SIMPLE_STATE_KEYS.forEach( ( key ) => {
      bit_writer.writeBits( SIMPLE_STATE_PROPERTIES[key].bits, this.state[key] );
    } );

    // write game_rules
    bit_writer.writeBits( SIMPLE_STATE_PROPERTIES['game_rules'].bits, this.state['game_rules'] );

    // write teleport
    bit_writer.writeBits( SIMPLE_STATE_PROPERTIES['teleport'].bits, this.state['teleport'] );

    // write active_figure_index
    var value = this.state.active_figure_index;
    if ( value === -1 ) {
      value = C.GRID_SIZE;
    }
    bit_writer.writeBits( C.GRID_SIZE_BITS, value );

    // write aoe_grid
    var aoe_grid_count = 0;
    this.state.aoe_grid.forEach( ( element ) => {
      if ( element ) {
        aoe_grid_count++;
      }
    } );
    bit_writer.writeBits( C.AOE_SIZE_BITS, aoe_grid_count );
    this.state.aoe_grid.forEach( ( element, index ) => {
      if ( element ) {
        bit_writer.writeBits( C.AOE_SIZE_BITS, index );
      }
    } );

    // write grid mapping
    const ordered_grid_mapping_keys = Object.keys( grid_mapping ).sort(
      function( a, b ) { return a - b; }
    );
    bit_writer.writeBits( C.GRID_SIZE_BITS, ordered_grid_mapping_keys.length );
    var last_location_written = -1;
    ordered_grid_mapping_keys.forEach( ( location ) => {
      // assume active locations are often near; save bits when they are
      const location_delta = location - last_location_written - 1;
      if ( location_delta < 4 ) {
        bit_writer.writeBits( 1, 0 );
        bit_writer.writeBits( 2, location_delta );
      }
      else {
        bit_writer.writeBits( 1, 1 );
        bit_writer.writeBits( C.GRID_SIZE_BITS, location_delta );
      }
      last_location_written = location;

      bit_writer.writeBits( 3, grid_mapping[location].content );
      if ( grid_mapping[location].figure != BRUSH.EMPTY ) {
        bit_writer.writeBits( 2, grid_mapping[location].figure - BRUSH.FIRST_FIGURE_BRUSH + 1 );
        bit_writer.writeBits( 4, grid_mapping[location].initiative );
      }
      else
      {
        bit_writer.writeBits( 2, 0 );
      }
      const any_walls = grid_mapping[location].walls[0]
        || grid_mapping[location].walls[1]
        || grid_mapping[location].walls[2];
      bit_writer.writeBits( 1, any_walls );
      if ( any_walls ) {
        bit_writer.writeBits( 1, grid_mapping[location].walls[0] );
        bit_writer.writeBits( 1, grid_mapping[location].walls[1] );
        bit_writer.writeBits( 1, grid_mapping[location].walls[2] );
      }
    } );

    bit_writer.flush();
    const result = bit_writer.result();
    const url = location.origin + URL_FOR.root + result;

    this.copy_ref.current.value = url;
    this.copy_ref.current.select();
    document.execCommand( 'copy' );

    this.message_ref.current.display(
      'alert-success',
      'A URL for the scenario has been copied to your clipboard.'
    );

    if ( !DEVELOPMENT ) {
      gtag( 'event', 'share', {
        event_category: 'ShareScenario',
        event_label: 'scenario',
        value: result.length,
      } );
    }
  }

  loadStateFromURL( url_scenario, state ) {
    function validate( value, min, max ) {
      if ( value < min || value > max ) {
        throw 'bad scenario URL';
      }
    }

    var scenario_state = {};

    // example URLs:
    // v1.0.0
    // - http://localhost:5000/AUgFMAe6fCZAgAABAgQIGQiCATAABsAgYQNhASEDgTAABgoPCBAgQIAAAQICBAoQQGhASAAGCIQBMFB4QAAKhAECBAgQEECAAAHCAgLQABKEMYQBAwbCAKEBAYgQBgSCIQEYICwgABmgQhhDGBKAAUIDAtAhDBAgQIAAAQIECBAWEBKAAUIHAgQIECBAAA
    // - http://localhost:5000/AUgFMgfcZCFAgAABAgQIECBAgBCB0AAMFiYQDEMCMECIQBAMEQgTCA3AQCECIQEYJEBAAAHCBAIECAggQIAAwcIEAgYMEiAkIEwgAAbBgEABYCAMECIQBAMGCBAEA4UKBAwSIECwUIGAAAIECBAQQIBwgUABAgQKFQgaAAMECICBwgWCYJAgGCRcIBAGwEBhA2EBYQMBKAAJoAFEIHwgQIAAAQI
    // v1.1.0
    // - http://localhost:5000/EUgFYA50-UyAAAECBAgQMhAEA2AADIBBwgbCAkIGAmEADBQeECBAgAABAgQECBQggNCAkAAMEAgDYKDwgAAUCAMECBAgIIAAAQKEBQSgASQIYwgDBgyEAUIDAhAhDAgEQwIwQFhAADJAhTCGMCQAA4QGBKBDGCBAgAABAgQIECAsICQAA4QOBAgQIECAAA
    // - http://localhost:5000/EUgFYg64yUKAAAECBAgQIECAACECoQEYLEwgGIYEYIAQgSAYIhAmEBqAgUIEQgIwSICAAAKECQQIEBBAgAABgoUJBAwYJEBIQJhAAAyCAYECwEAYIEQgCAYMECAIBgoVCBgkQIBgoQIBAQQIECAggADhAoECBAgUKhA0AAYIEAADhQsEwSBBMEi4QCAMgIHCBsICwgYCUAASQAOIQPhAgAABAgQ
    // - http://localhost:5000/EUAOUAEgqAKGE0ACVAkgDeoIJBZAYQg0AA [Gloom rules]
    // - http://localhost:5000/EUAOVAEgqAKGE0ACVAkgDeoIJBZAYQg0AA [JotL rules]
    // v1.2.0
    // - http://localhost:5000/IUgFxBzo8pkAAQIECBAgZCAIBsAAGACDhA2EBYQMBMIAGCg8IECAAAECBAgIEChAAKEBIQEYIBAGwEDhAQEoEAYIECBAQAABAgQICwhAA0gQxhAGDBgIA4QGBCBCGBAIhgRggLCAAGSACmEMYUgABggNCECHMECAAAECBAgQIEBYQEgABggdCBAgQIAAAQ
    // - http://localhost:5000/IUgFxhxwk4UAAQIECBAgQIAAAUIEQgMwWJhAMAwJwAAhAkEwRCBMIDQAA4UIhARgkAABAQQIEwgQICCAAAECBAsTCBgwSICQgDCBABgEAwIFgIEwQIhAEAwYIEAQDBQqEDBIgADBQgUCAggQIEBAAAHCBQIFCBAoVCBoAAwQIAAGChcIgkGCYJBwgUAYAAOFDYQFhA0EoAAkgAYQgfCBAAECBAg
    // - http://localhost:5000/IUAOpAJAUAUMJ4AEqBJAGtQRSCyAwhBoAA [Gloom rules]
    // - http://localhost:5000/IUAOqAJAUAUMJ4AEqBJAGtQRSCyAwhBoAA [JotL rules]
    // - http://localhost:5000/IUAOoAJAUAUMJ4AEqBJAGtQRSCyAwhBoAA [Frost rules]
    // - http://localhost:5000/IUgFxBwwAKEE4QThYwFCCQI
    // v1.3.0
    // - http://localhost:5000/MUgFVC3QRacECBAgQIAAoQSCYAAMgAEwSBiBsAChBAJhAAwULiBAgAABAgQICBAoQAAhA0ICYIBAGAADhQsIQIEwQIAAAQICCBAgQLiAADSABGEMYcCAgTBAqIAARAgDAsGQABggXEAAMkCFMIYwJAAGCBUQgA5hgAABAgQIECBAgHABIQEwQCiBAAECBAgQAA
    // - http://localhost:5000/MUgFVi3gxkEECBAgQIAAAQIECBA6IDQABgsbEAxDAmCA0AFBMERA2IDQABgodEBIAAwSICCAAGEDAgQICCBAgADBwgcEDBgkQEiAsAEBMAgGBAoAA2GA0AFBMGCAAEEwUOiAgEECBAgWQiAggAABAgQEECB8QKAAAQKFEAgaAAMECICBwgcEwSBBMEgYgUAYAAOFEQgLEE4gAAUgATSACIQTCBAgQIAA
    // - http://localhost:5000/MUAOFAiAwEBgmAFIgGoBSIPaAhILQOEKaAA [Gloom rules]
    // - http://localhost:5000/MUAOGAiAwEBgmAFIgGoBSIPaAhILQOEKaAA [JotL rules]
    // - http://localhost:5000/MUAOEAiAwEBgmAFIgGoBSIPaAhILQOEKaAA [Frost rules]
    // - http://localhost:5000/MUgFVC1gwCaEEggzEM4nJEAogQA
    // v1.5.0
    // - http://localhost:5000/UUgFpFqgi04JECBAgAABQgkEwQAYAANgkDACYQFCCQTCABgoXECAAAECBAgQECBQgABCBoQEwACBMAAGChcQgAJhgAABAgQEECBAgHABAWgACcIYwoABA2GAUAEBiBAGBIIhATBAuIAAZIAKYQxhSAAMECogAB3CAAECBAgQIECAAOECQgJggFACAQIECBAgAA
    // - http://localhost:5000/UUgFplrAjYMIECBAgAABAgQIECB0QGgADBY2IBiGBMAAoQOCYIiAsAGhATBQ6ICQABgkQEAAAcIGBAgQEECAAAGChQ8IGDBIgJAAYQMCYBAMCBQABsIAoQOCYMAAAYJgoNABAYMECBAshEBAAAECBAgIIED4gEABAgQKIRA0AAYIEAADhQ8IgkGCYJAwAoEwAAYKIxAWIJxAAApAAmgAEQgnECBAgAAB
    // - http://localhost:5000/UUAOJBAAgYHAMAOQANUCkAa1BSQWgMIV0AA [Gloom rules]
    // - http://localhost:5000/UUAOKBAAgYHAMAOQANUCkAa1BSQWgMIV0AA [JotL rules]
    // - http://localhost:5000/UUAOIBAAgYHAMAOQANUCkAa1BSQWgMIV0AA [Frost rules]
    // - http://localhost:5000/UUgFpFrAgE0IJRBmIJxPSIBQAgE
    // - http://localhost:5000/UQgE1A4AgXbAkAIBAgQIECC8AAU [teleport]
    // - http://localhost:5000/UQgEBBvAgNjAEANjBkYMbJiBEQMUAA [icy terrain]

    try {
      var bit_reader = new BitReader( url_scenario );

      // read data version
      const data_version_major = bit_reader.readBits( 4 );
      const data_version_minor = bit_reader.readBits( 3 );
      const data_version_build = bit_reader.readBits( 3 );
      var game_rules_data_version;
      var grid_data_version;
      var teleport_data_version;
      if ( data_version_major === 1
        && data_version_minor === 0
        && data_version_build === 0
      ) {
        game_rules_data_version = 0;
        grid_data_version = 0;
        teleport_data_version = 0;
      }
      else if ( data_version_major === 1
        && data_version_minor === 1
        && data_version_build === 0
      ) {
        game_rules_data_version = 1;
        grid_data_version = 0;
        teleport_data_version = 0;
      }
      else if ( data_version_major === 1
        && data_version_minor === 2
        && data_version_build === 0
      ) {
        game_rules_data_version = 2;
        grid_data_version = 0;
        teleport_data_version = 0;
      }
      else if ( data_version_major === 1
        && data_version_minor === 3
        && data_version_build === 0
      ) {
        game_rules_data_version = 2;
        grid_data_version = 1;
        teleport_data_version = 0;
      }
      else if ( data_version_major === 1
        && data_version_minor === 4
        && data_version_build === 0
      ) {
        game_rules_data_version = 2;
        grid_data_version = 1;
        teleport_data_version = 0;
      }
      else if ( data_version_major !== DATA_VERSION_MAJOR
        || data_version_minor !== DATA_VERSION_MINOR
        || data_version_build !== DATA_VERSION_BUILD
      ) {
        throw 'bad scenario URL';
      }
      else {
        game_rules_data_version = 2;
        grid_data_version = 1;
        teleport_data_version = 1;
      }

      // read simple keys
      SIMPLE_STATE_KEYS.forEach( ( key ) => {
        const value = bit_reader.readBits( SIMPLE_STATE_PROPERTIES[key].bits );
        validate(
          value,
          SIMPLE_STATE_PROPERTIES[key].min,
          SIMPLE_STATE_PROPERTIES[key].max
        );
        scenario_state[key] = value;
      } );

      // read game_rules or jotl
      if ( game_rules_data_version === 0 ) {
        scenario_state['game_rules'] = GAME_RULES_GLOOM;
      }
      else if ( game_rules_data_version === 1 ) {
        const value = bit_reader.readBits( SIMPLE_STATE_PROPERTIES['jotl'].bits );
        validate(
          value,
          SIMPLE_STATE_PROPERTIES['jotl'].min,
          SIMPLE_STATE_PROPERTIES['jotl'].max
        );
        if ( value === 0 ) {
          scenario_state['game_rules'] = GAME_RULES_GLOOM;
        }
        else {
          scenario_state['game_rules'] = GAME_RULES_JOTL;
        }
      }
      else {
        const value = bit_reader.readBits( SIMPLE_STATE_PROPERTIES['game_rules'].bits );
        validate(
          value,
          SIMPLE_STATE_PROPERTIES['game_rules'].min,
          SIMPLE_STATE_PROPERTIES['game_rules'].max
        );
        scenario_state['game_rules'] = value;
      }

      // read teleport
      if ( teleport_data_version === 0 ) {
        scenario_state['teleport'] = 0;
      }
      else {
        const value = bit_reader.readBits( SIMPLE_STATE_PROPERTIES['teleport'].bits );
        validate(
          value,
          SIMPLE_STATE_PROPERTIES['teleport'].min,
          SIMPLE_STATE_PROPERTIES['teleport'].max
        );
        scenario_state['teleport'] = value;
      }

      var grid_size;
      var grid_size_bits;
      var adjust_location;
      if ( grid_data_version === 0 ) {
        grid_size = C.GRID_SIZE_V0;
        grid_size_bits = C.GRID_SIZE_BITS_V0;
        adjust_location = function( location ) {
          const column = Math.floor( location / C.GRID_HEIGHT_V0 ) + C.COLUMN_ADJUST;
          const row = location % C.GRID_HEIGHT_V0 + C.ROW_ADJUST - column % 2;
          return column * C.GRID_HEIGHT + row
        }
      }
      else {
        grid_size = C.GRID_SIZE;
        grid_size_bits = C.GRID_SIZE_BITS;
        adjust_location = function( location ) {
          return location;
        }
      }

      // read active_figure_index
      var value = bit_reader.readBits( grid_size_bits );
      validate( value, 0, grid_size );
      if ( value === grid_size ) {
        value = NULL_INDEX;
      }
      else {
        value = adjust_location( value );
      }
      scenario_state.active_figure_index = value;

      // read aoe_grid
      scenario_state.aoe_grid = Array( C.AOE_SIZE ).fill( false );
      var aoe_grid_count = bit_reader.readBits( C.AOE_SIZE_BITS );
      for ( var i = 0; i < aoe_grid_count; i++ ) {
        var index = bit_reader.readBits( C.AOE_SIZE_BITS );
        validate( index, 0, C.AOE_SIZE - 1 );
        if ( C.AOE_GRID_SKIP_LIST.indexOf( index ) !== -1 ) {
          throw 'bad scenario URL';
        }
        scenario_state.aoe_grid[index] = true;
      }

      // read grid mapping

      scenario_state.grid = Array( C.GRID_SIZE ).fill( BRUSH.EMPTY );
      scenario_state.figures = Array( C.GRID_SIZE ).fill( BRUSH.EMPTY );
      scenario_state.initiatives = Array( C.GRID_SIZE ).fill( 1 );
      scenario_state.walls = Array( 3 * C.GRID_SIZE ).fill( false );
      var last_location_read = -1;
      const grid_mapping_size = bit_reader.readBits( grid_size_bits );
      for ( var i = 0; i < grid_mapping_size; i++ ) {
        var location_delta;
        if ( bit_reader.readBits( 1 ) === 0 ) {
          location_delta = bit_reader.readBits( 2 );
        }
        else {
          location_delta = bit_reader.readBits( grid_size_bits );
        }
        const location_read = last_location_read + location_delta + 1;
        validate( location_read, 0, grid_size - 1 );
        last_location_read = location_read;
        const location = adjust_location( location_read );

        scenario_state.grid[location] = bit_reader.readBits( 3 );
        validate( scenario_state.grid[location], BRUSH.EMPTY, BRUSH.LAST_TERRAIN_BRUSH );

        scenario_state.figures[location] = bit_reader.readBits( 2 );
        if ( scenario_state.figures[location] !== BRUSH.EMPTY ) {
          scenario_state.figures[location] += BRUSH.FIRST_FIGURE_BRUSH - 1;
          validate(
            scenario_state.figures[location],
            BRUSH.FIRST_FIGURE_BRUSH,
            BRUSH.LAST_FIGURE_BRUSH
          );
          scenario_state.initiatives[location] = bit_reader.readBits( 4 );
          validate(
            scenario_state.initiatives[location],
            1,
            MAX_INITIATIVE
          );
        }
        if ( bit_reader.readBits( 1 ) ) {
          scenario_state.walls[3 * location + 0] = bit_reader.readBits( 1 ) === 1;
          scenario_state.walls[3 * location + 1] = bit_reader.readBits( 1 ) === 1;
          scenario_state.walls[3 * location + 2] = bit_reader.readBits( 1 ) === 1;
        }
      }

      // validate active_figure_index
      var active_faction_brush = scenario_state.active_faction ? BRUSH.CHARACTER : BRUSH.MONSTER;
      if ( scenario_state.active_figure_index !== NULL_INDEX ) {
        if ( scenario_state.figures[scenario_state.active_figure_index] !== active_faction_brush ) {
          throw 'bad scenario URL';
        }
      }

      Object.assign( state, scenario_state );
      this.addDependentData( state );

      if ( !DEVELOPMENT ) {
        gtag( 'event', 'load_scenario', {
          event_category: 'LoadScenarioFromURL',
          event_label: 'success',
          value: url_scenario.length,
        } );
      }
    }
    catch ( e ) {
      if ( e === 'bad scenario URL' ) {
        // use timeout as error detected before message_ref set
        setTimeout( () => {
          this.message_ref.current.display(
            'alert-danger',
            'The URL contains a corrupt scenario description.'
          );
        }, 0 );

        if ( !DEVELOPMENT ) {
          gtag( 'event', 'load_scenario', {
            event_category: 'LoadScenarioFromURL',
            event_label: 'failure',
            value: url_scenario.length,
          } );
        }
      }
      else {
        throw( e );
      }
    }
  }

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
    this.setSharedToolsState( {
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

  handleDisplayDestinationChanged = () => {
    this.setState( {
      'show_destination': !this.state.show_destination,
    } );
  };

  handleDisplayFocusChanged = () => {
    this.setState( {
      'show_focus': !this.state.show_focus,
    } );
  };

  handleDisplaysightlineLinesChanged = () => {
    this.setState( {
      'show_sightline': !this.state.show_sightline,
    } );
  };

  // handleDebugToggle = () => {
  //   this.setScenario( {
  //     'debug_toggle': !this.state.debug_toggle,
  //   } );
  // };

  handleGameRulesChanged = ( value ) => {
    this.setScenario( {
      'game_rules': value,
    } );
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

  handleTeleportChange = ( value ) => {
    this.setScenario( {
      teleport: value,
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
    var focuses = Array( C.GRID_SIZE ).fill( false );
    var destinations = Array( C.GRID_SIZE ).fill( false );
    var sightline_lines = [];
    var debug_lines = [];
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
            solution_actions[index].focuses.forEach( ( location ) => {
              focuses[location] = true;
            } );
            solution_actions[index].destinations.forEach( ( location ) => {
              destinations[location] = true;
            } );
            solution_actions[index].sightlines.forEach( ( line ) => {
              sightline_lines.push( line );
            } );
            if ( 'debug_lines' in solution_actions[index] ) {
              solution_actions[index].debug_lines.forEach( ( line ) => {
                debug_lines.push( line );
              } );
            }
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
          solution_actions[action_displayed].focuses.forEach( ( location ) => {
            focuses[location] = true;
          } );
          solution_actions[action_displayed].destinations.forEach( ( location ) => {
            destinations[location] = true;
          } );
          solution_actions[action_displayed].sightlines.forEach( ( line ) => {
            sightline_lines.push( line );
          } );
          if ( 'debug_lines' in solution_actions[action_displayed] ) {
            solution_actions[action_displayed].debug_lines.forEach( ( line ) => {
              debug_lines.push( line );
            } );
          }
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

    var sightline_points = [];
    sightline_lines.forEach( ( line ) => {
      sightline_points.push( line[0] );
      sightline_points.push( line[1] );
    } );

    var display_state = {
      action_displayed: action_displayed,
      show_movement: show_movement,
      show_reach: show_reach,
      show_sight: show_sight,
      display_moves: moves,
      display_attacks: attacks,
      display_aoe: aoe,
      display_focuses: focuses,
      display_destinations: destinations,
      display_sightline_lines: sightline_lines,
      display_sightline_points: sightline_points,
      display_debug_lines: debug_lines,
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
      teleport: this.state.teleport,
      muddled: this.state.muddled,
      game_rules: this.state.game_rules,
      // debug_toggle: this.state.debug_toggle,
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
    add_elements( this.state.grid, 'obstacles', BRUSH.OBSTACLE );
    add_elements( this.state.grid, 'traps', BRUSH.TRAP );
    add_elements( this.state.grid, 'hazardous', BRUSH.HAZARDOUS_TERRAIN );
    add_elements( this.state.grid, 'difficult', BRUSH.DIFFICULT_TERRAIN );
    add_elements( this.state.grid, 'icy', BRUSH.ICY_TERRAIN );

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
      game_rules: this.state.game_rules,

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
    var complex_type;
    scenario.scenario_too_complex = false;
    if ( this.state.active_figure_index !== NULL_INDEX ) {
      if ( scenario.target_count > 30 ) {
        scenario.scenario_too_complex = true;
        complex_type = COMPLEXITY_ENEMIES;
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
              complex_type = COMPLEXITY_AOE;
            }
          }
        }
      }
    }

    scenario.scenario_too_complex = false;
    if ( scenario.scenario_too_complex ) {
      var message;
      if ( complex_type === COMPLEXITY_ENEMIES ) {
        const inactive_faction_string = this.state.active_faction ? 'monster' : 'character';
        message = 'The scenario cannot be solved in reasonable time. '
          + 'Reduce the number of ' + inactive_faction_string + 's.'
      }
      else {
        message = 'The scenario cannot be solved in reasonable time. '
          + 'Reduce the target number of the attack, or remove the area '
          + 'of effect, or reduce the range to melee.';
      }

      setTimeout( () => {
        this.message_ref.current.display( 'alert-danger', message );
      }, 0 );
    }
  }

  clearScenarioFromURL() {
    history.replaceState( null, '', URL_FOR.root );
  }

  setScenario( scenario ) {
    this.storeState( scenario );

    this.addDependentData( scenario );

    scenario.scenario_id = ( this.state.scenario_id + 1 ) % ( 256 * 256 * 256 );
    this.setState( scenario );

    this.clearScenarioFromURL();
  }

  setToolsState( tools_state ) {
    this.storeState( tools_state );
    this.setState( tools_state );
  }

  setSharedToolsState( tools_state ) {
    this.setToolsState( tools_state );
    this.clearScenarioFromURL();
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
    const game_rules_string = GAME_RULES_OPTIONS[this.state.game_rules][1];

    var display_move_solution = false;
    var status_label = null;
    if ( this.state.drag_source_index === NULL_INDEX ) {
      const action = this.determineActionRequired();
      switch ( action ) {
        case ACTION_WAITING_ON_SOLUTION:
        case ACTION_REQUEST_SOLUTION:
          status_label = <React.Fragment><div className='mr-2 throbber'></div> Solving...</React.Fragment>
          break;

        case ACTION_WAITING_ON_VIEW:
        case ACTION_REQUEST_START_VIEWS:
        case ACTION_REQUEST_SOLUTION_VIEWS:
          status_label = <React.Fragment><div className='mr-2 throbber'></div> Calculating...</React.Fragment>
          if ( this.state.show_movement && this.state.solution_actions ) {
            display_move_solution = true;
          }
          break;

        case ACTION_NO_ACTIVE_FIGURE:
        case ACTION_NO_REQUEST:
          break;

        case ACTION_SCENARIO_TOO_COMPLEX:
          status_label = 'The scenario is too complex.';
          break;

        case ACTION_NONE_REQUIRED:
          if ( this.state.show_movement && this.state.solution_actions ) {
            display_move_solution = true;
            if ( this.state.solution_actions.length === 1 ) {
              if ( this.state.solution_actions[0].attacks.length === 0 && this.state.solution_actions[0].move === this.state.active_figure_index ) {
                status_label = 'The ' + active_faction_string + ' takes no action.';
              }
              else {
                status_label = 'Showing the only movement option.';
              }
            }
            else if ( this.state.action_displayed === DISPLAY_ALL_ACTIONS ) {
              status_label = 'Showing ' + getNumberWord( solution_count ) + ' movement options.';
            }
            else {
              status_label = 'Showing the ' + getOrdinalWord( this.state.action_displayed + 1 ) + ' of ' + getNumberWord( solution_count ) + ' movement options.';
              if ( this.state.solution_actions[this.state.action_displayed].move === this.state.active_figure_index && this.state.solution_actions[this.state.action_displayed].attacks.length === 0 ) {
                status_label += ' No action taken.';
              }
            }
          }
          else if ( this.state.show_reach ) {
            status_label = 'Showing range.';
          }
          else if ( this.state.show_sight ) {
            status_label = 'Showing line-of-sight.';
          }
          break;
      }
    }

    return (
      <React.Fragment>
        <div className='container-fluid'>
          <div className='d-flex'>
            <div className='mt-5'>
              <BrushPicker
                flying={this.state.flying}
                teleport={this.state.teleport}
                initiative={this.state.next_initiative}
                selection={this.state.brush}
                activeFaction={this.state.active_faction}
                onSelection={this.handleBrushSelection}
              />
              <PropertyEditor
                activeFactionString={active_faction_string}
                inactiveFactionString={inactive_faction_string}
                move={this.state.move}
                range={this.state.range}
                target={this.state.target}
                flying={this.state.flying}
                teleport={this.state.teleport}
                muddled={this.state.muddled}
                initiative={this.state.selection === -1 ? -1 : this.state.initiatives[this.state.selection]}
                onMoveChange={this.handleMoveChange}
                onRangeChange={this.handleRangeChange}
                onTargetChange={this.handleTargetChange}
                onFlyingChange={this.handleFlyingChange}
                onTeleportChange={this.handleTeleportChange}
                onMuddledChange={this.handleMuddledChange}
                onInitiativeChange={this.handleInitiativeChange}
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
                    fade={false}
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
                    fade={false}
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
                    fade={false}
                    delay={C.TOOLTIP_DELAY}
                    target='next-action-button'
                  >
                    Show the next movement option.
                  </UncontrolledTooltip>
                </div>
              </div>

              <div>
                <Message ref={this.message_ref}/>
                <Grid
                  rotateGrid={this.state.rotate_grid}
                  activeHexes={this.state.brush !== BRUSH.THIN_WALL}
                  grid={this.state.grid}
                  walls={this.state.walls}
                  aoe={this.state.display_aoe}
                  reach={this.state.show_reach ? this.state.display_reach : null}
                  sight={this.state.show_sight ? this.state.display_sight : null}
                  figures={this.state.figures}
                  initiatives={this.state.initiatives}
                  displaySolution={display_solution}
                  displayMoveSolution={display_move_solution}
                  moves={this.state.display_moves}
                  destinations={this.state.show_destination ? this.state.display_destinations : null}
                  sightlineLines={this.state.show_sightline ? this.state.display_sightline_lines : null}
                  sightlinePoints={this.state.show_sightline ? this.state.display_sightline_points : null}
                  debugLines={this.state.display_debug_lines}
                  attacks={this.state.display_attacks}
                  focuses={this.state.show_focus ? this.state.display_focuses : null}
                  flying={this.state.flying}
                  teleport={this.state.teleport}
                  selection={this.state.selection}
                  rotate={this.state.rotate_grid}
                  dragSourceIndex={this.state.drag_source_index}
                  activeFaction={this.state.active_faction}
                  activeFigureIndex={this.state.active_figure_index}
                  dragRef={this.drag_ref}
                  onMouseUp={this.handleGridMouseUp}
                  onMouseLeave={this.handleGridMouseLeave}
                  onHexClick={this.handleHexClick}
                  onHexMouseDown={this.handleHexMouseDown}
                  onHexMouseUp={this.handleHexMouseUp}
                  onWallClick={this.handleWallClick}
                  onDragStart={this.handleDragStart}
                />
              </div>

              <div className='mt-2 d-flex'>
                <button
                  type='button'
                  className={'px-4 ml-4 btn btn-sm btn-dark' + ( this.state.active_faction ? ' active' : '' )}
                  id='switch-aggressors-button'
                  onClick={this.handleActiveFactionChanged}
                >
                  Switch Active Faction
                </button>
                <UncontrolledTooltip placement='top' fade={false} delay={C.TOOLTIP_DELAY} target='switch-aggressors-button'>
                  When set, the characters are the active faction. Use to determine the attack of an allied summon.
                </UncontrolledTooltip>
                <button
                  type='button'
                  className={'px-4 ml-3 btn btn-sm btn-dark' + ( this.state.rotate_grid ? ' active' : '' )}
                  onClick={this.handleRotateMapChanged}
                >
                  Rotate Board
                </button>
                <button
                  type='button'
                  className='mx-3 btn btn-sm btn-dark btn-block'
                  onClick={this.handleMapClear}
                >
                  Clear Board
                </button>
                <button
                  type='button'
                  className='px-4 mr-4 btn btn-sm btn-dark'
                  id='share-scenario-button'
                  onClick={this.handleShareScenario}
                >
                  Share Scenario
                </button>
                <UncontrolledTooltip placement='top' fade={false} delay={C.TOOLTIP_DELAY} target='share-scenario-button'>
                  Copy a URL for the scenario to your clipboard.
                </UncontrolledTooltip>
              </div>
            </div>

            <div className='mt-5 d-flex flex-column'>
              <svg width={C.AOE_EXTENT} height={C.AOE_EXTENT} viewBox={C.AOE_VIEWBOX}>
                <g transform={C.AOE_TRANSFORM}>
                  <AOEHexGrid
                    grid={this.state.aoe_grid}
                    melee={this.state.range === 0}
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

              <div className='w-75 mt-auto btn-group-vertical'>
                <button
                  type='button'
                  className={'btn btn-sm btn-dark btn-block text-left' + ( this.state.show_sight ? ' active' : '' )}
                  id='show-sight-button'
                  onClick={this.handleDisplaySightChanged}
                >
                  Show Line-of-Sight
                </button>
                <UncontrolledTooltip placement='left' fade={false} delay={C.TOOLTIP_DELAY} target='show-sight-button'>
                  <div className='text-left'>
                    Show hexes within the active {active_faction_string}'s line-of-sight.
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
                <UncontrolledTooltip placement='left' fade={false} delay={C.TOOLTIP_DELAY} target='show-reach-button'>
                  <div className='text-left'>
                    Show hexes within the range of the active {active_faction_string}'s attack.
                    <p/>
                    For a ranged area of effect attack, only a single hex of the area needs to be within the attack's range, though all targets must be within line-of-sight.
                  </div>
                </UncontrolledTooltip>
                <button
                  type='button'
                  className={'btn btn-sm btn-dark btn-block text-left' + ( this.state.show_movement ? ' active' : '' )}
                  id='show-movement-button'
                  onClick={this.handleDisplayMovementChanged}
                >
                  Show Movement
                </button>
                <UncontrolledTooltip placement='left' fade={false} delay={C.TOOLTIP_DELAY} target='show-movement-button'>
                  <div className='text-left'>
                    Show movement options for the active {active_faction_string}.
                    <p/>
                    Unset to test range or line-of-sight from the active {active_faction_string}'s initial location.
                  </div>
                </UncontrolledTooltip>
                <button
                  type='button'
                  className={'btn btn-sm btn-dark btn-block text-left' + ( this.state.show_focus ? ' active' : '' )}
                  id='show-focus-button'
                  onClick={this.handleDisplayFocusChanged}
                  disabled={!this.state.show_movement}
                >
                  Show Focus
                </button>
                <UncontrolledTooltip placement='left' fade={false} delay={C.TOOLTIP_DELAY} target='show-focus-button'>
                  <div className='text-left'>
                    Show the active {active_faction_string}'s focus.
                  </div>
                </UncontrolledTooltip>
                <button
                  type='button'
                  className={'btn btn-sm btn-dark btn-block text-left' + ( this.state.show_destination ? ' active' : '' )}
                  id='show-destination-button'
                  onClick={this.handleDisplayDestinationChanged}
                  disabled={!this.state.show_movement}
                >
                  Show Destination
                </button>
                <UncontrolledTooltip placement='left' fade={false} delay={C.TOOLTIP_DELAY} target='show-destination-button'>
                  <div className='text-left'>
                    Show the active {active_faction_string}'s destination when the {active_faction_string} cannot reach it.
                  </div>
                </UncontrolledTooltip>
                <button
                  type='button'
                  className={'btn btn-sm btn-dark btn-block text-left' + ( this.state.show_sightline ? ' active' : '' )}
                  id='show-unblocked-lines-button'
                  onClick={this.handleDisplaysightlineLinesChanged}
                  disabled={!this.state.show_movement}
                >
                  Show Sightline
                </button>
                <UncontrolledTooltip placement='left' fade={false} delay={C.TOOLTIP_DELAY} target='show-unblocked-lines-button'>
                  <div className='text-left'>
                    Show a sightline for the active {active_faction_string}'s attack.
                  </div>
                </UncontrolledTooltip>
                {/*
                <button
                  type='button'
                  className={'btn btn-sm btn-dark btn-block text-left' + ( this.state.debug_toggle ? ' active' : '' )}
                  id='show-unblocked-lines-button'
                  onClick={this.handleDebugToggle}
                >
                  Debug Toggle
                </button>
                */}
              </div>

              <div className='w-75 mt-4 btn-group-vertical'>
                <UncontrolledDropdown className='btn-group'>
                  <DropdownToggle id='game-rules-dropdown' className='btn btn-sm btn-dark dropdown-toggle text-left'>
                    {game_rules_string}
                  </DropdownToggle>
                  <UncontrolledTooltip placement='left' fade={false} delay={C.TOOLTIP_DELAY} target='game-rules-dropdown'>
                    <div className='text-left'>
                      Use the rules of this game.
                    </div>
                  </UncontrolledTooltip>
                  <DropdownMenu>
                    <DropdownItem
                      className='btn-sm'
                      id='use-frosthaven-rules-button'
                      onClick={() => { this.handleGameRulesChanged( 0 ); }}
                    >
                      {GAME_RULES_OPTIONS[0][1]}
                    </DropdownItem>
                    <UncontrolledTooltip placement='left-end' fade={false} delay={C.TOOLTIP_DELAY} target='use-frosthaven-rules-button'>
                      <div className='text-left'>
                        Two hexes have line-of-sight if a line can be drawn from any part of one hex to any part of the other without touching a wall.
                      </div>
                    </UncontrolledTooltip>
                    <DropdownItem
                      className='btn-sm'
                      id='use-gloomhaven-rules-button'
                      onClick={() => { this.handleGameRulesChanged( 1 ); }}
                    >
                      {GAME_RULES_OPTIONS[1][1]}
                    </DropdownItem>
                    <UncontrolledTooltip placement='left-end' fade={false} delay={C.TOOLTIP_DELAY} target='use-gloomhaven-rules-button'>
                      <div className='text-left'>
                        Two hexes have line-of-sight if a line can be drawn from any vertex of one hex to any vertex of the other without touching a wall.
                        <p/>
                        A vertex that starts or ends at a wall is considered touching it and cannot be used to draw line-of-sight.
                        <p/>
                        Avoiding disadvantage against the focus is prioritized above attacking as many targets as possible and above avoiding disadvantage against secondary targets.
                        <p/>
                        The last hex of a jump costs two movement points if entering difficult terrain.
                      </div>
                    </UncontrolledTooltip>
                    <DropdownItem
                      className='btn-sm'
                      id='use-jotl-rules-button'
                      onClick={() => { this.handleGameRulesChanged( 2 ); }}
                    >
                      {GAME_RULES_OPTIONS[2][1]}
                    </DropdownItem>
                    <UncontrolledTooltip placement='left-end' fade={false} delay={C.TOOLTIP_DELAY} target='use-jotl-rules-button'>
                      <div className='text-left'>
                        Two hexes have line-of-sight if a line can be drawn from any part of one hex to any part of the other without touching a wall.
                        <p/>
                        Avoiding disadvantage against the focus is prioritized above attacking as many targets as possible and above avoiding disadvantage against secondary targets.
                        <p/>
                        Proximity does not affect monster focus. Initiative is the only tiebreaker.
                      </div>
                    </UncontrolledTooltip>
                  </DropdownMenu>
                </UncontrolledDropdown>                             

              </div>

              <div className='mt-2 mb-4 text-secondary small'>
                <p/>
                <p className='footer'/>
                &copy; 2023 <a href='mailto:daniel.richard.nelson@gmail.com'>daniel.richard.nelson@gmail.com</a>
                <p className='footer'/>
                <a href='https://github.com/AluminumAngel/gloom'>github.com/AluminumAngel/gloom</a>
                <p className='footer'/>
                <a href='https://boardgamegeek.com/user/AluminumAngel'>boardgamegeek.com/user/AluminumAngel</a>
                <p className='footer'/>
                <a href='https://www.reddit.com/user/AluminumAngel'>u/AluminumAngel</a>
              </div>
            </div>
          </div>
        </div>
        <textarea
          ref={this.copy_ref}
          className='copy'
          readOnly
        />
      </React.Fragment>
    );
  }
}