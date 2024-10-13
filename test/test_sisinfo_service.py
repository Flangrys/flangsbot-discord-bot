import unittest

from src.services import sisinfo


class TestSYSYINFOService(unittest.IsolatedAsyncioTestCase):

    async def test_service_loging_expecting_no_errors(self):
        sisinfo_service = sisinfo.SYSINFOService()

        try:
            await sisinfo_service.setup()
            await sisinfo_service.login()

            if sisinfo_service.is_session_closed():
                self.fail("The loging method fails to open a new session.")

            await sisinfo_service.logout()

        except Exception:
            self.fail("The loging method should not fail.")
