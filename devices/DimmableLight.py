from typing import ClassVar

from devices.LightDevice import LightDevice


class DimmableLight(LightDevice):
    """
    A light that also tracks a brightness level from 0-100.

    Invariant, enforced everywhere: state == "off" means brightness == 0, and
    brightness == 0 means state == "off". There is no such thing as a light
    that is on at zero brightness.
    """

    CAN_DIM: ClassVar[bool] = True

    # Where turn_on() lands if this light has never been dimmed.
    DEFAULT_ON_BRIGHTNESS: ClassVar[int] = 100

    def __init__(self, device_id: str, name: str, brightness: int = 100):
        super().__init__(device_id, name)
        # Starts off, so brightness starts at 0 to satisfy the invariant.
        self._brightness = 0
        # Private memory of the last non-zero level, so turning the light off
        # and on again restores the dim setting instead of blasting to full.
        self._last_on_brightness = self._clamp(brightness) or self.DEFAULT_ON_BRIGHTNESS

    # --- public API ---------------------------------------------------

    @property
    def brightness(self) -> int:
        """Current level, 0-100. Always 0 while the light is off."""
        return self._brightness

    def get_brightness(self) -> int:
        return self._brightness

    def set_brightness(self, level: int) -> int:
        """
        Set the level and return what was actually applied.

        0 turns the light off. Any non-zero level turns it on, since dimming a
        light the user thinks is off is almost always meant to turn it on.
        """
        level = self._clamp(level)

        if level == 0:
            self.turn_off()
            return 0

        self._send_command("brightness", level=level)
        self._brightness = level
        self._last_on_brightness = level
        self.state = "on"
        return level

    def turn_on(self) -> None:
        """Restore the level this light was last on at - never 0."""
        self.set_brightness(self._last_on_brightness)

    def turn_off(self) -> None:
        super().turn_off()
        self._brightness = 0

    def status(self) -> dict:
        return {**super().status(), "brightness": self._brightness}

    # --- helpers --------------------------------------------------------

    @staticmethod
    def _clamp(level: int) -> int:
        """
        Coerce and bound an incoming level.

        The dim_lights tool schema bounds brightness to 0-100, but models break
        schemas - they send 150, or "80". Clamping keeps a bad argument from
        raising inside main.py's unguarded dispatch call.
        """
        try:
            level = int(level)
        except (TypeError, ValueError):
            raise ValueError(f"brightness must be a number 0-100, got {level!r}")
        return max(0, min(100, level))

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(device_id={self.device_id!r}, "
            f"name={self.name!r}, state={self.state!r}, "
            f"brightness={self._brightness!r})"
        )
