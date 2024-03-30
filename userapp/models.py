from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager, AbstractUser # new

from autoslug import AutoSlugField


# Create your models here.

_validate_phone = RegexValidator(
    regex=r"^[\+]?[9]{2}[8]?[0-9]{2}?[0-9]{3}?[0-9]{2}?[0-9]{2}$",
    message="Telefon raqamingiz 9 bilan boshlanishi va 12 belgidan oshmasligi lozim. Masalan: 998334568978",
)

DAYS = (
    ("toq","Du-Chor-Ju"),
    ("juft","Se-Pay-Shan"),
    ("boot","Bootcamp"),
)

TIME = (
    ('8',"8:00-11:00"),
    ('12',"12:00-14:00"),
    ('14',"14:00-17:00"),
)

class Field(models.Model):
    """ Field modeli - o'quv markazdagi yo'nalish(kurs)larni aniqlsh uchun yaratilgan. M: Backend, Frontend, 3D, ..."""
    name  = models.CharField(max_length=100, unique=True, verbose_name="Nomi")
    slug  = AutoSlugField(populate_from="name", unique=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=100000, blank=True, null=True, verbose_name="Narxi")
    duration = models.PositiveIntegerField(default=6, verbose_name="Kurs davomiyligi")

    status = models.BooleanField(default=True, verbose_name="Holati")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"
        ordering = ('-created_at',)

    def __str__(self):
        return self.name

class Role(models.Model):
    """ Role - xodimlarning vazifasini yaratuvchi model """
    name = models.CharField(max_length=50, verbose_name="Vazifasi nomi")
    slug  = AutoSlugField(populate_from="name", unique=True)

    status = models.BooleanField(default=True, verbose_name="Holati")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class WorkerManager(BaseUserManager):
    def create_user(self, username, password=None, password2=None, **extra_fields):
        if not username:
            raise ValueError('The username must be set')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('full_name', "Super Admin")

        if Role.objects.first():
            extra_fields.setdefault('role', Role.objects.first())
        else:
            Role.objects.create(
                name='Super admin',
                )
            extra_fields.setdefault('role', Role.objects.first())
            
        if Field.objects.first():
            extra_fields.setdefault('diriction', Field.objects.first())
        else:
            Field.objects.create(
                name = "None",
                cost = 100,
                duration = 10
            )
            extra_fields.setdefault('diriction', Field.objects.first())

        return self.create_user(username, password, **extra_fields)

class Worker(AbstractUser):
    """ Worker - xodimlar uchun model """
    full_name = models.CharField(max_length=100, verbose_name="Ism familya")
    slug  = AutoSlugField(populate_from="full_name", unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name="Vazifasi", related_name="workers", null=True, blank=True)
    diriction = models.ForeignKey(Field, on_delete=models.CASCADE, verbose_name="O'qtuvchining yo'nalishi", related_name="workers", null=True, blank=True)
    phone_number = models.CharField(max_length=12, validators=[_validate_phone], verbose_name="tel. raqam")
    passport = models.CharField(max_length=15, verbose_name="Passport")
    # percentage - ishchining maoshi foizga nisbatan hisoblansa
    percentage = models.PositiveIntegerField(default=10, verbose_name="Ishchining foizi", blank=True, null=True)
    # salary - xodimning maoshining summasi 
    salary = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Maoshi", blank=True, null=True)

    objects = WorkerManager() # new
    status = models.BooleanField(default=True, verbose_name="Holati")
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username" # login uchun talab qilinadigan asosiy maydon
    REQUIRED_FIELDS = [] # login uchun ta'lab qilinadigan qo'shimcha maydonlar
    
    email = models.EmailField(blank=True, null=True) 
    # Ota classimizdan bizga kerak bo'lmaydigan maydonlarga
    first_name = None # None qiymat berish orqali ularni "o'chirib" qo'yamiz
    last_name = None # new

    class Meta:
        verbose_name = "Xodim"
        verbose_name_plural = "Xodimlar"

    def __str__(self):
        return self.full_name

class Student(models.Model):
    """ O'quvchilar uchun model """
    full_name = models.CharField(max_length=100, verbose_name="Ismi")
    slug  = AutoSlugField(populate_from="full_name", unique=True)
    date_of_birth = models.DateField(verbose_name="Tug'ilgan sanasi")
    passport = models.CharField(max_length=15, verbose_name="Passport", unique=True)
    phone_number = models.CharField(max_length=12, validators=[_validate_phone], verbose_name="tel. raqam", unique=True)
    father_name = models.CharField(max_length=100, verbose_name="otasining ismi")
    father_phone = models.CharField(max_length=12, validators=[_validate_phone], verbose_name="tel. raqam", unique=True)
    # field - o'qish yo'nalishi 
    field = models.ForeignKey(Field, on_delete=models.CASCADE, verbose_name="Yo'nalishi", related_name="students")
    day = models.CharField(max_length=25, choices=DAYS, default='toq')
    time = models.CharField(max_length=25, choices=TIME, default='8')

    status = models.BooleanField(default=True, verbose_name="Holati")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "O'quvchi"
        verbose_name_plural = "O'quvchilar"

    def __str__(self):
        return self.full_name







