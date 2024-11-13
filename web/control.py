from flask import Flask, jsonify, request, render_template
import serial
import time

app = Flask(__name__)

def open_serial_port():
    try:
        motor_serial = serial.Serial('COM3', 9600)
        time.sleep(2)  
        return motor_serial
    except serial.SerialException as e:
        print(f"Error al abrir el puerto serial: {e}")
        return None

motor_status = "off" 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control_motor', methods=['POST'])
def control_motor():
    global motor_status

    motor_serial = open_serial_port()

    if motor_serial and motor_serial.is_open:
        comando = request.form.get('action')

        if comando == '1':  
            motor_serial.write(b'1')  
            motor_status = 'on'
        elif comando == 'A': 
            motor_serial.write(b'A')  
            motor_status = 'off'
        
        motor_serial.close() 
        return jsonify({"status": f"Motor {'encendido' if motor_status == 'on' else 'apagado'}"}), 200
    else:
        return jsonify({'status': 'Error de conexión serial'}), 500

@app.route('/estado_motor', methods=['GET'])
def estado_motor():
    return jsonify({'status': motor_status})

if __name__ == '__main__':
    app.run(debug=True)