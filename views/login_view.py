#importacion importantes
import sys, os
import tkinter as tk
import ctypes
from tkinter import ttk, messagebox
from utils.helpers import centrar_ventana
from controllers.login_controller import LoginController
from PIL import Image, ImageTk

# Permitir ejecuciones directas resolviendo la ruta raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#clase de la vista de inicio de sesion
class LoginView(tk.Tk):
    #constructor
    def __init__(self, controller=None):
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1) # Mejorar la resolución
        except:
            pass
        super().__init__() #hereda comportamients

        self.controller = controller # Asigna el controlador

        # Configuración de la ventana principal y 
        self.title("Login - Compensándote")

        # Obtener la carpeta principal del proyecto
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_icono = os.path.join(BASE_DIR, "img", "ico.png")
        #self.icono = tk.PhotoImage(file=ruta_icono)
        #self.iconphoto(False, self.icono)

        # Configuración de tamaño y posición
        self.ancho = 600
        self.alto = 580
        centrar_ventana(self, self.ancho, self.alto)
        self.configure(bg="#F4F6F8")
        self.resizable(False, False)

        self._password_visible = False # Estado para mostrar/ocultar contraseña
        self._configurar_estilos() # Configuración de estilos visuales
        self._crear_interfaz() # Construir la interfaz
        self._crear_menu() # Crear el menú de la ventana

    # funcion para asignar el controlador a la vista
    def set_controller(self, controller):
        self.controller = controller # Asigna el controlador a la vista
        
        # Conectar el botón de ingresar con la función procesar_login del controlador
        self.btn_ingresar.config(command=self.controller.procesar_login)
        # Conectar la tecla Enter en la caja de texto
        self.txt_password.bind("<Return>", lambda event: self.controller.procesar_login())

    #funcion para configurar los estilos de la interfaz
    def _configurar_estilos(self):
        self.style = ttk.Style(self) 
        self.style.theme_use('clam')

        # Colores personalizados
        self.COLOR_AZUL = "#00B4D8"
        self.COLOR_FONDO = "#F4F6F8"

        # Configuración de estilos para los widgets
        self.style.configure(".", background=self.COLOR_FONDO)
        self.style.configure("Card.TFrame", background="#FFFFFF")
        self.style.configure("Header.TFrame", background=self.COLOR_AZUL)

        # Estilo para el botón principal de ingreso
        self.style.configure("Login.TButton", 
                             font=("Segoe UI", 10, "bold"), 
                             background=self.COLOR_AZUL
                             , 
                             foreground="#FFFFFF")
        self.style.map("Login.TButton", background=[("active", "#0B3B2D")])

    #funcion para crear la interfaz de usuario
    def _crear_interfaz(self):
        # banner superior
        header_frame = ttk.Frame(self, style="Header.TFrame", padding=(25, 20))
        header_frame.pack(fill="x", side="top")
        left_header = tk.Frame(header_frame, bg=self.COLOR_AZUL)
        left_header.pack(side="left")

        # Logo y subtitulo
        lbl_logo = tk.Label(
            left_header, 
            text="🏢 Compensating you", 
            font=("Segoe UI", 16, "bold"), 
            bg=self.COLOR_AZUL, 
            fg="#FFFFFF"
        )
        lbl_logo.pack(anchor="w")

        lbl_subtitulo_header = tk.Label(
            left_header, 
            text="Customer Management System", 
            font=("Segoe UI", 10, "italic"), 
            bg=self.COLOR_AZUL, 
            fg="#FFFFFF"
        )
        lbl_subtitulo_header.pack(anchor="w", pady=(2, 0))

        # Slogan
        lbl_slogan = tk.Label(
            header_frame, 
            text="Family Compensation,\nAffiliation Control", 
            font=("Segoe UI", 9, "italic"), 
            bg=self.COLOR_AZUL, 
            fg="#FFFFFF",
            justify="right"
        )
        lbl_slogan.pack(side="right")

        # contenedor principal (card)
        card_frame = ttk.Frame(self, style="Card.TFrame", padding=25)
        card_frame.pack(fill="both", expand=True, padx=35, pady=25)

        # Datos del Autor
        author_frame = tk.Frame(card_frame, bg="#FFFFFF")
        author_frame.pack(fill="x", pady=(0, 15))

        lbl_avatar = tk.Label(author_frame, text="👤", font=("Segoe UI", 28), bg="#D1E7DD", fg=self.COLOR_AZUL, width=2, height=1)
        lbl_avatar.pack(side="left", padx=(0, 15))

        author_info = tk.Frame(author_frame, bg="#FFFFFF")
        author_info.pack(side="left")

        lbl_nombre_autor = tk.Label(
            author_info, 
            text="Johan David Aldana Castillo", 
            font=("Segoe UI", 12, "bold"), 
            bg="#FFFFFF", 
            fg="#0F172A"
        )
        lbl_nombre_autor.pack(anchor="w")

        lbl_carrera_autor = tk.Label(
            author_info, 
            text="System Engineering — UNAD", 
            font=("Segoe UI", 10), 
            bg="#FFFFFF", 
            fg="#64748B"
        )
        lbl_carrera_autor.pack(anchor="w")

        ttk.Separator(card_frame, orient="horizontal").pack(fill="x", pady=10)

        # Indicaciones
        lbl_indicacion_titulo = tk.Label(
            card_frame, 
            text="🛡️   Enter the password to continue.", 
            font=("Segoe UI", 11, "bold"), 
            bg="#FFFFFF", 
            fg="#0F172A"
        )
        lbl_indicacion_titulo.pack(anchor="w", pady=(5, 2))

        lbl_indicacion_sub = tk.Label(
            card_frame, 
            text="The password is masked (***).", 
            font=("Segoe UI", 9), 
            bg="#FFFFFF", 
            fg="#64748B"
        )
        lbl_indicacion_sub.pack(anchor="w", pady=(0, 15))

        # Campo de Contraseña
        input_container = tk.Frame(card_frame, bg="#F8FAFC", highlightbackground="#CBD5E1", highlightthickness=1)
        input_container.pack(fill="x", pady=(0, 20))

        lbl_lock = tk.Label(input_container, text="🔒", font=("Segoe UI", 12), bg="#F8FAFC")
        lbl_lock.pack(side="left", padx=10)

        self.txt_password = tk.Entry(
            input_container, 
            font=("Segoe UI", 11), 
            show="*", 
            bg="#F8FAFC", 
            bd=0, 
            relief="flat"
        )
        self.txt_password.pack(side="left", fill="x", expand=True, pady=8)

        self.btn_toggle_eye = tk.Button(
            input_container, 
            text="👁️", 
            font=("Segoe UI", 10), 
            bg="#F8FAFC", 
            bd=0, 
            cursor="hand2",
            command=self._toggle_password_visibility
        )
        self.btn_toggle_eye.pack(side="right", padx=10)

        # Botón Ingresar
        self.btn_ingresar = ttk.Button(
            card_frame, 
            text="➔   Enter the system   ➔", 
            style="Login.TButton"
        )
        self.btn_ingresar.pack(fill="x", ipady=8, pady=(5, 0))

        # Footer
        footer_frame = tk.Frame(self, bg=self.COLOR_FONDO)
        footer_frame.pack(side="bottom", fill="x", pady=(0, 15))

        lbl_footer = tk.Label(
            footer_frame, 
            text="🛡️   Data Structure  ·  Code: 301305  ·  ECBTI", 
            font=("Segoe UI", 8), 
            bg=self.COLOR_FONDO, 
            fg="#64748B"
        )
        lbl_footer.pack()

    def _crear_menu(self):
        self.menu_principal = tk.Menu(self)

        menu_help = tk.Menu(
            self.menu_principal,
            tearoff=0
        )

        menu_help.add_command(
            label="About",
            command=lambda: self.controller.mostrar_about()
        )

        self.menu_principal.add_cascade(
            label="Help",
            menu=menu_help
        )

        self.config(menu=self.menu_principal)

    #funcion para alternar la visibilidad de la contraseña
    def _toggle_password_visibility(self):
        #Alterna entre ocultar y mostrar el texto de la contraseña.
        if self._password_visible:
            self.txt_password.config(show="*")
            self._password_visible = False
        else:
            self.txt_password.config(show="")
            self._password_visible = True
