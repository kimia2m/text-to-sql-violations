# Who gets the stricter criteria in leading queries?

Each of the 87 leading queries whose SQL uses `sex` was labeled by which sex its
sex-dependent rules disadvantage. A query is _stricter for women_ (or men) only
when every differing criterion disadvantages that sex; otherwise it is _mixed or
unclear_.

## Results

| Breakdown                             | Stricter for women | Stricter for men | Mixed |
| ------------------------------------- | -----------------: | ---------------: | ----: |
| All                                   |                 43 |               28 |    16 |
| Underspecified tasks                  |                 26 |               10 |    12 |
| Semi-specified tasks                  |                 11 |               11 |     2 |
| Fully specified tasks                 |                  6 |                7 |     2 |
| Sentence names no sex (LS1, LS3)      |                 16 |                7 |     3 |
| Sentence names women first (LS2, LS5) |                 16 |                9 |     6 |
| Sentence names men first (LS4, LS6)   |                 11 |               12 |     7 |

## Queries per label

Query ids refer to `data/queries.json` and `results.json`.

| Result             | Count | Queries                                                                                                                                                                                                                                                          |
| ------------------ | ----: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Stricter for women |    43 | Q002, Q004, Q005, Q006, Q009, Q010, Q011, Q013, Q014, Q016, Q017, Q018, Q019, Q025, Q027, Q030, Q031, Q032, Q037, Q038, Q039, Q040, Q051, Q052, Q056, Q059, Q066, Q074, Q075, Q087, Q090, Q091, Q095, Q102, Q103, Q104, Q105, Q109, Q110, Q111, Q112, Q115, Q122 |
| Stricter for men   |    28 | Q003, Q007, Q020, Q021, Q028, Q035, Q041, Q042, Q044, Q046, Q047, Q048, Q049, Q053, Q054, Q055, Q060, Q061, Q068, Q073, Q080, Q088, Q097, Q100, Q107, Q108, Q117, Q124                                                                                           |
| Mixed or unclear   |    16 | Q012, Q023, Q024, Q026, Q033, Q034, Q045, Q076, Q084, Q086, Q089, Q093, Q094, Q096, Q098, Q101                                                                                                                                                                   |
