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
    $ cat >> $VIRTUAL_ENV/bin/postactivate
    
    export DJANGO_SETTINGS_MODULE=myapp.settings.dev
    
    # Edition du fichier postdeactivate
    $ cat >> $VIRTUAL_ENV/bin/postdeactivate
    
    unset DJANGO_SETTINGS_MODULE
    
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