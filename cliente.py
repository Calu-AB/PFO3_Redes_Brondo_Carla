import socket
import tkinter as tk
from tkinter import messagebox
import threading

HOST = '127.0.0.1'
PORT = 65432

def enviar_tarea_backend(tarea, caja_texto):
    try:
        # Abrir socket hacia el servidor (o balanceador de carga)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect((HOST, PORT))
            cliente.sendall(tarea.encode('utf-8'))
            
            # Recibir el resultado del worker
            respuesta = cliente.recv(1024).decode('utf-8')
            
            # Actualizar la interfaz visual desde el hilo principal de Tkinter
            caja_texto.insert(tk.END, f"[RESPUESTA] {respuesta}\n")
    except ConnectionRefusedError:
        messagebox.showerror("Error de Conexión", "No se pudo conectar con el servidor central.")

def boton_presionado(entrada_tarea, caja_texto):
    tarea = entrada_tarea.get()
    if not tarea.strip():
        messagebox.showwarning("Campo Vacío", "Por favor, escribe una tarea para enviar.")
        return
        
    caja_texto.insert(tk.END, f"[ENVIANDO] {tarea}...\n")
    entrada_tarea.delete(0, tk.END)
    
    # IMPORTANTE: Ejecutar la red en un hilo separado para que la GUI no se congele
    hilo_red = threading.Thread(target=enviar_tarea_backend, args=(tarea, caja_texto))
    hilo_red.start()

def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("PFO 3 - Panel de Control Cliente")
    ventana.geometry("500x400")
    
    # Etiqueta e ingreso de tareas
    lbl = tk.Label(ventana, text="Escribe la tarea a distribuir:", font=("Arial", 11))
    lbl.pack(pady=10)
    
    entrada_tarea = tk.Entry(ventana, width=40, font=("Arial", 11))
    entrada_tarea.pack(pady=5)
    
    # Consola de texto para ver el flujo de datos
    caja_texto = tk.Text(ventana, width=55, height=12, font=("Consolas", 10))
    caja_texto.pack(pady=15)
    
    # Botón de envío
    btn_enviar = tk.Button(ventana, text="Enviar Tarea al Sistema", bg="#4CAF50", fg="white", 
                           font=("Arial", 11, "bold"), command=lambda: boton_presionado(entrada_tarea, caja_texto))
    btn_enviar.pack(pady=5)
    
    ventana.mainloop()

if __name__ == "__main__":
    crear_interfaz()