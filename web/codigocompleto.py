import serial
import time

# Configurar el puerto serial
arduino_port = "COM3"  # Cambiar por el puerto donde está conectado el Arduino
baud_rate = 9600       # Velocidad del puerto serial
timeout = 1            # Tiempo de espera en segundos

# Iniciar la conexión serial
try:
    arduino = serial.Serial(arduino_port, baud_rate, timeout=timeout)
    print(f"Conectado al puerto {arduino_port}")
    time.sleep(2)  # Esperar a que el Arduino esté listo
except serial.SerialException:
    print("No se pudo conectar al Arduino. Verifica el puerto.")
    exit()

def enviar_comando(comando):
    """Enviar un comando al Arduino."""
    arduino.write(comando.encode())  # Enviar como bytes
    time.sleep(0.1)  # Esperar respuesta
    while arduino.in_waiting > 0:
        print("Arduino:", arduino.readline().decode().strip())

def medir_volumen():
    """Recibir medición de volumen desde el Arduino."""
    print("Solicitando medición...")
    enviar_comando('M')  # Comando ficticio para solicitar volumen
    while arduino.in_waiting > 0:
        print("Arduino:", arduino.readline().decode().strip())

# Interfaz de usuario simple
try:
    while True:
        print("\nOpciones:")
        print("1: Activar relé")
        print("A: Desactivar relé")
        print("V: Activar motor (horario)")
        print("0: Detener motor")
        print("M: Medir volumen")
        print("Q: Salir")

        opcion = input("Ingresa una opción: ").strip().upper()
        if opcion == 'Q':
            print("Saliendo...")
            break
        enviar_comando(opcion)

except KeyboardInterrupt:
    print("\nPrograma interrumpido por el usuario.")

finally:
    arduino.close()
    print("Conexión serial cerrada.")
