export ELASTIC_PORT=9299
export ELASTIC_URL=localhost:$(ELASTIC_PORT)
CSV=$(wildcard *.csv)
TST=$(CSV:.csv=.tst)

.PHONY: elastic_running stop all clean distclean types_updated

all: test

elastic_running:
	./ensure_elastic_running

elastic.id: elastic_running

types_injected: elastic.id ../../elastic_mappings/types/types
	../../elastic_mappings/types/types
	@touch types_injected
cities_injected: elastic.id ../../elastic_mappings/cities/inject_cities_in_elasticsearch.sh ../../elastic_mappings/cities/cp-france.csv ../../elastic_mappings/cities/city_unboost_terms.txt
	@echo injecting cities... please be patient
	../../elastic_mappings/cities/inject_cities_in_elasticsearch.sh
	@touch cities_injected

%.tst.inserted: %.csv elastic.id
	./insert_sample_data $<
	touch $@
%.tst.type.updated: %.tst.inserted types_injected elastic.id
	@curl -sf $(ELASTIC_URL)/_all/_refresh
	python ../../update_type.py
	@touch $@
%.tst.type: %.csv %.tst.type.updated elastic.id
	@curl -sf $(ELASTIC_URL)/_all/_refresh >/dev/null
	./validate_types $<
	@touch $@
%.tst.city.updated: %.tst.inserted cities_injected elastic.id
	@curl -sf $(ELASTIC_URL)/_all/_refresh
	python ../../update_locations.py
	@touch $@
%.tst.city: %.csv %.tst.city.updated elastic.id
	@curl -sf $(ELASTIC_URL)/_all/_refresh >/dev/null
	./validate_cities $<
	@touch $@
%.tst: %.tst.type %.tst.city
	@touch $@

test: $(TST)

stop:
	docker stop `cat elastic.id`
	rm elastic.id

clean:
	rm -f *.tst*

distclean: clean stop
	rm -f cities_injected types_injected
