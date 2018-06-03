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

    this.state = {
      // app state
      solution_pending: false,

      // tools state
      brush: BRUSH.ACTIVE_FIGURE,
      selection: NULL_INDEX,
      active_figure_index: NULL_INDEX,
      drag_source_index: NULL_INDEX,
      rotate_grid: false,
      next_initiative: 1,
      senario_too_complex: false,

      // analystics data
      target_count: 0,

      // senario state
      senario_id: 1,
      grid: Array( C.GRID_SIZE ).fill( 0 ),
      figures: Array( C.GRID_SIZE ).fill( 0 ),
      initiatives: Array( C.GRID_SIZE ).fill( 1 ),
      walls: Array( 3 * C.GRID_SIZE ).fill( false ),
      move: 2,
      range: 0,
      target: 1,
      flying: 0,
      muddled: 0,
      aoe_grid: Array( C.AOE_SIZE ).fill( false ),
      active_faction: false,

      // solution state
      solution_senario_id: 0,
      actions: null,
      action_displayed: DISPLAY_ALL_ACTIONS,
      display_moves: Array( C.GRID_SIZE ).fill( false ),
      display_attacks: Array( C.GRID_SIZE ).fill( false ),
      display_aoe: Array( C.GRID_SIZE ).fill( false ),
    };

    if ( !DEVELOPMENT ) {
      gtag( 'event', 'screen_view', {
        screen_name: 'Map Editor',
        app_name: APP_NAME,
        app_version: APP_VERSION,
      } );
    }
  }

  componentDidUpdate() {
    setTimeout( () => {
      if ( this.state.senario_id !== this.state.solution_senario_id ) {
        if ( !this.state.solution_pending ) {
          if ( this.state.active_figure_index !== NULL_INDEX ) {
            if ( !this.state.senario_too_complex ) {
              this.handleRequestSolution();
            }
          }
        }
      }
    }, 0 );
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
    this.setSenario( {
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
    this.setSenario( {
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

    this.setSenario( {
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

    const senario_changed = grid || figures || initiatives || active_figure_index != this.state.active_figure_index;
    if ( senario_changed || selection != this.state.selection ) {
      if ( senario_changed ) {

        // TODO: often don't need to do this
        const next_initiative = this.determineNextInitiative(
          figures ? figures : this.state.figures,
          initiatives ? initiatives : this.state.initiatives,
          this.state.active_faction
        );

        var senario_update = {
          selection: selection,
          active_figure_index: active_figure_index,
          next_initiative: next_initiative,
        };
        if ( grid ) {
          senario_update.grid = grid;
        }
        if ( figures ) {
          senario_update.figures = figures;
        }
        if ( initiatives ) {
          senario_update.initiatives = initiatives;
        }
        this.setSenario( senario_update );
      }
      else {
        this.setState( {
          selection: selection,
        } );
      }
    }
  };

  handleBrushSelection = ( brush ) => {
    this.setState( {
      brush: brush
    } );
  };

  handleMapClear = () => {
    this.setSenario( {
      grid: Array( C.GRID_SIZE ).fill( BRUSH.EMPTY ),
      figures: Array( C.GRID_SIZE ).fill( BRUSH.EMPTY ),
      initiatives: Array( C.GRID_SIZE ).fill( 1 ),
      walls: Array( 3 * C.GRID_SIZE ).fill( false ),
      selection: NULL_INDEX,
      active_figure_index: NULL_INDEX,
      next_initiative: 1,
    } );
  };

  handleAOEClear = () => {
    this.setSenario( {
      aoe_grid: Array( C.AOE_SIZE ).fill( false ),
    } );
  };

  handleRotateMapChanged = () => {
    this.setState( {
      rotate_grid: !this.state.rotate_grid,
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

    this.setSenario( {
      figures: figures,
      active_figure_index: NULL_INDEX,
      selection: NULL_INDEX,
      next_initiative: next_initiative,
      active_faction: !this.state.active_faction,
    } );
  };

  handleMoveChange = ( value ) => {
    this.setSenario( {
      move: value,
    } );
  };

  handleRangeChange = ( value ) => {
    this.setSenario( {
      range: value,
    } );
  };

  handleTargetChange = ( value ) => {
    this.setSenario( {
      target: value,
    } );
  };

  handleFlyingChange = ( value ) => {
    this.setSenario( {
      flying: value,
    } );
  };

  handleMuddledChange = ( value ) => {
    this.setSenario( {
      muddled: value,
    } );
  };

  handleInitiativeChange = ( value ) => {
    if ( this.state.selection !== -1 ) {

      var initiatives = this.state.initiatives.slice();
      initiatives[this.state.selection] = value;

      var next_initiative = this.determineNextInitiative( this.state.figures, initiatives, this.state.active_faction );

      this.setSenario( {
        initiatives: initiatives,
        next_initiative: next_initiative,
      } );
    }
  };

  handleSenarioSelection = ( senario ) => {
    this.setState( {
      senario: senario,
    } );
  };

  unpackSolution( solution ) {
    var moves = Array( C.GRID_SIZE ).fill( false );
    var attacks = Array( C.GRID_SIZE ).fill( false );
    var aoe = Array( C.GRID_SIZE ).fill( false );

    solution.actions.forEach( ( action ) => {
      moves[action.move] = true;
      action.attacks.forEach( ( location ) => {
        attacks[location] = true;
      } );
      action.aoe.forEach( ( location ) => {
        aoe[location] = true;
      } );
    } );
    this.setState( {
      solution_senario_id: solution.senario_id,
      actions: solution.actions.slice(),
      action_displayed: DISPLAY_ALL_ACTIONS,
      display_moves: moves,
      display_attacks: attacks,
      display_aoe: aoe,
    } );
  }

  packSenario() {
    var senario = {
      senario_id: this.state.senario_id,

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
        senario.aoe.push( index );
      }
    } );

    function add_elements( map_layer, key, brush ) {
      senario.map[key] = [];
      map_layer.forEach( ( element, index ) => {
        if ( element === brush ) {
          senario.map[key].push( index );
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
    senario.map.initiatives = [];
    this.state.figures.forEach( ( figure, index ) => {
      if ( figure === inactive_faction_brush ) {
        senario.map.initiatives.push( this.state.initiatives[index] );
      }
    } );

    senario.map.thin_walls = [];
    this.state.walls.forEach( ( wall, index ) => {
      if ( wall ) {
        senario.map.thin_walls.push( [ Math.trunc( index / 3 ), index % 3 ] );
      }
    } );

    return senario;
  }

  unpackSenario( senario ) {
    var grid = Array( C.GRID_SIZE ).fill( 0 );
    var figures = Array( C.GRID_SIZE ).fill( 0 );
    var initiatives = Array( C.GRID_SIZE ).fill( 1 );
    var walls = Array( 3 * C.GRID_SIZE ).fill( false );
    var aoe_grid = Array( C.AOE_SIZE ).fill( false );

    function get_index( c, r ) {
      return r + c * C.GRID_HEIGHT;
    }

    // TODO: clean data
    // TODO: don't allow more than one active monster
    // TODO: validate characters on walls and obstables
    // TODO: validate thins vs standard walls

    var map = senario.map;
    function add_elements( map_layer, key, brush ) {
      map[key].forEach( ( item ) => {
        map_layer[get_index( item[0], item[1] )] = brush;
      } );
    }

    add_elements( figures, 'characters', BRUSH.CHARACTER );
    add_elements( figures, 'monsters', BRUSH.MONSTER  );
    add_elements( grid, 'walls', BRUSH.WALL );
    add_elements( grid, 'obsticles', BRUSH.OBSTICLE );
    add_elements( grid, 'traps', BRUSH.TRAP );
    add_elements( grid, 'hazardous', BRUSH.HAZARDOUS_TERRAIN );
    add_elements( grid, 'difficult', BRUSH.DIFFICULT_TERRAIN );

    for ( var i = 0; i < map['initiatives'].length; i++ )
    {
      initiatives[get_index(map['characters'][i][0],map['characters'][i][1])] = map['initiatives'][i];
    }

    for ( var i = 0; i < map['thin_walls'][0].length; i++ )
    {
      walls[0+3*get_index(map['thin_walls'][0][i][0], map['thin_walls'][0][i][1])] = true;
    }
    for ( var i = 0; i < map['thin_walls'][1].length; i++ )
    {
      walls[1+3*get_index(map['thin_walls'][1][i][0], map['thin_walls'][1][i][1])] = true;
    }
    for ( var i = 0; i < map['thin_walls'][2].length; i++ )
    {
      walls[2+3*get_index(map['thin_walls'][2][i][0], map['thin_walls'][2][i][1])] = true;
    }

    for ( var i = 0; i < senario.aoe.length; i++ )
    {
      aoe_grid[senario.aoe[i]] = true;
    }

    const active_figure_index = get_index( senario.active_figure[0], senario.active_figure[1] );

    this.setSenario( {
      grid: grid,
      figures: figures,
      initiatives: initiatives,
      walls: walls,
      selection: NULL_INDEX,
      active_figure_index: active_figure_index,

      move: senario.move,
      range: senario.range,
      target: senario.target,
      flying: senario.flying,
      muddled: senario.muddled,
      aoe_grid: aoe_grid,
    } );
  }

  handleRequestSolution = () => {
    if ( !DEVELOPMENT ) {
      gtag( 'event', 'request', {
        event_category: 'Solution',
        event_label: this.state.active_faction ? 'characters' : 'monsters',
        value: this.state.target_count,
      } );
    }

    var senario = this.packSenario();
    this.setState( {
      solution_pending: true,
    } );
    axios.put( URL_FOR.solve, senario )
      .then( ( response ) => {
        this.setState( {
          solution_pending: false,
        } );
        this.unpackSolution( response.data );
      } )
      .catch( () => {
        console.log( 'solution failed' );
        this.setState( {
          solution_pending: false,
        } );
      } );
  };

  handleRequestSenario = () => {
    axios.get( URL_FOR.senario )
      .then( ( response ) => {
        this.unpackSenario( response.data );
      } )
      .catch( () => {
      } );
  };

  handlePreviousAction = () => {
    var action_displayed = this.state.action_displayed;
    if ( this.state.actions && this.state.actions.length > 1 ) {
      if ( action_displayed === DISPLAY_ALL_ACTIONS ) {
        action_displayed = this.state.actions.length - 1;
      }
      else if ( action_displayed === 0 ) {
        action_displayed = this.state.actions.length - 1;
      }
      else {
        action_displayed -= 1;
      }
    }
    this.setActionDisplayed( action_displayed );
  };

  handleNextAction = () => {
    var action_displayed = this.state.action_displayed;
    if ( this.state.actions && this.state.actions.length > 1 ) {
      if ( action_displayed === DISPLAY_ALL_ACTIONS ) {
        action_displayed = 0;
      }
      else if ( action_displayed === this.state.actions.length - 1 ) {
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
    if ( this.state.actions && this.state.actions.length > 1 ) {
      action_displayed = DISPLAY_ALL_ACTIONS;
    }
    this.setActionDisplayed( action_displayed );
  };

  setActionDisplayed( action_displayed ) {
    if ( action_displayed === this.state.action_displayed ) {
      return;
    }
    
    var moves = Array( C.GRID_SIZE ).fill( false );
    var attacks = Array( C.GRID_SIZE ).fill( false );
    var aoe = Array( C.GRID_SIZE ).fill( false );

    function applyAction( action ) {
      moves[action.move] = true;
      action.attacks.forEach( ( location ) => {
        attacks[location] = true;
      } );
      action.aoe.forEach( ( location ) => {
        aoe[location] = true;
      } );
    }

    if ( action_displayed === DISPLAY_ALL_ACTIONS ) {
      this.state.actions.forEach( ( action ) => {
        applyAction( action );
      } );
    }
    else {
      applyAction( this.state.actions[action_displayed] );
    }

    this.setState( {
      action_displayed: action_displayed,
      display_moves: moves,
      display_attacks: attacks,
      display_aoe: aoe,
    } );
  }

  setSenario( senario ) {
    // TEMP
    // Determine if the senario is too complex to request a solution.
    // If there are more than 20 characters.
    // If its a ranged aoe and the target count is above 3.
    senario.senario_too_complex = false;
    senario.target_count = 0;
    var inactive_faction_brush = this.inactiveFactionBrush();
    var figures = senario.figures !== undefined ? senario.figures : this.state.figures;
    figures.forEach( ( figure ) => {
      if ( figure === inactive_faction_brush ) {
        senario.target_count++;
      }
    } );
    if ( senario.target_count > 20 ) {
      senario.senario_too_complex = true;
    }
    else {
      var target = senario.target !== undefined ? senario.target : this.state.target;
      if ( target > 3 ) {
        var range = senario.range !== undefined ? senario.range : this.state.range;
        if ( range > 1 ) {
          var active_aoe = false;
          var aoe_grid = senario.aoe_grid !== undefined ? senario.aoe_grid : this.state.aoe_grid;
          for ( var index = 0; index < aoe_grid.length; index++ ) {
            if ( aoe_grid[index] ) {
              active_aoe = true;
              break;
            }
          }
          if ( active_aoe ) {
            senario.senario_too_complex = true;
          }
        }
      }
    }

    senario.senario_id = ( this.state.senario_id + 1 ) % ( 256 * 256 * 256 );
    this.setState( senario );
  }

  isDisplayingSolution() {
    if ( this.state.drag_source_index !== NULL_INDEX ) {
      return false;
    }
    return this.state.senario_id === this.state.solution_senario_id;
  }

  render() {
    const display_solution = this.isDisplayingSolution();
    const solution_count = this.state.actions ? this.state.actions.length : 0;
    const multiple_actions = display_solution && solution_count > 1;

    var status_label;
    const solving = ( this.state.solution_pending || this.state.senario_id !== this.state.solution_senario_id )
      && this.state.active_figure_index !== NULL_INDEX;
    if ( solving ) {
      if ( this.state.senario_too_complex ) {
        const faction_string = this.state.active_faction ? 'monsters' : 'characters';
        status_label = (
          <span>
            Too complex. Reduce the target count, area of effect, or {faction_string}.
          </span>
        );
      }
      else {
        status_label = (
          <span><div className='mr-2 throbber'></div> Solving...</span>
        );
      }
    }
    else {
      var status_message;
      if ( display_solution ) {
        if ( this.state.actions ) {
          if ( this.state.actions.length === 1 ) {
            if ( this.state.actions[0].attacks.length === 0 && this.state.actions[0].move === this.state.active_figure_index ) {
              const faction_string = this.state.active_faction ? 'character' : 'monster';
              status_message = 'The ' + faction_string + ' will not move.';
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
          }
        }
      } 
      else {
        status_message = '';
      }
      status_label = (
        <span>
          {status_message}
        </span>
      );
    }

    const x_margin = C.GRID_MARGIN + ( this.state.rotate_grid ? 0 : C.GRID_DELTA );
    const y_margin = C.GRID_MARGIN + ( this.state.rotate_grid ? C.GRID_DELTA : 0 );
    const view_box = ( -x_margin ) + ' ' + ( -y_margin ) + ' ' + ( C.GRID_EXTENT ) + ' ' + ( C.GRID_EXTENT );

    // TODO: clean
    var x_grad;
    var y_grad;
    if ( !this.state.rotate_grid ) {
      x_grad = ( <rect x={0} y={-y_margin} width={C.GRID_EXTENT - 2 * x_margin} height={y_margin} fill='url(#fadeGrad)'/> );
      y_grad = ( <rect x={C.GRID_EXTENT - 2 * x_margin} y={-y_margin} width={x_margin} height={C.GRID_EXTENT} fill='url(#fadeGradHR)'/> );
    }
    else {
      x_grad = ( <rect x={-x_margin} y={-y_margin} width={C.GRID_EXTENT} height={y_margin} fill='url(#fadeGrad)'/> );
      y_grad = ( <rect x={C.GRID_EXTENT - 2 * x_margin} y={0} width={x_margin} height={C.GRID_EXTENT - 2 * y_margin} fill='url(#fadeGradHR)'/> );
    }

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
                tooltip={this.state.active_faction
                  ?
                    <React.Fragment>
                      Set whether the active character is muddled.
                    </React.Fragment>
                  :
                    <React.Fragment>
                      Set whether the active monster is muddled.
                    </React.Fragment>
                }
              />
              <NumberSelector
                label='Initiative'
                options={INITIATIVE_OPTIONS}
                value={this.state.selection == -1 ? 1 : this.state.initiatives[this.state.selection]}
                disabled={this.state.selection == -1}
                onChange={this.handleInitiativeChange}
                tooltip={this.state.active_faction
                  ?
                    <React.Fragment>
                      Set the initiative rank of the selected monster.
                    </React.Fragment>
                  :
                    <React.Fragment>
                      Set the initiative rank of the selected character.
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
                  disabled={!multiple_actions}
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
                  disabled={!multiple_actions}
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
                  disabled={!multiple_actions}
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
              mask='url(#edge_fade)'
              onMouseUp={this.handleGridMouseUp}
              onMouseLeave={this.handleGridMouseLeave}
            >
              <defs>
                <linearGradient id='fadeGrad' y2='1' x2='0'>
                  <stop offset='0' stopColor='white' stopOpacity='0'/>
                  <stop offset='1' stopColor='white' stopOpacity='1'/>
                </linearGradient>
                <linearGradient id='fadeGradR' y2='1' x2='0'>
                  <stop offset='0' stopColor='white' stopOpacity='1'/>
                  <stop offset='1' stopColor='white' stopOpacity='0'/>
                </linearGradient>
                <linearGradient id='fadeGradH' y2='0' x2='1'>
                  <stop offset='0' stopColor='white' stopOpacity='0'/>
                  <stop offset='1' stopColor='white' stopOpacity='1'/>
                </linearGradient>
                <linearGradient id='fadeGradHR' y2='0' x2='1'>
                  <stop offset='0' stopColor='white' stopOpacity='1'/>
                  <stop offset='1' stopColor='white' stopOpacity='0'/>
                </linearGradient>
                <mask id='edge_fade' maskContentUnits='userSpaceOnUse'>
                  {x_grad}
                  <rect x={-x_margin} y={-y_margin} width={x_margin} height={C.GRID_EXTENT} fill='url(#fadeGradH)'/>
                  <rect x={-x_margin} y={C.GRID_EXTENT - 2.0 * y_margin} width={C.GRID_EXTENT} height={y_margin} fill='url(#fadeGradR)'/>
                  {y_grad}
                  <rect x={0} y={0} width={C.GRID_EXTENT - 2.0 * x_margin} height={C.GRID_EXTENT - 2.0 * y_margin} fill='white'/>
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
                <OverlayHexGrid
                  displaySolution={display_solution}
                  aoe={this.state.display_aoe}
                />
                <FigureGrid
                  figures={this.state.figures}
                  initiatives={this.state.initiatives}
                  displaySolution={display_solution} 
                  moves={this.state.display_moves}
                  attacks={this.state.display_attacks}
                  flying={this.state.flying}
                  selection={this.state.selection}
                  rotate={this.state.rotate_grid}
                  dragSourceIndex={this.state.drag_source_index}
                  activeFaction={this.state.active_faction}
                  activeFigureIndex={this.state.active_figure_index}
                />
                <WallGrid
                  walls={this.state.walls}
                  activeWalls={this.state.brush == BRUSH.THIN_WALL}
                  onWallClick={this.handleWallClick}
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
          </div>
        </div>
      </div>
    );
  }
}