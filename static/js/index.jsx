// next:
// - try selection with standard figure stroke now (since we have triangles)
// - unblocked los line visualitzation

// - check obstruction perf again, in aoe situations

// - switch between blocked and unblocked lines correctly
// - fix when i show blocked lines (use distance and not always focus)
// - measure overhead of sight line calculation
// - optimize sight lines to not always calculate
// - i like unblocked sight lines; decide after completion if i like blocked ones
// - for blocked, color idea:
// --- red dots for blocked vertix
// --- green dot for open vertex w/ red line for blocked line
// --- use closest enemy in range, not focus (cause focus doesn't work)
// - for blocked los, i'm drawing way more circles than i need to; do i care?
// - two buttons:
// --- Show unblocked Sight Lines
// --- Show Blocked Sight Lines
// - unblocked_lines => unblocked_lines

// - tooltip is too big and is off screen
// - also, reconsider tooltip text

// CLEAN
// - all server line code
// - SightLine.jsx and SightLines.jsx

// - share on subreddit
// - share all the other places that BGG post says to share
// - move los overlays under thin walls, but keep aoe overlays over thin walls (???)

// button to show the clean line for line of sight targets
// -- show line that is most parallel with line between hex centers)\
// -- and that is shortest

// think about:
// -- putting # of traps/hazzards hit by move in status text
// -- advanced options menu
// -- adv option:  base-2-base LOS house rule (fin mentinons on BGG first)
// -- adv scenario setting:  # of traps/hazzards to kill active character
// ---- then allow character to move to death (as per that rule i'm ignoring)
// ---- then show in status whether character dies
// ---- defaults to infinity
// ---- do hazzards and all traps do equal damage (i suspect not)

// when sending scenario to client app, add walls around smaller board?
// - so all solutions are still valid

// new optimization is great; consider upping the max allowed target value

// ideally reach and los are under thin walls, while AoE is over thin walls

// validate json to schema in both directions
// - http://json-schema.org/implementations.html#validators

// feature - "Show LOS lines" button (draw actual vertex to vertex lines for attacks)

// top todos:
// -- server down/fail behaviors
// -- scenario loader
// -- cancel and resend request (see email for idea)
// -- harden communiction ends (validate json; see above link)
// -- footer with credits, email, etc.

// handleRequestViewsForStart and friends call setState twice; fix

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

// brushes for multi-hex map tiles
// --- see the tile move around as you move the mouse (flashing?)
// --- click to stamp
// --- kind of want undo then, given how hard it is to erase

// add undo button

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

// share scenario button
// -- button that copy a link to clipboard (and shows it)
// -- hitting that URL recreates the scenario
// -- basically, allow scenario to be encoded in URL

import React from 'react';
import ReactDOM from 'react-dom';
import MapEditor from './MapEditor';

ReactDOM.render(
  <MapEditor/>,
  document.getElementById( 'root' )
);