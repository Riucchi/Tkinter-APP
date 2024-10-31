import customtkinter as ctk
from clientes import Clientes
from stock import Stock

class MiAplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación Administrativa")
        self.root.geometry("800x600")

        self.frame_login = ctk.CTkFrame(root)
        self.frame_login.pack(pady=20, padx=20, fill='both', expand=True)

        self.label = ctk.CTkLabel(self.frame_login, text="Usuario", font=('Roboto', 16))
        self.label.pack(pady=10)
        self.entry_user = ctk.CTkEntry(self.frame_login)
        self.entry_user.pack(pady=10)

        self.label_password = ctk.CTkLabel(self.frame_login, text="Contraseña", font=('Roboto', 16))
        self.label_password.pack(pady=10)
        self.entry_password = ctk.CTkEntry(self.frame_login, show="*")
        self.entry_password.pack(pady=10)

        self.boton = ctk.CTkButton(self.frame_login, text="Log-in", command=self.login)
        self.boton.pack(pady=10)

    def login(self):
        usuario = self.entry_user.get()
        contraseña = self.entry_password.get()
        if usuario == "lucas" and contraseña == "lucas44":
            self.interfaz_administrativa()
        else:
            ctk.CTkMessageBox.show_error("Error", "Contraseña o Usuario Incorrecto")

    def interfaz_administrativa(self):
        ventana_nueva = ctk.CTkToplevel(self.root)
        ventana_nueva.title("Bienvenido")
        ventana_nueva.geometry("800x600")

        label_de_bienvenida = ctk.CTkLabel(ventana_nueva, text="Bienvenido", font=('Roboto', 20))
        label_de_bienvenida.pack(pady=10)

        ctk.CTkButton(ventana_nueva, text="Clientes", command=lambda: Clientes(ventana_nueva)).pack(pady=10)
        ctk.CTkButton(ventana_nueva, text="Stock", command=lambda: Stock(ventana_nueva)).pack(pady=10)

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = MiAplicacion(root)
    root.mainloop()