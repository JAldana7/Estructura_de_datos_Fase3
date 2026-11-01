# importaciones necesarias
import sys
from tkinter import messagebox
from datetime import datetime
from models.affiliate_service import AffiliateService
from models.affiliate import Affiliate
from models.enums import IDType, EmploymentType, DesiredService, StructureType
from models.about_info import AboutInfo

# clase principal del controlador
class MainController:
    # inicialización del controlador con la vista asociada
    def __init__(self, view):
        self.view = view
        self.service = AffiliateService()
        self.about_info = AboutInfo()

        # establecer los callbacks del controlador en la vista
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
        
        self.refresh_display() # Refresca la visualización inicial de la estructura seleccionada

    # Función para recalcular la cuota de afiliación dinámica en el evento de keyup de la entrada
    def handle_recalculate_fee(self) -> None:
        income_str = self.view.var_current_income.get().strip()
        if not income_str:
            self.view.var_affiliation_fee.set("$0.00")
            return # retorna si el campo de ingreso está vacío

        # Validación: Asegurarse de que el ingreso sea un número positivo
        try: 
            income = float(income_str)
            if income < 0:
                self.view.var_affiliation_fee.set("Invalid Income")
                return
            
            employment = EmploymentType(self.view.var_employment_type.get()) # Obtener el tipo de empleo seleccionado
            service = DesiredService(self.view.var_desired_service.get()) # Obtener el servicio deseado seleccionado

            # Crear un afiliado temporal para calcular la cuota de afiliación
            temp_affiliate = Affiliate(
                id_type=IDType.CC,
                id_number="0",
                full_name="Temp",
                current_income=income,
                desired_service=service,
                employment_type=employment,
                affiliation_date=datetime.now()
            )
            self.view.var_affiliation_fee.set(f"${temp_affiliate.affiliation_fee:,.2f}") # Formatear la cuota de afiliación como moneda
        except ValueError:
            self.view.var_affiliation_fee.set("Invalid Income") # mensaje de error si el ingreso no es un número válido

    # Manejo del registro de un nuevo afiliado con validaciones estrictas
    def handle_register(self) -> None:
        # Obtener y limpiar los valores de entrada del formulario
        id_num = self.view.var_id_number.get().strip()
        full_name = self.view.var_full_name.get().strip()
        income_str = self.view.var_current_income.get().strip()

        # 1. validación: Todos los campos son obligatorios
        if not id_num or not full_name or not income_str:
            messagebox.showwarning("Validation Error", "All input fields are required.", parent=self.view)
            return

        # 2. Validación: Solo dígitos numéricos para el número de identificación
        if not id_num.isdigit():
            messagebox.showwarning("Validation Error", "ID Number must contain numeric digits only.", parent=self.view)
            return

        # 3. Validación: Solo letras y espacios para el nombre completo
        if not full_name.replace(" ", "").isalpha():
            messagebox.showwarning("Validation Error", "Full Name must contain letters and spaces only.", parent=self.view)
            return

        # 4. Validación: Ingreso actual debe ser un número positivo mayor que 0
        try:
            income = float(income_str)
            if income <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Validation Error", "Current Income must be a positive number greater than 0.", parent=self.view)
            return

        # 5. Validación: Fecha de afiliación debe ser una fecha válida
        try:
            day = int(self.view.var_day.get())
            month = int(self.view.var_month.get())
            year = int(self.view.var_year.get())
            aff_date = datetime(year, month, day)
        except ValueError:
            messagebox.showwarning("Validation Error", "Invalid calendar date selected.", parent=self.view)
            return

        # agregar el afiliado a la estructura seleccionada
        affiliate = Affiliate(
            id_type=IDType(self.view.var_id_type.get()),
            id_number=id_num,
            full_name=full_name,
            current_income=income,
            desired_service=DesiredService(self.view.var_desired_service.get()),
            employment_type=EmploymentType(self.view.var_employment_type.get()),
            affiliation_date=aff_date
        )

        # Agregar el afiliado a la estructura seleccionada y mostrar un mensaje de éxito
        selected_struct = StructureType(self.view.var_selected_structure.get())
        self.service.add_affiliate(selected_struct, affiliate)

        # Mostrar mensaje de éxito y limpiar los campos de entrada
        messagebox.showinfo("Success", f"Affiliate added successfully to {selected_struct.value}!", parent=self.view)
        self.view.clear_inputs()
        self.refresh_display() # Refresca la visualización de la estructura después de agregar un nuevo afiliado

    # Manejo de la acción de limpiar los campos de entrada del formulario
    def handle_clear(self) -> None:
        self.view.clear_inputs()

    # Manejo del cambio de estructura seleccionada para actualizar la visualización
    def handle_structure_changed(self) -> None:
        self.refresh_display()

    # Manejo de la acción de generar un reporte basado en la estructura seleccionada
    def handle_report(self) -> None:
        # Obtener la estructura seleccionada y generar el reporte correspondiente
        selected_struct = StructureType(self.view.var_selected_structure.get())
        report_message = self.service.get_structure_report(selected_struct)
        
        self.view.var_report_text.set(report_message) # 1. Actualizar el campo inferior no editable

        # 2. Definir título descriptivo según la estructura activa
        titles = {
            StructureType.STACK: "Stack Fee Sum Report",
            StructureType.QUEUE: "Queue Record Count Report",
            StructureType.LIST: "List Income Average Report"
        }
        
        dialog_title = titles.get(selected_struct, "Structure Report")

        # 3. Mostrar el MessageBox emergente de manera explícita
        messagebox.showinfo(
            dialog_title,
            f"Selected Structure: {selected_struct.value}\n\n{report_message}",
            parent=self.view
        )

    # Manejo de la acción de eliminar un afiliado de la estructura seleccionada
    def handle_delete(self) -> None:
        selected_struct = StructureType(self.view.var_selected_structure.get())

        # Validación: Si la estructura seleccionada es Lista, se requiere un número de identificación para eliminar
        if selected_struct == StructureType.LIST:
            id_num = self.view.var_id_number.get().strip()
            if not id_num:
                messagebox.showwarning("Search Required", "Please enter an ID Number in the form to search and remove from List.", parent=self.view)
                return

            if not self.service.find_in_list(id_num):
                messagebox.showerror("Not Found", f"No record found in List with ID Number: {id_num}", parent=self.view)
                return

            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to permanently delete affiliate ID {id_num} from List?", parent=self.view)
            if confirm:
                deleted = self.service.remove_affiliate(selected_struct, id_num)
                if deleted:
                    messagebox.showinfo("Deleted", f"Affiliate {deleted.full_name} removed from List.", parent=self.view)
                    self.refresh_display()
        else: # Para Stack y Queue, se elimina el elemento según la regla de la estructura (LIFO/FIFO)
            if self.service.is_structure_empty(selected_struct):
                messagebox.showwarning("Empty Structure", f"The {selected_struct.value} is currently empty.", parent=self.view)
                return

            confirm = messagebox.askyesno("Confirm Deletion", f"Remove item from {selected_struct.value} based on default structure rule?", parent=self.view)
            if confirm:
                deleted = self.service.remove_affiliate(selected_struct)
                if deleted:
                    messagebox.showinfo("Deleted", f"Removed: {deleted.full_name}", parent=self.view)
                    self.refresh_display()

    # Manejo de la acción de mostrar información sobre la aplicación
    def handle_about(self) -> None:
        messagebox.showinfo("About", self.about_info.get_info(), parent=self.view)

    # Manejo de la acción de salir de la aplicación con confirmación
    def handle_exit(self) -> None:
        if messagebox.askyesno("Exit", "Are you sure you want to exit the application?", parent=self.view):
            self.view.destroy()
            sys.exit(0)

    # Función para refrescar la visualización de la estructura seleccionada y actualizar la barra inferior
    def refresh_display(self) -> None:
        selected_struct = StructureType(self.view.var_selected_structure.get())
        
        # Obtener y refrescar registros en la tabla
        records = self.service.get_all_from_structure(selected_struct)
        data_tuples = [item.to_tuple() for item in records]
        self.view.update_treeview(data_tuples)
        
        # Actualizar únicamente el texto de la barra inferior (sin pop-up)
        report_message = self.service.get_structure_report(selected_struct)
        self.view.var_report_text.set(report_message)