// next:
// -- potential bug - focus determination does not check los to targets???

// top todos:
// -- los mode (show los of active character)
// -- squares monster can attack given its current attack
// -- server down/fail behaviors
// -- senario loader
// -- cancel and resend request (see email for idea)
// -- clean js/python/css
// -- harden communiction ends
// -- footer with credits, email, etc.

// impacted by this reactstrap issue
// -- https://github.com/react-community/react-native-safe-area-view/issues/28

// optimization:
// inside the loop over aoe_pattern_list
// -- cache all results for aoe_targets, _of_rank, _disadvantage
// -- if a new result is equal in answer to cached result, skip
// -- should help greatly with big aoes tthat often hit the same targets in many orientations
// -- especially if TARGET count is high

// learn how to use google analytics well enough to look at character counts

// server failure/error
// -- clean error display
// -- button to retry solution request

// event responses function syntax unification
// two ways i'm doing it
// -- arrow notation
// -- local function in render()

// use center point of figure circle to determine drop hex
// -- is this doable?

// check email for many notes; move here

// layout
// -- navbar for help and senario loader
// -- help
// -- header
// -- footer
// -- match aoe rotation to cards; don't rotate dynamically
// -- match aoe hex style to cards/rulebook
// - senario loader page

// test all test senario in the client app
// -- can i automate that?
// -- client app could track when it solves an unedited senario request
// edit senarios as needed for map size increase
// -- map size breaks some senarios

// camel-back vs underbar variable names is random in JS

// stop pinging for solutions if we get a server error
// add a buton to restore solution pings ('server error; try again?')

// some test senarios are broken because the monster can leave the original map area
//   and go around walls

// two way data valication
// switch to sending indexes, not coordinates; index is fine since i'm sending board C.GRID_SCALED_HEIGHT/C.GRID_SCALED_WIDTH
// clean up senario fetch and solve state
// undo, redo on grid state
// const correctness pass
// sanitize solution; currently we just trust the json structure
// validate walls vs thin walls
// mode for showing LOS
// mode for showing LOS and in range
// so much dirty python now in the solver

// remove all exit() calls from server; just return 404

// solver optimization path
// -- make a set up with
// ---- huge ranged aoe
// ---- many, many characters
// ---- large +attack count

// style aoe hexes to match cards/rules

// should be crediting:  https://icons8.com/license/

import React from 'react';
import ReactDOM from 'react-dom';
import MapEditor from './MapEditor';

ReactDOM.render(
  <MapEditor/>,
  document.getElementById( 'root' )
);
