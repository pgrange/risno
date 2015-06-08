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

* Creates a virtual machine called *risno-dev* for the development environment :

        $ ./docker-machine create -d virtualbox risno-dev
        $ eval "$(./docker-machine env risno-dev)"

* Check *risno* machine runnning :

        $ ./docker-machine ls

* Launch *risno* :

        $ ./docker-compose up

* Open your browser and navigate to the IP address associated with the
*risno* virtual machine :

        $ ./docker-machine ip

* To see which environment variables are available to the **web** service,
run:

        $ ./docker-compose run web env


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


## Deployment

### Cloud

With our app running locally, we can now push this exact same environment
to a cloud hosting provider with Docker Machine (Like [RunAbove][]).

Set your credentials in your environment using the [OpenRC file][] that
you can download using the OpenStack Horizon dashboard.

    $ source XXXXXXX-openrc.sh

You need to set the availability zone where you want to deploy your new
instance (SBG-1 or BHS-1) using the following environment variable:

    $ export OS_REGION_NAME=SBG-1

Deploy a new instance :

    $ docker-machine create -d openstack \
        --openstack-flavor-name="ra.intel.ha.s" \
        --openstack-image-name="Ubuntu 14.04" \
        --openstack-net-name="Ext-Net" \
        --openstack-ssh-user="admin" \
        risno-prod

Now we have two Machines running, one locally and one on Digital Ocean:

    $ docker-machine ls
    NAME           ACTIVE     DRIVER         STATE     URL
    risno-dev      *          virtualbox     Running   tcp://w.x.y.z:2376
    risno-prod                openstack      Running   tcp://a.b.c.d:2376

Set *risno-prod* as the active machine and load the Docker environment :

    $ ./docker-machine active risno-prod
    $ eval "$(./docker-machine env risno-prod)"

Finally, let's build the application in the Cloud :

    $ ./docker-compose build
    $ ./docker-compose up -d -f production.yml


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

[OpenRC file]: https://manager.runabove.com/horizon/project/access_and_security/api_access/openrc/
