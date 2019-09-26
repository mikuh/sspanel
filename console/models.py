from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import functional, timezone
from sspanel.utils import generate_port_password
from django.db.models import Max
import uuid


class Level(models.Model):
    """
    Service Level the user buy
    """
    name = models.CharField(default='free', max_length=100, help_text="Choose a user level")
    price_per_year = models.DecimalField(verbose_name="ETH Balance", decimal_places=6, max_digits=12, default=0.1, )

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name


class User(AbstractUser):
    username = models.EmailField(verbose_name='Email address', unique=True)
    address = models.CharField(verbose_name='ETH address', unique=True, max_length=100, null=True, blank=True)
    private_key = models.CharField(verbose_name='ETH private key', max_length=100, null=True, blank=True)
    balance = models.DecimalField(verbose_name="ETH Balance", decimal_places=6, max_digits=12, default=0, editable=True,
                                  null=True, blank=True, )
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True)
    level_expire_time = models.DateTimeField(verbose_name="Service expiration time", default=timezone.now)
    inviter_id = models.CharField(unique=True, default=uuid.uuid4, max_length=128,
                                    help_text="User use this code to invite other person")
    port = models.PositiveIntegerField(verbose_name="User's port ", default=1025,
                                       validators=[MaxValueValidator(1024), MinValueValidator(49151)], )
    port_password = models.CharField(verbose_name='Port password', default=generate_port_password, max_length=36)
    batch = models.PositiveIntegerField(verbose_name="User batch", default=0,
                                        validators=[MaxValueValidator(100), MinValueValidator(
                                            0)], )  # prevent too many users, port not enough points

    def display_level(self):
        if self.level:
            return self.level.name
        return 'free'

    display_level.short_description = 'Level'


class Node(models.Model):
    METHOD_CHOICES = (
        ("aes-256-cfb", "aes-256-cfb"),
        ("aes-128-ctr", "aes-128-ctr"),
        ("rc4-md5", "rc4-md5"),
        ("salsa20", "salsa20"),
        ("chacha20", "chacha20"),
        ("none", "none"),
    )
    name = models.CharField(verbose_name='node name', max_length=100, default='')
    ipv4 = models.CharField(verbose_name='vps ipv4', unique=True, max_length=100)
    ipv6 = models.CharField(verbose_name='vps ipv6', unique=True, max_length=100)
    domain = models.CharField(verbose_name='vps domain', unique=True, max_length=100, null=True, blank=True)
    method = models.CharField(verbose_name="encryption", default='aes-256-cfb', max_length=32, choices=METHOD_CHOICES)
    batch = models.PositiveIntegerField(verbose_name="User batch", default=0,
                                        validators=[MaxValueValidator(100), MinValueValidator(0)], )
    username = models.CharField(verbose_name="username", default='root', max_length=36)
    password = models.CharField(verbose_name="password", default='', max_length=128)

    def __str__(self):
        return self.name

    @classmethod
    def get_max_batch(self):
        t = Node.objects.all()
        if t:
            return t.aggregate(Max('batch'))
        return 0
