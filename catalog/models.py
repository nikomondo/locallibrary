from django.db import models
from django.urls import reverse
import uuid  # Required for unique book instances


class Genre(models.Model):
    """Model representing a book genre."""

    name = models.CharField(
        max_length=200,
        help_text="Saisir le genre de livre (e.g. Science Fiction, Poesie etc.)",
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""

    name = models.CharField(
        max_length=200,
        help_text="Saisir la langue du livre (e.g. English, French, Japanese etc.)",
    )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name    

class Book(models.Model):
    """Cet objet représente un livre (mais ne traite pas les copies présentes en rayon)."""

    title = models.CharField(max_length=200)

    # La clé étrangère (ForeignKey) est utilisée car elle représente correcte le modèle de relation en livre et son auteur :
    #  Un livre a un seul auteur, mais un auteur a écrit plusieurs livres.
    # Le type de l'objet Author est déclré comme une chaîne de caractère car
    # la classe d'objet Author n'a pas encore été déclarée dans le fichier
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)

    summary = models.TextField(
        max_length=1000, help_text="Saisir une breve description du livre"
    )
    isbn = models.CharField(
        "ISBN",
        max_length=13,
        help_text='13 Caractères a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>',
    )

    # Le type ManyToManyField décrit correctement le modèle de relation en un livre et un genre.
    #  un livre peut avoir plusieurs genres littéraire et réciproquement.
    # Comme la classe d'objets Genre a été définit précédemment, nous pouvons manipuler l'objet.
    genre = models.ManyToManyField(Genre, help_text="Selectionner le genre de ce livre")

    language = models.ForeignKey(
        "Language", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        """Fonction requise par Django pour manipuler les objets Book dans la base de données."""
        return self.title

    def get_absolute_url(self):
        """Cette fonction est requise pas Django, lorsque vous souhaitez détailler le contenu d'un objet."""
        return reverse("book-detail", args=[str(self.id)])


class BookInstance(models.Model):
    """Cet objet représente une copie spécifique d'un livre (i.e. que l'on peut emprunter dans une bibliothèque)."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="ID unique pour ce livre particulier dans toute la bibliothèque",
    )
    book = models.ForeignKey("Book", on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("o", "Emprunté"),
        ("a", "Disponible"),
        ("r", "Réservé"),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default="m",
        help_text="Disponibilité du livre",
    )

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        """Fonction requise par Django pour manipuler les objets BookInstance dans la base de données."""
        return f"{self.id} ({self.book.title})"

class Author(models.Model):
    """Model representing an author."""

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    date_of_birth = models.DateField(null=True, blank=True)

    date_of_death = models.DateField("died", null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.last_name}, {self.first_name}"