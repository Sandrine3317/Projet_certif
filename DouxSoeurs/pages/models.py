from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

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
        # Recette liée (facultative) : permet d'afficher « Voir la recette » sur la carte
    recette = models.ForeignKey(
        "pages.RecettePage",
        null=True,
        blank=True,                      # facultatif : une pâtisserie peut ne pas avoir de recette
        on_delete=models.SET_NULL,       # si la recette est supprimée, la pâtisserie reste
        related_name="+",                # pas de lien inverse inutile
        verbose_name="Recette liée",     # le nom affiché dans l'admin
    ) 

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
    # Introduction courte de la recette
    introduction = models.TextField(blank=True, verbose_name="Introduction")

    # Informations pratiques
    temps_preparation = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Temps de préparation (en minutes)",
    )
    portions = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Nombre de portions",
    )
    difficulte = models.CharField(
        max_length=10,
        blank=True,
        choices=[("facile", "Facile"), ("moyen", "Moyen"), ("difficile", "Difficile")],
        verbose_name="Difficulté",
    )

    # Ingrédients en blocs : des sous-titres et des listes d'ingrédients
    ingredients = StreamField(
        [
            ("sous_titre", blocks.CharBlock(label="Sous-titre (ex : Pour la ganache)")),
            ("liste", blocks.ListBlock(blocks.CharBlock(label="Ingrédient"), label="Liste d'ingrédients")),
        ],
        blank=True,
    )

    # Préparation en blocs : une étape = un bloc (numérotées automatiquement sur le site)
    preparation = StreamField(
        [
            ("etape", blocks.RichTextBlock(features=["bold", "italic", "link"], label="Étape")),
        ],
        blank=True,
    )

    # Les champs visibles dans l'admin
    content_panels = Page.content_panels + [
        FieldPanel("photo"),
        FieldPanel("introduction"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("temps_preparation"),
                        FieldPanel("portions"),
                        FieldPanel("difficulte"),
                    ]
                ),
            ],
            heading="Informations pratiques",
        ),
        FieldPanel("ingredients"),
        FieldPanel("preparation"),
    ]

    # Une recette ne peut être créée que sous « Nos recettes »
    parent_page_types = ["pages.RecettesIndexPage"]

class ContactFormField(AbstractFormField):
    # Chaque champ du formulaire est rattaché à la page Contact
    page = ParentalKey(
        "ContactPage",
        on_delete=models.CASCADE, 
        related_name="form_fields")


class ContactPage(AbstractEmailForm):
    intro = RichTextField(blank=True, verbose_name="Texte d'introduction")
    texte_rgpd = RichTextField(blank=True, verbose_name="Texte RGPD")
    message_remerciement = RichTextField(blank=True, verbose_name="Message de remerciement")

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Champs du formulaire"),
        FieldPanel("texte_rgpd"),
        FieldPanel("message_remerciement"),
        MultiFieldPanel(
            [
                FieldRowPanel([FieldPanel("from_address"), FieldPanel("to_address")]),
                FieldPanel("subject"),
            ],
            heading="Envoi de l'e-mail",
        ),
    ]

@register_setting(icon="mail")  # apparaît dans l'admin : Paramètres > Coordonnées
class CoordonneesSettings(BaseSiteSetting):
    adresse = models.CharField(max_length=255, blank=True)
    telephone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Format international sans espaces : +33600000000",
    )
    email = models.EmailField(blank=True)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)

    panels = [
        MultiFieldPanel(
            [FieldPanel("adresse"), FieldPanel("telephone"), FieldPanel("email")],
            heading="Coordonnées",
        ),
        MultiFieldPanel(
            [FieldPanel("instagram"), FieldPanel("facebook")],
            heading="Réseaux sociaux",
        ),
    ]

    class Meta:
        verbose_name = "Coordonnées"