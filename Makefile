#!/usr/bin/env make

# card3d displays index cards in a 3D environment.
HOME=.
BANNER=python $(HOME)/Banner/Banner.py -b -t "wm!"

all:
	@$(BANNER) "$(MODULE): all"
	@echo "A message will be displayed on MacOS:"
	@echo "Do you want the application “Python.app” to accept incoming network connections?"
	@echo "Clicking Deny may limit the application’s behavior. This setting can be changed in the Firewall pane of Security & Privacy preferences."
	@echo "Click Allow."
	@-./card3d.py

.PHONY: clean
clean:
	@$(BANNER) "$(MODULE): clean"
	rm -f *.pep8 *.pyflakes *.pylint

.PHONY: lint
lint: card3d.py
	@$(BANNER) "$(MODULE): lint"
	@-pep8 $< > $<.pep8 2>&1
	@-pylint $< > $<.pylint 2>&1
	@-pyflakes $< > $<.pyflakes 2>&1

