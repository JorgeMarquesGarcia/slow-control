from __future__ import annotations

import time
from abc import ABC, abstractmethod

from slow_control.devices.device import Device


class Sensor(ABC):
    def __init__(self, device: Device):
        self._device: Device = device
        self._sensor_type: str
        self._measurement_value: any = None
        self._measurement_time: int = 0  # Unix time

    def __enter__(self):
        self._device.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._device.release()
        return False

    def update(self) -> None:
        self._update_measurement()
        self._update_time()

    @abstractmethod
    def _update_measurement(self) -> None:
        pass

    @abstractmethod
    def get_insert_sql(self) -> str:
        pass

    @property
    def measurement_value(self):
        return self._measurement_value

    @property
    def measurement_time(self):
        return self._measurement_time

    def _update_time(self):
        self._measurement_time = int(time.time())