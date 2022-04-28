========================
Django-drybones
========================

.. image:: https://landscape.io/github/unistra/django-drybones/master/landscape.svg?style=flat
   :target: https://landscape.io/github/unistra/django-drybones/master
   :alt: Code Health

Template pour les projets Django 3.2.

Prérequis
===================
pip, virtualenv et virtualenvwrapper doivent être installés.

Procédure
===================
Pour générer un template pour le projet "**myapp**" :

Création de l'environnement virtuel
-----------------------------------

Pour créer l'environnement virtuel, se placer dans le répertoire d'installation du projet::

    $ mkvirtualenv myapp

Installation de Django
----------------------

Pour installer Django dans l'environnement virtuel::

    $ pip install "Django>=3.2,<3.3"

Création du projet
-------------------

Pour créer le nouveau projet en utilisant le template::

    $ django-admin startproject --template=https://github.com/unistra/django-drybones/archive/master.zip --extension=html,rst,ini,coveragerc --name=Makefile myapp

Configuration du projet
-----------------------

Pour configurer le projet dans l'environnement virtuel::

    $ cd myapp
    $ setvirtualenvproject $VIRTUAL_ENV $(pwd)

    # Edition du fichier postactivate
    $ echo "export DJANGO_SETTINGS_MODULE=myapp.settings.dev" >> $VIRTUAL_ENV/bin/postactivate

    # Edition du fichier postdeactivate
    $ echo "unset DJANGO_SETTINGS_MODULE" >> $VIRTUAL_ENV/bin/postdeactivate

    # Rechargement de l'environnement virtuel
    $ workon myapp

Installation des librairies
---------------------------

Pour installer les librairies ::

    $ cdproject
    $ pip install -r requirements/dev.txt

Lancer le serveur de développement
----------------------------------

Pour finaliser l'installation et lancer le serveur::

    $ chmod u+x manage.py
    $ ./manage.py migrate
    $ ./manage.py runserver

Goodies
-------

Vous pouvez ajouter une fonction à vos dotfiles pour faciliter la création d'un projet::

    # inits project for django-drybones project
    # see https://github.com/unistra/django-drybones
    # Usage initproject project_name [-p python_version] [-d django_version] [-i]
    # example initproject my-django-project -p 3.10 -d 3.2
    initproject () {

        local PYTHON_VERSION=${DRY_BONES_PYTHON_VERSION:=3.10}
        local DJANGO_VERSION=${DRY_BONES_DJANGO_VERSION:="3.2"}
        local PROJECT_NAME=""
        local INTERACTIVE_MODE=0

        local ARGS=`getopt --long -o p:d:i "$@"`
        eval set -- "$ARGS"
        while true
        do
            case "$1" in
                (-p) PYTHON_VERSION=$2
                        shift 2 ;;
                (-d) DJANGO_VERSION=$2
                        shift 2 ;;
                (-i) INTERACTIVE_MODE=1
                        echo interactive
                        shift 1 ;;
                (*) case "$#" in
                        (1) echo "Missing argument!"
                            break ;;
                        (2) PROJECT_NAME=$2
                            break ;;
                        (*) echo "Too many arguments!"
                            break ;;
                    esac
                    break ;;
            esac
        done

        test -z $PROJECT_NAME && {
                echo -e "Script usage:\n" \
                "\t initproject project_name [-p python_version] [-d django_version] [-i]\n" \
                "\t example : initproject my-django-project -p 3.10 -d 3.2"
                return 1
        }

        echo "creating \"$PROJECT_NAME\", django $DJANGO_VERSION project for python $PYTHON_VERSION"

        mkvirtualenv $PROJECT_NAME -p python"$PYTHON_VERSION"

        test -n ${VIRTUAL_ENV-} || {
            echo no env, no gain >&2
            return 1
        }

        pip install "Django==$DJANGO_VERSION"

        if test $INTERACTIVE_MODE -eq 0
            then django-admin startproject --template=https://github.com/unistra/django-drybones/archive/master.zip \
                --extension=html,rst,ini,coveragerc --name=Makefile $PROJECT_NAME
                echo "interactive mode off"
            else echo "interactive mode ON"
                return 0
        fi

        cd $PROJECT_NAME
        setvirtualenvproject $VIRTUAL_ENV $PWD
        echo "export DJANGO_SETTINGS_MODULE=$PROJECT_NAME.settings.dev" >> $VIRTUAL_ENV/bin/postactivate
        echo "unset DJANGO_SETTINGS_MODULE" >> $VIRTUAL_ENV/bin/postdeactivate
        workon $PROJECT_NAME
        chmod +x manage.py
        pip install -r requirements/dev.txt
    }

Et ensuite pour creer le virtualenv, installer django et initialiser le projet::

    $ initproject mon_projet

pour preciser la version de python et/ou de django -p pour la version de python et -d pour la version de django::

    $ initproject mon_projet -p 3.7 -d 3.2

