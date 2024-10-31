import customtkinter as ctk
import pandas as pd
from tkinter import ttk, messagebox

class Stock:
    def __init__(self, parent):
        self.parent = parent
        self.ventana_stock = ctk.CTkToplevel(parent)
        self.ventana_stock.title("Administración de Stock")
        self.ventana_stock.geometry("1200x800")

        self.stock_frame = ctk.CTkFrame(self.ventana_stock)
        self.stock_frame.pack(expand=True, fill='both', padx=20, pady=20)

        self.boton_cargar = ctk.CTkButton(self.stock_frame, text="Cargar Datos", command=self.cargar_datos)
        self.boton_cargar.pack(pady=10)

        self.boton_agregar = ctk.CTkButton(self.stock_frame, text="Agregar Producto", command=self.abrir_dialogo_producto)
        self.boton_agregar.pack(pady=5)

        self.boton_editar = ctk.CTkButton(self.stock_frame, text="Editar Producto", command=self.editar_producto)
        self.boton_editar.pack(pady=5)

        self.columns = ('Producto', 'Cantidad', 'Distribuidor', 'Precio de compra', 'Precio con IVA', 'Gasto total')
        self.tree = ttk.Treeview(self.stock_frame, columns=self.columns, show='headings')
        for col in self.columns:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill='both', pady=10)
        self.producto_actual = None 

    def cargar_datos(self):
        df = pd.read_excel('stock.xlsx')

    
        df['Precio con IVA'] = round(df['Precio de compra'] * 1.21, 2)
        df['Gasto total'] = df['Cantidad'] * df['Precio con IVA']

        for row in self.tree.get_children():
            self.tree.delete(row)

        for index, row in df.iterrows():
            self.tree.insert("", "end", values=(row['Producto'], row['Cantidad'], row['Distribuidor'], 
                                            row['Precio de compra'], row['Precio con IVA'], row['Gasto total']))

    def abrir_dialogo_producto(self):
        self.dialogo = ctk.CTkToplevel(self.ventana_stock)
        self.dialogo.title("Agregar/Editar Producto")
        self.dialogo.geometry("400x400")

        self.label_producto = ctk.CTkLabel(self.dialogo, text="Nombre del Producto:")
        self.label_producto.pack(pady=5)
        self.entry_producto = ctk.CTkEntry(self.dialogo)
        self.entry_producto.pack(pady=5)

        self.label_cantidad = ctk.CTkLabel(self.dialogo, text="Cantidad:")
        self.label_cantidad.pack(pady=5)
        self.entry_cantidad = ctk.CTkEntry(self.dialogo)
        self.entry_cantidad.pack(pady=5)

        self.label_distribuidor = ctk.CTkLabel(self.dialogo, text="Distribuidor:")
        self.label_distribuidor.pack(pady=5)
        self.entry_distribuidor = ctk.CTkEntry(self.dialogo)
        self.entry_distribuidor.pack(pady=5)

        self.label_precio = ctk.CTkLabel(self.dialogo, text="Precio de compra:")
        self.label_precio.pack(pady=5)
        self.entry_precio = ctk.CTkEntry(self.dialogo)
        self.entry_precio.pack(pady=5)

        if self.producto_actual:
            self.entry_producto.insert(0, self.producto_actual[0])
            self.entry_cantidad.insert(0, self.producto_actual[1])
            self.entry_distribuidor.insert(0, self.producto_actual[2])
            self.entry_precio.insert(0, self.producto_actual[3])

        self.boton_guardar = ctk.CTkButton(self.dialogo, text="Guardar", command=self.guardar_producto)
        self.boton_guardar.pack(pady=10)
    
    def guardar_producto(self):
        producto = self.entry_producto.get()
        cantidad = self.entry_cantidad.get()
        distribuidor = self.entry_distribuidor.get()
        precio_compra = self.entry_precio.get()

        if producto and cantidad and distribuidor and precio_compra:
            try:
                cantidad = int(cantidad)
                precio_compra = float(precio_compra)

                
                precio_con_iva = round(precio_compra * 1.21, 2)

                df = pd.read_excel('stock.xlsx')

                if self.producto_actual:
                    index = self.tree.index(self.tree.selection()[0])
                    df.loc[index, 'Producto'] = producto
                    df.loc[index, 'Cantidad'] = cantidad
                    df.loc[index, 'Distribuidor'] = distribuidor
                    df.loc[index, 'Precio de compra'] = precio_compra
                    df.loc[index, 'Precio con IVA'] = precio_con_iva
                else:
                    new_data = pd.DataFrame({
                        'Producto': [producto],
                        'Cantidad': [cantidad],
                        'Distribuidor': [distribuidor],
                        'Precio de compra': [precio_compra],
                        'Precio con IVA': [precio_con_iva] 
                    })
                    df = pd.concat([df, new_data], ignore_index=True)

                df.to_excel('stock.xlsx', index=False) 
                self.cargar_datos()  
                self.dialogo.destroy()
                self.producto_actual = None 
            except ValueError:
                messagebox.showerror("Error", "Por favor ingresa valores válidos para cantidad y precio.")
        else:
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")

    def editar_producto(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor selecciona un producto para editar.")
            return

        item = self.tree.item(selected_item)
        self.producto_actual = item['values'] 
        self.abrir_dialogo_producto() 