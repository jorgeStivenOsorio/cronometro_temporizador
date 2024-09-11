import tkinter as tk  # Importa tkinter, un módulo de Python para crear interfaces gráficas de usuario
from tkinter import messagebox  # Importa el messagebox para mostrar ventanas emergentes de advertencia o error
import time  # Módulo para trabajar con tiempo
import threading  # Permite ejecutar procesos en segundo plano
import pygame  # Módulo para reproducir sonidos, importante para alertas sonoras

class CronometroTemporizadorApp:
    def __init__(self, root):
        """
        Inicializa la aplicación de cronómetro y temporizador.

        Parámetros:
        - root: la ventana principal de la aplicación, gestionada por tkinter.
        """
        self.root = root
        self.root.title("Cronómetro y Temporizador")
        self.root.geometry("400x300")  # Define el tamaño de la ventana de la app

        # Inicializa pygame para manejar los sonidos
        pygame.mixer.init()

        # Crea los elementos gráficos y resetea los valores iniciales
        self.create_widgets()
        self.reset()  # Resetea el estado inicial de la aplicación

    def create_widgets(self):
        """
        Crea y organiza los widgets (botones, etiquetas, etc.) de la interfaz gráfica.
        """
        # Etiqueta del cronómetro
        self.label_cronometro = tk.Label(self.root, text="Cronómetro", font=("Arial", 16))
        self.label_cronometro.pack(pady=10)

        # Display que muestra el tiempo del cronómetro
        self.display_cronometro = tk.Label(self.root, text="00:00:00", font=("Arial", 48))
        self.display_cronometro.pack(pady=10)

        # Botones de control del cronómetro
        self.boton_iniciar = tk.Button(self.root, text="Iniciar", command=self.iniciar_cronometro)
        self.boton_iniciar.pack(side=tk.LEFT, padx=10)

        self.boton_parar = tk.Button(self.root, text="Parar", command=self.detener_cronometro)
        self.boton_parar.pack(side=tk.LEFT, padx=10)

        self.boton_resetear = tk.Button(self.root, text="Resetear", command=self.reset_cronometro)
        self.boton_resetear.pack(side=tk.LEFT, padx=10)

        # Espacio en blanco entre cronómetro y temporizador
        tk.Label(self.root, text="").pack(pady=20)

        # Etiqueta del temporizador
        self.label_temporizador = tk.Label(self.root, text="Temporizador", font=("Arial", 16))
        self.label_temporizador.pack(pady=10)

        # Caja de entrada para el tiempo del temporizador
        self.entry_temporizador = tk.Entry(self.root, width=10, font=("Arial", 24))
        self.entry_temporizador.pack(pady=10)

        # Botones de control del temporizador
        self.boton_iniciar_temporizador = tk.Button(self.root, text="Iniciar Temporizador", command=self.iniciar_temporizador)
        self.boton_iniciar_temporizador.pack(side=tk.LEFT, padx=10)

        self.boton_resetear_temporizador = tk.Button(self.root, text="Resetear Temporizador", command=self.reset_temporizador)
        self.boton_resetear_temporizador.pack(side=tk.LEFT, padx=10)

    def reset(self):
        """
        Resetea los valores iniciales de la aplicación.
        """
        self.horas = 0
        self.minutos = 0
        self.segundos = 0
        self.cronometro_corriendo = False  # Variable para saber si el cronómetro está en funcionamiento
        self.temporizador_segundos = 0  # Segundos del temporizador
        self.display_cronometro.config(text="00:00:00")  # Reinicia la pantalla del cronómetro
        self.entry_temporizador.delete(0, tk.END)  # Borra el campo de entrada del temporizador

    def iniciar_cronometro(self):
        """
        Inicia el cronómetro. Verifica si ya está en funcionamiento.
        """
        if not self.cronometro_corriendo:
            self.cronometro_corriendo = True  # Cambia el estado a "corriendo"
            self.run_cronometro()  # Llama al método que actualiza el tiempo

    def detener_cronometro(self):
        """
        Detiene el cronómetro.
        """
        self.cronometro_corriendo = False  # Detiene la actualización del cronómetro

    def reset_cronometro(self):
        """
        Resetea el cronómetro a su valor inicial (00:00:00).
        """
        self.reset()  # Llama al método reset que también resetea el cronómetro

    def run_cronometro(self):
        """
        Actualiza el cronómetro cada segundo mientras esté corriendo.
        """
        if self.cronometro_corriendo:
            self.segundos += 1  # Incrementa los segundos
            if self.segundos == 60:
                self.segundos = 0
                self.minutos += 1
                if self.minutos == 60:
                    self.minutos = 0
                    self.horas += 1

            # Actualiza el texto mostrado en el display
            tiempo_formateado = f"{self.horas:02}:{self.minutos:02}:{self.segundos:02}"
            self.display_cronometro.config(text=tiempo_formateado)

            # Llama a esta función nuevamente después de 1 segundo
            self.root.after(1000, self.run_cronometro)

    def iniciar_temporizador(self):
        """
        Inicia el temporizador basado en el tiempo ingresado por el usuario.
        """
        try:
            # Convierte el valor ingresado en el cuadro de texto a entero
            tiempo = int(self.entry_temporizador.get())
            self.temporizador_segundos = tiempo
            self.run_temporizador()  # Comienza el temporizador
        except ValueError:
            # Si el usuario ingresa algo que no es un número, muestra un mensaje de error
            messagebox.showerror("Error", "Por favor, ingrese un número válido.")

    def reset_temporizador(self):
        """
        Resetea el temporizador a su valor inicial.
        """
        self.temporizador_segundos = 0  # Resetea los segundos del temporizador
        self.entry_temporizador.delete(0, tk.END)  # Limpia la caja de texto

    def run_temporizador(self):
        """
        Actualiza el temporizador cada segundo y emite una alerta sonora cuando llega a cero.
        """
        if self.temporizador_segundos > 0:
            self.temporizador_segundos -= 1  # Resta un segundo
            minutos, segundos = divmod(self.temporizador_segundos, 60)  # Calcula minutos y segundos restantes
            tiempo_formateado = f"{minutos:02}:{segundos:02}"  # Formato MM:SS
            self.entry_temporizador.delete(0, tk.END)  # Limpia la caja de texto
            self.entry_temporizador.insert(0, tiempo_formateado)  # Actualiza el valor mostrado

            # Llama a esta función nuevamente después de 1 segundo
            self.root.after(1000, self.run_temporizador)
        else:
            # Reproduce el sonido de alerta cuando el temporizador llega a cero
            pygame.mixer.music.load('alerta.mp3')  # Asegúrate de tener el archivo 'alerta.mp3'
            pygame.mixer.music.play()

# Código principal que ejecuta la aplicación
if __name__ == "__main__":
    root = tk.Tk()  # Crea la ventana principal de la aplicación
    app = CronometroTemporizadorApp(root)  # Crea una instancia de la clase CronometroTemporizadorApp
    root.mainloop()  # Ejecuta el bucle principal de eventos de tkinter
