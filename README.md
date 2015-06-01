risno
=====

Real-estate search engine. You can try it here : http://risno.org
*risno* stack is based on :

* [elasticsearch][] (v1.5.2)
* [nodejs][] (v0.10.38)


# How to use

Hardly ! Not still mature enough to be used ealily. But if you still want to try something, read on.

## Development

A development environment is provided based on [machine][] and [compose][].

### Tools

* Install tools:

        $ make init

* Creates directory for *risno* data on host :

        $ mkdir /opt/risno

* Creates a virtual machine for the development environment :

        $ ./machine create -d virtualbox risno
        $ eval "$(./machine env risno)"

* Check *risno* machine runnning :

        $ ./machine ls

* Launch *risno* :

        $ ./compose up

* Open your browser and navigate to the IP address associated with the *risno* virtual machine :

        $ ./machine ip

* To see which environment variables are available to the **web** service, run:

        $ ./compose run web env


### Initialization

*risno* use an elasticsearch database running in a docker container.
Then you have to initialize indexes. To do that you need to install jq :

    $ apt-get install jq

Know, initialize french cities index this may take as long as 15 minutes, by running :

    $ ./elasticsearch/mappings/cities/inject_cities_in_elasticsearch.sh

After that you can initialize the index where risno stores the ads, by running :

    $ ./elasticsearch/mappings/ads/ads_1.0
    $ ./elasticsearch/mappings/ads/ads_2.0
    $ ./elasticsearch/mappings/ads/ads_2.1

Elasticsearch is now ready for *risno*.



## Contributing

See [CONTRIBUTING](CONTRIBUTING.md).


## License

See [LICENSE][] for the complete license.


## Changelog

TODO.


## Contact

Pascal Grange


[elasticsearch]: https://www.elastic.co
[nodejs]: https://nodejs.org

[machine]: https://github.com/docker/machine
[compose]: https://github.com/docker/compose
