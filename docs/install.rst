Install
=========

Server `Ubuntu 14.04 <http://releases.ubuntu.com/14.04/>`_

Installiamo tramite apt-get dei pacchetti ``supervisor``, ``nginx`` e di ``git``:

.. code-block:: bash

    $ apt-get install -y install supervisor nginx git

Installiamo tramite apt-get del sofwtare e delle librerie necessarie all'installazione di pacchetti python "sotto" virtualenv:

.. code-block:: bash

    $ apt-get install -y python3-dev build-essential libpq-dev libfreetype6-dev libpcre3 libpcre3-dev

Creiamo directory per virtualenv, applicazioni, configurazioni

.. code-block:: bash

    $ mkdir /Projects/virtualenvs
    $ mkdir /Projects/djangoprjs
    $ mkdir /Projects/.envs_conf

Installiamo ``pip`` (sotto la versione di python di defalut, attualmente python2)

.. code-block:: bash

    $ wget https://bootstrap.pypa.io/get-pip.py
    $ python get-pip.py

Installiamo i pacchetti ``python`` a livello di sistema

.. code-block:: bash

    $ pip install -U virtualenv virtualenvwrapper setuptools


Aggiungiamo al file ``.bashrc`` (o ``.profile``) le seguenti righe necessarie a
configurare ``virtualenvwrapper`` e ``pip``

.. code-block:: bash

    export WORKON_HOME=/Projects/virtualenvs
    export PROJECT_HOME=/Projects/djangoprjs
    export PIP_DOWNLOAD_CACHE=/opt/.pip-cache
    source /usr/local/bin/virtualenvwrapper.sh

uscire e riaprire una nuova shell in modo che le precedenti direttive vengano eseguite.

Creazione e attivazione del virtualenv per ``pympa``

.. code-block:: bash

    $ mkvirtualenv -p $(which python3) pympa
    $ workon pympa


spostarsi nella directory che conterrà l'applicazione pympa e clonazione del repository git

.. code-block:: bash

    (pympa)$ cd /Projects/djangoprjs
    (pympa)$ git clone git@github.com:simodalla/pympa.git pympa
    
e installiamo il software necessario a pympa

.. code-block:: bash

    (pympa)$ cd pympa
    (pympa)$ pwd pympa
    /Projects/djangoprjs/pympa/pympa
    (pympa)$ pip install -r requirements/production.txt
    
Installazione e configurazione ``uswgi`` (vedere la documentazione per più informazioni https://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html)

.. code-block:: bash

    $ mkdir /Projects/uwsgi_conf
    $ mkdir /var/log/uwsgi
    $ chown www-data:www-data /var/log/uwsgi
    $ workon pympa7
    (pympa7)$ pip install -U uwsgi

copiamo il template di file di configurazione di uwsgi
``/Projects/djangoprjs/pympa7/pympa/uwsgi/uwsgi.ini`` nella directory
``/Projects/uwsgi_conf``

.. code-block:: bash

    $ cp /Projects/djangoprjs/pympa7/pympa/uwsgi/pympa.ini /Projects/uwsgi_conf/pympa.ini

e aggiustiamo i vari valori secondo le varie esigenze

.. code-block:: ini

    [uwsgi]
    chdir           = /opt/projects/pympa/
    module          = pympa.wsgi
    home            = /opt/projects/pympa/
    virtualenv 	    = /opt/projects/pympa/
    master          = true
    processes       = 10
    enable-threads  = true
    socket          = /tmp/pympa_uwsgi.sock
    chmod-socket    = 664
    uid             = www-data
    gid             = www-data
    vacuum          = true
    logto           = /var/log/uwsgi/pympa.log
    for-readline    = /Projects/.envs_conf/pympa.ini
      env = %(_)
    end-for =

creiamo ora il file ``/Projects/.envs_conf/pympa.conf`` letto dalla direttiva
``for-readline`` di ``uwsgi`` contente le variabili di ambiente necessarie a
``pympa`` nella forma ``DJANGO_NOME_VARIABILE=valore della varibile``, una
per ciascuna riga

.. code-block:: bash

    ...
    DJANGO_CONFIGURATION=Production
    DJANGO_SETTINGS_MODULE=pympa.config
    DJANGO_SECRET_KEY=1234567890
    ...

creiamo un file di configurazione per gestire un gruppo di processi ``pympa``
di ``supervisor``

.. code-block:: bash

    $ touch /etc/supervisor/conf.d/pympa.conf

ed editiamolo con il seguente contenuto

.. code-block:: ini

    [group:pympa]
    programs=uswgi_pympa
    priority=999
    e con il seguente contenuto uswgi_pympa.conf:

creiamo un file di configurazione per gestire ``uswgi`` con ``supervisor``

.. code-block:: ini

    $ touch /etc/supervisor/conf.d/uswgi_pympa.conf

ed editiamolo con il seguente contenuto

.. code-block:: ini

    [program:uswgi_pympa]
    command=/Projects/virtualenvs/pympa/bin/uwsgi --ini /Projects/uwsgi_conf/pympa_uwsgi.ini
    autostart=true
    autorestart=true
    stopsignal=QUIT

e facciamo "vedere" a supervisor i nuovi file di configurazione

.. code-block:: bash

    $ supervisorctl reread
    $ supervisorctl reload
    $ supervictl start pympa:*

configuriamo ora ``nginx`` creando il file

.. code-block:: bash

    $ vi /etc/nginx/sites-available/pympa

ed editandolo con il seguente contenuto

.. code-block:: nginx

    upstream pympa {
        server unix:///tmp/pympa_uwsgi.sock;
    }

    server {
            listen 80;
            server_name pympa.example.com;
            client_max_body_size 10M;
            keepalive_timeout    15;
            charset     utf-8;

            access_log /var/log/nginx/pympa.access.log;
            error_log /var/log/nginx/pympa.error.log;

            root /usr/share/nginx/www_pympa;
            index index.html index.htm;

            location /pympa/static {
                    alias            /Projects/djangoprjs/pympa/staticfiles;
                    access_log      off;
                    log_not_found   off;
            }

            location /pympa/favicon.ico {
                    alias           /Projects/djangoprjs/pympa/staticfiles/pympa/images/favicon.ico;
                    access_log      off;
                    log_not_found   off;
            }

            location / {
                    uwsgi_pass  pympa;
                    include     /Projects/djangoprjs/pympa/pympa/uwsgi/uwsgi_params;
            }
    }

creiamo il link simbolico e poi facciamo il reload dei file di configurazione 
per ``nginx``

.. code-block:: bash

    $ ln -s /etc/nginx/sites-available/pympa /etc/nginx/sites-enabled/pympa
    $ service nginx reload
    
Per lanciare i comandi ``Django`` come ``manage.py shell`` o
``manage.py collectstatic``
è necessario che la shell abbia impostato delle variabili di ambiente come
quelleprecedentemente impostate per ``uswgi``. Di solito si inserivano delle
direttive ``export`` nel file ``/Projects/virtualenvs/pympa/bin/postactivate``

.. code-block:: bash

    export DJANGO_VAR=1234

e delle direttive ``unset`` nel file ``/Projects/virtualenvs/pympa/bin/postdeactivate``

.. code-block:: bash

    unset $DJANGO_VAR

Queste variabilii sono state già impostate per ``uwsgi`` nel file
``/Projects/.envs_conf/pympa.conf`` e per evitare di raddoppiare queste
definizioni ad inserire il seguente snippet nel file ``/Projects/virtualenvs/pympa/bin/postactivate``

.. code-block:: bash

    #!/bin/bash
    # This hook is sourced after this virtualenv is activated.

    ENV_CONF=/Projects/.envs_conf/pympa_staging.conf
    while read var; do export "$var"; done < $ENV_CONF;

e il seguente snippet nel file ``/Projects/virtualenvs/pympa/bin/postdeactivate``

.. code-block:: bash

    #!/bin/bash
    # This hook is sourced after this virtualenv is deactivated.

    ENV_CONF=/Projects/.envs_conf/pympa_staging.conf
    while read row; do var=`echo $row | awk -F'=' '{print $1}'`; unset $var; done < $ENV_CONF


