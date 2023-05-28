from django.db import models
from django.contrib.auth import get_user_model
from cryptography.fernet import Fernet
from django.contrib.auth.hashers import make_password, check_password
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.utils.crypto import get_random_string
from django_cryptography.fields import encrypt
import base64

User = get_user_model()



# Create your models here.
class AccountCredential(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    password = encrypt(models.CharField(max_length=255, blank=True))
    encrypted_password = models.BinaryField(blank=True)
    password_salt = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    is_favorite = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def set_password(self, master_pin):
        print("called set password function")

        key = self.derive_encryption_key(master_pin)
        print(f"Set password encryption key: {key}")
        cipher_suite = Fernet(key)
        self.encrypted_password = cipher_suite.encrypt(self.password.encode('utf-8'))
        print(f"Encrypted password: {self.encrypted_password}")
        print("password encrypted...")

    def get_password(self):
        print("called get password")
        # decrypt and return the password using the user's master pin
        
        encryption_key = EncryptionKey.objects.get(credential=self)
        key = encryption_key.key
        print("got encryption key...")
        cipher_suite = Fernet(key)
        decrypted_password = cipher_suite.decrypt(self.encrypted_password)
        return decrypted_password.decode('utf-8')

    def derive_encryption_key(self, master_pin):
        salt_string = get_random_string(16)
        self.password_salt = salt_string.encode('utf-8')
        print("deriving encryption key...")
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.password_salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_pin.encode('utf-8')))
        print(f"derive encryption key: {key}")

        self.save()

        EncryptionKey.objects.filter(credential=self).delete()

        EncryptionKey.objects.create(
            credential=self,
            key=key
        )
        return key
    

class EncryptionKey(models.Model):
    credential = models.OneToOneField(AccountCredential, on_delete=models.CASCADE)
    key = encrypt(models.BinaryField())