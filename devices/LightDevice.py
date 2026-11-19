from abc import ABC, abstractmethod
from typing import ClassVar


class LightDevice(ABC):
    """
    Base class for every light Jarvis can control, and the full API for a
    plain non-dimmable light.

    Subclasses implement _send_command() and nothing else - that method is the
    single seam between this code and whatever vendor API, bridge or SDK
    actually drives the hardware. Everything above it stays vendor-agnostic.
    """

    # Constant per class, never per instance. A plain light cannot dim;
    # DimmableLight overrides this with True.
    CAN_DIM: ClassVar[bool] = False

    def __init__(self, device_id: str, name: str):
        self.device_id = device_id
        self.name = name
        self.state = "off"

    # --- public API ---------------------------------------------------

    def turn_on(self) -> None:
        self._send_command("on")
        self.state = "on"

    def turn_off(self) -> None:
        self._send_command("off")
        self.state = "off"

    def set_state(self, state: str) -> str:
        """
        Idempotent on/off, matching the string enum the toggle_lights tool
        already uses. Returns the resulting state so the tool layer has
        something to hand back to the model.
        """
        if state == "on":
            self.turn_on()
        elif state == "off":
            self.turn_off()
        else:
            raise ValueError(f"state must be 'on' or 'off', got {state!r}")
        return self.state

    def get_state(self) -> str:
        return self.state

    def is_on(self) -> bool:
        return self.state == "on"

    def status(self) -> dict:
        """Serializable snapshot - what a tool call reports back to the model."""
        return {
            "id": self.device_id,
            "name": self.name,
            "state": self.state,
            "can_dim": self.CAN_DIM,
        }

    # --- vendor seam ----------------------------------------------------

    @abstractmethod
    def _send_command(self, command: str, **kwargs) -> None:
        """
        Push a single command to the real hardware.

        command: "on", "off", or "brightness" (dimmable lights only).
        kwargs:  command-specific payload, e.g. level=75 for "brightness".

        Implementations should raise on transport failure so the caller can
        leave self.state untouched rather than reporting a lie.
        """
        ...

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(device_id={self.device_id!r}, "
            f"name={self.name!r}, state={self.state!r})"
        )
