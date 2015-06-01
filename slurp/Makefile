export ELASTIC_PORT=9299
export ELASTIC_URL=localhost:$(ELASTIC_PORT)
export BLUEBIRD_DEBUG=1

SRC=$(wildcard *.coffee)
JS=$(SRC:.coffee=.js)
NODE_UNIT=./node_modules/nodeunit/bin/nodeunit
COFFEE=./node_modules/coffee-script/bin/coffee
BROWSERIFY=./node_modules/browserify/bin/cmd.js

help:
	@echo -e "\tmake config: start web configuration tool"
	@echo -e "\tmake test: run tests"
	@echo -e "\tmake clean: clean all build files"
	@echo -e "\tmake dist-clean: purge all generated file, node modules..."

config: compile public/js/bundle.js
	node config

public/js/bundle.js: public/js/parsing.js slurp.js
	$(BROWSERIFY) public/js/parsing.js -o public/js/bundle.js

test: compile elastic_running
	$(NODE_UNIT) test*.js

clean: elastic_stop
	-rm *.js *.map public/js/bundle.js

compile: install $(JS)
install: .installed
.installed: package.json
	npm install
	@touch .installed
dist-clean: clean
	-rm .installed
	-rm -rf node_modules
%.js: %.coffee
	$(COFFEE) -c -m $<

elastic_running:
	./ensure_elastic_running
elastic_stop:
	-docker stop `cat .elastic.id`
	-rm .elastic.id


.PHONY: clean help dist-clean install compile run test elastic_running elastic_stop
