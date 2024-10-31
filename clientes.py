import customtkinter as ctk
import pandas as pd
from tkinter import ttk
from tkinter import messagebox 

class Clientes:
    def __init__(self, parent):
        self.parent = parent
        self.ventana_clientes = ctk.CTkToplevel(parent)
        self.ventana_clientes.title("Administración de Clientes")
        self.ventana_clientes.geometry("800x600")

        self.clientes_frame = ctk.CTkFrame(self.ventana_clientes)
        self.clientes_frame.pack(expand=True, fill='both', padx=20, pady=20)

        self.clientes = []
        self.columns = ('Nombre', 'Edad', 'Email')  
        self.tree = ttk.Treeview(self.clientes_frame, columns=self.columns, show='headings')
        for col in self.columns:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill='both', pady=10)

        self.cargar_clientes() 

        self.boton_agregar_cliente = ctk.CTkButton(self.ventana_clientes, text="Agregar Cliente", command=lambda: self.abrir_clientes("Agregar"))
        self.boton_agregar_cliente.pack(pady=10)

        self.boton_editar_cliente = ctk.CTkButton(self.ventana_clientes, text="Editar Cliente", command=self.editar_cliente, state='disabled')  # Inicialmente deshabilitado
        self.boton_editar_cliente.pack(pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def cargar_clientes(self):
        try:
            df = pd.read_excel('clientes.xlsx')
            self.clientes = df.values.tolist()
            self.mostrar_clientes()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo: {e}") 

    def mostrar_clientes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)  

        for cliente in self.clientes:
            self.tree.insert("", "end", values=(cliente[0], cliente[1], cliente[2]))

    def on_tree_select(self, event):
        
        if self.tree.selection():
            self.boton_editar_cliente.configure(state='normal')
        else:
            self.boton_editar_cliente.configure(state='disabled')

    def editar_cliente(self):
        selected_item = self.tree.selection()
        if selected_item:
            cliente = self.tree.item(selected_item)['values']
            self.abrir_clientes("Editar", cliente)

    def abrir_clientes(self, modo, cliente=None):
        formulario = ctk.CTkToplevel(self.ventana_clientes)
        formulario.title(f"{modo} Cliente")
        formulario.geometry("400x300")

        ctk.CTkLabel(formulario, text="Nombre", font=('Roboto', 16)).pack(pady=10)
        entry_nombre = ctk.CTkEntry(formulario)
        entry_nombre.pack(pady=5)

        ctk.CTkLabel(formulario, text="Edad", font=('Roboto', 16)).pack(pady=5)
        entry_edad = ctk.CTkEntry(formulario)
        entry_edad.pack(pady=5)

        ctk.CTkLabel(formulario, text="Email", font=('Roboto', 16)).pack(pady=5)
        entry_email = ctk.CTkEntry(formulario)
        entry_email.pack(pady=5)

        if modo == "Editar" and cliente:
            entry_nombre.insert(0, cliente[0])
            entry_edad.insert(0, cliente[1])
            entry_email.insert(0, cliente[2]) 

        ctk.CTkButton(formulario, text=modo, command=lambda: self.guardar_cliente(modo, entry_nombre.get(), entry_edad.get(), entry_email.get(), cliente, formulario)).pack(pady=10)
    
    def guardar_cliente(self, modo, nombre, edad, email, cliente, formulario):
        try:
            edad = int(edad)
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número entero.")
            return
            
        if modo == "Agregar":
            self.clientes.append([nombre, edad, email])
            self.agregar_a_excel(nombre, edad, email)
        elif modo == "Editar":
            index = self.clientes.index(cliente)
            self.clientes[index] = [nombre, edad, email]
            self.actualizar_excel()

        self.mostrar_clientes()
        formulario.destroy()

    def agregar_a_excel(self, nombre, edad, email):
        try:
            df = pd.read_excel('clientes.xlsx')
            df = df.append({"Nombre": nombre, "Edad": edad, "Email": email}, ignore_index=True)
            df.to_excel('clientes.xlsx', index=False)
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar el cliente: {e}")

    def actualizar_excel(self):
        try:
            df = pd.DataFrame(self.clientes, columns=["Nombre", "Edad", "Email"])
            df.to_excel('clientes.xlsx', index=False)
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar el archivo: {e}")
