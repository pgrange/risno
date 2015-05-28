risno
=====

Real-estate search engine. You can try it here : http://risno.org

# How to use

Hardly ! Not still mature enough to be used ealily. But if you still want to try something, read on.

Copy *risnorc_sample* into a file named *risno* in the directory *$HOME/.config*, and edit values.

## Development

How install *risno* on localhost :

### Tools

* Install tools [machine][] and [compose][]:

        $ make init

* Creates a virtual machine for the development environment :

        $ ./machine create -d virtualbox risno
        $ eval "$(./machine env risno)"

* Check *risno* machine runnning :

        $ ./machine ls

* Launch *risno* :

        $ ./compose up


### Elasticsearch

*risno* use an elasticsearch database running in a docker container.
Then you have to initialize indexes. To do that you need to install jq :

    $ apt-get install jq

Know, initialize french cities index this may take as long as 15 minutes, by running :

    $ ./elastic_mappings/cities/inject_cities_in_elasticsearch.sh

After that you can initialize the index where risno stores the ads, by running :

    $ ./elastic_mappings/ads/ads_1.0
    $ ./elastic_mappings/ads/ads_2.0
    $ ./elastic_mappings/ads/ads_2.1

Elasticsearch is now ready for risno.

### Fetch pubs

Install Python tools:

    $ wget https://bootstrap.pypa.io/get-pip.py
    $ python get-pip.py

Install dependencies :

    $ virtualenv --python=/usr/bin/python2.7 venv
    $ . venv/bin/activate
	$ pip install -r requirements.txt

You are now ready to fetch pubs from several sites by running :

    $ fetch_all.sh

## Consult pubs

Install [NodeJS](http://nodejs.org/) and [Npm](https://npmjs.org/) :

    $ apt-get install nodejs npm

Install dependencies :

    $ cd nodejs && npm install

Start the node web server. To do that, go inside nodejs subdirectory and run :

    $ node index.js

You can now browse this url and take a look at the pubs :

    http://localhost:12043/

WARNING ! If you used risno before ads_2.0 model, go to this url to find your
liked and dislikes opinions :

    http://localhost:12043/12043/new


[machine]: https://github.com/docker/machine/
[compose]: https://github.com/docker/compose
