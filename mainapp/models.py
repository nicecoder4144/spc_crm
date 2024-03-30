from django.db import models
from autoslug import AutoSlugField
from userapp.models import Worker, Student, Field, DAYS, TIME

# Create your models here.

class Branch(models.Model):
    """ Branch - ushbu model Filiallar uchun yaratilgan."""
    name  = models.CharField(max_length=100, unique=True, verbose_name="Nomi")
    slug  = AutoSlugField(populate_from="name", unique=True)
    adress = models.CharField(max_length=250, verbose_name="Manzil")

    status = models.BooleanField(default=True, verbose_name="Holati")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Filial"
        verbose_name_plural = "Filiallar"
        ordering = ('-created_at',)

    def __str__(self):
        return self.name
    

def slugify_two_fields(self):
        """ Ikkita maydonni sludada birlashtirish """
        return "{}-{}".format(self.branch.name, self.number)


class Room(models.Model):
    """ Room - Har bir Filialdagi xonalar uchun madel """
    number = models.PositiveIntegerField(verbose_name="Raqami", default=1)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name="Filial", related_name="rooms")
    # slug  = AutoSlugField(populate_from="number-branch", unique=True)
    slug = AutoSlugField(
        (u'slug'),
        populate_from=slugify_two_fields,
        unique=True
    )
    capacity = models.PositiveIntegerField(default=8, verbose_name="Sig'imi") # o'quvchilar sig'immi

    status = models.BooleanField(default=True, verbose_name="Holati")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Xona"
        verbose_name_plural = "Xonalar"
        ordering = ('-created_at',)

    def __str__(self):
        text = f"{self.number}"
        return text


class Group(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, 
                              related_name='groups', verbose_name="Kurs")
    name = models.CharField(max_length=50, verbose_name="Nomi")
    slug  = AutoSlugField(populate_from="name", unique=True)
    teacher = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='group', verbose_name="O'qtuvchi")
    students = models.ManyToManyField(Student, related_name="students", 
                                      verbose_name="O'quvchilar")
    day = models.CharField(max_length=25, choices=DAYS, default='toq')
    time = models.CharField(max_length=25, choices=TIME, default='8')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='groups', 
                             verbose_name="xona" )
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="groups",
                                verbose_name="Filial")
    
    status = models.BooleanField(default=True, verbose_name="Holati")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhar"
        ordering = ('-created_at',)

    def __str__(self):
        text = f"{self.branch.name} - {self.field.name} - {self.name}"
        return text    


