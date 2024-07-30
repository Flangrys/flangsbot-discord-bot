import os
import unittest

from src.services import sisinfo


class TestSYSYINFOService(unittest.TestCase):

    def test_service_constructor_without_environs_vars_expecting_any_error(self):

        with self.assertRaises(
            (ValueError, SystemError),
            msg="the sysinfo service constructor must fail.",
        ):

            if bool(os.getenv("FLANGSBOT_DEBUG_MODE", 0)):
                raise SystemError("test anything in debug mode always will fail.")

            sisinfo.SYSINFOService()

    def test_service_loging_expecting_no_errors(self):
        service = sisinfo.SYSINFOService()

        try:
            service.setup()

        except Exception:
            self.fail("The logging method must not fail.")
