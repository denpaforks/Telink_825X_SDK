import argparse
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import struct
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tools = load_module("telink_tools", "make/Telink_Tools.py")
firmware_tools = load_module("firmware_tools", "make/tl_firmware_tools.py")


class FakePort:
    def __init__(self, response=b""):
        self.response = response
        self.writes = []
        self.baudrate = 115200

    def flushInput(self):
        pass

    def flushOutput(self):
        pass

    def write(self, data):
        self.writes.append(data)
        return len(data)

    def inWaiting(self):
        return len(self.response)

    def read_all(self):
        result = self.response
        self.response = b""
        return result


class FlashProtocolTests(unittest.TestCase):
    def test_invalid_erase_ranges_do_not_write(self):
        port = FakePort()
        invalid = [(-tools.FLASH_SECTOR_SIZE, 1), (1, 1), (0, 0),
                   (0, 256), (tools.FLASH_SIZE, 1)]
        for address, sectors in invalid:
            with self.subTest(address=address, sectors=sectors):
                self.assertFalse(tools.telink_flash_erase(port, address, sectors))
        self.assertEqual([], port.writes)

    def test_invalid_write_ranges_do_not_write(self):
        port = FakePort()
        self.assertFalse(tools.telink_flash_write(port, -1, b"x"))
        self.assertFalse(tools.telink_flash_write(port, tools.FLASH_SIZE, b"x"))
        self.assertFalse(tools.telink_flash_write(port, 0, b""))
        self.assertEqual([], port.writes)

    def test_read_times_out_instead_of_blocking_forever(self):
        port = FakePort()
        ok, data = tools.telink_flash_read(port, 0x4000, 16, timeout=0.02)
        self.assertFalse(ok)
        self.assertEqual(b"", data)
        self.assertEqual(1, len(port.writes))

    def test_read_accepts_exact_response_length(self):
        port = FakePort(b"ABCDOK_02")
        ok, data = tools.telink_flash_read(port, 0x4000, 4, timeout=0.1)
        self.assertTrue(ok)
        self.assertEqual(b"ABCD", data)


class CommandSafetyTests(unittest.TestCase):
    def test_oversized_firmware_is_rejected_before_baud_change_or_erase(self):
        with tempfile.NamedTemporaryFile(delete=False) as firmware:
            firmware.seek(tools.MAX_FIRMWARE_SIZE)
            firmware.write(b"x")
            name = firmware.name
        self.addCleanup(lambda: os.path.exists(name) and os.unlink(name))
        args = argparse.Namespace(filename=name)
        with mock.patch.object(tools, "change_baud") as change_baud, \
                mock.patch.object(tools, "telink_flash_erase") as erase:
            self.assertFalse(tools.burn(FakePort(), args))
        change_baud.assert_not_called()
        erase.assert_not_called()

    def test_valid_firmware_is_written_in_256_byte_chunks(self):
        with tempfile.NamedTemporaryFile(delete=False) as firmware:
            firmware.write(b"A" * 300)
            name = firmware.name
        self.addCleanup(lambda: os.path.exists(name) and os.unlink(name))
        args = argparse.Namespace(filename=name)
        with mock.patch.object(tools, "change_baud"), \
                mock.patch.object(tools, "telink_flash_erase", return_value=True), \
                mock.patch.object(tools, "telink_flash_write", return_value=True) as write, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(tools.burn(FakePort(), args))
        self.assertEqual([256, 44], [len(call.args[2]) for call in write.call_args_list])
        self.assertEqual([0, 256], [call.args[1] for call in write.call_args_list])

    def test_triad_secret_is_redacted(self):
        secret = "11" * 16
        args = argparse.Namespace(productID="1", MAC="aabbccddeeff", Secret=secret)
        output = io.StringIO()
        with mock.patch.object(tools, "telink_flash_erase", return_value=True), \
                mock.patch.object(tools, "telink_flash_write", return_value=True), \
                contextlib.redirect_stdout(output):
            self.assertTrue(tools.burn_triad(FakePort(), args))
        self.assertNotIn(secret, output.getvalue())
        self.assertIn("[REDACTED]", output.getvalue())


class FirmwareUtilityTests(unittest.TestCase):
    def test_add_crc_appends_big_endian_crc32(self):
        import zlib

        payload = b"firmware-data"
        with tempfile.NamedTemporaryFile(delete=False) as firmware:
            firmware.write(payload)
            name = firmware.name
        self.addCleanup(lambda: os.path.exists(name) and os.unlink(name))
        with contextlib.redirect_stdout(io.StringIO()):
            firmware_tools.add_crc(argparse.Namespace(filename=name))
        data = Path(name).read_bytes()
        self.assertEqual(payload, data[:-4])
        self.assertEqual(zlib.crc32(payload) & 0xFFFFFFFF, struct.unpack(">I", data[-4:])[0])


if __name__ == "__main__":
    unittest.main()
