from models.auth_model import Auth
from tkinter import messagebox

class LoginController:
    def __init__(self, view):
        self.view = view
        self.login_model = Auth()  # Instancia del modelo de autenticación
        self.view.set_controller(self)  # Asignar el controlador a la vista

    def procesar_login(self):
        password_input = self.view.txt_password.get()  # Obtener la contraseña ingresada

        if not password_input:
            messagebox.showwarning("Advertencia", "Por favor, ingrese su contraseña.")
            return

        # Validar credenciales con el modelo
        if self.login_model.validate_password(password_input):
            messagebox.showinfo("Acceso Exitoso", "¡Bienvenido al sistema Sabor & Sazón!")
            
            self.view.destroy() #cerrar la ventana de Login actual
            
            #app_registro = RegistroClienteView()
            #controller_registro = GestionController(app_registro)  # Asocia el controlador a la vista
            #app_registro.mainloop()
        else:
            messagebox.showerror("Acceso Denegado", "Contraseña incorrecta. Intente nuevamente.")
            self.view.txt_password.delete(0, 'end')  # Limpiar el campo de contraseña
