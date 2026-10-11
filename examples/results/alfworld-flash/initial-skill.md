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
- When the stated task is complete, reply {"action": "stop"}.
