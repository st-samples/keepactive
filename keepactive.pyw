import sys
import time
import threading
import pyautogui
import keyboard
import random
import base64
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QInputDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTemporaryFile

# Base64-encoded .ico file (embedded)
ICO_BASE64 = b"""
iVBORw0KGgoAAAANSUhEUgAAADIAAAAvCAYAAAChd5n0AAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw1AUhU9TpSIRBzuoOGSoTnZREcdSxSJYKG2FVh1MXvoHTRqSFBdHwbXg4M9i1cHFWVcHV0EQ/AFxF5wUXaTE+5JCixgvPN7Hefcc3rsPEJpVplk9MUDTbTOdiEu5/KoUekUAIkIYQVRmlpHMLGbhW1/31E11F+VZ/n1/1oBasBgQkIhjzDBt4g3i2U3b4LxPHGZlWSU+J5406YLEj1xXPH7jXHJZ4JlhM5ueJw4TS6UuVrqYlU2NeIY4omo65Qs5j1XOW5y1ap2178lfKBb0lQzXaY0hgSUkkYIEBXVUUIWNKO06KRbSdB738Y+6/hS5FHJVwMixgBo0yK4f/A9+z9YqTk95SWIc6H1xnI9xILQLtBqO833sOK0TIPgMXOkdf60JzH2S3uhokSNgcBu4uO5oyh5wuQMMPxmyKbtSkJZQLALvZ/RNeWDoFuhf8+bWPsfpA5ClWS3fAAeHwESJstd93t3XPbd/e9rz+wGg03K5tqMQZgAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+kBDQUeJ0UVWdgAAA/WSURBVGjezVl5eJNVuv+dbE3S5Es32pS2SXfatIYWqaUtlEWWAsO+jYisKuBc2WQedbYrM46I6BVGQEQRGFwQroLi1YIgyCJgW8rSAgOl0H1L0qbN1izfe/9IG2BaNh2V93nyPHm+75z3e3/nvOddfkeIDln6X89K3U7npkCO+11kz/DUvn3SxMMeHdpQUFTkxAMgzz41P1ClVIwKUHFPBakClsdGaxPnz517+NDRo7cOHDIw93GVUEgcY8QxRkrGKC4qqrVv79678gYPyZsxZarklzZ+zowZfkNy+o/VxcXtjuoRau20jWOMesjlrqkTJui7TOqdrPuMY4zSH9LzI0eMcKkEAi8ggFQCAfXSaksHZGY+PSFvpPznBjB6+HBlRlr6swla7WWVQEBKgDjGKFShIL0uuSlYKuU5xign45E/dc5hAPD7RYtku3fvLm+srla/9/EOGjdhPF9dVSU8deoUtm3ZiuMHvgFjDALG0CMioiwiIuKlMePG7Vj+4ouemw3YuGaN8PiJ7zXNLeYEk8mo5T18j6CQEM5gaGqXiCR2mVzWJJfJKgNVAVdHj8irnDJnlvvm+csXLRYfO35sVl1N7Z+M9XXazucjJkzE9BmPIzMzE2FhYYa/vrQicO0rfxfG6pK/PVN64VGfgpnTpsWHKRQejjE6XVREN4vNZqNjR4/RnJmzSAmQkjEKEIl4fa9eB0cOfTR+/uzZPXMyMuanJMTvStBoakMVCt9udvdTCQQUplS6UuPj6/vq9Z8NzM5+ctH8BWEjhw5NTYqNPaEUCMgfIH+AlixeTKeLiqi9vf0Wmz7fs5s4xihBo2n4y/PPy3xARgwa+JvOD9XW1FJ34nK56PixYzR+7FifUZqwMEd4YKBTAVDnr8N/KSk2jjLS+9Cg/rk0qH9/ykhLp8SYGAqWSm8BpgQoMjjEqVap2jt1PP7YdCoqKiKPx9OtLcWnTxPHGIWrVJ6p48dF+4AMzspeyjFGYUqO7HY73UksFgt9uH07RYf39O4QQD2Dg2jpokW0a+cndLqoiGpraqitrY3cLjfxPE88z5Pb5aK21laqrq6mwsJC+ujDD+jpefMoSOrnW4SUXkm0+7Pdd7WhqrLKtxBjhg8f4gOS2zdjNccY5Q0dettV+He5UFpKE8aN9xqQmEhGg5HuVyoqKkgdoCJ/gGbNnEnXrl27p3ktLc0+IMNyB84EABEAeIgCACAiKrLj+N9dknU6bH5/M/7nDR1+OHkKjLH7jk4CgQAR2mhMffExLFz4DJRK5T3N8/OTQiyRwOV0QiwWBfmAEIMfAMikMjAw2NosEEvEEPv53VFhYFAQXlqxAm63G35S6X0DiYyMxNHvv4efVAqBQHDX8e02GxgTQCAUQCgWw+V0gvfwYh8QkUgMACDiQUQ4f/AonFYLQuOioUnVQabwv61yoUgEoUj0o3OGTH73tNRqMKHiXCmaa+oQGh+L2D4Pgfd4OnbHm6dFAMB7PO0AYLPa4HI64Wi1AADqLl1DQ1kl9MMHISA0+FcpTWrLynHleEFH1mNoM5jg9njgdroAAC1mcxsACACA5z0mAKipqYbT7gCBeXMlY4hMTYIqJPBXq7FCtVEIidECTAgwBofVhnaHAzzv3RGZTN7iAyIWi+sA4FxBIYz1DSAABIbovnrE9NaB3YP//lwiEouRnJOB0DgtiBjcLjeqr1fcdPD9qn1A5HL5ZQCwWSw4c+QUiASITO0FrS7xR0Wj/7QIhEIkZvZBQIQaIIYT+w4DALjgELfMX37NB8RfoTjvHxDgJiLU1tQhKDIcsWm6BwLEjaAiREr/RyBVKVFVXQUAkCv9G3Q6XZMPyEN6fT0XEFBNAGpampCcnX5P4fCXFrGfBEnZfVBy+aL3fEjlZ//yt785fUD+++WXXf4KxXEAKCm/BKFYhAdVeAFDwZlCeD3J/zuf+wHAkzOfENmsVi1jQHVVFex2+wMLpLW1FU67HUQEt9utveXlsIGDRgeKxTzHGB08eIAeZOF5nja/9x4pAYoOV1unT53irX7XrlrFeiclfcUxRpMnTuxS+z+IYjQaKEGrJY4xyuyTvgIAhBFhavW5M8VrnQ6H6OXVq5GUnHzbbXU6nWhoqEezqRkikQgSyX+ujXe73WhsbIDJaIJQJIJYLL5t1JTJ5GBCIb7Nz4dEKu05YfyYt/HogAEzvM2QP9XV1RHfzQq43S7av28fjc7L85XPKYmJ9N6mTWQ2m3+yqxQWFNCM6dN9upNiY2nDunXU3Gy67bwzxcWkBChEJqMnpk5NQZpOt1EJ0IzHHiOXy9VlgsfjoU3vbCQlQHNnzaYD33xDX+z5nHL69SOOMXpq3lwym1t+NJD9+/eRWqWiqZMn0778fPpy7156dNAgUjJGM6ZPJ5Op+z6ntdVMKQkJxDFGuZmZC6BPSipQAvSPNWuIutmPUydPEscY9dHrqbGh8abnp3y00fp1b/0oEJWVFRQT0ZPiNBqqrKy40coWF/t257VXX+12rsfjoWcWLCAlQJlp6e8KXC5XHGMM0TEx6NJVEeGjDz8AESFVr0dIjxDfK2201kfDrHjxDzA0Nd33udi/bx8MNbVI1euhVqtv6NZoffXdyj//GfX1dd02ZZ3n2eVyJQjsVmsAAAQGdq1wrTYbjh7+Dg/n5qJfVhaqO0oDIkJRYaEPtsNiwdWrV+8byOFDh5Cg12P0mDGoqLhRCJ47d9ZX3XrcblwrL+92fkhIiDcgEIWJbG1trKMC7jLQ5XKirdWMCZMnY9KkSVg4fz7GjBsLg8GAD/+5HU8uWYx316wFANhstvsCQUSora5B/9xcTJkyBcuWLkV2dhZsdjs2/OMtLHxuOTa+8YZ3oRzt3erojJoSiUSGMIWCOMboxPffd/FDh91OA7KzSSUQUHxU1C00zto336Tr169TXMfzosKCbn3ZZrPdlhVZsmgRcYxRtFp9i+6li5dQY2Mj9eubQd1xbZ2ya+cnxDFGWX36XEMvrdbDMUbfHT7U7eCNGzZ0Idne3/wutTscxPM8lV25QgOysnyRy2g0+qJfQ3095WZn05hRo8hqtRARkd1m94Xs/K+/9lFKnbpXvfoqWSzesfX1dfTYtKnU0tJ9VNy2dStxjFFaUnIx+qSkNCgZo8/37Ol2cFNTE+Xm5NwCJCo0lLZu2UJ1tXU0sH8O7dm922uk3U5DcnPp6NEjPlLv+d8vpw3r1xHPe2mmHR9/RMuWLCHe4yG73U5zZs8i5U261QEBtGrlSjKbW2jS+PH02aef3jbqvbpyJXGM0SO9074WEfGXGRBaXu49rO0OB9avXwdLmwVarRZPzJqFLdu24blly/Dt3r0AAHNTE955ewNazS2YPXcefjNmjM/vW5qbcbWsDFlZ2aisuI79+fsQERWJCRMnIjg4BJcvX4HZ3AICIJVKsWrVaxAJhfjk/a0ACDazGZs3bYJSqcTYceMwdtxYtLW1YeOGDbDb7UhO1mHKtKlwu904XVjYcUbEF0QSqawAQP9vDxzEwoXPgIhgs9rQ1toKW2M9yNiAGKUMH7y9HkVLlqDkwkXYrFZoNFHIeCQT0THRvlJCKpViyfLlWPTkk9i+dRvOFRbi6QGDYDC3oV9aOiKjo3Hl4kVs37nT1+/0CA3FW+vWY/acuTh39izsDjs0Gg0eTusNbVAgYGwE2e2wGJpg471BhYjQ1NiEA19+6e0UOVURGzl06IhjBw/mMwAHTvyAjMy+3lWvqcS5r/agh78MSVE9vSvuzwHJfcBkt6eHPB4PiouLcWX/AUQ2mZAREwMXEU5eLYcxJhL64cOQlKyDQHD77pMMdUBZCZjbBTCGHy5dgdCfg27EWMgCg0AE7NqxC089Pg3KwCBX3qhRMQKNJupIuEbbQAD27PwCllYrLl68iFETp2DMgiUoLLnk+wCztoKqyu/ckgqF6Nu3L6ZNGI8B8bGQioRQikUYltgL0yZPgi4l5Y4gQNQBwgl07PTH+w5h8PS5eGL2HDSbTKivacSODz4BESE4LPREcqquVlhUfMYdFxMTYmyo7192/SrS9f0QGh6CUJkEL8+cggHpqV436KxEQ3uCcfdAD0nEQMkFLx9DAIklQHYm2N3IPAagxQTmsPq+Ofjh3hg9MBfBSanQaOOQv/cg3l77d4AxxPXq9YdN7285LwSAIYMHX6xvaJjb3FgvhVCClKQ0DB2bh+DwcK//iyQAFwTSJECgjroB6k72SKVAcDDQagFxHNjgAWBB98KPMbDgMJBE6v2O2A/CwFCE981GfEpvFJ0sxVvrX0d9dQUiYmNL9L31S4vPnrtx4TQgK+u5zjvEl55/mQqOnyO7zfHANFPNRjMd/OoEzfrtvM5rONeYvLzhPpf23VpNn17UZDJlNBsM8adOHkVgsBoSoQJyfynk/rJfjRrieR4V5bUoOlmKT3b+E59+/J63YNTrXz945Mg7XYAcOX7cM2TI4HynxzOiualJfeL4ITChCHJJAKzWdsj8/eAnlfxigIgIxqYWnC+6grOFJdiy7W3kf7EDAJCUlvZRVr/MZ08WFPBdgADA+dJS+/BhQz9185RjamyMOn+mECWXSqBUBMBlY2gxWcAEDDKZHwTCn4f3am93or7WgH+du4bLpddx9Mi3eHPNX3HpfBEEIhES9frNY8ePe/qV1a+7/j1GdJHlzy6SH/7uu5XXL1/+nbPdIQRjyModhtGjJiA+LhliPz/0CFOhR1ggAoM5yGSye74g6m7lbRY7TMZWNNW3oMVghsPuQOnFs9jzxQ6Unj4JAqAICrLHJya+oNVq123fsYPvLtjd/r572PCBV69efaOhqvJhj9sNApCo640Rw8ehV1IqeoSEQSQSwU8mgSpQASUnh8xfCj8/CcQSEYRCAVhHziCe4PHwcDvdcDicsFntaGuxocVkgcvphtvlRkNjLUovnMGXX/0vaq+XeUlsiYQiYmMPJsTHL/5s794Ld4rad5Q1r68W5e/bN7nyeuXyhqrKdFd7u8+nUtIfQUZGDjSaGISFhoNTqiCR+EEg7MwVBCLc+M8DjBg8vAcuVzvMZhMaGutQfq0MPxQcQ9mFszdYdrncExEdfVyjjV41a+bM/Em/ncbfLf3ck7ywbJmwpPRCf4PBMLfZaBxdV1ER7DWUfAFAGRiMmLheCO2hRmBQMKRSOUQiIRhj4D08rFYLTCYjmgz1KC+7BEuL6VZjBAL0jImu4zjVp6Fq9daHUlNOv/LaasI9ZZ8fIQvmzlNWVlbmGI3GkW2trbl2u01nrKu7b5KLAASrw+0KjitRKBSHuQDV/+n1+oLX33zTdr+6fnIsXfHHPwosbTauvPxqSrOpWWdz2OOETBBhs9lVcrlcZTG3eklxAXOIxCI7Y2iW+ElqJCLx5TC1+mJ4RMS/eoar25574QX6KXb8P9F06OnkQOOnAAAAAElFTkSuQmCC
"""

class MouseMover:
    def __init__(self):
        self.running = True
        self.paused = False
        self.tray_icon = None
        self.interval = 600  # Default interval in seconds (10 minutes)
        self.lock = threading.Lock()  # Lock for thread-safe interval updates

    def responsive_sleep(self, duration):
        """Sleep in small chunks to allow dynamic interval updates."""
        remaining = duration
        chunk_size = 1  # Check every 1 second
        while remaining > 0 and self.running:
            if self.paused:
                print("Paused. Sleeping for 1 second...")
                time.sleep(1)
            else:
                sleep_time = min(chunk_size, remaining)
                time.sleep(sleep_time)
                remaining -= sleep_time
                with self.lock:
                    current_interval = self.interval
                if current_interval != duration:
                    print(f"Interval changed during sleep. New interval: {current_interval} seconds.")
                    return  # Exit early to start using the new interval

    def move_mouse(self):
        while self.running:
            try:
                if not self.paused:
                    print("Moving mouse...")
                    if random.choice([True, False]):
                        pyautogui.move(-1, 0)
                    else:
                        pyautogui.move(1, 0)
                    with self.lock:
                        current_interval = self.interval
                    print(f"Mouse moved. Sleeping for {current_interval} seconds.")
                    self.responsive_sleep(current_interval)
                else:
                    print("Mouse movement paused.")
                    time.sleep(1)
            except Exception as e:
                print(f"Error in move_mouse: {e}")

    def press_f15(self):
        while self.running:
            try:
                if not self.paused:
                    print("Pressing F15...")
                    keyboard.press_and_release('F15')
                    with self.lock:
                        current_interval = self.interval
                    print(f"F15 pressed. Sleeping for {current_interval} seconds.")
                    self.responsive_sleep(current_interval)
                else:
                    print("F15 keypress paused.")
                    time.sleep(1)
            except Exception as e:
                print(f"Error in press_f15: {e}")

    def create_tray_icon(self):
        try:
            print("Creating tray icon...")
            self.tray_icon = QSystemTrayIcon()

            # Check if the system tray is available
            if not QSystemTrayIcon.isSystemTrayAvailable():
                print("System tray is not available on this system.")
                sys.exit(1)

            # Create a temporary .ico file from the embedded base64 data
            temp_icon = QTemporaryFile()
            temp_icon.setAutoRemove(False)  # Keep the file alive during runtime
            if temp_icon.open():
                temp_icon.write(base64.b64decode(ICO_BASE64))
                temp_icon.close()
                self.tray_icon.setIcon(QIcon(temp_icon.fileName()))
                print("Temporary icon file created and set.")
            else:
                print("Failed to create temporary icon file. Using default icon.")
                self.tray_icon.setIcon(QIcon(QApplication.style().standardIcon(QSystemTrayIcon.SP_MessageBoxInformation)))

            self.tray_icon.setToolTip("UwU")

            # Tray menu and actions
            self.tray_menu = QMenu()

            # Pause/Unpause action
            self.toggle_pause_action = QAction("Pause", self.tray_menu)
            self.toggle_pause_action.triggered.connect(self.toggle_pause)
            self.tray_menu.addAction(self.toggle_pause_action)

            # Interval adjustment options
            interval_menu = QMenu("Set Interval", self.tray_menu)
            short_interval = QAction("Short (1-5 min)", interval_menu)
            medium_interval = QAction("Medium (5-10 min)", interval_menu)
            long_interval = QAction("Long (10-30 min)", interval_menu)
            custom_interval = QAction("Custom Interval...", interval_menu)

            short_interval.triggered.connect(lambda: self.set_interval(60, 300))
            medium_interval.triggered.connect(lambda: self.set_interval(300, 600))
            long_interval.triggered.connect(lambda: self.set_interval(600, 1800))
            custom_interval.triggered.connect(self.set_custom_interval)

            interval_menu.addAction(short_interval)
            interval_menu.addAction(medium_interval)
            interval_menu.addAction(long_interval)
            interval_menu.addAction(custom_interval)

            self.tray_menu.addMenu(interval_menu)

            # Exit action
            self.exit_action = QAction("Exit", self.tray_menu)
            self.exit_action.triggered.connect(self.exit_script)
            self.tray_menu.addAction(self.exit_action)

            self.tray_icon.setContextMenu(self.tray_menu)
            self.tray_icon.show()
            print("Tray icon created successfully.")
        except Exception as e:
            print(f"Error creating tray icon: {e}")

    def set_interval(self, min_time, max_time):
        with self.lock:  # Lock to ensure thread safety
            self.interval = random.randint(min_time, max_time)
        print(f"Interval set to {self.interval} seconds.")

    def set_custom_interval(self):
        """Allow the user to set a custom interval."""
        try:
            value, ok = QInputDialog.getInt(None, "Set Custom Interval", 
                                            "Enter interval in seconds:", 
                                            min=1, max=86400)
            if ok:
                with self.lock:  # Lock to ensure thread safety
                    self.interval = value
                print(f"Custom interval set to {self.interval} seconds.")
        except Exception as e:
            print(f"Error setting custom interval: {e}")

    def toggle_pause(self):
        self.paused = not self.paused
        self.toggle_pause_action.setText("Unpause" if self.paused else "Pause")
        print(f"Paused state toggled: {self.paused}")

    def exit_script(self):
        print("Exiting script...")
        self.running = False
        self.tray_icon.hide()
        QApplication.quit()

if __name__ == '__main__':
    try:
        print("Starting application...")
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)

        mouse_mover = MouseMover()

        # Create threads for moving the mouse and pressing F15
        mouse_move_thread = threading.Thread(target=mouse_mover.move_mouse)
        f15_press_thread = threading.Thread(target=mouse_mover.press_f15)

        mouse_move_thread.daemon = True
        f15_press_thread.daemon = True

        print("Starting threads...")
        mouse_move_thread.start()
        f15_press_thread.start()

        # Create system tray icon
        mouse_mover.create_tray_icon()

        print("Application is running.")
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Unhandled exception in main: {e}")
