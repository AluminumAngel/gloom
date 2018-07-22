// next:
// -- check in to git!
// -- check in to p4!
// -- move los overlays under thin walls, but keep aoe overlays over thin walls (???)
// - drag and drop cursor often broken!?

// variable name cleanup: solution is overloaded
// - any solution
// - action (vs views) solution

// button to show destinations
// button to show focuses
// button to show the clean line for line of sight targets
// -- show line that is most parallel with line between hex centers)\
// -- and that is shortest

// when sending scenario to client app, add walls around smaller board?
// - so all solutions are still valid

// new optimization is great; consider upping the max allowed target value

// ideally reach and los are under thin walls, while AoE is over thin walls

// validate json to schema in both directions
// - http://json-schema.org/implementations.html#validators

// feature - "Show LOS lines" button (draw actual vertex to vertex lines for attacks)
// feature - "show focus and destination" buttons

// top todos:
// -- squares monster can attack given its current attack
// -- server down/fail behaviors
// -- scenario loader
// -- cancel and resend request (see email for idea)
// -- harden communiction ends
// -- footer with credits, email, etc.

// impacted by this reactstrap issue
// -- https://github.com/react-community/react-native-safe-area-view/issues/28
// -- looking at this again:  this seems like completely the wrong issue
// -- it's this, right?
// ---- "Can't call setState (or forceUpdate) on an unmounted component.""

// optimization:
// inside the loop over aoe_pattern_list
// -- cache all results for aoe_targets, _of_rank, _disadvantage
// -- if a new result is equal in answer to cached result, skip
// -- should help greatly with big aoes tthat often hit the same targets in many orientations
// -- especially if TARGET count is high

// server failure/error
// -- clean error display
// -- button to retry solution request

// use center point of figure circle to determine drop hex
// -- is this doable?

// check email for many notes; move here

// test scenario loader
// -- search
// -- descriptions
// -- URL links to BGG
// -- ability to read description of currently loaded scenario (after loaded)

// layout
// -- navbar for help and scenario loader
// -- help
// -- footer
// - scenario loader page

// edit scenarios as needed for map size increase
// -- map size breaks some scenarios

// stop pinging for solutions if we get a server error
// add a buton to restore solution pings ('server error; try again?')

// some test scenarios are broken because the monster can leave the original map area
//   and go around walls

// two way data valication
// undo, redo on grid state
// sanitize solution; currently we just trust the json structure
// validate walls vs thin walls
// so much dirty python now in the solver; clean

// remove all exit() calls from server; just return 404

// should be crediting:  https://icons8.com/license/

// do aoe reach visualization super perfect by placing all possible aoe templates

// would be nice:
// -- do sight and los calculations (and display) for border hexes

// # test: https://boardgamegeek.com/geeklist/234575/gloomhaven-rules-quiz
// # faq: https://boardgamegeek.com/thread/1897763/official-faq-game-revs-1-and-2
// # los: https://boardgamegeek.com/image/3930242/caseyharris

// # add remaining online tests
// # online test set was extended!!!

// # test idea - monster prioritizes disadvantage over extra aoe_targets
// # test idea - monster prioritizes better focus-rank extra target over disadvantage on extra aoe_targets

import React from 'react';
import ReactDOM from 'react-dom';
import MapEditor from './MapEditor';

ReactDOM.render(
  <MapEditor/>,
  document.getElementById( 'root' )
);