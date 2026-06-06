import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 65432

def procesar_tarea_worker(conn, addr, tarea):
    print(f"[WORKER - HILO {threading.current_thread().name}] Procesando: {tarea}")
    
    # Simula el procesamiento distribuido o guardado en DB / S3
    time.sleep(1.5) 
    respuesta = f"Éxito: '{tarea}' procesada y registrada en almacenamiento."
    
    try:
        conn.sendall(respuesta.encode('utf-8'))
    except Exception as e:
        print(f"[ERROR] No se pudo enviar respuesta a {addr}: {e}")
    finally:
        conn.close()

def atender_cliente(conn, addr):
    try:
        data = conn.recv(1024)
        if data:
            tarea = data.decode('utf-8')
            # Lanza la tarea en un hilo separado (Simulación del Pool de Workers)
            hilo_worker = threading.Thread(target=procesar_tarea_worker, args=(conn, addr, tarea))
            hilo_worker.start()
    except Exception as e:
        print(f"[ERROR] Conexión fallida con {addr}: {e}")
        conn.close()

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVIDOR CENTRAL] Escuchando en {HOST}:{PORT}...")
    
    while True:
        conn, addr = server.accept()
        # El receptor delega inmediatamente la conexión para no bloquear el puerto
        hilo_conexion = threading.Thread(target=atender_cliente, args=(conn, addr))
        hilo_conexion.start()

if __name__ == "__main__":
    iniciar_servidor()