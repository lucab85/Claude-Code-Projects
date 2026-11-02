# HANDOFF: pricing.py readability refactor

## What changed
- calc() no longer nests ten levels deep. Guard clauses skip invalid
  items, and two private helpers, _discount() and _shipping(), hold
  the discount and shipping rules.
- Tax rates moved into a module-level table, TAX_RATES, with
  DEFAULT_TAX_RATE (0.10) for every other country.
- Empty `else: pass` branches were removed.

## Why
The function was correct but hard to review or change safely. Its
cyclomatic complexity drops from 17 to 6 (radon), and it is 14 lines
shorter.

## Risk and how to roll back
Low. The signature is unchanged, the 8 tests pass and
`python3 golden.py check` reports 576 of 576 cases unchanged.
To roll back, `git revert` the refactor commit.

## Watch-outs for the next engineer
- VIP is checked with `== True` on purpose: {"vip": "no"} or
  {"vip": 2} must not get the discount. Don't simplify it to a
  truthiness check; golden.py will fail.
- The item guard is `not (qty > 0 and unit_price > 0)` rather than
  `qty <= 0 or unit_price <= 0`, so a NaN price is still skipped.
- VIP beats coupons, and discounts never stack.
- Country and coupon codes are case-sensitive: "us" pays the 10%
  default tax, and "save10" gets no discount.
- Shipping is based on the discounted subtotal, before tax.
