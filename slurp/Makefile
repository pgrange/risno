SRC=$(wildcard *.coffee)
JS=$(SRC:.coffee=.js)
NODE_UNIT=./node_modules/nodeunit/bin/nodeunit
COFFEE=./node_modules/coffee-script/bin/coffee

help:
	@echo "\tmake test: run tests"
	@echo "\tmake clean: clean all build files"
	@echo "\tmake dist-clean: you probably don't want this"

test: compile
	$(NODE_UNIT) test*.js

clean:
	rm *.js *.map

compile: install $(JS)
install: .installed
.installed: package.json
	npm install
	@touch .installed
dist-clean: clean
	rm .installed
	rm -rf node_modules
%.js: %.coffee
	$(COFFEE) -c -m $<
.PHONY: clean help dist-clean install compile run test
