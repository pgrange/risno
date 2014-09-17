SRC=$(wildcard *.coffee)
JS=$(SRC:.coffee=.js)
NODE_UNIT=./node_modules/nodeunit/bin/nodeunit
COFFEE=./node_modules/coffee-script/bin/coffee
BROWSERIFY=./node_modules/browserify/bin/cmd.js

help:
	@echo "\tmake config: start web configuration tool"
	@echo "\tmake test: run tests"
	@echo "\tmake clean: clean all build files"
	@echo "\tmake dist-clean: you probably don't want this"

config: compile public/js/bundle.js
	node config

public/js/bundle.js: public/js/parsing.js
	$(BROWSERIFY) public/js/parsing.js -o public/js/bundle.js

test: compile
	$(NODE_UNIT) test*.js

clean:
	rm *.js *.map public/js/bundle.js

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
