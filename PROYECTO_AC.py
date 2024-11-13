import tkinter as tk
from tkinter import messagebox

sistema_agua = []

class Agua:
    def __init__(self, cantidad, destino):
        self.cantidad = cantidad
        self.destino = destino

class Tanque:
    def __init__(self):
        self.tanque_elevado = 0
        self.tanque_tierra = 3

tanque = Tanque()

def iniciar_monitoreo():
    try:
        cantidad = float(entry_cantidad.get())
    except ValueError:
        messagebox.showwarning("Advertencia", "La cantidad debe ser un número.")
        return

    if cantidad > 3:
        messagebox.showwarning("Advertencia", "La cantidad máxima permitida es de 3 litros.")
        return

    if tanque.tanque_tierra >= cantidad:
        tanque.tanque_elevado += cantidad
        tanque.tanque_tierra -= cantidad
        messagebox.showinfo("Éxito", f"{cantidad} litros enviados al Tanque Elevado.")
        
        agua = Agua(cantidad, "Tanque Elevado")
        sistema_agua.append(agua)
    else:
        messagebox.showwarning("Advertencia", "No hay suficiente agua en el Tanque a Tierra.")
    
    limpiar_campos_agua()
    mostrar_info_tanques()

def limpiar_campos_agua():
    entry_cantidad.delete(0, tk.END)

def mostrar_info_tanques():
    if not sistema_agua:
        messagebox.showwarning("Advertencia", "No hay registros de agua.")
        return

    agua_info = "\n".join([f"Cantidad: {a.cantidad} litros, Destino: {a.destino}" for a in sistema_agua])
    agua_info += f"\n\nLitros en tanque elevado: {tanque.tanque_elevado} litros"
    agua_info += f"\nLitros en tanque a tierra: {tanque.tanque_tierra} litros"
    messagebox.showinfo("Información de los Tanques", agua_info)

def encender_electrobomba():
    if sistema_agua:
        messagebox.showinfo("Electrobomba", "Electrobomba encendida.")
    else:
        messagebox.showwarning("Advertencia", "No hay registros de agua. Primero registre una cantidad.")

def apagar_electrobomba():
    messagebox.showinfo("Electrobomba", "Electrobomba apagada.")

def salir():
    ventana.destroy()

ventana = tk.Tk()
ventana.title("Sistema de Gestión del Agua")
ventana.geometry("400x400")
ventana.configure(bg="#e0f7fa")

titulo = tk.Label(ventana, text="DISEÑO DE UN SISTEMA AUTOMATIZADO PARA CONTROL DE FLUJO Y VOLUMEN DE AGUA EN LA CIUDAD DE CAJAMARCA.", font=("Arial", 16), bg="#00796b", fg="white", padx=10, pady=10)
titulo.pack(fill=tk.X)

frame_agua = tk.LabelFrame(ventana, text="Gestión de Agua", padx=10, pady=10, bg="#b2ebf2")
frame_agua.pack(pady=10, padx=10, fill="both")

label_cantidad = tk.Label(frame_agua, text="Cantidad a enviar (máximo 3 litros):", bg="#b2ebf2")
label_cantidad.grid(row=0, column=0, sticky=tk.W)
entry_cantidad = tk.Entry(frame_agua)
entry_cantidad.grid(row=0, column=1)

btn_iniciar_monitoreo = tk.Button(frame_agua, text="Enviar Agua al Tanque Elevado", command=iniciar_monitoreo, bg="#00796b", fg="white")
btn_iniciar_monitoreo.grid(row=1, column=0, pady=10)
btn_mostrar_info = tk.Button(frame_agua, text="Mostrar Información de los Tanques", command=mostrar_info_tanques, bg="#00796b", fg="white")
btn_mostrar_info.grid(row=1, column=1, pady=10)
btn_encender = tk.Button(frame_agua, text="Encender Electrobomba", command=encender_electrobomba, bg="#00796b", fg="white")
btn_encender.grid(row=2, column=0, pady=10)
btn_apagar = tk.Button(frame_agua, text="Apagar Electrobomba", command=apagar_electrobomba, bg="#d32f2f", fg="white")
btn_apagar.grid(row=2, column=1, pady=10)
btn_salir = tk.Button(frame_agua, text="Salir", command=salir, bg="#d32f2f", fg="white")
btn_salir.grid(row=3, columnspan=2, pady=10)

ventana.mainloop()
