from flask import Flask, jsonify, request, render_template
import serial
import time

app = Flask(__name__)

# Función para abrir el puerto serial
def open_serial_port():
    try:
        motor_serial = serial.Serial('COM3', 9600)
        time.sleep(2)  # Esperar un momento para asegurar que el puerto esté listo
        return motor_serial
    except serial.SerialException as e:
        print(f"Error al abrir el puerto serial: {e}")
        return None

# Inicializamos la variable de estado del motor
motor_status = "off"  # Puede ser 'on' o 'off'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control_motor', methods=['POST'])
def control_motor():
    global motor_status

    # Intentamos abrir el puerto serial en cada solicitud
    motor_serial = open_serial_port()

    # Si el puerto se abre correctamente, procedemos con la acción
    if motor_serial and motor_serial.is_open:
        comando = request.form.get('action')

        if comando == '1':  # Encender el motor
            motor_serial.write(b'1')  # Enviar el comando para encender
            motor_status = 'on'
        elif comando == 'A':  # Apagar el motor
            motor_serial.write(b'A')  # Enviar el comando para apagar
            motor_status = 'off'
        
        motor_serial.close()  # Cerrar el puerto después de la acción
        return jsonify({"status": f"Motor {'encendido' if motor_status == 'on' else 'apagado'}"}), 200
    else:
        return jsonify({'status': 'Error de conexión serial'}), 500

@app.route('/estado_motor', methods=['GET'])
def estado_motor():
    return jsonify({'status': motor_status})

if __name__ == '__main__':
    app.run(debug=True)