StatCollector
=============

Simple tool to obtain various development statistics from a number of 
web services.

Currently supported:
--------------------

- github
- travis

Usage
-----

1. Download a copy of the source
2. Unpack and `cd` into the directory
3. Build-out::
    
    $ python bootstrap.py
    $ ./bin/buildout

4. Create a config file, for example (`config.yml`)::

    settings:
      loglevel: warning #debug
    output:
      format: xml
      location: stats.xml
    plugins:
    -  travis:
         user: {github_user}
    -  github:
         user: {github_user}
         password: {github_pass}
         token: {github_secret_token}

5. Run the script::

    $ ./bin/collector -c path/to/config.yml
