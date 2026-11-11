import html
import json
import re

from django.db import migrations


def _texte(fragment):
    """Enlève les balises HTML d'un morceau de texte et nettoie les espaces."""
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def _blocs_html(contenu):
    """Découpe le texte de l'ancien champ en blocs <p>, <ul> et <ol>, dans l'ordre."""
    return re.findall(r"<(p|ul|ol)[^>]*>(.*?)</\1>", contenu or "", flags=re.S)


def convertir_ingredients(contenu):
    """Ancien texte libre -> blocs : sous-titres (<p>) et listes (<ul>/<ol>)."""
    resultat = []
    for balise, interieur in _blocs_html(contenu):
        if balise == "p":
            texte = _texte(interieur)
            if texte:
                resultat.append({"type": "sous_titre", "value": texte})
        else:
            lignes = [_texte(li) for li in re.findall(r"<li[^>]*>(.*?)</li>", interieur, flags=re.S)]
            lignes = [ligne for ligne in lignes if ligne]
            if lignes:
                resultat.append({"type": "liste", "value": lignes})
    return resultat


def convertir_preparation(contenu):
    """Ancien texte libre -> un bloc « étape » par élément de liste ou paragraphe."""
    etapes = []
    for balise, interieur in _blocs_html(contenu):
        if balise == "p":
            textes = [_texte(interieur)]
        else:
            textes = [_texte(li) for li in re.findall(r"<li[^>]*>(.*?)</li>", interieur, flags=re.S)]
        for texte in textes:
            if texte:
                etapes.append({"type": "etape", "value": "<p>" + html.escape(texte, quote=False) + "</p>"})
    return etapes


def convertir(apps, schema_editor):
    RecettePage = apps.get_model("pages", "RecettePage")
    for page in RecettePage.objects.all():
        page.ingredients = json.dumps(convertir_ingredients(page.ingredients_ancien))
        page.preparation = json.dumps(convertir_preparation(page.preparation_ancien))
        page.save(update_fields=["ingredients", "preparation"])


class Migration(migrations.Migration):
    """Étape 3/4 : on convertit les recettes existantes vers les nouveaux blocs."""

    dependencies = [
        ("pages", "0009_recettepage_nouveaux_champs"),
    ]

    operations = [
        migrations.RunPython(convertir, migrations.RunPython.noop),
    ]
