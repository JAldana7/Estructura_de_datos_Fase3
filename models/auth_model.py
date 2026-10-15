#clase usser como constructor con atributos y metodos para validar que los datos ingresados sean correctos
class Auth:
    #atributos privados de la clase usser
    def __init__(self, password: str = "Caja"):
        self._password = password

    @property
    def password(self) -> str:
        return self._password

    #funcion para validar la clave ingresada
    def validate_password(self, password: str) -> bool:
        return password == self._password