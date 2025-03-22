import time
import win32gui
import win32con
import win32process
import ctypes
import keyboard  # Importar la librería keyboard

# Cargar la función AttachThreadInput de la biblioteca de Windows
user32 = ctypes.WinDLL('user32', use_last_error=True)


def get_roblox_windows():
    roblox_windows = []

    def callback(hwnd, extra):
        # Obtener el título y la clase de la ventana
        window_text = win32gui.GetWindowText(hwnd)
        is_visible = win32gui.IsWindowVisible(hwnd)

        # Filtrar ventanas visibles que contengan 'Roblox' en el título
        if 'Roblox' in window_text and is_visible:
            roblox_windows.append(hwnd)

    # Enumerar todas las ventanas
    win32gui.EnumWindows(callback, None)
    return roblox_windows


def bring_window_to_foreground(hwnd):
    # Trae la ventana a primer plano
    foreground_hwnd = win32gui.GetForegroundWindow()
    foreground_thread_id = win32process.GetWindowThreadProcessId(foreground_hwnd)[0]
    target_thread_id = win32process.GetWindowThreadProcessId(hwnd)[0]

    # Adjuntar el hilo de entrada
    user32.AttachThreadInput(foreground_thread_id, target_thread_id, True)

    # Minimizar y restaurar la ventana para forzarla a primer plano
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

    win32gui.SetForegroundWindow(hwnd)
    user32.AttachThreadInput(foreground_thread_id, target_thread_id, False)


def send_input_to_window(hwnd):
    # Enfoca la ventana
    bring_window_to_foreground(hwnd)

    # Añadir un pequeño delay para asegurar que la ventana esté en foco
    time.sleep(0.5)  # Aumentar el delay para asegurar que la ventana esté lista

    # Verificar que la ventana está en foco antes de enviar el input
    if win32gui.GetForegroundWindow() == hwnd:
        # Usa la librería keyboard para presionar y mantener "espacio" por un breve momento
        keyboard.press('space')
        time.sleep(0.1)  # Mantener la tecla presionada por un corto tiempo
        keyboard.release('space')
    else:
        print("La ventana no está en foco. No se envió la tecla 'espacio'.")


def prevent_inactivity():
    roblox_windows = get_roblox_windows()

    if roblox_windows:
        interval = 60  # Intervalo en segundos para enviar inputs

        print(
            f"El script está en ejecución para {len(roblox_windows)} ventana(s) de Roblox. Para detenerlo, cierra la consola.")
        try:
            while True:
                for hwnd in roblox_windows:
                    send_input_to_window(hwnd)
                    print(f"Presionando tecla 'espacio' para evitar inactividad en la ventana con hwnd: {hwnd}...")

                    # Delay de 1 segundo entre ventanas
                    time.sleep(1)

                # Espera antes de repetir el ciclo
                time.sleep(interval)
        except KeyboardInterrupt:
            print("El script ha sido detenido.")
    else:
        print("No se encontraron ventanas de Roblox.")


if __name__ == "__main__":
    prevent_inactivity()
