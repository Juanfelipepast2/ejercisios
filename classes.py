import random
import string
import time


class tecnico:
    def __init__(self, id: int, nombre: str, apellido: str, contrasena: str, admin: bool, pO: bool):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.contrasena = contrasena
        self.admin = admin
        self.pO = pO

    def __str__(self):
        return f"{self.id} {self.nombre} {self.apellido} {self.contrasena} {self.admin} {self.pO}"
    
    def iniciarSesion(self, id, contrasena):
        if self.id == id and self.contrasena == contrasena:
            return True
        else:
            return False
    
contrasena = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
print(contrasena)