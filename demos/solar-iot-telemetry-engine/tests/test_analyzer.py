"""
Unit tests for Solar Telemetry Analyzer and Anomaly Detection.
"""

import unittest
from src.models import InverterTelemetry, FaultType, FaultSeverity
from src.analyzer import SolarTelemetryAnalyzer


class TestSolarTelemetryAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = SolarTelemetryAnalyzer()

    def test_nominal_operating_conditions(self):
        # 10 kW system under 800 W/m2 sunlight at 40 deg C
        telemetry = InverterTelemetry(
            inverter_id="inv-01",
            timestamp="2026-09-12T12:00:00Z",
            dc_voltage_v=600.0,
            dc_current_a=12.5,  # 7.5 kW DC
            ac_active_power_kw=7.2,  # 96% efficiency
            module_temp_c=45.0,
            irradiance_w_per_m2=800.0,
            rated_stc_capacity_kw=10.0
        )

        result = self.analyzer.analyze(telemetry)
        self.assertTrue(result.is_healthy)
        self.assertEqual(len(result.anomalies), 0)
        self.assertGreaterEqual(result.metrics.inverter_efficiency_pct, 95.0)
        self.assertAlmostEqual(result.metrics.dc_power_kw, 7.5, places=2)

    def test_thermal_hotspot_fault_detected(self):
        # Temperature spike to 82 deg C (above 75 deg C threshold)
        telemetry = InverterTelemetry(
            inverter_id="inv-02",
            timestamp="2026-09-12T13:30:00Z",
            dc_voltage_v=550.0,
            dc_current_a=10.0,
            ac_active_power_kw=5.2,
            module_temp_c=82.0,  # Hotspot!
            irradiance_w_per_m2=900.0,
            rated_stc_capacity_kw=10.0
        )

        result = self.analyzer.analyze(telemetry)
        self.assertFalse(result.is_healthy)
        self.assertTrue(any(a.fault_type == FaultType.THERMAL_HOTSPOT for a in result.anomalies))
        self.assertTrue(any(a.severity == FaultSeverity.CRITICAL for a in result.anomalies))

    def test_string_disconnect_detected(self):
        # High sunlight (850 W/m2) and DC voltage present (580V) but 0.05A current
        telemetry = InverterTelemetry(
            inverter_id="inv-03",
            timestamp="2026-09-12T11:15:00Z",
            dc_voltage_v=580.0,
            dc_current_a=0.05,  # Disconnect!
            ac_active_power_kw=0.0,
            module_temp_c=35.0,
            irradiance_w_per_m2=850.0,
            rated_stc_capacity_kw=10.0
        )

        result = self.analyzer.analyze(telemetry)
        self.assertFalse(result.is_healthy)
        self.assertTrue(any(a.fault_type == FaultType.STRING_DISCONNECT for a in result.anomalies))

    def test_inverter_derating_warning(self):
        # Inverter efficiency drops to 82% (below 91% threshold)
        telemetry = InverterTelemetry(
            inverter_id="inv-04",
            timestamp="2026-09-12T14:00:00Z",
            dc_voltage_v=600.0,
            dc_current_a=10.0,  # 6.0 kW DC
            ac_active_power_kw=4.9,  # 4.9 / 6.0 = 81.6% efficiency
            module_temp_c=50.0,
            irradiance_w_per_m2=700.0,
            rated_stc_capacity_kw=10.0
        )

        result = self.analyzer.analyze(telemetry)
        self.assertTrue(any(a.fault_type == FaultType.INVERTER_DERATING for a in result.anomalies))
        self.assertTrue(any(a.severity == FaultSeverity.WARNING for a in result.anomalies))


if __name__ == "__main__":
    unittest.main()
