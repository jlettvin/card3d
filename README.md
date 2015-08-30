card3d
======

* A cloud of index cards is suspended in a 3D space.
* Cards repel each other by default by inverse square law (TODO).
* Cards sharing a keyword are attracted to each other by same law (TODO).
* Cards with explicit connection stay close to each other by spring law (TODO).
* Cards data are currently stored in "config" file (maybe SQL later).

The goal is to navigate through this index card space (mouse/touchscreen),
to enable/disable various forces, causing auto-reorganizing on similarities,
and to add/delete cards rapidly.

Dict is used to simplify control data sharing in the app.

Banner is used in the Makefile, and may be used for monitoring.

Similar will be used to enable fuzzy keyword recognition.

Run card3d.py to display cards stored in card3d.cfg.

Browse localhost:50000/?card2_Opportunity to change card2 text to Opportunity.

Requirements:
* visual python
