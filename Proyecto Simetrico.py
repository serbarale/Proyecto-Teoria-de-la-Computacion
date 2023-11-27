import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet
import os

class CifradorApp:
    def __init__(self, master):
        # Inicio de la aplicacion
        self.master = master
        self.master.title("Simulador de Cifrado Simétrico")
        self.master.geometry("550x400")
        self.master.resizable(0, 0)
        self.master.configure(bg="lightblue")
        self.clave_path = "clave.txt"  # Ruta al archivo que contiene la clave
        self.cargar_clave()  # Cargar o generar la clave al iniciar la aplicación

        # Configuración de la interfaz gráfica
        self.label_titulo = tk.Label(master, text="SIMULADOR DE CIFRADO SIMÉTRICO", font=("Cheddar gothic", 14), bg="lightblue")
        self.label_titulo.grid(row=0, column=0, columnspan=4, pady=10)

        self.label_clave = tk.Label(master, text=f"Clave para cifrado: {self.clave}", bg="lightblue")
        self.label_clave.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="w")

        # Creacion de boton para copiar la clave
        self.copiar_clave_button = tk.Button(master, text="Copiar Clave", command=self.copiar_clave, bg="yellow",
                                             relief=tk.GROOVE, bd=4)
        self.copiar_clave_button.grid(row=1, column=3, padx=10, pady=5, sticky="w")

        # Creacion de pestañas para el cifrado y descifrado
        self.notebook = ttk.Notebook(master)
        self.tab_cifrado = ttk.Frame(self.notebook)
        self.tab_descifrado = ttk.Frame(self.notebook)

        # Configuración de las pestañas de cifrado y descifrado
        self.notebook.add(self.tab_cifrado, text="Cifrado")
        self.notebook.add(self.tab_descifrado, text="Descifrado")
        self.notebook.grid(row=2, column=0, columnspan=4, padx=10, pady=5, sticky="ew")

        # Pestaña de cifrado
        self.label_clave_cifrado = tk.Label(self.tab_cifrado, text="Clave:")
        self.label_clave_cifrado.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.clave_cifrado_entry = tk.Entry(self.tab_cifrado, show="*", width=53)
        self.clave_cifrado_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.label_mensaje_cifrado = tk.Label(self.tab_cifrado, text="Mensaje:")
        self.label_mensaje_cifrado.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.mensaje_cifrado_entry = tk.Entry(self.tab_cifrado, width=53)
        self.mensaje_cifrado_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.label_resultado_cifrado = tk.Label(self.tab_cifrado, text="Mensaje cifrado:")
        self.label_resultado_cifrado.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.resultado_cifrado_text = tk.Text(self.tab_cifrado, height=5, width=40)
        self.resultado_cifrado_text.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Creacion de botones en la pestaña de cifrado
        self.copiar_cifrado_button = tk.Button(self.tab_cifrado, text="Copiar cifrado", command=self.copiar_cifrado,
                                                bg="orange", relief=tk.GROOVE, bd=4)
        self.copiar_cifrado_button.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.limpiar_cifrado_button = tk.Button(self.tab_cifrado, text="Limpiar Entradas", command=self.limpiar_cifrado,
                                                bg="orange", relief=tk.GROOVE, bd=4)
        self.limpiar_cifrado_button.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.cifrar_button = tk.Button(self.tab_cifrado, text="Cifrar", command=self.cifrar_mensaje, bg="orange",
                                       relief=tk.GROOVE, bd=4)
        self.cifrar_button.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        # Pestaña de descifrado
        self.label_clave_descifrado = tk.Label(self.tab_descifrado, text="Clave:")
        self.label_clave_descifrado.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.clave_descifrado_entry = tk.Entry(self.tab_descifrado, show="*", width=53)
        self.clave_descifrado_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.label_mensaje_cifrado_descifrado = tk.Label(self.tab_descifrado, text="Mensaje cifrado:")
        self.label_mensaje_cifrado_descifrado.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.mensaje_cifrado_descifrado_entry = tk.Entry(self.tab_descifrado, width=53)
        self.mensaje_cifrado_descifrado_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.label_resultado_descifrado = tk.Label(self.tab_descifrado, text="Mensaje descifrado:")
        self.label_resultado_descifrado.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.resultado_descifrado_text = tk.Text(self.tab_descifrado, height=5, width=40)
        self.resultado_descifrado_text.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Creacion de botones para la pestaña de descifrado
        self.copiar_descifrado_button = tk.Button(self.tab_descifrado, text="Copiar descifrado", command=self.copiar_descifrado, bg="orange", relief=tk.GROOVE, bd=4)
        self.copiar_descifrado_button.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.limpiar_descifrado_button = tk.Button(self.tab_descifrado, text="Limpiar Entradas", command=self.limpiar_descifrado, bg="orange", relief=tk.GROOVE, bd=4)
        self.limpiar_descifrado_button.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.descifrar_button = tk.Button(self.tab_descifrado, text="Descifrar", command=self.descifrar_mensaje, bg="orange", relief=tk.GROOVE, bd=4)
        self.descifrar_button.grid(row=4, column=0, padx=10, pady=5, sticky="w")

    def cargar_clave(self):
        # Carga la clave del archivo txt creado
        if os.path.exists(self.clave_path):
            with open(self.clave_path, "r") as file:
                self.clave = file.read()
        else:
            # Si no existe el archivo genera otra clave
            self.clave = Fernet.generate_key().decode()
            with open(self.clave_path, "w") as file:
                file.write(self.clave)

    # Guarda la clave en un archivo txt
    def guardar_clave(self):
        # Guardar la clave en el archivo
        with open(self.clave_path, "w") as file:
            file.write(self.clave)

    def copiar_cifrado(self):
        # Permite copiar el mensaje cifrado al portapapeles
        mensaje_cifrado = self.resultado_cifrado_text.get("1.0", tk.END)
        self.master.clipboard_clear()
        self.master.clipboard_append(mensaje_cifrado)
        # Muestra un pop up que informa al usuario que el texto fue copiado
        messagebox.showinfo("Copiado", "Mensaje cifrado copiado al portapapeles.")

    def limpiar_cifrado(self):
        # Limpiar las entradas en la pestaña de cifrado
        self.clave_cifrado_entry.delete(0, tk.END)
        self.mensaje_cifrado_entry.delete(0, tk.END)
        self.resultado_cifrado_text.delete("1.0", tk.END)

    def copiar_descifrado(self):
        # Permite copiar el mensaje descifrado al portapapeles
        mensaje_descifrado = self.resultado_descifrado_text.get("1.0", tk.END)
        self.master.clipboard_clear()
        self.master.clipboard_append(mensaje_descifrado)
        # Muestra un pop up que informa al usuario que el texto fue copiado
        messagebox.showinfo("Copiado", "Mensaje descifrado copiado al portapapeles.")

    def limpiar_descifrado(self):
        # Limpiar las entradas en la pestaña de descifrado
        self.clave_descifrado_entry.delete(0, tk.END)
        self.mensaje_cifrado_descifrado_entry.delete(0, tk.END)
        self.resultado_descifrado_text.delete("1.0", tk.END)

    def copiar_clave(self):
        # Copiar la clave al portapapeles
        self.master.clipboard_clear()
        self.master.clipboard_append(self.clave)
        # Muestra un pop up que informa al usuario que la clave fue copiada
        messagebox.showinfo("Copiado", "Clave copiada al portapapeles.")

    def cifrar_mensaje(self):
        # Cifrar el mensaje en la pestaña de cifrado
        # Lee la clave que ingresa el usuario
        clave_cifrado = self.clave_cifrado_entry.get()
        # Lee el mensaje que ignresa el usuario para cifrar
        mensaje = self.mensaje_cifrado_entry.get()
        # Comprueba si el mensaje y la clave fueron ingresados
        if not clave_cifrado or not mensaje:
            messagebox.showerror("Error", "Por favor, ingresa la clave y el mensaje para cifrar.")
            return
        # Si la clave es incorrecta, muestra un pop up al usuario
        if clave_cifrado != self.clave:
            messagebox.showerror("Error", "La clave de cifrado no es válida.")
            return
        # Si la clave es correcta empieza cifrar el mensaje
        try:
            fernet = Fernet(clave_cifrado.encode())
            mensaje_cifrado = fernet.encrypt(mensaje.encode())
            self.resultado_cifrado_text.delete("1.0", tk.END)
            self.resultado_cifrado_text.insert(tk.END, mensaje_cifrado.decode())
        except Exception as e:
            messagebox.showerror("Error", f"Error al cifrar el mensaje: {str(e)}")

    def descifrar_mensaje(self):
        # Descifrar el mensaje en la pestaña de descifrado
        # Lee la clave y el mensaje cifrado
        clave_descifrado = self.clave_descifrado_entry.get()
        mensaje_cifrado = self.mensaje_cifrado_descifrado_entry.get()

        # Comprueba si el mensaje cifrado y la clave fueron ingresados
        if not clave_descifrado or not mensaje_cifrado:
            messagebox.showerror("Error", "Por favor, ingresa la clave y el mensaje cifrado para descifrar.")
            return

        # Si la clave es incorrecta, muestra un pop up al usuario
        if clave_descifrado != self.clave:
            messagebox.showerror("Error", "La clave de descifrado no es válida.")
            return

        # Si la clave es correcta empieza cifrar el mensaje
        try:
            fernet = Fernet(clave_descifrado.encode())
            mensaje_descifrado = fernet.decrypt(mensaje_cifrado.encode())
            self.resultado_descifrado_text.delete("1.0", tk.END)
            self.resultado_descifrado_text.insert(tk.END, mensaje_descifrado.decode())
        except Exception as e:
            messagebox.showerror("Error", f"Error al descifrar el mensaje: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CifradorApp(root)
    root.mainloop()

