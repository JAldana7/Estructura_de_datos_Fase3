# importaciones necesarias
import tkinter as tk
from tkinter import ttk
import ctypes
from typing import Callable, Dict, List
from utils.helpers import centrar_ventana
from models.enums import IDType, EmploymentType, DesiredService, StructureType

# clase principal de la vista
class MainView(tk.Frame):
    def __init__(self, parent: tk.Tk):
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1) # Mejorar la resolución
        except:
            pass
        super().__init__(parent) # hereda comportamientos
        self.parent = parent # referencia a la ventana principal
        self.parent.title("Compensándote — Affiliation Control") 
        centrar_ventana(self.parent, 1150, 700) # Configuración de tamaño y posición
        self.parent.resizable(True, True)

        self.callbacks: Dict[str, Callable] = {} # diccionario para almacenar las funciones de callback

        # UI Variables
        self.var_id_type = tk.StringVar(value=IDType.CC.value)
        self.var_id_number = tk.StringVar()
        self.var_full_name = tk.StringVar()
        self.var_current_income = tk.StringVar()
        self.var_employment_type = tk.StringVar(value=EmploymentType.EMPLOYEE.value)
        self.var_desired_service = tk.StringVar(value=DesiredService.UNEMPLOYMENT_SUBSIDY.value)
        self.var_affiliation_fee = tk.StringVar(value="$0.00")
        
        # seleccion de la fecha de afiliacion
        self.var_day = tk.StringVar(value="-")
        self.var_month = tk.StringVar(value="-")
        self.var_year = tk.StringVar(value="2026")

        # seleccion de la estructura de datos
        self.var_selected_structure = tk.StringVar(value=StructureType.STACK.value)
        self.var_report_text = tk.StringVar(value="Total Affiliation Fees Sum: $0.00") # texto de afiliacion

        # Configuración de estilos y construcción de la interfaz
        self._configure_modern_palette()
        self._create_menu_bar()
        self.pack(fill=tk.BOTH, expand=True)
        self._build_ui()

    # funcion para configurar la paleta de colores moderna
    def _configure_modern_palette(self) -> None:
        # Colores de la paleta moderna
        self.bg_window = "#F1F5F9"        
        self.bg_card = "#FFFFFF"          
        self.border_gray = "#CBD5E1"      
        self.fg_dark = "#1E293B"          
        self.fg_label = "#334155"         
        
        # colores de acento
        self.cyan_header = "#00B4D8"      
        self.cyan_accent = "#00B4D8"      
        self.bg_fee_box = "#E0F2FE"      
        
        # paleta de colores para botones
        self.btn_register = "#00B4D8"     
        self.btn_clear = "#78869B"        
        self.btn_report = "#00B67A"      
        self.btn_delete = "#F97316"      
        self.btn_exit = "#EF4444"         

        # Configuración de la ventana principal
        self.parent.configure(bg=self.bg_window)
        self.configure(bg=self.bg_window)

        # estilos para los widgets de la interfaz
        style = ttk.Style()
        style.theme_use("clam")

        # estilo para la tabla (Treeview)
        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#1E293B",
            fieldbackground="#FFFFFF",
            rowheight=28,
            bordercolor="#E2E8F0",
            font=("Segoe UI", 9)
        )
        style.configure(
            "Treeview.Heading",
            background="#E0F2FE",
            foreground="#0284C7",
            relief="flat",
            font=("Segoe UI", 9, "bold")
        )
        style.map("Treeview", background=[("selected", "#BAE6FD")], foreground=[("selected", "#0369A1")])

    # funcion para crear la barra de menu
    def _create_menu_bar(self) -> None:
        menubar = tk.Menu(self.parent)
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="About...", command=lambda: self._trigger_callback("on_about"))
        menubar.add_cascade(label="About", menu=about_menu)
        self.parent.config(menu=menubar)

    # funcion para construir la interfaz de usuario
    def _build_ui(self) -> None:
        # banner superior con fondo cian y texto blanco
        header_banner = tk.Frame(self, bg=self.cyan_header, height=50)
        header_banner.pack(fill=tk.X, side=tk.TOP)

        title_container = tk.Frame(header_banner, bg=self.cyan_header)
        title_container.pack(side=tk.LEFT, padx=15, pady=10)

        # Etiqueta de título con el nombre de la aplicación
        tk.Label(
            title_container,
            text="🏢  Compensándote — Affiliation Control",
            font=("Segoe UI", 15, "bold"),
            fg="white",
            bg=self.cyan_header
        ).pack(side=tk.LEFT)

        # Etiqueta de pie de página con derechos reservados
        body_container = tk.Frame(self, bg=self.bg_window)
        body_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        self._build_left_form_card(body_container)
        self._build_right_grid_card(body_container)

    # funcion para construir la tarjeta de formulario en la columna izquierda
    def _build_left_form_card(self, parent: tk.Widget) -> None:
        # Contenedor de la tarjeta de formulario
        form_wrapper = tk.Frame(parent, bg=self.bg_card, bd=1, relief=tk.SOLID)
        form_wrapper.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15), ipadx=0, ipady=0)

        # encabezado del formulario
        header_frame = tk.Frame(form_wrapper, bg=self.btn_register, height=40)
        header_frame.pack(fill=tk.X)

        tk.Label(
            header_frame,
            text="👥   Member Registration Data",
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg=self.btn_register
        ).pack(side=tk.LEFT, padx=12, pady=8)

        # Form Content Area
        form_body = tk.Frame(form_wrapper, bg=self.bg_card, padx=12, pady=10)
        form_body.pack(fill=tk.BOTH, expand=True)

        # ID Type
        tk.Label(form_body, text="ID Type:", fg=self.fg_label, bg=self.bg_card, anchor="w", font=("Segoe UI", 9)).pack(fill=tk.X, pady=(2, 2))
        cb_id_type = ttk.Combobox(form_body, textvariable=self.var_id_type, values=[e.value for e in IDType], state="readonly")
        cb_id_type.pack(fill=tk.X, pady=(0, 8))

        # ID Number
        tk.Label(form_body, text="ID Number (digits only):", fg=self.fg_label, bg=self.bg_card, anchor="w", font=("Segoe UI", 9)).pack(fill=tk.X, pady=(2, 2))
        entry_id = tk.Entry(form_body, textvariable=self.var_id_number, bg="#FFFFFF", fg=self.fg_dark, bd=1, relief=tk.SOLID)
        entry_id.pack(fill=tk.X, pady=(0, 8))

        # Full Name
        tk.Label(form_body, text="Full Name (letters only):", fg=self.fg_label, bg=self.bg_card, anchor="w", font=("Segoe UI", 9)).pack(fill=tk.X, pady=(2, 2))
        entry_name = tk.Entry(form_body, textvariable=self.var_full_name, bg="#FFFFFF", fg=self.fg_dark, bd=1, relief=tk.SOLID)
        entry_name.pack(fill=tk.X, pady=(0, 8))

        # Current Income
        tk.Label(form_body, text="Current Monthly Income ($):", fg=self.fg_label, bg=self.bg_card, anchor="w", font=("Segoe UI", 9)).pack(fill=tk.X, pady=(2, 2))
        entry_income = tk.Entry(form_body, textvariable=self.var_current_income, bg="#FFFFFF", fg=self.fg_dark, bd=1, relief=tk.SOLID)
        entry_income.pack(fill=tk.X, pady=(0, 8))
        entry_income.bind("<KeyRelease>", lambda e: self._trigger_callback("on_recalculate_fee"))

        # Employment Type (Radio Buttons)
        tk.Label(form_body, text="Employment Type:", fg=self.fg_label, bg=self.bg_card, anchor="w", font=("Segoe UI", 9, "bold")).pack(fill=tk.X, pady=(2, 2))
        emp_frame = tk.Frame(form_body, bg=self.bg_card)
        emp_frame.pack(fill=tk.X, pady=(0, 8))
        for emp in EmploymentType:
            rb = tk.Radiobutton(
                emp_frame, text=emp.value, value=emp.value, variable=self.var_employment_type,
                fg=self.fg_dark, bg=self.bg_card, activebackground=self.bg_card,
                command=lambda: self._trigger_callback("on_recalculate_fee")
            )
            rb.pack(side=tk.LEFT, padx=(0, 10))

        # servicio deseado (combobox)
        tk.Label(form_body, text="Desired Service:", fg=self.fg_label, bg=self.bg_card, anchor="w", font=("Segoe UI", 9)).pack(fill=tk.X, pady=(2, 2))
        cb_service = ttk.Combobox(form_body, textvariable=self.var_desired_service, values=[s.value for s in DesiredService], state="readonly")
        cb_service.pack(fill=tk.X, pady=(0, 8))
        cb_service.bind("<<ComboboxSelected>>", lambda e: self._trigger_callback("on_recalculate_fee"))

        # Calculated Fee (Read-only Blue Highlight)
        tk.Label(form_body, text="Calculated Affiliation Fee:", fg=self.fg_label, bg=self.bg_card, anchor="w", font=("Segoe UI", 9)).pack(fill=tk.X, pady=(2, 2))
        entry_fee = tk.Entry(
            form_body, textvariable=self.var_affiliation_fee, state="readonly", 
            bg=self.bg_fee_box, fg=self.cyan_accent, font=("Segoe UI", 10, "bold"), 
            bd=1, relief=tk.SOLID
        )
        entry_fee.pack(fill=tk.X, pady=(0, 8))

        # Affiliation Date
        tk.Label(form_body, text="Affiliation Date (dd/mm/yyyy):", fg=self.fg_label, bg=self.bg_card, anchor="w", font=("Segoe UI", 9)).pack(fill=tk.X, pady=(2, 2))
        date_frame = tk.Frame(form_body, bg=self.bg_card)
        date_frame.pack(fill=tk.X, pady=(0, 4))
        # Comboboxes for Day, Month, Year
        ttk.Combobox(date_frame, textvariable=self.var_day, values=[str(i) for i in range(1, 32)], width=3, state="readonly").pack(side=tk.LEFT, padx=1)
        tk.Label(date_frame, text="/", fg=self.fg_dark, bg=self.bg_card).pack(side=tk.LEFT)
        ttk.Combobox(date_frame, textvariable=self.var_month, values=[str(i) for i in range(1, 13)], width=3, state="readonly").pack(side=tk.LEFT, padx=1)
        tk.Label(date_frame, text="/", fg=self.fg_dark, bg=self.bg_card).pack(side=tk.LEFT)
        ttk.Combobox(date_frame, textvariable=self.var_year, values=[str(i) for i in range(2020, 2031)], width=5, state="readonly").pack(side=tk.LEFT, padx=1)

    # funcion para construir la tarjeta de tabla en la columna derecha
    def _build_right_grid_card(self, parent: tk.Widget) -> None:
        display_frame = tk.Frame(parent, bg=self.bg_window)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Structure Selector Toolbar
        toolbar = tk.Frame(display_frame, bg=self.bg_window)
        toolbar.pack(fill=tk.X, pady=(0, 10))

        tk.Label(toolbar, text="View Data Structure:", fg=self.fg_dark, bg=self.bg_window, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        cb_structure = ttk.Combobox(toolbar, textvariable=self.var_selected_structure, values=[s.value for s in StructureType], state="readonly", width=18)
        cb_structure.pack(side=tk.LEFT)
        cb_structure.bind("<<ComboboxSelected>>", lambda e: self._trigger_callback("on_structure_changed"))

        # Treeview Container
        tree_frame = tk.Frame(display_frame, bg=self.bg_card, bd=1, relief=tk.SOLID)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12))

        columns = ("id_type", "id_number", "full_name", "income", "employment", "service", "fee", "date")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")

        # Configuración de encabezados y columnas
        self.tree.heading("id_type", text="Type")
        self.tree.heading("id_number", text="ID Number")
        self.tree.heading("full_name", text="Full Name")
        self.tree.heading("income", text="Income")
        self.tree.heading("employment", text="Employment")
        self.tree.heading("service", text="Service")
        self.tree.heading("fee", text="Fee")
        self.tree.heading("date", text="Date")

        # Configuración de ancho y alineación de columnas
        self.tree.column("id_type", width=55, anchor="center")
        self.tree.column("id_number", width=95, anchor="center")
        self.tree.column("full_name", width=140, anchor="w")
        self.tree.column("income", width=85, anchor="e")
        self.tree.column("employment", width=95, anchor="center")
        self.tree.column("service", width=130, anchor="w")
        self.tree.column("fee", width=85, anchor="e")
        self.tree.column("date", width=80, anchor="center")
        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        # Pack the Treeview and Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Report Row Bar
        report_frame = tk.Frame(display_frame, bg=self.bg_window)
        report_frame.pack(fill=tk.X, pady=(0, 12))

        # Etiqueta y entrada de texto para mostrar el reporte
        tk.Label(report_frame, text="Report:", fg=self.fg_dark, bg=self.bg_window, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        entry_report = tk.Entry(
            report_frame, textvariable=self.var_report_text, state="readonly", 
            bg=self.bg_fee_box, fg=self.cyan_accent, font=("Segoe UI", 10, "bold"), 
            bd=1, relief=tk.SOLID
        )
        entry_report.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Action Pill Buttons Panel
        btn_frame = tk.Frame(display_frame, bg=self.bg_window)
        btn_frame.pack(fill=tk.X)

        # conjunto de botones con iconos y texto para realizar acciones
        tk.Button(btn_frame, text="👤+ Register", bg=self.btn_register, fg="white", font=("Segoe UI", 9, "bold"), bd=0, relief=tk.FLAT, command=lambda: self._trigger_callback("on_register")).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3, ipady=5)
        tk.Button(btn_frame, text="✏️ Clear", bg=self.btn_clear, fg="white", font=("Segoe UI", 9, "bold"), bd=0, relief=tk.FLAT, command=lambda: self._trigger_callback("on_clear")).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3, ipady=5)
        tk.Button(btn_frame, text="📑 Report", bg=self.btn_report, fg="white", font=("Segoe UI", 9, "bold"), bd=0, relief=tk.FLAT, command=lambda: self._trigger_callback("on_report")).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3, ipady=5)
        tk.Button(btn_frame, text="🗑️ Delete", bg=self.btn_delete, fg="white", font=("Segoe UI", 9, "bold"), bd=0, relief=tk.FLAT, command=lambda: self._trigger_callback("on_delete")).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3, ipady=5)
        tk.Button(btn_frame, text="🚪 Exit", bg=self.btn_exit, fg="white", font=("Segoe UI", 9, "bold"), bd=0, relief=tk.FLAT, command=lambda: self._trigger_callback("on_exit")).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3, ipady=5)

    # funcion para establecer las funciones de callback del controlador
    def set_controller_callbacks(self, callbacks: Dict[str, Callable]) -> None:
        self.callbacks = callbacks

    # funcion para disparar la función de callback correspondiente a una acción
    def _trigger_callback(self, key: str) -> None:
        if key in self.callbacks:
            self.callbacks[key]()

    # funcion para actualizar los datos en la tabla (Treeview)
    def update_treeview(self, data: List[tuple]) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in data:
            self.tree.insert("", tk.END, values=row)

    # funcion para actualizar el texto del reporte
    def clear_inputs(self) -> None:
        self.var_id_number.set("")
        self.var_full_name.set("")
        self.var_current_income.set("")
        self.var_affiliation_fee.set("$0.00")
        self.var_id_type.set(IDType.CC.value)
        self.var_employment_type.set(EmploymentType.EMPLOYEE.value)
        self.var_desired_service.set(DesiredService.UNEMPLOYMENT_SUBSIDY.value)