========================
Django-drybones
========================

Template pour les projets Django 1.6.

Prérequis
===================
pip, virtualenv et virtualenvwrapper doivent être installés.

Procédure
===================
Pour générer un template pour le projet "**myapp**" :

Création de l'environnement virtuel
-----------------------------------

Pour créer l'environnement virtuel, se placer dans le répertoire d'installation du projet::

    $ mkvirtualenv my_app

Installation de Django
----------------------

Pour installer Django dans l'environnement virtuel::

    $ pip install Django==1.6

Création du projet
-------------------

Pour créer le nouveau projet en utilisant le template::

    $ django-admin.py startproject --template=https://github.com/unistra/django-drybones/archive/master.zip --extension=html,rst,ini --name=Makefile myapp

Configuration du projet
-----------------------

Pour configurer le projet dans l'environnement virtuel::

    $ cd my_app
    $ setvirtualenvproject $VIRTUAL_ENV $(pwd)

    # Edition du fichier postactivate
    $ echo "export DJANGO_SETTINGS_MODULE=myapp.settings.dev" >> $VIRTUAL_ENV/bin/postactivate

    # Edition du fichier postdeactivate
    $ echo "unset DJANGO_SETTINGS_MODULE" >> $VIRTUAL_ENV/bin/postdeactivate

    # Rechargement de l'environnement virtuel
    $ workon my_app

Installation des librairies
---------------------------

Pour installer les librairies ::

    $ cdproject
    $ pip install -r requirements/dev.txt

Lancer le serveur de développement
----------------------------------

Pour finaliser l'installation et lancer le serveur::

    $ chmod u+x manage.py
    $ ./manage.py syncdb
    $ ./manage.py migrate
    $ ./manage.py runserver

Goodies
-------

Vous pouvez ajouter une fonction à vos dotfiles pour faciliter la création d'un projet::

    # inits project for django-drybone project
    # see https://github.com/unistra/django-drybones
    # Usage initproject project_name [ -p python_version -d django_version]
    # example initproject -p 3 -d 1.6.1
    initproject() {
        unset PYTHON_VERSION
        unset PYTHON_PATH
        unset DJANGO_VERSION
        if [ -z "$1" ];then
            echo -e "Missing argument. Script usage:\n" \
            "   initproject project_name [ -p python_version -d django_version]" \
            "   example : initproject -p 3 -d 1.6.1 "
        else
            PROJECT_NAME=$1
            ARGS=`getopt --long -o "p:d:" "$@"`
            eval set -- "$ARGS"
            while true ; do
                case "$1" in
                    -p )
                        PYTHON_VERSION=$2
                        shift 2
                    ;;
                    -d )
                        DJANGO_VERSION=$2
                        shift 2
                    ;;
                    *)
                        break
                    ;;
                esac
            done;
            PYTHON_VERSION_PATH=`which python$PYTHON_VERSION`
            mkvirtualenv $PROJECT_NAME -p "$PYTHON_VERSION_PATH"
            if [ -z "$DJANGO_VERSION" ];then
                DJANGO_VERSION=1.6
            fi
            pip install Django==$DJANGO_VERSION
            django-admin.py startproject --template=https://github.com/unistra/django-drybones/archive/master.zip --extension=html,rst,ini --name=Makefile $PROJECT_NAME
            cd $PROJECT_NAME
            setvirtualenvproject $VIRTUAL_ENV $(pwd)
            echo "export DJANGO_SETTINGS_MODULE=$PROJECT_NAME.settings.dev" >> $VIRTUAL_ENV/bin/postactivate
            echo "unset DJANGO_SETTINGS_MODULE" >> $VIRTUAL_ENV/bin/postdeactivate
            workon $PROJECT_NAME
            chmod +x manage.py
            pip install -r requirements/dev.txt
        fi
    }

Et ensuite pour creer le virtualenv, installer django et initialiser le projet::

    $ initproject mon_projet

pour preciser la version de python et/ou de django -p pour la version de python et -d pour la version de django::

    $ initproject mon_projet -p 3 -d 1.6.1


