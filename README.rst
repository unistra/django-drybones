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
    # Usage intpoject project_name
    initproject() {
        if [ -z "$1" ];then
            echo -e "Missing argument. Script usage:\n" \
            "   initproject project_name"
        else
            mkvirtualenv $1
            read -e -p "Which django version to install:" -i "1.6" DJANGO_VERSION
            pip install Django==$DJANGO_VERSION
            django-admin.py startproject --template=https://github.com/unistra/django-drybones/archive/master.zip --extension=html,rst,ini --name=Makefile $1
            cd $1
            setvirtualenvproject $VIRTUAL_ENV $(pwd)
            echo "export DJANGO_SETTINGS_MODULE=$1.settings.dev" >> $VIRTUAL_ENV/bin/postactivate
            echo "unset DJANGO_SETTINGS_MODULE" >> $VIRTUAL_ENV/bin/postdeactivate
            workon $1
            pip install -r requirements/dev.txt
        fi
    }

Et ensuite pour creer le virtualenv, installer django et initialiser le projet::

    $ initproject mon_projet


