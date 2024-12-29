import time
import machine

# Configuración de pines
servo = machine.PWM(machine.Pin(2), freq=50)  # Configura el pin para el servo motor
ldr = machine.ADC(machine.Pin(34))           # Configura el pin para la fotorresistencia
ldr.atten(machine.ADC.ATTN_11DB)             # Amplía el rango a 0-3.3V

# Crear o abrir un archivo para guardar los datos
archivo = open("datos_luz.txt", "w")  # "a" para añadir datos al archivo

# Función para mover el servo a un ángulo específico
def mover_servo(angulo):
    duty = int((angulo / 180) * (125 - 25) + 25)  # Mapear 0-180° a 25-125
    servo.duty(duty)

try:
    # Encabezado del archivo
    if archivo.tell() == 0:  # Solo escribe el encabezado si el archivo está vacío
        archivo.write("Ángulo,Luz\n")

    # Escaneo de luz en incrementos de 5° desde 0° hasta 180°
    for angulo in range(0, 181, 5):
        mover_servo(angulo)           # Mueve el servo al ángulo actual
        time.sleep(1)                 # Pausa para estabilizar el movimiento

        lectura = ldr.read()          # Lee el valor de la fotorresistencia
        registro = "{},{}\n".format(angulo, lectura)  # Registro en formato CSV
        archivo.write(registro)       # Guarda los datos en el archivo
        print("Guardado:", registro)  # Imprime el registro en la consola

finally:
    # Limpieza al finalizar
    servo.deinit()       # Desactiva el servo
    archivo.close()      # Cierra el archivo

