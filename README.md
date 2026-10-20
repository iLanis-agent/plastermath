# Plaster Math

Wall plaster amount arithmetic from a label rate. 40 m² at 2 mm a coat with a label rate of 1 kg per m² per mm, in 2 coats, needs 160 kg, which is 7 bags of 25 kg.

## What it computes

- **The amount truth** - kilograms for an area (0.1 to 1000 m²), a coat thickness (0.1 to 50 mm), a label rate you read off the bag (0.1 to 5 kg per m² per mm) and 1 to 5 coats.
- **The bags truth** - the whole bags (1 to 50 kg each) for that amount, and the kilograms left over in the last bag.
- **The cover truth** - the area one bag covers in one coat at that thickness and label rate.

## Boundary

Arithmetic only. The label rate is the owner's own entry from the bag. It has not seen any wall and does not know the surface, the plaster, how thick a coat can go, how it dries, or how much a wall soaks up beyond what is entered, and it gives no verdict that an amount is enough or that a product is right. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers on tenths, half-up rounding).
- `oracle.py` - the Python mirror (Fractions, adding bags one at a time) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/plastermath/
Repo: https://github.com/iLanis-agent/plastermath
