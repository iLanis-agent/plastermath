// Plaster Math engine: wall coat arithmetic from a label rate. Kilograms for an area, thickness and number of coats, whole bags with what is left, and the area one bag covers. Exact integers on tenths, results rounded half up.
function _t(t, err, lo, hi) { // decimal text with at most one place -> tenths
  t = typeof t === "string" ? t.trim() : "";
  var m = /^([0-9]{1,4})(?:\.([0-9]))?$/.exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * 10 + (m[2] ? parseInt(m[2], 10) : 0);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
function _w(t, err, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,3}$/.test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _AREA = "the wall area must be from 0.1 to 1000 m2 with at most one decimal place";
var _THICK = "the coat thickness must be from 0.1 to 50 mm with at most one decimal place";
var _RATE = "the label rate must be from 0.1 to 5 kg per m2 per mm with at most one decimal place";
var _COATS = "the number of coats must be a whole number from 1 to 5";
var _BAG = "the bag size must be a whole number of kg from 1 to 50";
function _hu(n, d) { return Math.floor((2 * n + d) / (2 * d)); }
function _dec(v, places) {
  var base = Math.pow(10, places);
  var s = String(Math.floor(v / base)), f = String(v % base).padStart(places, "0").replace(/0+$/, "");
  return f ? s + "." + f : s;
}
function _coats(c) { return c + (c === 1 ? " coat" : " coats"); }
function _in(area, thick, rate, coats) {
  return { a: _t(area, _AREA, 1, 10000), t: _t(thick, _THICK, 1, 500), r: _t(rate, _RATE, 1, 50), c: _w(coats, _COATS, 1, 5) };
}
function _lead(p) {
  return _dec(p.a, 1) + " m² at " + _dec(p.t, 1) + " mm a coat with a label rate of " + _dec(p.r, 1) + " kg per m² per mm, in " + _coats(p.c);
}

function amountTruth(area, thick, rate, coats) {
  var p = _in(area, thick, rate, coats), n = p.a * p.t * p.r * p.c;      // kg times 1000
  return _lead(p) + ", needs " + _dec(_hu(n, 10), 2) + " kg.";
}
function bagsTruth(area, thick, rate, coats, bagKg) {
  var p = _in(area, thick, rate, coats), b = _w(bagKg, _BAG, 1, 50), n = p.a * p.t * p.r * p.c;
  var bags = Math.floor((n + 1000 * b - 1) / (1000 * b));
  var left = bags * b * 1000 - n;                                          // kg times 1000
  var lead = "The " + _dec(_hu(n, 10), 2) + " kg comes to " + bags + (bags === 1 ? " bag" : " bags") + " of " + b + " kg";
  if (left === 0) return lead + ", with nothing left over.";
  return lead + ", with " + _dec(_hu(left, 10), 2) + " kg left over.";
}
function coverTruth(bagKg, thick, rate) {
  var b = _w(bagKg, _BAG, 1, 50), t = _t(thick, _THICK, 1, 500), r = _t(rate, _RATE, 1, 50);
  return "A " + b + " kg bag at a label rate of " + _dec(r, 1) + " kg per m² per mm covers " + _dec(_hu(b * 1000, r * t), 1) + " m² one coat " + _dec(t, 1) + " mm thick.";
}
