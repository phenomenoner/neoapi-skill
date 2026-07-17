"""Behavioral regression tests for GitHub Issues #1 and #2."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import unittest


DEFAULT_SKILL_ROOT = Path(__file__).parents[1] / "skills" / "neoapi-python"
SKILL_ROOT = Path(os.environ.get("NEOAPI_SKILL_ROOT", DEFAULT_SKILL_ROOT))
MODULE_PATH = SKILL_ROOT / "references" / "guardrail_patterns.py"
SPEC = importlib.util.spec_from_file_location("neoapi_guardrail_patterns", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load guardrail patterns from {MODULE_PATH}")
PATTERNS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PATTERNS)


class FakeSDK:
    def __init__(self) -> None:
        self.login_args: tuple[str, ...] | None = None

    def login(self, *args: str) -> tuple[str, ...]:
        self.login_args = args
        return args


class DefaultCertificateLoginTests(unittest.TestCase):
    def test_default_password_mode_calls_three_argument_login(self) -> None:
        sdk = FakeSDK()

        result = PATTERNS.login_with_certificate(
            sdk,
            "A123456789",
            "login-password",
            "client.pfx",
            use_default_certificate_password=True,
        )

        self.assertEqual(result, ("A123456789", "login-password", "client.pfx"))
        self.assertEqual(len(sdk.login_args or ()), 3)

    def test_default_password_mode_rejects_explicit_empty_password(self) -> None:
        with self.assertRaisesRegex(ValueError, "Omit cert_password"):
            PATTERNS.login_with_certificate(
                FakeSDK(),
                "A123456789",
                "login-password",
                "client.pfx",
                use_default_certificate_password=True,
                cert_password="",
            )

    def test_custom_password_mode_fails_closed_when_missing(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-empty"):
            PATTERNS.login_with_certificate(
                FakeSDK(), "A123456789", "login-password", "client.pfx"
            )


class WebSocketPriceTests(unittest.TestCase):
    def test_zero_price_preserves_matching_limit_flag(self) -> None:
        decoded = PATTERNS.decode_ws_price_state(
            {"price": 0, "isLimitUpPrice": True}, "price"
        )

        self.assertEqual(decoded["value"], 0)
        self.assertTrue(decoded["is_zero_encoded"])
        self.assertTrue(decoded["is_limit_up"])
        self.assertFalse(decoded["is_limit_down"])
        self.assertTrue(decoded["has_limit_marker"])

    def test_missing_boolean_flags_are_false(self) -> None:
        decoded = PATTERNS.decode_ws_price_state({"ask": 0}, "ask")

        self.assertFalse(decoded["is_limit_up"])
        self.assertFalse(decoded["is_limit_down"])
        self.assertFalse(decoded["has_limit_marker"])

    def test_market_string_hallucination_is_rejected(self) -> None:
        with self.assertRaisesRegex(TypeError, "must be numeric"):
            PATTERNS.decode_ws_price_state({"price": "市價"}, "price")


if __name__ == "__main__":
    unittest.main()
