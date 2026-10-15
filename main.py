"""
Autor: Johan Aldana
Fecha: 24/09/2026
Fuente: Autoria propia
"""
from views.login_view import LoginView
from controllers.login_controller import LoginController

def main():
    app_login = LoginView() # 1. Instanciar la vista de Login
    controller = LoginController(app_login) # 2. Instanciar el controlador y asociarle la vista
    app_login.mainloop() # 3. Iniciar el bucle de la aplicación

if __name__ == "__main__":
    main()