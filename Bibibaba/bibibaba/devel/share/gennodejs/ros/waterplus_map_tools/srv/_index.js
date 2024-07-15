
"use strict";

let GetChargerByName = require('./GetChargerByName.js')
let GetWaypointByIndex = require('./GetWaypointByIndex.js')
let GetNumOfWaypoints = require('./GetNumOfWaypoints.js')
let GetWaypointByName = require('./GetWaypointByName.js')
let SaveWaypoints = require('./SaveWaypoints.js')
let AddNewWaypoint = require('./AddNewWaypoint.js')

module.exports = {
  GetChargerByName: GetChargerByName,
  GetWaypointByIndex: GetWaypointByIndex,
  GetNumOfWaypoints: GetNumOfWaypoints,
  GetWaypointByName: GetWaypointByName,
  SaveWaypoints: SaveWaypoints,
  AddNewWaypoint: AddNewWaypoint,
};
