========================
Django-drybones
========================

Template pour les projets Django 4.2.

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

    $ pip install "Django>=4.2,<5"

Création du projet
-------------------

Pour créer le nouveau projet en utilisant le template de la dernière version de django supportée::

    $ django-admin startproject --template=https://github.com/unistra/django-drybones/archive/master.zip --extension=html,rst,ini,coveragerc --name=Makefile myapp

Pour une version spécifique::

    $ django-admin startproject --template=https://github.com/unistra/django-drybones/archive/refs/heads/django3.2.zip --extension=html,rst,ini,coveragerc --name=Makefile myapp

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

    # inits project for django-drybone project
    # see https://github.com/unistra/django-drybones
    # Usage initproject project_name [-p python_version] [-d django_version]
    # example initproject -p 3.11 -d 4.2
    function initproject () {
        unset PYTHON_VERSION
        unset DJANGO_VERSION
        declare -g PYTHON_VERSION
        declare -g PYTHON_PATH=
        declare -g PYTHON_VERSION_PATH
        local ARGS
        test -z "$1" && {
                echo -e "Missing argument. Script usage:\n" "  initproject project_name [-p python_version] [-d django_version]" "\n   example : initproject -p 3.11 -d 3.2 "
                return 1
        } || PROJECT_NAME=$1
        ARGS=$(getopt --long -o "p:d:" "$@")
        eval set -- "$ARGS"
        while true
        do
                case "$1" in
                        (-p) PYTHON_VERSION=$2
                                shift 2 ;;
                        (-d) DJANGO_VERSION=$2
                                shift 2 ;;
                        (*) break ;;
                esac
        done
        PYTHON_VERSION=${PYTHON_VERSION:=3.10}
        DJANGO_VERSION=${DJANGO_VERSION:=4.2}
        PYTHON_VERSION_PATH=$( which python$PYTHON_VERSION )
        mkvirtualenv "$PROJECT_NAME" -p "$PYTHON_VERSION_PATH" >&2 || {
            echo "Virtualenv creation failed" >&2
            return 1
        }
        workon "$PROJECT_NAME"
        pip install "Django==$DJANGO_VERSION" || {
            echo "Django installation failed" >&2
            return 1
        }
        django-admin startproject --template="https://github.com/unistra/django-drybones/archive/refs/heads/django$DJANGO_VERSION.zip" --extension=html,rst,ini,coveragerc --name=Makefile "$PROJECT_NAME" >&2 || {
            echo "Project creation failed (maybe wrong django version)" >&2
            return 1
        }
        cd "$PROJECT_NAME" || {
            echo "No app directory" >&2
            return 1
        }
        setvirtualenvproject "$VIRTUAL_ENV" "$PWD"
        echo "export DJANGO_SETTINGS_MODULE=$PROJECT_NAME.settings.dev" >> "$VIRTUAL_ENV/bin/postactivate"
        echo "unset DJANGO_SETTINGS_MODULE" >> "$VIRTUAL_ENV/bin/postdeactivate"
        workon "$PROJECT_NAME"
        chmod +x manage.py
        pip install -r requirements/dev.txt
    }

Et ensuite pour creer le virtualenv, installer django et initialiser le projet::

    $ initproject mon_projet

pour preciser la version de python et/ou de django -p pour la version de python et -d pour la version de django::

    $ initproject mon_projet -p 3.12 -d 4.2
