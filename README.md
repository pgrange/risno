risno
=====

real-estate search engine

# How to use

Hardly ! Not still mature enough to be used ealily. But if you still want to try something, read on.

## Elasticsearch

risno use an elasticsearch database running in a docker container. If you have [Docker]http://www.docker.io/() installed,
take a look at start_elastic.sh and make the appropriate changes so that it will store its data in a secure adapted directory.
Then run :

    $ start_elastic.sh

Then you have to initialize indexes. First, initialize french cities index this may take as long as 15 minutes, by running :

    $ inject_cities_in_elasticsearch.sh

After that you can initialize the index where risno stores the pubs. To do that, first edit *init-elastic-search.py* and change
"immo2" (the index name) for "immo". Revert this change after index creation... just in case you accidentally re-run this script
because it would destroy all your index.

Install Python tools:

    $ apt-get install python-pip
	$ pip install virtualenvwrapper
	$ source /usr/local/bin/virtualenvwrapper.sh

Install dependencies :

    $ mkvirtualenv risno
	$ pip install -r requirements.txt

To create the index, run :

    $ python init-elastic-search.py

Elasticsearch is now ready for risno.

## Fetch pubs

You are now ready to fetch pubs from several sites by running :

    $ fetch_all.sh

## Consult pubs

Install [NodeJS](http://nodejs.org/):

    $ apt-get install nodejs

Start the node web server. To do that, go inside nodejs subdirectory and run :

    $ node index.js

You can now browse this url and take a look at the pubs :

    http://localhost:12043/
