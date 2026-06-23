========================
Django-drybones
========================

Ce document présente les étapes minimales nécessaires pour mettre en place un projet *Django* (version 4.2) en utilisant le template *drybones*

Prérequis
===================
pipx et python (dans cette doc, **python3.12**, dépendamment des besoins la versions peut être différente)  doivent être installés ::

    $ sudo apt install pipx

Pour python, je recommande l'utilisation de **pyenv** dans la mesure où il permet facilement de passer d'une version à l'autre

Procédure
===================
Pour générer un template pour le projet "**myapp**" :

Initialiser le projet Django
----------------------------
Tout d'abord, installez la version requise de *django* (à l'heure de la rédaction de ce document, la **4.2.16**) via pipx ::

    $ pipx install django==4.2.16
    $ pipx install poetry --python python3.12 // à remplacer par votre version de python
    $ pipx install

Ensuite, créez le projet en utilisant le template de la dernière version de django supportée ::

    $ django-admin startproject --template=https://github.com/unistra/django-drybones/archive/master.zip --extension=html,rst,ini,coveragerc --name=Makefile myapp

Ou, pour une version de django [AUTRE_VERSION] spécifique ::

    $ django-admin startproject --template=https://github.com/unistra/django-drybones/archive/refs/heads/django[AUTRE_VERSION].zip --extension=html,rst,ini,coveragerc --name=Makefile myapp

Configuration du projet
=======================
Installez poetry via pipx ::

    $ pipx install poetry --python python3.12 // à remplacer par votre version de python

Ou autrement : `voir la doc officielle <https://python-poetry.org/docs/#installation>`_ puis installez les plugins suivants (sans `pipx inject` et avec `self add` si l'installation de poetry s'est faite autrement que par pipx) ::

    # Plugin de gestion des exports
    $ pipx inject poetry poetry-plugin-export # avec pipx
    OU
    $ poetry self add poetry-plugin-export # autre installation

    # Plugin permettant de trier par ordre alphabétique les dépendances
    $ pipx inject poetry poetry-plugin-sort

    # Plugin permettant de gérer les variables d'environnement depuis un fichier .env
    $ pipx inject poetry poetry-dotenv-plugin

    # Plugin permettant de soumettre les packages utilisés et détecte les alertes de sécurité
    $ pipx inject poetry poetry-audit-plugin

Installation des dépendances
----------------------------
Il faudra ensuite installer les différentes dépendances ::

    # Initialisation
    $ cd myapp
    $ poetry init

    # Installation des dépendances communes :
    $ poetry add [contenu de requirements/common.txt]

    # Installation des dépendances de dev:
    $ poetry add --group dev [requirements/dev.txt]

    # Installation des dépendances de test :
    $ poetry add --group test [requirements/test.txt]

    # Installation des dépendances de prod :
    $ poetry add --group prod [requirements/prod.txt]

    # Installation des dépendances de pré prod :
    $ poetry add --group preprod [requirements/preprod.txt]

Et rajouter / modifier les lignes suivantes dans le fichier *pyproject.toml* ::

    [tool.poetry]
    ...
    package-mode = false <-- ligne à ajouter

    ...
    [tool.poetry.dependencies]
    django = "^4.2.0" --(remplacer par)--> django = "~4.2.0"

Génération des requirements
---------------------------
Creéz un script .sh (ex: *generate-requirements.sh*) contenant le script suivant ::

    #!/bin/bash

    echo "📦️ generating common.txt"
    poetry export -o requirements/common.txt --without-hashes

    for env in test preprod prod;
    do
    echo "📦️ generating $env.txt"
    poetry export -o requirements/$env.txt --with $env
    done

    echo "📦️ generating dev.txt"
    poetry export -o requirements/dev.txt --without-hashes --with dev

Rendez-le exécutable puis lancez-le afin de générer les différents requirements ::

    $ chmod +x generate-requirements.sh && ./generate-requirements.sh

Configuration de la base de données
-----------------------------------
Afin de pouvoir lancer le projet en suivant le template drybones, il convient de configurer une base de données (postgresql en l'occurrence) 

Ajoutez un fichier *docker-compose.yaml* à la racine du projet avec la configuration minimale suivante ::

    services:
    db:
        image: "postgres_12_fr"
        build: ./docker
        container_name: test_db
        restart: unless-stopped
        environment:
        - POSTGRES_PASSWORD=test
        - POSTGRES_USER=test
        - POSTGRES_DB=test
        ports:
        - "5432:5432"
        volumes:
        - test_db:/var/lib/postgresql/data

    volumes:
    test_db:
        driver: local

Puis ajoutez un fichier *docker/Dockerfile* à la racine du projet avec le contenu suivant ::

    FROM postgres:12

    RUN localedef -i fr_FR -c -f UTF-8 -A /usr/share/locale/locale.alias fr_FR.UTF-8

    ENV LANG fr_FR.utf8

Créez le fichier *.env* à la racine de projet, avec le contenu suivant ::

    DJANGO_SETTINGS_MODULE="myapp.settings.dev"

Vous pouvez spécifier les valeurs des variables d'environnement dans ce même fichier plutôt que dans les settings de votre projet (dans settings/dev.py pour la phase de dev)

Lancez un docker compose (en mode détaché ou pas) afin de démarrer l'image postgresql ::

    $ docker compose up

Vous pouvez maintenant  initialiser la base de données :

* Utilisez votre environnement virtuel ::

    $ poetry shell (pour les versions de poetry antérieure à la 2.0.0, inutile autrement)

* Puis exécutez la commande *migrate* ::

    $ python manage.py migrate (pour les versions de poetry antérieure à la 2.0.0)
    OU
    $ poetry run manage.py migrate (pour les version de poetry supérieures à la 2.0.0)

Configuration de pre-commit
---------------------------
Installez pre-commit ::

    $ pipx install pre-commit

Puis créez le fichier *.pre-commit-config.yaml* à la racine de votre projet. Pour le remplissage, vous pouvez vous aider avec :

* La `doc officielle <https://pre-commit.com/>`_
* Un fichier de config existant, celui d'`octant <https://git.unistra.fr/di/cesar/octant/back/-/blob/develop/.pre-commit-config.yaml?ref_type=heads>`_ par exemple

Il suffira ensuite d'installer les hooks correspondants (depuis la racine du projet) ::

    # Soyez sûr d'avoir au préalable initialisé votre repo avec un `git init` (ou `git flow init`)
    $ pre-commit install

Tester la configuration du projet
=================================
Afin de vérifier que la configuration de votre projet s'est bien passée, vous pouvez lancer l'application ::

    $ poetry shell
    $ python manage.py runserver (poetry version inférieure à la 2.0.0)

    OU

    $ poetry run manage.py runserver (poetry version supérieure à la 2.0.0)
