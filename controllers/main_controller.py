import sys
from tkinter import messagebox
from datetime import datetime

from models.affiliate_service import AffiliateService
from models.affiliate import Affiliate
from models.enums import IDType, EmploymentType, DesiredService, StructureType
from models.about_info import AboutInfo

class MainController:
    """
    Controller responsible for handling business logic and events for MainView.
    Manages data registration, validation, deletion, and reporting across linear structures.
    """

    def __init__(self, view):
        self.view = view
        self.service = AffiliateService()
        self.about_info = AboutInfo()

        # Vincular las acciones de la vista con los métodos de este controlador
        self.view.set_controller_callbacks({
            "on_register": self.handle_register,
            "on_clear": self.handle_clear,
            "on_report": self.handle_report,
            "on_delete": self.handle_delete,
            "on_exit": self.handle_exit,
            "on_about": self.handle_about,
            "on_structure_changed": self.handle_structure_changed,
            "on_recalculate_fee": self.handle_recalculate_fee
        })

        # Cargar vista inicial
        self.refresh_display()

    def handle_recalculate_fee(self) -> None:
        """Dynamically updates the fee entry field based on form inputs."""
        try:
            income_str = self.view.var_current_income.get().strip()
            if not income_str:
                self.view.var_affiliation_fee.set("$0.00")
                return

            income = float(income_str)
            employment = EmploymentType(self.view.var_employment_type.get())
            service = DesiredService(self.view.var_desired_service.get())

            # Crear una instancia temporal de afiliado para calcular la tarifa
            temp_affiliate = Affiliate(
                id_type=IDType.CC,
                id_number="0",
                full_name="Temp",
                current_income=income,
                desired_service=service,
                employment_type=employment,
                affiliation_date=datetime.now()
            )
            self.view.var_affiliation_fee.set(f"${temp_affiliate.affiliation_fee:,.2f}")
        except ValueError:
            self.view.var_affiliation_fee.set("Invalid Income")

    def handle_register(self) -> None:
        """Validates inputs and adds a new affiliate to the selected data structure."""
        id_num = self.view.var_id_number.get().strip()
        full_name = self.view.var_full_name.get().strip()
        income_str = self.view.var_current_income.get().strip()

        # 1. Validaciones básicas de campos vacíos
        if not id_num or not full_name or not income_str:
            messagebox.showwarning("Validation Error", "All fields are required.", parent=self.view)
            return

        # 2. Validar que el ID contenga solo números
        if not id_num.isdigit():
            messagebox.showwarning("Validation Error", "ID Number must contain digits only.", parent=self.view)
            return

        # 3. Validar que el Nombre contenga solo letras y espacios
        if not full_name.replace(" ", "").isalpha():
            messagebox.showwarning("Validation Error", "Full Name must contain letters only.", parent=self.view)
            return

        # 4. Validar Ingresos
        try:
            income = float(income_str)
            if income <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Validation Error", "Current Income must be a positive number.", parent=self.view)
            return

        # Construir objeto datetime desde los Spinbox
        try:
            day = int(self.view.var_day.get())
            month = int(self.view.var_month.get())
            year = int(self.view.var_year.get())
            aff_date = datetime(year, month, day)
        except ValueError:
            messagebox.showwarning("Validation Error", "Invalid date selected.", parent=self.view)
            return

        # Crear entidad Affiliate
        affiliate = Affiliate(
            id_type=IDType(self.view.var_id_type.get()),
            id_number=id_num,
            full_name=full_name,
            current_income=income,
            desired_service=DesiredService(self.view.var_desired_service.get()),
            employment_type=EmploymentType(self.view.var_employment_type.get()),
            affiliation_date=aff_date
        )

        # Seleccionar estructura activa y agregar registro
        selected_struct = StructureType(self.view.var_selected_structure.get())
        self.service.add_affiliate(selected_struct, affiliate)

        messagebox.showinfo("Success", f"Affiliate registered successfully in {selected_struct.value}!", parent=self.view)
        
        # Limpiar formulario y actualizar tabla
        self.view.clear_inputs()
        self.refresh_display()

    def handle_clear(self) -> None:
        """Clears form fields without affecting structure records."""
        self.view.clear_inputs()

    def handle_structure_changed(self) -> None:
        """Handles change in structure dropdown selection."""
        self.refresh_display()

    def handle_report(self) -> None:
        """Generates and displays report for selected structure in the report entry field."""
        selected_struct = StructureType(self.view.var_selected_structure.get())
        report = self.service.get_structure_report(selected_struct)
        self.view.var_report_text.set(report)

    def handle_delete(self) -> None:
        """Deletes a record according to selected structure rules (LIFO/FIFO/Search by ID)."""
        selected_struct = StructureType(self.view.var_selected_structure.get())

        if selected_struct == StructureType.LIST:
            id_num = self.view.var_id_number.get().strip()
            if not id_num:
                messagebox.showwarning("Search Required", "Please enter an ID Number to search and remove from List.", parent=self.view)
                return

            if not self.service.find_in_list(id_num):
                messagebox.showerror("Not Found", f"No affiliate found with ID: {id_num}", parent=self.view)
                return

            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete affiliate ID {id_num} from List?", parent=self.view)
            if confirm:
                deleted = self.service.remove_affiliate(selected_struct, id_num)
                if deleted:
                    messagebox.showinfo("Deleted", f"Affiliate {deleted.full_name} removed.", parent=self.view)
                    self.refresh_display()
        else:
            if self.service.is_structure_empty(selected_struct):
                messagebox.showwarning("Empty Structure", f"The {selected_struct.value} is currently empty.", parent=self.view)
                return

            confirm = messagebox.askyesno("Confirm Deletion", f"Remove top/first item from {selected_struct.value}?", parent=self.view)
            if confirm:
                deleted = self.service.remove_affiliate(selected_struct)
                if deleted:
                    messagebox.showinfo("Deleted", f"Removed: {deleted.full_name}", parent=self.view)
                    self.refresh_display()

    def handle_about(self) -> None:
        """Displays About dialog information."""
        messagebox.showinfo("About", self.about_info.get_info(), parent=self.view)

    def handle_exit(self) -> None:
        """Terminates the application."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit the application?", parent=self.view):
            self.view.destroy()
            sys.exit(0)

    def refresh_display(self) -> None:
        """Refreshes Treeview and Report field based on current structure."""
        selected_struct = StructureType(self.view.var_selected_structure.get())
        records = self.service.get_all_from_structure(selected_struct)
        data_tuples = [item.to_tuple() for item in records]
        self.view.update_treeview(data_tuples)
        self.handle_report()