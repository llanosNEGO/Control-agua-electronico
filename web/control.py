from flask import Flask, jsonify, request, render_template
import serial
import time

app = Flask(__name__)

ARDUINO_PORT = 'COM5'
BAUD_RATE = 9600
TIMEOUT = 2

motor_status = "off"  # Estado inicial del motor
valve_status = "off"  # Estado inicial de la válvula

def open_serial_port():
    """Abrir la conexión serial con el Arduino."""
    try:
        motor_serial = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=TIMEOUT)
        time.sleep(2) 
        return motor_serial
    except serial.SerialException as e:
        print(f"Error al abrir el puerto serial: {e}")
        return None

@app.route('/')
def index():
    """Renderizar la página principal."""
    return render_template('index.html')

@app.route('/control_motor', methods=['POST'])
def control_motor():
    """Controlar el motor o válvula basado en el comando recibido."""
    global motor_status, valve_status
    comando = request.form.get('action') 
    motor_serial = open_serial_port()

    if motor_serial and motor_serial.is_open:
        try:
            if comando == '1':  # Encender motor
                motor_serial.write(b'1')
                motor_status = "on"
            elif comando == 'A':  # Apagar motor
                motor_serial.write(b'A')
                motor_status = "off"
            elif comando == 'V':  # Abrir válvula
                motor_serial.write(b'V')
                valve_status = "open"
            elif comando == '0':  # Cerrar válvula
                motor_serial.write(b'0')
                valve_status = "closed"
            else:
                return jsonify({"status": "Comando desconocido"}), 400

            motor_serial.close()
            return jsonify({"status": f"Comando '{comando}' ejecutado correctamente"}), 200
        except Exception as e:
            print(f"Error al enviar comando: {e}")
            return jsonify({'status': 'Error al enviar comando'}), 500
    else:
        return jsonify({'status': 'Error de conexión serial'}), 500

@app.route('/estado_motor', methods=['GET'])
def estado_motor():
    """Obtener el estado actual del motor y la válvula."""
    return jsonify({
        'motor_status': motor_status,
        'valve_status': valve_status
    })

@app.route('/medir_volumen', methods=['GET'])
def medir_volumen():
    """Medir el volumen actual desde el Arduino."""
    motor_serial = open_serial_port()

    if motor_serial and motor_serial.is_open:
        try:
            motor_serial.write(b'M')  
            time.sleep(0.5)  

            if motor_serial.in_waiting > 0:
                volumen = motor_serial.readline().decode('utf-8').strip()
                motor_serial.close()
                return jsonify({"volumen": volumen}), 200
            else:
                motor_serial.close()
                return jsonify({"status": "Sin respuesta del Arduino"}), 500
        except Exception as e:
            print(f"Error al medir volumen: {e}")
            return jsonify({'status': 'Error al medir volumen'}), 500
    else:
        return jsonify({'status': 'Error de conexión serial'}), 500

if __name__ == '__main__':
    app.run(debug=True)