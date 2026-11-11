from django.db import migrations


class Migration(migrations.Migration):
    """Étape 1/4 : on met de côté les anciens champs texte de RecettePage.

    Ils sont renommés (pas supprimés) pour pouvoir convertir leur contenu
    vers les nouveaux blocs (StreamField) dans la migration suivante.
    """

    dependencies = [
        ("pages", "0007_coordonneessettings"),
    ]

    operations = [
        migrations.RenameField(
            model_name="recettepage",
            old_name="ingredients",
            new_name="ingredients_ancien",
        ),
        migrations.RenameField(
            model_name="recettepage",
            old_name="preparation",
            new_name="preparation_ancien",
        ),
    ]
