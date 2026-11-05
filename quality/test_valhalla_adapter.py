#!/usr/bin/env python3
"""Execute Valhalla response adapter without DOM or Leaflet."""
import pathlib
import subprocess

html=(pathlib.Path(__file__).resolve().parent.parent/"index.html").read_text()
start=html.index("var p2mValhallaAdapter=(function(){")
end=html.index("function valhallaTripResult(",start)
adapter=html[start:end]
assert "document" not in adapter and "L." not in adapter and "fetch(" not in adapter
script=adapter+"""
const assert=require('node:assert/strict');
const pins=[{id:1},{id:2}];
const input={trip:{summary:{length:1.5,time:120},legs:[
 {shape:'a',summary:{length:0.5,time:40}},
 {shape:'b',summary:{length:1,time:80}}
]}};
const decode=s=>s==='a'?[[9,48],[9.1,48.1]]:[[9.1,48.1],[9.2,48.2]];
const result=p2mValhallaAdapter.normalizeTrip(input,pins,decode);
assert.deepEqual(result.geometry.coordinates,[[9,48],[9.1,48.1],[9.2,48.2]]);
assert.equal(result.distance,1500);
assert.equal(result.duration,120);
assert.deepEqual(result.legs,[{distance:500,duration:40},{distance:1000,duration:80}]);
assert.equal(result.routeItems,pins);
assert.throws(()=>p2mValhallaAdapter.normalizeTrip({},pins,decode),/Keine Route/);
assert.equal(Object.isFrozen(p2mValhallaAdapter),true);
console.log('PASS: Valhalla response adapter conversion and invalid payload');
"""
subprocess.run(["node","-e",script],check=True)
