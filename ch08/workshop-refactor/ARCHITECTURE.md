# ARCHITECTURE — pricing module (reference)

## Diagram

```text
   items[]                customer
      |                       |
      v                       v
  +----------+    +----------------------+
  | iter +   |    | discount selector    |
  | filter   |--->| (vip > coupon > 1.0) |
  +----------+    +----------+-----------+
                             |
                             v
                       subtotal (sum)
                             |
                +------------+------------+
                |                         |
        +-------v--------+        +-------v--------+
        | _TAX_RATES[c]  |        | shipping ladder|
        +-------+--------+        +-------+--------+
                |                         |
                +-----------+-------------+
                            v
                        round(final, 2)
```

## Components

- **iter+filter**: walks `items`, skips `None` / wrong arity / non-positive `qty` / non-positive `unit_price`. Output: `(qty, price)` pairs.
- **discount selector**: applies VIP (×0.9) first; else SAVE10 (×0.9) / SAVE20 (×0.8); else identity. Pure function of `customer`.
- **subtotal**: sum of `qty × discounted unit_price`.
- **`_TAX_RATES[c]`**: dict of country → rate, default 0.10 for unknown.
- **shipping ladder**: 9.99 if subtotal < 50; 4.99 if < 200; 0.0 otherwise.

## Known limitations

1. Coupons are case-sensitive.
2. No support for stacking discounts.
3. Tax is applied to the full discounted subtotal — does not exclude shipping.
4. Currency is implicit — caller must already be in a single currency.
5. No audit trail of which discount applied; a future receipt feature would need that.
