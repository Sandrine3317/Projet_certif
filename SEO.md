# SEO et référencement – Doux-Sœurs sucrées

Ce document liste chaque optimisation appliquée au site et explique pourquoi elle est utile **pour ce projet précis** : un site vitrine de deux sœurs pâtissières (Sandrine et Lucie), qui présente leurs pâtisseries et leurs recettes, géré dans Wagtail par des personnes qui ne touchent pas au code, et surtout consulté sur téléphone.

---

## 1. Titre SEO et description de chaque page

**Ce qui est fait.** Chaque page publiée a un `seo_title` et une `search_description` différents, saisis dans l'onglet « Promotion » de l'admin Wagtail. Le gabarit `base.html` affiche le titre SEO dans `<title>` (ou le titre de la page s'il est vide) et la description dans `<meta name="description">`.

| Page | Titre SEO | Description (début) |
|---|---|---|
| Accueil | Doux-Sœurs sucrées, pâtisseries maison | Deux sœurs pâtissent ensemble des gâteaux faits maison… |
| Nos pâtisseries | Nos pâtisseries maison | Découvrez les pâtisseries faites maison : gâteaux, tartes… |
| Nos recettes | Nos recettes sucrées | Retrouvez les recettes : bûche de Noël, gâteaux traditionnels… |
| Bûche de Noël | Recette de la bûche de Noël | Ingrédients et étapes de préparation… |
| Cookies | Recette de cookies maison | Ingrédients et étapes, simples et gourmands… |
| Biscuit du millionnaire | Recette du biscuit du millionnaire | Sablé, caramel et chocolat… |
| Contact | Contactez les Doux-Sœurs sucrées | Une question, une envie, une demande spéciale ?… |
| Confidentialité | Politique de confidentialité | Comment sont utilisées les données du formulaire… |

**Pourquoi pour ce site.** Les visiteurs arrivent surtout en cherchant une recette précise (« recette bûche de Noël », « cookies maison »). Le titre SEO de chaque fiche reprend donc exactement ces mots, et la description dit ce qu'on trouvera (ingrédients, étapes) pour donner envie de cliquer. Aucun texte n'est répété d'une page à l'autre, sinon Google ne saurait pas quelle page montrer.

## 2. Hiérarchie des titres

**Ce qui est fait.** Un seul `<h1>` par page, puis des `<h2>` et `<h3>` sans saut de niveau :
- Accueil : h1 « Fait maison, avec amour et gourmandise » → h2 « Notre histoire » ;
- Nos recettes : h1 → h2 recette du moment → h2 « Découvrez d'autres recettes » → h3 nom de chaque recette ;
- Fiche recette : h1 nom du gâteau → h2 « Ingrédients » (h3 pour chaque partie, ex. « Pour le caramel ») → h2 « Préparation ».
- Correction : la page de recherche utilisait des `<h4>` directement sous le `<h1>` (saut de niveau). Ils sont passés en `<h2>`, et les pages de recherche, 404 et 500 ont été traduites en français.

**Pourquoi pour ce site.** Sur une fiche recette, le h1 dit à Google « cette page parle des cookies », et les h2 « Ingrédients » / « Préparation » montrent que c'est une vraie recette structurée. C'est aussi ce qui permet à une personne avec un lecteur d'écran de sauter directement aux ingrédients.

## 3. Texte alternatif des images

**Ce qui est fait.** Un champ **« Description de la photo »** (`photo_alt`) a été ajouté sur les pâtisseries et sur les recettes. Sandrine ou Lucie le remplissent dans l'admin au moment où elles choisissent la photo. Le gabarit l'utilise comme `alt` ; s'il est vide, le nom du gâteau sert de secours (`alt=page.photo_alt|default:page.title`), donc une image n'a jamais d'alt vide par oubli.
Exemple : avant `alt="Fraisier"`, après `alt="Fraisier entier garni de fraises fraîches et de crème, avec une part servie à côté"`.
Les photos de l'accueil ont un alt descriptif (« Sandrine et Lucie en train de pâtisser »). Le logo et le cupcake de la page Contact sont décoratifs : `alt=""`, car le nom du site est déjà écrit en texte à côté du logo.

**Pourquoi pour ce site.** C'est un site de pâtisserie : les photos sont le contenu principal. Un alt qui décrit vraiment le gâteau permet aux photos d'apparaître dans Google Images (très utilisé pour chercher des idées de gâteaux) et aide les personnes malvoyantes. Le champ est dans l'admin plutôt que dans le code, parce que ce sont les sœurs qui ajoutent les photos, pas une développeuse.

## 4. Sitemap (`/sitemap.xml`)

**Ce qui est fait.** Activé avec `django.contrib.sitemaps` et `wagtail.contrib.sitemaps`. Il liste les 8 pages publiées, avec leur date de dernière modification. La recette « Moelleux au chocolat », encore en brouillon, n'y apparaît pas.

**Pourquoi pour ce site.** De nouvelles recettes seront ajoutées régulièrement, et une recette n'est reliée qu'à la page « Nos recettes » (et parfois à une carte pâtisserie). Le sitemap se met à jour tout seul : dès qu'une recette est publiée, Google la trouve sans attendre de la découvrir par les liens, et sans action technique des sœurs.

## 5. robots.txt (`/robots.txt`)

**Ce qui est fait.**
```
User-agent: *
Allow: /
Disallow: /admin/
Sitemap: https://<domaine>/sitemap.xml
```

**Pourquoi pour ce site.** Tout le contenu public peut être exploré. L'espace d'administration Wagtail (`/admin/`) est exclu : il n'a aucun intérêt dans les résultats de recherche. La ligne `Sitemap` donne à Google l'adresse du sitemap dès sa première visite. L'adresse est construite à partir du domaine réel de la requête, donc elle reste juste en local comme en production.

## 6. Poids des images

**Ce qui est fait.**
- Les photos gérées dans Wagtail sont **redimensionnées à leur taille d'affichage** (`fill-400x300` pour les cartes, `fill-600x400` pour la recette du moment, `fill-800x500` pour la photo d'une fiche) au lieu d'envoyer l'original.
- Elles sont en plus **converties en WebP** (`format-webp`). Plusieurs photos avaient été déposées en PNG, un format fait pour les dessins et très lourd pour une photo.
- Les images sous le premier écran ont `loading="lazy"` : elles ne se chargent que quand on fait défiler la page.
- Les images fixes ont des attributs `width` et `height` : la place est réservée avant le chargement, la page ne « saute » pas.
- Le logo (affiché à 140 px) est passé de 500×500 à 280×280 px, et l'illustration cupcake de PNG à WebP.

| Page | Images avant | Images après |
|---|---|---|
| Nos pâtisseries | ≈ 890 Ko | 150 Ko |
| Nos recettes | ≈ 370 Ko | 103 Ko |
| Fiche Biscuit du millionnaire | ≈ 790 Ko | 81 Ko |
| Contact | ≈ 255 Ko | 78 Ko |
| Accueil (photos déjà compressées : 2,9 Mo → 0,4 Mo) | ≈ 390 Ko | 346 Ko |

**Pourquoi pour ce site.** Les visiteurs regardent les recettes sur leur téléphone, souvent en 4G, parfois directement dans la cuisine. La page « Nos pâtisseries » est 6 fois plus légère : elle s'affiche plus vite, consomme moins de forfait, et Google, qui tient compte de la vitesse sur mobile, la classe mieux. La conversion est automatique : même si les sœurs déposent une photo lourde, le visiteur reçoit une version légère.

## 7. Audit Lighthouse

- **Catégorie SEO** (mode mobile) : 100/100 sur les 7 pages (accueil, pâtisseries, recettes, 2 fiches recette, contact, confidentialité).
- **Catégorie Accessibilité** (mobile et desktop) : 100/100 sur Contact et une fiche recette.

L'outil confirme les vérifications faites à la main, mais chaque point ci-dessus a d'abord été compris et appliqué volontairement.

---

## À faire au déploiement

- Dans l'admin Wagtail (Paramètres > Sites), remplacer le nom d'hôte `localhost` par le vrai nom de domaine : le sitemap utilise cette adresse.
- Lancer `python manage.py migrate` (nouveau champ « Description de la photo »), puis remplir ce champ pour chaque pâtisserie et recette dans l'admin de production.
