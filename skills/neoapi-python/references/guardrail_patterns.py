"""Runnable NeoAPI guardrail patterns used by the skill regression tests."""

from __future__ import annotations

from typing import Any


def login_with_certificate(
    sdk: Any,
    user_id: str,
    login_password: str,
    cert_path: str,
    *,
    use_default_certificate_password: bool = False,
    cert_password: str | None = None,
) -> Any:
    """Login without ever converting a missing certificate password to ``""``."""

    if use_default_certificate_password:
        if cert_password is not None:
            raise ValueError(
                "Omit cert_password when using the official default-password mode."
            )
        return sdk.login(user_id, login_password, cert_path)

    if not cert_password:
        raise ValueError("A non-empty custom certificate password is required.")
    return sdk.login(user_id, login_password, cert_path, cert_password)


def decode_ws_price_state(data: dict[str, Any], field: str = "price") -> dict[str, Any]:
    """Decode numeric WebSocket prices with their field-specific limit flags."""

    flag_names = {
        "price": ("isLimitUpPrice", "isLimitDownPrice"),
        "bid": ("isLimitUpBid", "isLimitDownBid"),
        "ask": ("isLimitUpAsk", "isLimitDownAsk"),
    }
    if field not in flag_names:
        raise ValueError(f"Unsupported WebSocket price field: {field}")

    value = data.get(field)
    if value is not None and (
        not isinstance(value, (int, float)) or isinstance(value, bool)
    ):
        raise TypeError(f"WebSocket {field} must be numeric, got {type(value).__name__}")

    up_flag, down_flag = flag_names[field]
    is_limit_up = bool(data.get(up_flag, False))
    is_limit_down = bool(data.get(down_flag, False))
    return {
        "value": value,
        "is_zero_encoded": value == 0,
        "is_limit_up": is_limit_up,
        "is_limit_down": is_limit_down,
        "has_limit_marker": is_limit_up or is_limit_down,
    }
