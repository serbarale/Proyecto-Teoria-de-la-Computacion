import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet
import os

class EncriptadorApp:
    def __init__(self, master):
        # Inicio de la aplicacion
        self.master = master
        self.master.title("Simulador de Encriptación Simétrica")
        self.master.geometry("550x400")
        self.master.resizable(0,0)
        self.master.configure(bg = "lightblue")
        self.clave_path = "clave.txt"  # Ruta al archivo que contiene la clave
        self.cargar_clave()  # Cargar o generar la clave al iniciar la aplicación

        # Configuración de la interfaz gráfica
        self.label_titulo = tk.Label(master, text="SIMULADOR DE ENCRIPTACION SIMETRICA", font=("Cheddar gothic", 14),bg = "lightblue")
        self.label_titulo.grid(row=0, column=0, columnspan=4, pady=10)

        self.label_clave = tk.Label(master, text=f"Clave para encriptación: {self.clave}",bg = "lightblue")
        self.label_clave.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="w")

        # Creacion de boton para copiar la clave
        self.copiar_clave_button = tk.Button(master, text="Copiar Clave", command=self.copiar_clave,bg = "yellow",relief=tk.GROOVE, bd=4)
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
        self.label_clave_encriptacion = tk.Label(self.tab_cifrado, text="Clave:")
        self.label_clave_encriptacion.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.clave_encriptacion_entry = tk.Entry(self.tab_cifrado, show="*", width=53)
        self.clave_encriptacion_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.label_mensaje = tk.Label(self.tab_cifrado, text="Mensaje:")
        self.label_mensaje.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.mensaje_entry = tk.Entry(self.tab_cifrado, width=53)
        self.mensaje_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.label_resultado_encriptacion = tk.Label(self.tab_cifrado, text="Mensaje encriptado:")
        self.label_resultado_encriptacion.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.resultado_encriptacion_text = tk.Text(self.tab_cifrado, height=5, width=40)
        self.resultado_encriptacion_text.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Creacion de botones en la pestaña de cifrado
        self.copiar_encriptado_button = tk.Button(self.tab_cifrado, text="Copiar Encriptado", command=self.copiar_encriptado, bg="orange",relief=tk.GROOVE, bd=4)
        self.copiar_encriptado_button.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.limpiar_cifrado_button = tk.Button(self.tab_cifrado, text="Limpiar Entradas", command=self.limpiar_cifrado, bg="orange",relief=tk.GROOVE, bd=4)
        self.limpiar_cifrado_button.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.cifrar_button = tk.Button(self.tab_cifrado, text="Cifrar", command=self.cifrar_mensaje, bg="orange",relief=tk.GROOVE, bd=4)
        self.cifrar_button.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        # Pestaña de cifrado
        self.label_clave_desencriptacion = tk.Label(self.tab_descifrado, text="Clave:")
        self.label_clave_desencriptacion.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.clave_desencriptacion_entry = tk.Entry(self.tab_descifrado, show="*", width=53)
        self.clave_desencriptacion_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.label_mensaje_encriptado = tk.Label(self.tab_descifrado, text="Mensaje encriptado:")
        self.label_mensaje_encriptado.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.mensaje_encriptado_entry = tk.Entry(self.tab_descifrado, width=53)
        self.mensaje_encriptado_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.label_resultado_desencriptacion = tk.Label(self.tab_descifrado, text="Mensaje desencriptado:")
        self.label_resultado_desencriptacion.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.resultado_desencriptacion_text = tk.Text(self.tab_descifrado, height=5, width=40)
        self.resultado_desencriptacion_text.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Creacion de botones para la pestaña de descifrado
        self.copiar_desencriptado_button = tk.Button(self.tab_descifrado, text="Copiar Desencriptado", command=self.copiar_desencriptado,bg="orange",relief=tk.GROOVE, bd=4)
        self.copiar_desencriptado_button.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.limpiar_descifrado_button = tk.Button(self.tab_descifrado, text="Limpiar Entradas",command=self.limpiar_descifrado,bg="orange",relief=tk.GROOVE, bd=4)
        self.limpiar_descifrado_button.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.desencriptar_button = tk.Button(self.tab_descifrado, text="Descifrar", command=self.desencriptar_mensaje,bg="orange",relief=tk.GROOVE, bd=4)
        self.desencriptar_button.grid(row=4, column=0, padx=10, pady=5, sticky="w")

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

    def copiar_encriptado(self):
        # Permite copiar el mensaje encriptado al portapapeles
        mensaje_encriptado = self.resultado_encriptacion_text.get("1.0", tk.END)
        self.master.clipboard_clear()
        self.master.clipboard_append(mensaje_encriptado)
        # Muestra un pop up que informa al usuario que el texto fue copiado
        messagebox.showinfo("Copiado", "Mensaje encriptado copiado al portapapeles.")

    def limpiar_cifrado(self):
        # Limpiar las entradas en la pestaña de cifrado
        self.clave_encriptacion_entry.delete(0, tk.END)
        self.mensaje_entry.delete(0, tk.END)
        self.resultado_encriptacion_text.delete("1.0", tk.END)

    def copiar_desencriptado(self):
        # Permite copiar el mensaje desencriptado al portapapeles
        mensaje_desencriptado = self.resultado_desencriptacion_text.get("1.0", tk.END)
        self.master.clipboard_clear()
        self.master.clipboard_append(mensaje_desencriptado)
        # Muestra un pop up que informa al usuario que el texto fue copiado
        messagebox.showinfo("Copiado", "Mensaje desencriptado copiado al portapapeles.")

    def limpiar_descifrado(self):
        # Limpiar las entradas en la pestaña de descifrado
        self.clave_desencriptacion_entry.delete(0, tk.END)
        self.mensaje_encriptado_entry.delete(0, tk.END)
        self.resultado_desencriptacion_text.delete("1.0", tk.END)

    def copiar_clave(self):
        # Copiar la clave al portapapeles
        self.master.clipboard_clear()
        self.master.clipboard_append(self.clave)
        # Muestra un pop up que informa al usuario que la clave fue copiado
        messagebox.showinfo("Copiado", "Clave copiada al portapapeles.")

    def cifrar_mensaje(self):
        # Cifrar el mensaje en la pestaña de cifrado
        # Lee la clave que ingresa el usuario
        clave_encriptacion = self.clave_encriptacion_entry.get()
        # Lee el mensaje que ignresa el usuario para cifrar
        mensaje = self.mensaje_entry.get()
        # Comprueba si el mensaje y la clave fueron ingresados
        if not clave_encriptacion or not mensaje:
            messagebox.showerror("Error", "Por favor, ingresa la clave y el mensaje para cifrar.")
            return
        # Si la clave es incorrecta, muestra un pop up al usuario
        if clave_encriptacion != self.clave:
            messagebox.showerror("Error", "La clave de encriptación no es válida.")
            return
        # Si la clave es correcta empieza cifrar el mensaje
        try:
            fernet = Fernet(clave_encriptacion.encode())
            mensaje_encriptado = fernet.encrypt(mensaje.encode())
            self.resultado_encriptacion_text.delete("1.0", tk.END)
            self.resultado_encriptacion_text.insert(tk.END, mensaje_encriptado.decode())
        except Exception as e:
            messagebox.showerror("Error", f"Error al cifrar el mensaje: {str(e)}")

    def desencriptar_mensaje(self):
        # Descifrar el mensaje en la pestaña de descifrado

        # Lee la clave y el mensaje encriptado
        clave_desencriptacion = self.clave_desencriptacion_entry.get()
        mensaje_encriptado = self.mensaje_encriptado_entry.get()

        # Comprueba si el mensaje encriptado y la clave fueron ingresados
        if not clave_desencriptacion or not mensaje_encriptado:
            messagebox.showerror("Error", "Por favor, ingresa la clave y el mensaje encriptado para desencriptar.")
            return

        # Si la clave es incorrecta, muestra un pop up al usuario
        if clave_desencriptacion != self.clave:
            messagebox.showerror("Error", "La clave de desencriptación no es válida.")
            return

        # Si la clave es correcta empieza cifrar el mensaje
        try:
            fernet = Fernet(clave_desencriptacion.encode())
            mensaje_desencriptado = fernet.decrypt(mensaje_encriptado.encode())
            self.resultado_desencriptacion_text.delete("1.0", tk.END)
            self.resultado_desencriptacion_text.insert(tk.END, mensaje_desencriptado.decode())
        except Exception as e:
            messagebox.showerror("Error", f"Error al desencriptar el mensaje: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EncriptadorApp(root)
    root.mainloop()

