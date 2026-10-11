# ALFWorld operating skill (initial version)

You are completing household tasks in a text simulator. Reusable guidance may
be added to this file; it is loaded before every episode.

Current guidance (v0):

- Read the task sentence in the observation first; it names the object and the
  destination (for example a ladle on a countertop).
- Explore receptacles one at a time with go to and examine until you find the
  named object.
- Manipulation verbs have fixed effects: take moves an object into your
  inventory; put places it; heat needs the microwave; cool needs the fridge;
  clean needs the sinkbasin; use turns a lamp on while holding nothing else.
- The observation lists admissible commands; prefer exact strings from it.
- Closed receptacles (fridge, cabinets, drawers, microwave) hide their
  contents: after "go to" you must "open" them before the contents appear.
  Budget two actions (go to + open) for every closed receptacle you check.
- Search in likely-first order instead of exhaustively. In kitchens, items
  are most often on countertops, near the sink, on the dining table, or in
  the fridge/microwave; check those before opening every cabinet. In living
  areas, check sofas, coffee tables, tv stands, and side tables.
- Budget your actions. Episodes have a step limit (usually around 24). A
  full pick-and-place task needs: search steps + take + any transform
  (heat/cool/clean) + go to destination + put/move. Reserve at least the
  last two actions for delivery; if more than half the budget is spent
  still searching, change strategy rather than continuing the same sweep.
- Do not examine or revisit receptacles you already searched; move to a new
  candidate each step.
- The goal type tells you the pipeline: "pick X then place in Y" needs
  take, optional heat/cool/clean, then move/put at Y. "look at X in light"
  needs take X, go to the lamp, then use the lamp while holding X. "two of
  the same object" means find and deliver two copies before stopping.
- When the stated task is complete, reply {"action": "stop"}.
