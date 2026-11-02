# ARCHITECTURE: pricing module

pricing.py turns an order into a final price. It has one public
function, calc(items, country, customer), and no dependencies.

## Data flow

```text
  items          customer               country
    |                |                      |
    v                v                      |
[item guard]   [_discount()]                |
    | valid items    | multiplier           |
    +-------+--------+                      |
            v                               |
  [line totals: qty x price x multiplier]   |
            |                               |
            v                               v
       [subtotal] ------------------> [tax: TAX_RATES]
            |                               |
            v                               |
   [_shipping(subtotal)]                    |
            |                               |
            +---------------+---------------+
                            v
           round(subtotal + tax + shipping, 2)
```

## Components
- **Item guard** (inside calc): skips None, items that aren't
  (name, qty, unit_price) triples, and items whose quantity or price
  isn't positive. Skipped items are dropped silently.
- **_discount(customer)**: returns the price multiplier. A vip value
  equal to True (True or 1) gives 0.9; otherwise SAVE10 gives 0.9 and
  SAVE20 gives 0.8; anything else gives 1.0.
- **Subtotal**: the sum of quantity x price x multiplier over the
  valid items.
- **Tax**: subtotal x TAX_RATES[country], or DEFAULT_TAX_RATE (0.10)
  for any country not in the table.
- **_shipping(subtotal)**: 9.99 below 50, 4.99 below 200, otherwise
  free.
- **Result**: subtotal + tax + shipping, rounded to 2 decimal places.

## Known limitations
1. Only four countries have their own tax rate, and codes are
   case-sensitive.
2. Two hard-coded coupons, case-sensitive, and discounts don't stack.
3. Invalid items are dropped without an error or a log entry.
4. Money is a float, rounded once at the end. Use Decimal before
   this handles real payments.
5. There is no notion of currency; all prices must already be in one.
