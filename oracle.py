#!/usr/bin/env python3
# Plaster Math oracle - mirrors engine.js with Fractions: kilograms are the product of the entered numbers, the bag count is found by adding bags one at a time until they hold the plaster, rounding is Decimal half-up.
import json, re, random
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

AREA = "the wall area must be from 0.1 to 1000 m2 with at most one decimal place"
THICK = "the coat thickness must be from 0.1 to 50 mm with at most one decimal place"
RATE = "the label rate must be from 0.1 to 5 kg per m2 per mm with at most one decimal place"
COATS = "the number of coats must be a whole number from 1 to 5"
BAG = "the bag size must be a whole number of kg from 1 to 50"
def dec(t, err, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,4}(\.[0-9])?", t) or not F(lo) <= F(t) <= F(hi): raise ValueError(err)
    return F(t)
def whole(t, err, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,3}", t) or not lo <= int(t) <= hi: raise ValueError(err)
    return int(t)
def txt(fr, places):
    v = int((Decimal(fr.numerator) / Decimal(fr.denominator) * (10 ** places)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    ip, fp = divmod(v, 10 ** places); fs = str(fp).zfill(places).rstrip("0")
    return f"{ip}.{fs}" if fs else str(ip)
def inputs(a, t, r, c):
    return dec(a, AREA, "0.1", "1000"), dec(t, THICK, "0.1", "50"), dec(r, RATE, "0.1", "5"), whole(c, COATS, 1, 5)
def lead(a, t, r, c):
    return f"{txt(a,1)} m² at {txt(t,1)} mm a coat with a label rate of {txt(r,1)} kg per m² per mm, in {c} coat{'' if c == 1 else 's'}"

def amount(a, t, r, c):
    A, T, R, C = inputs(a, t, r, c)
    return lead(A, T, R, C) + f", needs {txt(A * T * R * C, 2)} kg."
def bags(a, t, r, c, b):
    A, T, R, C = inputs(a, t, r, c); B = whole(b, BAG, 1, 50)
    kg = A * T * R * C; n = 0
    while n * B < kg: n += 1
    left = n * B - kg
    s = f"The {txt(kg,2)} kg comes to {n} bag{'' if n == 1 else 's'} of {B} kg"
    return s + (", with nothing left over." if left == 0 else f", with {txt(left,2)} kg left over.")
def cover(b, t, r):
    B = whole(b, BAG, 1, 50); T = dec(t, THICK, "0.1", "50"); R = dec(r, RATE, "0.1", "5")
    return f"A {B} kg bag at a label rate of {txt(R,1)} kg per m² per mm covers {txt(B / (R * T), 1)} m² one coat {txt(T,1)} mm thick."

FNS = {"amountTruth": amount, "bagsTruth": bags, "coverTruth": cover}

def cases():
    c = []
    areas = ["0.1", "7.5", "40", "100.3", "1000"]; ths = ["0.1", "2", "3.5", "12", "50"]; rates = ["0.1", "1", "1.3", "5"]
    for a in areas:
        for t in ths:
            for r in rates[:3]:
                c.append(("amountTruth", [a, t, r, "2"]))
    for a in areas:
        for t in ["0.1", "2", "12"]:
            for co in ["1", "5"]:
                for b in ["1", "25", "50"]:
                    c.append(("bagsTruth", [a, t, "1", co, b]))
    for b in ["1", "25", "50"]:
        for t in ["0.1", "2", "50"]:
            for r in rates: c.append(("coverTruth", [b, t, r]))
    for a, t, r, co, b in [("40", "2", "1", "2", "25"), ("12.5", "2", "1", "1", "25"), ("25", "2", "1", "1", "50"), ("10", "1", "1", "1", "10"), ("0.1", "0.1", "0.1", "1", "1"), (" 40 ", " 2 ", " 1 ", " 2 ", " 25 ")]:
        c += [("amountTruth", [a, t, r, co]), ("bagsTruth", [a, t, r, co, b])]
    c.append(("coverTruth", ["25", "2", "1"]))
    bad = ["", "x", "0", "0.0", "0.05", "1.25", "-1", ".5", "5.", "1e2", "10001", "99999"]
    for v in bad:
        c += [("amountTruth", [v, "2", "1", "2"]), ("amountTruth", ["40", v, "1", "2"]), ("amountTruth", ["40", "2", v, "2"]), ("amountTruth", ["40", "2", "1", v]),
              ("bagsTruth", ["40", "2", "1", "2", v]), ("coverTruth", [v, "2", "1"]), ("coverTruth", ["25", v, "1"]), ("coverTruth", ["25", "2", v])]
    for a, t, r, co, b in [("1000.1", "2", "1", "2", "25"), ("40", "50.1", "1", "2", "25"), ("40", "2", "5.1", "2", "25"), ("40", "2", "1", "6", "25"), ("40", "2", "1", "0", "25"), ("40", "2", "1", "1.5", "25"), ("40", "2", "1", "2", "51"), ("40", "2", "1", "2", "0")]:
        c += [("amountTruth", [a, t, r, co]), ("bagsTruth", [a, t, r, co, b])]
    r = random.Random(710)
    for _ in range(8):
        a = f"{r.randint(0, 999)}.{r.randint(0, 9)}"; t = f"{r.randint(0, 49)}.{r.randint(0, 9)}"; rt = f"{r.randint(0, 4)}.{r.randint(0, 9)}"
        a = "0.1" if a == "0.0" else a; t = "0.1" if t == "0.0" else t; rt = "0.1" if rt == "0.0" else rt
        co = str(r.randint(1, 5)); b = str(r.randint(1, 50))
        c += [("amountTruth", [a, t, rt, co]), ("bagsTruth", [a, t, rt, co, b]), ("coverTruth", [b, t, rt])]
    return c

out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    f.write("[\n" + ",\n".join(json.dumps(o, separators=(",", ":"), ensure_ascii=False) for o in out) + "\n]\n")
print(len(out), "cases written")
