import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict, Any, List
from models.enums import IDType, EmploymentType, DesiredService, StructureType

class MainView(tk.Frame):
    """
    Main Application Window View for Compensándote Affiliation Control.
    Implements a dark theme layout with a left form panel and a right Treeview panel.
    """

    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.parent = parent
        self.parent.title("Caja Compensándote - Control de Afiliados")
        self.parent.geometry("1100x680")
        self.parent.resizable(True, True)

        # Callbacks container for Controller bindings
        self.callbacks: Dict[str, Callable] = {}

        # UI Control variables
        self.var_id_type = tk.StringVar(value=IDType.CC.value)
        self.var_id_number = tk.StringVar()
        self.var_full_name = tk.StringVar()
        self.var_current_income = tk.StringVar()
        self.var_employment_type = tk.StringVar(value=EmploymentType.EMPLOYEE.value)
        self.var_desired_service = tk.StringVar(value=DesiredService.UNEMPLOYMENT_SUBSIDY.value)
        self.var_affiliation_fee = tk.StringVar(value="$0.00")
        
        # Date variables
        self.var_day = tk.StringVar(value="1")
        self.var_month = tk.StringVar(value="1")
        self.var_year = tk.StringVar(value="2026")

        # Structure selection and report variables
        self.var_selected_structure = tk.StringVar(value=StructureType.STACK.value)
        self.var_report_text = tk.StringVar(value="Select a structure and click Report")

        # Set theme styles and build layout
        self._configure_styles()
        self._create_menu_bar()
        self._build_ui()

    def _configure_styles(self) -> None:
        """Configures custom dark blue styles matching the reference design."""
        self.bg_dark = "#0F172A"       # Main background (slate dark)
        self.bg_card = "#1E293B"       # Panel background
        self.fg_light = "#F8FAFC"      # Primary text color
        self.accent_cyan = "#06B6D4"    # Primary action color
        self.accent_red = "#EF4444"     # Danger / Exit action color
        self.accent_orange = "#F97316"  # Secondary action color

        self.parent.configure(bg=self.bg_dark)
        self.configure(bg=self.bg_dark)

        style = ttk.Style()
        style.theme_use("clam")

        # Treeview styling
        style.configure(
            "Treeview",
            background="#1E293B",
            foreground="#F8FAFC",
            fieldbackground="#1E293B",
            rowheight=25,
            bordercolor="#334155"
        )
        style.configure(
            "Treeview.Heading",
            background="#0F172A",
            foreground="#06B6D4",
            font=("Consolas", 10, "bold")
        )
        style.map("Treeview", background=[("selected", "#0284C7")])

    def _create_menu_bar(self) -> None:
        """Creates top menu bar with 'About' option."""
        menubar = tk.Menu(self.parent)
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(
            label="About...", 
            command=lambda: self._trigger_callback("on_about")
        )
        menubar.add_cascade(label="About", menu=about_menu)
        self.parent.config(menu=menubar)

    def _build_ui(self) -> None:
        """Constructs main 2-column layout."""
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Header Title Banner
        header_frame = tk.Frame(self, bg=self.bg_dark)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        title_label = tk.Label(
            header_frame,
            text="Compensándote — Affiliation Control",
            font=("Segoe UI", 16, "bold"),
            fg=self.accent_cyan,
            bg=self.bg_dark
        )
        title_label.pack(side=tk.LEFT)

        # Main Split Container
        main_container = tk.Frame(self, bg=self.bg_dark)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Left Column: Data Input Form
        self._build_form_panel(main_container)

        # Right Column: Data View & Control Panel
        self._build_display_panel(main_container)

    def _build_form_panel(self, parent: tk.Widget) -> None:
        """Builds left input controls panel."""
        form_frame = tk.LabelFrame(
            parent,
            text=" Member Registration Data ",
            font=("Segoe UI", 11, "bold"),
            fg=self.accent_cyan,
            bg=self.bg_card,
            bd=1,
            relief=tk.SOLID
        )
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), ipadx=10, ipady=10)

        # ID Type
        tk.Label(form_frame, text="ID Type:", fg=self.fg_light, bg=self.bg_card, anchor="w").pack(fill=tk.X, pady=(5, 2))
        cb_id_type = ttk.Combobox(
            form_frame, 
            textvariable=self.var_id_type, 
            values=[e.value for e in IDType], 
            state="readonly"
        )
        cb_id_type.pack(fill=tk.X, pady=(0, 8))

        # ID Number
        tk.Label(form_frame, text="ID Number (digits only):", fg=self.fg_light, bg=self.bg_card, anchor="w").pack(fill=tk.X, pady=(2, 2))
        entry_id = tk.Entry(form_frame, textvariable=self.var_id_number, bg="#334155", fg=self.fg_light, insertbackground="white")
        entry_id.pack(fill=tk.X, pady=(0, 8))

        # Full Name
        tk.Label(form_frame, text="Full Name (letters only):", fg=self.fg_light, bg=self.bg_card, anchor="w").pack(fill=tk.X, pady=(2, 2))
        entry_name = tk.Entry(form_frame, textvariable=self.var_full_name, bg="#334155", fg=self.fg_light, insertbackground="white")
        entry_name.pack(fill=tk.X, pady=(0, 8))

        # Current Income
        tk.Label(form_frame, text="Current Monthly Income ($):", fg=self.fg_light, bg=self.bg_card, anchor="w").pack(fill=tk.X, pady=(2, 2))
        entry_income = tk.Entry(form_frame, textvariable=self.var_current_income, bg="#334155", fg=self.fg_light, insertbackground="white")
        entry_income.pack(fill=tk.X, pady=(0, 8))
        entry_income.bind("<KeyRelease>", lambda e: self._trigger_callback("on_recalculate_fee"))

        # Employment Type (Radio buttons)
        tk.Label(form_frame, text="Employment Type:", fg=self.fg_light, bg=self.bg_card, anchor="w").pack(fill=tk.X, pady=(2, 2))
        emp_frame = tk.Frame(form_frame, bg=self.bg_card)
        emp_frame.pack(fill=tk.X, pady=(0, 8))
        for emp in EmploymentType:
            rb = tk.Radiobutton(
                emp_frame,
                text=emp.value,
                value=emp.value,
                variable=self.var_employment_type,
                fg=self.fg_light,
                bg=self.bg_card,
                selectcolor=self.bg_dark,
                activebackground=self.bg_card,
                activeforeground=self.accent_cyan,
                command=lambda: self._trigger_callback("on_recalculate_fee")
            )
            rb.pack(side=tk.LEFT, padx=5)

        # Desired Service
        tk.Label(form_frame, text="Desired Service:", fg=self.fg_light, bg=self.bg_card, anchor="w").pack(fill=tk.X, pady=(2, 2))
        cb_service = ttk.Combobox(
            form_frame, 
            textvariable=self.var_desired_service, 
            values=[s.value for s in DesiredService], 
            state="readonly"
        )
        cb_service.pack(fill=tk.X, pady=(0, 8))
        cb_service.bind("<<ComboboxSelected>>", lambda e: self._trigger_callback("on_recalculate_fee"))

        # Calculated Fee (Read-only)
        tk.Label(form_frame, text="Calculated Affiliation Fee:", fg=self.fg_light, bg=self.bg_card, anchor="w").pack(fill=tk.X, pady=(2, 2))
        entry_fee = tk.Entry(form_frame, textvariable=self.var_affiliation_fee, state="readonly", bg="#1E293B", fg=self.accent_cyan, font=("Segoe UI", 10, "bold"))
        entry_fee.pack(fill=tk.X, pady=(0, 8))

        # Affiliation Date (Spinboxes)
        tk.Label(form_frame, text="Affiliation Date (dd/mm/yyyy):", fg=self.fg_light, bg=self.bg_card, anchor="w").pack(fill=tk.X, pady=(2, 2))
        date_frame = tk.Frame(form_frame, bg=self.bg_card)
        date_frame.pack(fill=tk.X, pady=(0, 8))

        tk.Spinbox(date_frame, from_=1, to=31, textvariable=self.var_day, width=4).pack(side=tk.LEFT, padx=2)
        tk.Label(date_frame, text="/", fg=self.fg_light, bg=self.bg_card).pack(side=tk.LEFT)
        tk.Spinbox(date_frame, from_=1, to=12, textvariable=self.var_month, width=4).pack(side=tk.LEFT, padx=2)
        tk.Label(date_frame, text="/", fg=self.fg_light, bg=self.bg_card).pack(side=tk.LEFT)
        tk.Spinbox(date_frame, from_=2020, to=2030, textvariable=self.var_year, width=6).pack(side=tk.LEFT, padx=2)

    def _build_display_panel(self, parent: tk.Widget) -> None:
        """Builds right display panel with Treeview, report field, and action buttons."""
        display_frame = tk.Frame(parent, bg=self.bg_dark)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Structure Selector Toolbar
        toolbar = tk.Frame(display_frame, bg=self.bg_dark)
        toolbar.pack(fill=tk.X, pady=(0, 8))

        tk.Label(toolbar, text="View Data Structure:", fg=self.fg_light, bg=self.bg_dark, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        cb_structure = ttk.Combobox(
            toolbar,
            textvariable=self.var_selected_structure,
            values=[s.value for s in StructureType],
            state="readonly",
            width=15
        )
        cb_structure.pack(side=tk.LEFT)
        cb_structure.bind("<<ComboboxSelected>>", lambda e: self._trigger_callback("on_structure_changed"))

        # Treeview Container
        tree_frame = tk.Frame(display_frame, bg=self.bg_dark)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        columns = ("id_type", "id_number", "full_name", "income", "employment", "service", "fee", "date")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id_type", text="Type")
        self.tree.heading("id_number", text="ID Number")
        self.tree.heading("full_name", text="Full Name")
        self.tree.heading("income", text="Income")
        self.tree.heading("employment", text="Employment")
        self.tree.heading("service", text="Service")
        self.tree.heading("fee", text="Fee")
        self.tree.heading("date", text="Date")

        self.tree.column("id_type", width=50, anchor="center")
        self.tree.column("id_number", width=90, anchor="center")
        self.tree.column("full_name", width=140, anchor="w")
        self.tree.column("income", width=90, anchor="e")
        self.tree.column("employment", width=90, anchor="center")
        self.tree.column("service", width=130, anchor="w")
        self.tree.column("fee", width=80, anchor="e")
        self.tree.column("date", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Non-editable Report Field
        report_frame = tk.Frame(display_frame, bg=self.bg_dark)
        report_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(report_frame, text="Report:", fg=self.fg_light, bg=self.bg_dark, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        entry_report = tk.Entry(
            report_frame, 
            textvariable=self.var_report_text, 
            state="readonly", 
            bg="#1E293B", 
            fg=self.accent_cyan, 
            font=("Segoe UI", 10, "bold")
        )
        entry_report.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Action Buttons Panel
        btn_frame = tk.Frame(display_frame, bg=self.bg_dark)
        btn_frame.pack(fill=tk.X)

        btn_register = tk.Button(
            btn_frame, text="Register", bg=self.accent_cyan, fg="black", font=("Segoe UI", 9, "bold"),
            command=lambda: self._trigger_callback("on_register")
        )
        btn_register.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        btn_clear = tk.Button(
            btn_frame, text="Clear", bg="#64748B", fg="white", font=("Segoe UI", 9, "bold"),
            command=lambda: self._trigger_callback("on_clear")
        )
        btn_clear.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        btn_report = tk.Button(
            btn_frame, text="Report", bg="#10B981", fg="black", font=("Segoe UI", 9, "bold"),
            command=lambda: self._trigger_callback("on_report")
        )
        btn_report.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        btn_delete = tk.Button(
            btn_frame, text="Delete", bg=self.accent_orange, fg="white", font=("Segoe UI", 9, "bold"),
            command=lambda: self._trigger_callback("on_delete")
        )
        btn_delete.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        btn_exit = tk.Button(
            btn_frame, text="Exit", bg=self.accent_red, fg="white", font=("Segoe UI", 9, "bold"),
            command=lambda: self._trigger_callback("on_exit")
        )
        btn_exit.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

    def set_controller_callbacks(self, callbacks: Dict[str, Callable]) -> None:
        """Binds controller event handler methods to view events."""
        self.callbacks = callbacks

    def _trigger_callback(self, key: str) -> None:
        """Helper to invoke controller callback if registered."""
        if key in self.callbacks:
            self.callbacks[key]()

    def update_treeview(self, data: List[tuple]) -> None:
        """Refreshes Treeview rows with provided list of tuples."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in data:
            self.tree.insert("", tk.END, values=row)

    def clear_inputs(self) -> None:
        """Resets all input fields without clearing Treeview data."""
        self.var_id_number.set("")
        self.var_full_name.set("")
        self.var_current_income.set("")
        self.var_affiliation_fee.set("$0.00")
        self.var_id_type.set(IDType.CC.value)
        self.var_employment_type.set(EmploymentType.EMPLOYEE.value)
        self.var_desired_service.set(DesiredService.UNEMPLOYMENT_SUBSIDY.value)