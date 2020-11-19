// next:
// - try selection with standard figure stroke now (since we have triangles)

// - move los overlays under thin walls, but keep aoe overlays over thin walls (???)

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

// top todos:
// -- server down/fail behaviors
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

// package dependency cleanup
// - don't believe I'm using dev vs std dependencies correctly
// - axios, react, reactstrap should not be devDependencies?

// test URL
// https://gloom.aluminumangel.org/AQgEMCeFgSiQRFmYB4qkiaqsK9O2zvvAUCRL80TZ1n2ZY9pDzmPlY-KD4iPag9GD4UPmI95j1iPWI9Jj3WPdY9Ej0oPJQ81D3oPWQ-Ej2iPig8VD4SPeg9Uj4YPeY9aD1WPJg8ZD3UPeQ91D4iPSY91D1kPVg84j1iPGY9pD5WPWQ-JjxSPRY95D0kPOY9ZD5kPKI92DymPWg9KD3WPlY-Ej4oPSQ9Ij4iPVI9Zj4UPhY8VjzSPhg-FDzWPhQ9Uj0oPGg8VjzUPOg9KD3mPhI-VD5YPiY9Ij0oPKY95j5kPig8ZD4mPlg8VDxWPJI91DzmPZQ82D0kPiQ-aD4SPGY80jzkPFQ9VjzSPKQ9lj0WPZQ-UjziPRg8Zj4mPmI9Jj4YPVI9GD3SPdY80jxSPlQ-Zj4WPaI8Vj1UPhQ91D1SPRQ9Ij1SPmY8aDyYPFg8mDzmPJQ9pDxYPiQ-JDxmPhQ-Ej2UPFQ85D1iPKY8ljxUPKQ-Uj4oPNQ9JD0mPdg-Uj3WPNY9pDziPJI8Vj0kPJI9kj0UPVQ9JD1oPhQ9Uj3mPRY90j1iPiI-VjzkPiI9Vj1UPVI8Vj2iPeY8qDxoPmQ8Yj4UPGQ9VjxYPZQ86D3mPKI84j0iPmQ8VDyYPKY-aDxWPVY9pDziPSY91D1oPhY85D1SPeQ82D4kPKI91D0UPig9UjzWPKI91j0WPlg86D0UPRY-Fj5YPKI8lDzoPmY9pj3UPGg9Zj3kPKY9aD3iPJY9VD3oPGQ-aDyWPaY9FDySPlI84j1WPVg9oj4mPlQ86DyWPlI85D2iPGI8VD1iPmY-EjzoPlY-Ej1iPWQ9IjziPWY8kj3mPdQ9Ej0mPGI8VjymPWI9ojymPNg96DzSPiQ9GD5YPVg9Jj2kPSg9kj3UPJQ8aD3kPJg8qD4YPRQ9lDxSPdg8Yj3WPFQ8lj3iPlY-VD1mPag9FD2iPWg-KD2SPmQ9IjxWPZI9Yj1mPmI9lj3oPlY9JDyYPiI8qD0UPmY-Fj2oPWY9lDzUPdg81D0oPmI9kj2iPFQ-FD1iPaY95jymPmg-FD1UPeQ92D2kPOY8lj2UPmI9pjzoPiQ9mD5iPFQ84jzkPSY8mD4iPFI9VD0WPWg-EjykPKQ-YjxmPdI9JD0UPSQ-Vj2kPJg8qD5UPdQ9VjzoPSI9ojzkPFg9FjxoPWI9pDzSPeg94j1iPWg-Vj1mPhY-YjzkPGY9GD2mPGg-FD0kPmg-FjzSPRg9qD5kPWQ-Yj4WPmI-UjySPOQ90j4YPKY-YD

import React from 'react';
import ReactDOM from 'react-dom';
import MapEditor from './MapEditor';

ReactDOM.render(
  <MapEditor/>,
  document.getElementById( 'root' )
);