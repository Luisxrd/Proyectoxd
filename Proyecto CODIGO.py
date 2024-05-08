import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import RPi.GPIO as GPIO

class MotorControl(QWidget):
    def _init_(self):
        super()._init_()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Control de Motor Paso a Paso')

        self.btn_start = QPushButton('Iniciar Motor', self)
        self.btn_start.setGeometry(50, 50, 100, 50)
        self.btn_start.clicked.connect(self.start_motor)

        self.btn_stop = QPushButton('Detener Motor', self)
        self.btn_stop.setGeometry(50, 110, 100, 50)
        self.btn_stop.clicked.connect(self.stop_motor)

        self.btn_reverse = QPushButton('Invertir Giro', self)
        self.btn_reverse.setGeometry(160, 50, 100, 50)
        self.btn_reverse.clicked.connect(self.reverse_motor)

        self.btn_speed = QPushButton('Cambiar Velocidad', self)
        self.btn_speed.setGeometry(160, 110, 100, 50)
        self.btn_speed.clicked.connect(self.change_speed)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)

        self.pwm = GPIO.PWM(18, 1000) # Pin 18, frecuencia PWM 1000Hz
        self.pwm.start(50) # Duty cycle inicial: 50%

        self.direction = GPIO.HIGH # Dirección inicial: adelante

    def start_motor(self):
        # Iniciar el motor en la dirección actual
        self.pwm.start(50) # Reiniciar PWM
        GPIO.output(18, self.direction)

    def stop_motor(self):
        # Detener el motor
        self.pwm.stop()

    def reverse_motor(self):
        # Invertir la dirección del motor
        if self.direction == GPIO.HIGH:
            self.direction = GPIO.LOW
        else:
            self.direction = GPIO.HIGH

    def change_speed(self):
        # Cambiar la velocidad del motor
        duty_cycle = int(input("Ingrese el nuevo ciclo de trabajo (0-100): "))
        self.pwm.ChangeDutyCycle(duty_cycle)

if _name_ == '_main_':
    app = QApplication(sys.argv)
    window = MotorControl()
    window.show()
    sys.exit(app.exec_())