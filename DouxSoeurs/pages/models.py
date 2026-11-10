from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet


class PatisseriesIndexPage(Page):
    def get_context(self, request, *args, **kwargs):
        # On récupère le contexte normal de la page
        context = super().get_context(request, *args, **kwargs)
        # On y ajoute la liste des pâtisseries, triées par leur champ "ordre"
        context["patisseries"] = Patisserie.objects.order_by("ordre")
        return context

@register_snippet
class Patisserie(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    ) 
    ordre = models.IntegerField(default=0)   

    def __str__(self):
        return self.titre

class RecettesIndexPage(Page):
    # La recette mise en valeur en haut de la page (choisie dans l'admin)
    recette_vedette = models.ForeignKey(
        "pages.RecettePage",
        null=True,
        blank=True,                      # facultatif
        on_delete=models.SET_NULL,       # si la recette est supprimée, la page ne casse pas
        related_name="+",
        verbose_name="Recette mise en valeur",
    )

    content_panels = Page.content_panels + [
        FieldPanel("recette_vedette"),
    ]

    # Sous « Nos recettes », on ne peut créer que des recettes
    subpage_types = ["pages.RecettePage"]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Les recettes publiées qui sont enfants de cette page
        recettes = RecettePage.objects.child_of(self).live()
        # On retire la recette mise en valeur : elle a déjà sa place en haut
        if self.recette_vedette:
            recettes = recettes.exclude(pk=self.recette_vedette.pk)
        # Les plus récentes d'abord
        context["recettes"] = recettes.order_by("-first_published_at")
        return context

class RecettePage(Page):
    # Photo de la recette (le nom du gâteau = le titre de la page)
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    # Texte avec mise en forme (listes, gras...)
    ingredients = RichTextField(blank=True)
    preparation = RichTextField(blank=True)

    # Les champs visibles dans l'admin
    content_panels = Page.content_panels + [
        FieldPanel("photo"),
        FieldPanel("ingredients"),
        FieldPanel("preparation"),
    ]

    # Une recette ne peut être créée que sous « Nos recettes »
    parent_page_types = ["pages.RecettesIndexPage"]

class ContactPage(Page):
    pass

