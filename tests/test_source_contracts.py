from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding='utf-8')


class PublicSourceContracts(unittest.TestCase):
    def test_local_config_is_ignored_and_not_allowlisted(self) -> None:
        self.assertIn('hardware/firmware/src/config.local.h', text('.gitignore'))
        allowlist = text('docs/source-allowlist.txt')
        self.assertNotIn('config.local.h', allowlist)
        self.assertNotIn('App.config', allowlist)
        self.assertNotIn('database.sql', allowlist)
        self.assertNotIn('SmartAgriculture/Data/', allowlist)

    def test_solution_has_one_public_desktop_entry(self) -> None:
        solution = text('SmartAgriculture.sln')
        self.assertIn('desktop\\SmartAgriculture.csproj', solution)
        self.assertNotIn('WinForms', solution)
        project = text('desktop/SmartAgriculture.csproj')
        self.assertIn('<TargetFramework>net8.0</TargetFramework>', project)
        self.assertNotIn('MySql', project)
        self.assertNotIn('System.Configuration', project)

    def test_desktop_has_no_login_database_or_device_control_surface(self) -> None:
        self.assertFalse((ROOT / 'desktop/Data').exists())
        for rel in ['desktop/ViewModels/LoginViewModel.cs', 'desktop/ViewModels/HistoryViewModel.cs',
                    'desktop/ViewModels/ThresholdViewModel.cs', 'desktop/Views/LoginView.axaml',
                    'desktop/Views/HistoryView.axaml', 'desktop/Views/ThresholdView.axaml',
                    'desktop/Views/ControlView.axaml']:
            self.assertFalse((ROOT / rel).exists(), rel)
        main_view = text('desktop/Views/MainWindow.axaml')
        self.assertNotIn('LoginView', main_view)
        self.assertNotIn('ControlView', main_view)
        self.assertIn('示例数据（非真机）', main_view)

    def test_desktop_network_and_commands_are_absent(self) -> None:
        monitor = text('desktop/ViewModels/MonitorViewModel.cs')
        parser = text('desktop/Services/TelemetryParser.cs')
        self.assertIn('DemoEnvironmentDataSource.CreateSample()', monitor)
        self.assertIn('TryImportTeachingJson', monitor)
        self.assertNotIn('TcpListener', monitor)
        self.assertNotIn('SendCommand', monitor)
        self.assertNotIn('Socket', monitor)
        self.assertIn('Network listening and device commands are intentionally absent', parser)
        self.assertNotIn('TcpListener', parser)
        self.assertNotIn('NetworkStream', parser)
        self.assertNotIn('SendCommand', parser)
        self.assertIn('json.Length > 4096', parser)

    def test_desktop_xaml_resources_are_defined(self) -> None:
        app = text('desktop/App.axaml')
        monitor = text('desktop/Views/MonitorView.axaml')
        self.assertIn('x:Key="TextSecondary"', app)
        self.assertIn('{StaticResource TextSecondary}', monitor)

    def test_firmware_defaults_disable_network_and_outputs(self) -> None:
        config = text('hardware/firmware/src/config.h')
        firmware = text('hardware/firmware/src/main.cpp')
        ini = text('hardware/firmware/platformio.ini')
        self.assertIn('#if __has_include("config.local.h")', config)
        self.assertLess(config.index('#if __has_include("config.local.h")'), config.index('#ifndef ENABLE_EXPERIMENTAL_WIFI_TCP'))
        self.assertIn('ENABLE_EXPERIMENTAL_WIFI_TCP == 1', config)
        self.assertIn('ENABLE_EXPERIMENTAL_ACTUATORS == 1', config)
        self.assertIn('[env:esp32-s3-public-default]', ini)
        default_environment = ini.split('[env:esp32-s3-public-default]', 1)[1].split(
            '[env:esp32-s3-network-telemetry-compile]', 1
        )[0]
        self.assertIn('-D ENABLE_EXPERIMENTAL_WIFI_TCP=0', default_environment)
        self.assertIn('-D ENABLE_EXPERIMENTAL_ACTUATORS=0', default_environment)
        self.assertIn('esp32-s3-network-telemetry-compile', ini)
        self.assertIn('esp32-s3-actuator-compile', ini)
        self.assertRegex(firmware, r'#else\s+// Do not configure actuator pins as output in the public default build\.\s+pinMode\(FAN_PIN_A, INPUT\);')
        self.assertNotIn('readStringUntil', firmware)
        self.assertNotIn('indexOf("\\\"fan', firmware)
        self.assertIn('no downlink commands', firmware)
        self.assertIn('Public default: observe only', firmware)

    def test_actuator_opt_in_stays_deenergized(self) -> None:
        firmware = text('hardware/firmware/src/main.cpp')
        self.assertIn('digitalWrite(FAN_PIN_A, LOW);', firmware)
        self.assertIn('digitalWrite(FAN_PIN_B, LOW);', firmware)
        self.assertIn('fill_solid(leds, NUM_LEDS, CRGB::Black);', firmware)
        self.assertIn('There is no automatic threshold control', firmware)

    def test_public_docs_preserve_boundaries_and_license_notice(self) -> None:
        self.assertIn('不是农业自动化产品', text('README.md'))
        self.assertIn('**未执行**当前公开 commit 的日期化复测', text('README.md'))
        self.assertIn('不代表无外设 I/O', text('README.md'))
        self.assertIn('没有 TCP listener', text('SECURITY.md'))
        notices = text('THIRD_PARTY_NOTICES.md')
        self.assertIn('Rob Tillaart', notices)
        self.assertIn('FastLED', notices)
        self.assertTrue((ROOT / 'LICENSES/ACD10-MIT.txt').is_file())

    def test_scanners_cover_core_publication_exclusions(self) -> None:
        for rel in ['scripts/secret_scan.py', 'scripts/check_repo.py']:
            scanner = text(rel)
            for value in ["'app.config'", "'config.local.h'", "'.pio'", "'bin'", "'obj'", "'.zip'"]:
                self.assertIn(value, scanner, rel)
        self.assertIn("'private LAN literal'", text('scripts/secret_scan.py'))

    def test_source_provenance_does_not_publish_local_path(self) -> None:
        provenance = text('docs/SOURCE_PROVENANCE.md')
        self.assertNotIn('/home/', provenance)
        self.assertIn('只读取该清单', provenance)
        self.assertNotIn('config.local.h\n', text('docs/source-allowlist.txt'))


if __name__ == '__main__':
    unittest.main()
