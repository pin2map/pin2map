#!/usr/bin/env python3
"""ADR-008: execute extracted pure routing domain in isolated Node VM."""
import pathlib
import subprocess

html = (pathlib.Path(__file__).resolve().parent.parent / "index.html").read_text()
start = html.index("var p2mRoutingDomain=(function(){")
end = html.index("function formatRouteDuration(sec){", start)
domain = html[start:end]
assert "document" not in domain and "window" not in domain and "fetch(" not in domain and "L." not in domain
script = domain + """
const assert = require('node:assert/strict');
const d = p2mRoutingDomain;
assert.equal(d.durationLabel(45), '1 min');
assert.equal(d.durationLabel(3600), '1 h ');
assert.equal(d.durationLabel(3660), '1 h 1 min');
assert.equal(d.durationLabel(0), '0 min');
assert.equal(d.airDistanceMeters({lat:48.7758,lng:9.1829},{lat:48.7758,lng:9.1829}),0);
const metres=d.airDistanceMeters({lat:48.7758,lng:9.1829},{lat:48.7768,lng:9.1840});
assert.ok(metres > 100 && metres < 200, metres);
const points=[
 {lat:0,lng:0}, {lat:0,lng:0.03}, {lat:0,lng:0.01}, {lat:0,lng:0.04}
];
assert.deepEqual(d.optimizeWaypointIndices(points),[0,2,1,3]);
assert.deepEqual(d.optimizeWaypointIndices([{lat:0,lng:0},{lat:0,lng:0.01}]),[0,1]);
assert.deepEqual(d.optimizeWaypointIndices([{lat:0,lng:0},{lat:0,lng:0.01},{lat:0,lng:0.02}]),[0,1,2]);
assert.deepEqual(points,[{lat:0,lng:0},{lat:0,lng:0.03},{lat:0,lng:0.01},{lat:0,lng:0.04}]);
const osrm={code:'Ok',routes:[{distance:180,duration:45,geometry:{type:'LineString',coordinates:[[9,48],[9.1,48.1]]},legs:[{steps:[{geometry:{coordinates:[[9,48],[9.05,48.05]]}},{geometry:{coordinates:[[9.05,48.05],[9.1,48.1]]}}]}]}]};
const normalized=d.normalizeOsrmRoute(osrm);
assert.equal(normalized.distance,180);
assert.equal(normalized.duration,45);
assert.deepEqual(normalized.segments,[[[9,48],[9.05,48.05],[9.1,48.1]]]);
assert.equal(osrm.routes[0].legs[0].steps[1].geometry.coordinates.length,2);
assert.throws(()=>d.normalizeOsrmRoute({code:'NoRoute',routes:[]}),/Keine Route/);
assert.throws(()=>d.normalizeOsrmRoute(null),/Keine Route/);
assert.equal(Object.isFrozen(d),true);
console.log('PASS: pure route domain duration, coordinates, immutability');
"""
subprocess.run(["node", "-e", script], check=True)
