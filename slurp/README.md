Cette documentation explique comment configurer un nouveau site pour la récupération d'annonces.

On explique d'abord comment modifier la configuration d'un site existant avant d'expliquer comment ajouter un nouveau site.

Vous devez considérer votre travail comme une contribution à risno. Consultez le [guide de contribution](../CONTRIBUTING.md).

Cette procédure est complexe et sa documentation pas forcément limpide. Si vous avez besoin d'aide, [ouvrez une issue sur le projet github de risno](https://github.com/pgrange/risno/issues/new).

Bon courage !

# Prérequis

Consultez le [guide de contribution](../CONTRIBUTING.md). Pour la version naïve, obtenez une copie de risno et effectuez vos changements dans la branche *develop* :

    # git clone https://github.com/pgrange/risno.git
    # cd risno/slurp
    # git checkout develop

Vous aurez besoin de [GNU make](https://www.gnu.org/software/make/) et [nodejs](https://nodejs.org/).

# Modifier une configuration

Une interface web rudimentaire vous permet de modifier la configuration d'un site existant. Pour la démarrer, lancez la commande (dans le répertoire *risno/slurp*) :

    # make config

Lorsque l'interface est prête, un message s'affiche dans la console pour vous inviter à vous connecter à l'url [http://localhost:12045](http://localhost:12045).

Rendez-vous sur cette page et sélectionnez le site dont vous souhaitez modifier la configuration.

Un formulaire affiche un certain nombre de champs correspondant aux différents paramètres de configuration du site (les valeurs de la configuration actuelle s'affichent). Dessous, vous pouvez voir un aperçu de la deuxième page d'annonce du site ainsi que les annonces détectées sur la page. Si aucune annonce n'est détectée sur la page, c'est que la configuration est erronnée. Vous faites bien de la modifier...

Effectuez vos modifications. Si vous constatez que les annonces sont détectées comme vous le souhaitez, vous pouvez sauvegarder vos modifications en cliquant sur le bouton *save*. Les différents champs du formulaire sont décrits ci-dessous.

## url sequence

Il s'agit du champs le plus difficile à paramétrer et qui vous demandera le plus d'efforts. Il désigne l'URL du site cible à laquelle se trouvent les annonces. Si l'aperçu affiché ne correspond pas à ce que vous attendez, c'est-à-dire s'il ne s'agit pas d'une page affichant la liste des annonces du site cible, vous devez modifier ce paramètre.

Avec votre navigateur, commencez par vous rendre sur le site d'annonces cible puis effectuez une recherche d'annonces immobilières. Votre recherche doit satisfaire les critères suivants :
- ne concerner que l'immobilier (risno ne gère rien d'autre) ;
- ne concerner que des ventes (risno ne gère rien d'autre) ;
- concerner toute la région et exclusivement la région Aquitaine.

Pour le moment, risno ne gère que les régions Aquitaine et Midi-pyrénées. La page de configuration affiche, par défaut, la région Aquitaine. Ainsi, si vous choisissez cette région dans votre recherche de base, vous pourrez directement comparer le site cible avec l'aperçu affiché dans la page de configuration de risno et ainsi vous assurer que vous n'avez pas commis d'erreur.

Sur certains sites, le choix d'une région (Aquitaine dans cet exemple) n'est pas directement possible. Dans ce cas, débrouillez-vous pour sélectionner la région Aquitaine d'une autre façon. Par exemple en sélectionnant manuellement tous les départements de la région si le site permet la recherche par département...

Suite à votre recherche, le site cible devrait vous afficher une liste d'annonces correspondant à vos critère : toutes les ventes immobilières en Aquitaine référencées sur ce site. Vu le nombre, logiquement, cette liste devrait être paginée et vous devriez être sur la première page. Pour préparer la configuration risno, rendez-vous sur la deuxième page, en cliquant sur le bouton *suivant* du site, par exemple.

Vous consultez maintenant la deuxième page des ventes immoblières en Aquitaine sur le site cible. Copiez l'URL affichée dans votre navigateur et collez-la dans le champ *url sequence* de la page de configuration de risno.

Le travail n'est pas terminé.

Vous devez maintenant repérer différentes portions de l'URL que vous devrez rendre paramétrable pour risno. Pour cela, vous allez remplacer ces portions d'URL par des mots clés interprétables par risno. Ces différents mots clés sont décrits ci-dessous.

### HOST

Remplacez le nom d'hôte de l'url par le mot clé *HOST*.

Par exemple si votre url ressemble à :

    http://immo.com/aquitaine/2

Remplacez-la par l'url suivante :

    http://HOST/aquitaine/2

### REGION

Remplacez la portion de l'url qui précise la région de votre recherche par le mot clé *REGION*.

Par exemple, si votre url ressemble maintenant à :

    http://HOST/aquitaine/2

Remplacez-la par :

    http://HOST/REGION/2

Sur le site cible, la région s'appelle rarement par son nom dans l'url. Dans votre exemple, vous ne trouverez probablement pas la chaîne *aquitaine* dans votre url. A vous de trouver quelle partie représente la région. Il pourra s'agir d'un identifiant, comme par exemple *2-72* ou encore de la liste des départements que vous avez sélectionnés, par exemple *24,33,40,47,64*.

Quoiqu'il en soit, vous devrez trouver cet identifiant et le noter précieusement. Nous verrons plus loin quoi en faire.

Il existe des sites spécialisés sur une région ou une zone géographique très restreinte. Dans ce cas, la sélection de la région n'a pas de sens et rien ne désigne la région dans l'URL. *souston-immo.com* ne va probablement proposer des annonces que pour les alentours de Souston. Si c'est le cas du site dont vous mettez la configuration à jour, vous pouvez ignorer cette section et laisser le champs *REGION* vide.

### PAGE

Remplacez la portion de l'url qui précise le numéro de la page par le mot clé *PAGE*.

Par exemple, si votre url ressemble maintenant à :

    http://HOST/REGION/2

Remplacez-la par :

    http://HOST/REGION/PAGE

Le mot clé PAGE supporte quelques opérations arithmétiques.

Il peut arriver que la numérotation des pages du site cible commence à 0 au lieu de 1. Dans ce cas, la deuxième page porte le numéro 1 au lieu de 2. Remplacez alors le numéro de la page par l'expression (les parenthèses sont importantes) :

    (PAGE-1)

Ainsi, si l'url de la deuxième page du site était :

    http://HOST/REGION/1

Remplacez-la par :

    http://HOST/REGION/(PAGE-1)

De même, certains sites ne numérotent pas leurs pages mais précisent l'index de la première annonce à afficher sur la page. Par exemple pour un site qui afficherait 10 annonces par page, dans l'url de la deuxième page, vous devriez trouver 20 (s'il numérote les annonces à partir de 0) au lieu de 2. De la même façon, utilisez un peu d'arithmétique :

    ((PAGE-1)*20)

Ainsi, si l'url de la deuxième page du site était :

    http://HOST/REGION/20

Remplacez-la par :

    http://HOST/REGION/((PAGE-1)*20)

### Correspondance région / identifiant url

Une fois toutes ces modifications effectuées, vous pouvez sauvegarder en cliquant sur le bouton *save*.

Vous pouvez constater que le fichier de configuration *config.json* a été mis à jour avec vos modifications.

Abordons maintenant la partie la plus complexe (si, si) : la correspondance région / identifiant de région dans l'url. Cette partie n'est malheureusement pas gérée par l'interface pour le moment et il va vous falloir éditer manuellement le fichier de configuration.

Arrêtez l'outil de configuration que vous avez lancé précédemment après vous être assuré d'avoir bien sauvegardé.

Ouvrez le fichier de configuration *config.json* avec l'éditeur de votre choix et recherchez la configuration du site que vous souhaitez modifier.

    "immo": {
      "name": "immo",
      "host": "immo.com",
      "url_sequence": [
        "http://HOST/REGION/((PAGE-1)*20)"
      ],
      "region_id": {
      },
      "ads": "",
      "selectors": {
        "price": "",
        "description": "",
        "location": ""
      }
    }

Si la partie *region_id* n'existe pas déjà vous l'ajouterez avec les informations pour les régions Aquitaine et Midi-Pyrénées qui sont les seules supportées par risno pour le moment.

Reprenez l'URL que vous avez décortiquée précédemment. Dans cette url, vous avez réussi à reconnaître la partie qui permet d'identifier spécifiquement la région sélectionnée. Il peut s'agit d'un identifiant (par exemple *2-72*) ou de la suite des départements de la région (par exemple *24,33,40,47,64*) ou encore d'autre chose comme *Aquitaine* (remarquez la majuscule).

A priori, à cette étape, vous n'avez repéré cet identifiant que pour la région Aquitaine. Débrouillez-vous pour trouver l'équivalent pour la région Midi-Pyrénées.

Insérez maintenant cette information dans le fichier de configuration dans la partie *region_id*. Par exemple si l'identifiant correspond à la liste des départements de la région, votre configuration devrait maintenant ressembler à :

    "immo": {
      "name": "immo",
      "host": "immo.com",
      "url_sequence": [
        "http://HOST/REGION/((PAGE-1)*20)"
      ],
      "region_id": {
        "aquitaine": "24,33,40,47,64",
        "midi_pyrenees": "09,12,31,32,46,65,81,82"
      },
      "ads": "",
      "selectors": {
        "price": "",
        "description": "",
        "location": ""
      }
    }

Sauvegardez le fichier de configuration et quittez votre éditeur puis relancez l'outil de configuration :

    make config

En cas de problème de syntaxe dans le fichier, une erreur s'affichera immédiatement. Corrigez le fichier et recommencez.

Si tout s'est bien passé, connectez-vous à nouveau sur l'interface de configuration en vous rendant à l'adresse [http://localhost:12045](http://localhost:12045).

Vérifiez que la page du site cible affichée dans l'aperçu correspond bien à la deuxième page des annonces immobilières en Aquitaine du site cible. Il est possible que le style de la page soit un peu détraqué mais n'en tenez pas compte. Ce qui est important c'est que vous retrouviez bien la même liste d'annonces que sur le site cible.

Si la page affichée dans l'aperçu ne correspond pas... c'est que vous avez raté quelque chose. Bon courage ! Vous pouvez toujours [ouvrir une issue sur le projet github de risno](https://github.com/pgrange/risno/issues/new) pour obtenir de l'aide.

Si tout correspond, félicitations ! vous pouvez passer à l'étape suivante.

## Ad selector

Le plus dur étant passé (quoique) attaquons-nous maintenant au champs suivant dans l'interface de configuration.

Le deuxième champs à renseigner s'intitule *Ad selector*. Vous devez préciser ici le [sélecteur CSS](http://www.w3schools.com/cssref/css_selectors.asp) qui permettra à risno d'identifier toutes les annonces (et uniquement les annonces) présentes sur la page.

Modifiez la valeur du champs puis quittez la zone de saisie afin que la détection d'annonces se mette à jour sur la page.

A coté de ce champs, vous pouvez constater le nombre d'annonces détectées avec ce sélecteur CSS sur la page.

Par exemple, si les annonces sont dans des blocs de type *div* dont la classe css est *listing*, saisissez *div.listing* dans le champs *Ad selector* et vérifiez si elles sont bien détectées.

Vous pouvez vous aidez des fonctions d'inspection de votre navigateur pour consulter le source des annonces et ainsi trouver le bon sélecteur css.

Les annonces détectées sur la page du site cible sont mises en évidence dans l'aperçu.

## price selector

De la même façon, renseignez le sélecteur css, dans une annonce, permettant d'identifier le prix d'une annonce.

## description selector

De la même façon, renseignez le sélecteur css, dans une annonce, permettant d'identifier le texte décrivant l'annonce.

## location selector

De la même façon, renseignez le sélecteur css, dans une annonce, permettant d'identifier l'emplacement du bien (ville) dans l'annonce.

Ce champs est optionnel. Si le site cible ne précise pas l'emplacement du bien ailleurs que dans la description identifiée ci-dessus, ne remplissez pas ce champs.

Lorsque vous avez positionné toutes les valeurs des champs et que vous constatez que la détection s'opère bien sur l'aperçu, sauvegardez vos modifications en cliquant sur le bouton *save*.

# Ajouter un nouveau site

L'interface de configuration ne permet pas encore d'ajouter un nouveau site. Pour cela, vous devrez éditer le fichier config.json.

Ouvrez le fichier config.json avec l'éditeur de votre choix et ajoutez une section pour préparer la configuration de votre nouveau site avec quelques informations de base.

Par exemple pour ajouter le site *immo.com*, ajoutez les lignes suivantes dans le fichier *config.json* (attention à respecter la syntaxe json) :

    "immo": {
      "name": "immo",
      "host": "immo.com",
      "selectors": {
      }
    }

Sauvegardez le fichier et lancez l'outil de configuration :

    make config

En cas de problème de syntaxe dans le fichier, une erreur s'affichera immédiatement. Corrigez le fichier et recommencez.

Si tout s'est bien passé, connectez-vous sur l'interface de configuration en vous rendant à l'adresse [http://localhost:12045](http://localhost:12045).

Sélectionnez le site que vous venez d'initialiser et renseignez les informations de ce site en suivant les indications de la section précédente [Modifier une configuration](#modifier une configuration).

# Soumettre votre contribution

Consultez le [guide de contribution](../CONTRIBUTING.md).

Lorsque vous êtes satisfait de votre configuration, commitez le fichier *config.json* et soumettez cette nouvelle version sur le projet github de risno, le plus pratique étant de soumettre une *pull-request*.

Si vous avez besoin d'aide, n'hésitez pas [ouvrir une issue sur le projet github de risno](https://github.com/pgrange/risno/issues/new) pour obtenir de l'aide.
