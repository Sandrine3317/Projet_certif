# SEO et référencement – Doux-Sœurs sucrées

Justification des optimisations mises en place (une ligne par choix, en lien avec le projet).

## 1. Titre SEO et description de chaque page
Chaque page publiée (Accueil, Nos pâtisseries, Nos recettes, chaque recette, Contact, Politique de confidentialité) a un **seo_title** et une **search_description** différents, saisis dans l'onglet « Promotion » de l'admin Wagtail.
Le site vise des personnes de la région de Bordeaux qui cherchent des recettes ou un atelier de pâtisserie : chaque titre reprend des mots qu'elles taperaient (« recettes », « pâtisseries », « Bordeaux », « ateliers ») et deux pages n'ont jamais le même texte, pour que Google les distingue.
Le gabarit `base.html` affiche le titre SEO s'il existe, sinon le titre de la page.

## 2. Hiérarchie des titres
Un seul `<h1>` par page (le titre de la page), puis des `<h2>` et `<h3>` sans saut de niveau (ex. « Découvrez d'autres recettes » en h2 puis le nom de chaque recette en h3).
Sur l'accueil, le h1 est l'accroche « Fait maison, avec amour et gourmandise ». Cela indique clairement à Google le sujet de chaque page.

## 3. Texte alternatif des images
Les photos de pâtisseries et de recettes ont un `alt` renseigné automatiquement avec le nom du gâteau (`alt=patisserie.titre`, `alt=recette.title`) : il décrit donc vraiment l'image et change à chaque photo ajoutée par Sandrine ou Lucie, sans qu'elles touchent au code.
Les photos de l'accueil ont un alt descriptif (« Sandrine et Lucie en train de pâtisser »…). Le logo et le cupcake sont décoratifs (`alt=""`) : le nom du site est déjà écrit en texte à côté.

## 4. Sitemap (`/sitemap.xml`)
Activé avec `wagtail.contrib.sitemaps`. Il liste automatiquement toutes les pages publiées (y compris chaque nouvelle recette) : quand les sœurs ajoutent une recette, Google la découvre sans action de leur part.

## 5. robots.txt (`/robots.txt`)
Il autorise l'exploration du site, **interdit `/admin/`** (aucun intérêt à indexer l'espace d'administration) et indique l'adresse du sitemap.

## 6. Poids des images
Les photos gérées dans Wagtail sont redimensionnées à la taille affichée (`fill-400x300` pour les cartes, `fill-600x400` et `fill-800x500` pour les mises en valeur) au lieu de charger l'original. Les photos de l'accueil ont été compressées (2,9 Mo → 0,4 Mo). Le site est surtout consulté sur téléphone : une page légère charge plus vite et est mieux classée.

## 7. Audit Lighthouse
- **Catégorie SEO** (mode mobile) : 100/100 sur les 7 pages (accueil, pâtisseries, recettes, 2 fiches recette, contact, confidentialité).
- **Catégorie Accessibilité** (mode mobile et desktop) : 100/100 sur Contact et une fiche recette.

## À prévoir au déploiement
Dans l'admin Wagtail (Paramètres > Sites), remplacer le nom d'hôte `localhost` par le vrai nom de domaine : le sitemap utilise cette adresse.
