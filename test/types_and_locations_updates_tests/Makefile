export ELASTIC_PORT=9299
export ELASTIC_URL=localhost:$(ELASTIC_PORT)

.PHONY: elastic_running stop all clean cclean

all: test

elastic_running:
	./ensure_elastic_running

elastic.id: elastic_running

types_injected: elastic.id ../../elastic_mappings/types/types
	../../elastic_mappings/types/types
	@touch types_injected

types_updated: types_injected data_injected
	@curl -sf $(ELASTIC_URL)/_all/_refresh
	python ../../update_type.py --all
	touch types_updated

cities_injected: elastic.id ../../elastic_mappings/cities/inject_cities_in_elasticsearch.sh ../../elastic_mappings/cities/cp-france.csv ../../elastic_mappings/cities/city_unboost_terms.txt
	@echo injecting cities... please be patient
	../../elastic_mappings/cities/inject_cities_in_elasticsearch.sh
	@touch cities_injected

cities_updated: cities_injected data_injected
	@curl -sf $(ELASTIC_URL)/_all/_refresh >/dev/null
	python ../../update_locations.py --all
	@touch cities_updated

data_injected: elastic.id sample_data.csv
	./insert_sample_data
	@touch data_injected

test_type: types_updated
	@curl -sf $(ELASTIC_URL)/_all/_refresh >/dev/null
	./validate_types

test_city: cities_updated
	@curl -sf $(ELASTIC_URL)/_all/_refresh >/dev/null
	./validate_cities

test: test_type test_city

stop:
	docker stop `cat elastic.id`
	rm elastic.id

clean:
	rm -f cities_updated types_updated data_injected

cclean: clean stop
	rm -f cities_injected types_injected
