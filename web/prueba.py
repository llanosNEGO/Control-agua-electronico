import serial
import time

# Configura el puerto serial y la velocidad de transmisión
arduino = serial.Serial('COM3', 9600)  # Reemplaza 'COM3' con el puerto correcto
time.sleep(2)  # Tiempo de espera para que se establezca la conexión

print("Conexión establecida. Ingresa '1' para encender el LED o 'A' para apagarlo.")
while True:
    comando = input("Introduce comando ('1' para encender, 'A' para apagar, 'q' para salir): ")
    
    if comando == 'q':
        print("Cerrando conexión...")
        break
    elif comando in ['1', 'A']:
        arduino.write(comando.encode())  # Envía el comando a Arduino
        print(f"Comando '{comando}' enviado.")
    else:
        print("Comando no válido, ingresa '1', 'A' o 'q'.")

# Cierra la conexión serial
arduino.close()
print("Conexión cerrada.")