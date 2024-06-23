from django.db import models
import uuid
# Create your models here.

class Genre(models.Model):
    title = models.CharField(max_length= 60, help_text= 'Enter a book genre(e.g. Science Fiction, French Poetry etc.)')

    def __str__(self) -> str:
        return self.title
    

class Language(models.Model):
    title = models.CharField(max_length= 60, help_text= 'Enter a book languege(English, Farsi etc.)')

    def __str__(self) -> str:
        return self.title
    
 
class Book(models.Model):
    title = models.CharField(max_length= 200)
    summary = models.TextField(max_length= 1000, help_text= 'Enter a brief description of the book')
    isbn = models.CharField(max_length= 13, help_text= '13 Character <a href="https://www.isbn-international.org/content/what-isbn/10">ISBN number</a>')
    
    # ManyToManyField used because a Genre can contain Many books AND a book can cover Many genres.
    # Genre class has alreay been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text= 'select a text for this book')
    
    # ForeignKey used becaus a Book can only have one author BUT an Author can have Many books.
    # Author class hasn't been defined yet so we use it as a string rather than an object.
    author = models.ForeignKey('Author', on_delete= models.SET_NULL, null= True)

    language = models.ForeignKey(Language, on_delete= models.SET_NULL, null= True)
    

    def __str__(self) -> str:
        return self.title
    

class Author(models.Model):
    first_name = models.CharField(max_length= 100)
    last_name = models.CharField(max_length= 100)
    date_of_birth = models.DateField(null=True, blank= True)
    date_of_death = models.DateField('Died',null=True, blank= True)

    class Meta:
        ordering = ['last_name','first_name']

    def __str__(self) -> str:
        return f'{self.first_name}, {self.last_name}'
    

class BookInstance(models.Model):
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, 
                          help_text= 'Unique ID for this particular book across whole library')
    book = models.ForeignKey(Book, on_delete= models.SET_NULL, null= True)
    imprint = models.CharField(max_length= 200)
    due_back = models.DateField(null= True, blank= True)

    LOAN_STATUS = (
        ('m','Maintenance'),
        ('o','On Loan'),
        ('a','Available'),
        ('r','Reserved'),
    )

    status = models.CharField(max_length= 1, choices= LOAN_STATUS, blank= True, default= 'm',
                              help_text= 'Book availability')
    

    class Meta:
        ordering = ['due_back']

    def __str__(self) -> str:
        return f'{self.id} ({self.book.title})'