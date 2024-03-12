from __future__ import annotations

import serial

from slow_control.devices.device import Device


class ArduinoDevice(Device):
    def __init__(self, *, name: str, port: str):
        super().__init__(name=name)
        self._port = port
        try:
            self.open()
        except Exception as e:
            print(f"Failed to open {self.name} on port {self._port}: {e}")

    def open(self):
        self._handler = serial.Serial(self._port, 9600)
        self._open = True

    def close(self):
        self._handler = None
        self._open = False
