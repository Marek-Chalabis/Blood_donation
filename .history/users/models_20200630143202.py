from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_image/default_profile.jpg', upload_to='profile_image')
    position = models.CharField(max_length=50, choices=(
        ('doctor', 'doctor'), ('resident doctor', 'resident doctor'), ('medical specialist', 'medical specialist'),
        ('habilitated doctor', 'habilitated doctor'), ('professor', 'professor'), ('nurse', 'nurse')))
    branch = models.CharField(max_length=50, default='Warszawa', choices=(
        ('Warszawa', 'Warszawa'), ('Lublin', 'Lublin'), ('Radom', 'Radom'), ('Gdynia', 'Gdynia'), ('Kraków', 'Kraków')))

    def save(self, *args, **kwargs):
        # overwrite save to change size of uploaded image
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 250 or img.width > 250:
            compressed_size = (250, 250)
            img.thumbnail(compressed_size)
            img.save(self.image.path)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - Profile'
