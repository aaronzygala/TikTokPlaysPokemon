# main.py
import constants
import tiktok_live_client
import key_press_simulator
import queue
import backend
import os, sys
from threading import Thread
from singleton_instances import get_live_manager, get_key_simulator

def main():
    key_simulator = get_key_simulator()
    live_manager = get_live_manager()
    restart_thread = Thread(target=handle_restart, args=(key_simulator,live_manager))

    try:
        key_simulator.start()
        restart_thread.start()
        live_manager.run()

    finally:
        key_simulator.stop()
        restart_thread.join()
        live_manager.stop()

def handle_restart(key_sim, live_man):
    restart = False
    while not restart:
        # Check the restart flag
        restart = backend.restart

    try:
        # Stop the key press simulator thread
        key_sim.stop()
        live_man.stop()
        # Stop the Flask thread and wait for it to join
        backend.stop_server()

    finally:
        # Restart the application
        print("Restarting the application...")
        os.execv(sys.executable, ['python'] + sys.argv)

if __name__ == '__main__':
    try:
        backend.start_server()
        main()
    finally:
        backend.stop_server()
