"""
Solar Telemetry Performance Analyzer and Anomaly Detection Engine.
"""

from typing import List, Tuple
from .models import (
    InverterTelemetry,
    PerformanceMetrics,
    TelemetryAnomaly,
    TelemetryAnalysisResult,
    FaultType,
    FaultSeverity
)


class SolarTelemetryAnalyzer:
    # Standard crystalline silicon temperature coefficient: -0.38% / deg C
    TEMP_COEFFICIENT = -0.0038
    STC_TEMPERATURE_C = 25.0
    STC_IRRADIANCE_W_M2 = 1000.0

    # Operational thresholds
    HOTSPOT_THRESHOLD_C = 75.0
    MIN_EFFICIENCY_PCT = 91.0
    MIN_PR_WARNING_PCT = 75.0

    def analyze(self, telemetry: InverterTelemetry) -> TelemetryAnalysisResult:
        anomalies: List[TelemetryAnomaly] = []

        # 1. DC Power: P_dc (kW) = (V * I) / 1000
        dc_power_kw = round((telemetry.dc_voltage_v * telemetry.dc_current_a) / 1000.0, 3)

        # 2. Temperature Derated Expected Power Output
        # P_expected = P_stc * (G / 1000) * (1 + gamma * (T - 25))
        irradiance_ratio = telemetry.irradiance_w_per_m2 / self.STC_IRRADIANCE_W_M2
        temp_delta = telemetry.module_temp_c - self.STC_TEMPERATURE_C
        temp_derate_factor = max(0.5, 1.0 + (self.TEMP_COEFFICIENT * temp_delta))

        expected_power_kw = round(
            telemetry.rated_stc_capacity_kw * irradiance_ratio * temp_derate_factor,
            3
        )
        # Cap expected power if solar is below daylight threshold
        if telemetry.irradiance_w_per_m2 < 50.0:
            expected_power_kw = 0.0

        # 3. Inverter Conversion Efficiency: (P_ac / P_dc) * 100
        if dc_power_kw > 0.1:
            efficiency_pct = round((telemetry.ac_active_power_kw / dc_power_kw) * 100.0, 2)
            efficiency_pct = min(100.0, max(0.0, efficiency_pct))
        else:
            efficiency_pct = 0.0

        # 4. Performance Ratio: (P_actual / P_expected) * 100
        if expected_power_kw > 0.2:
            pr_pct = round((telemetry.ac_active_power_kw / expected_power_kw) * 100.0, 2)
            pr_pct = min(120.0, max(0.0, pr_pct))
        else:
            pr_pct = 100.0 if telemetry.irradiance_w_per_m2 < 50.0 else 0.0

        metrics = PerformanceMetrics(
            dc_power_kw=dc_power_kw,
            expected_power_kw=expected_power_kw,
            actual_power_kw=telemetry.ac_active_power_kw,
            inverter_efficiency_pct=efficiency_pct,
            performance_ratio_pct=pr_pct
        )

        # 5. Fault Detection & Anomaly Rules
        # Fault A: Thermal Hotspot
        if telemetry.module_temp_c >= self.HOTSPOT_THRESHOLD_C:
            anomalies.append(TelemetryAnomaly(
                fault_type=FaultType.THERMAL_HOTSPOT,
                severity=FaultSeverity.CRITICAL,
                message=f"Thermal hotspot detected: Module temperature ({telemetry.module_temp_c}°C) exceeds safe ceiling ({self.HOTSPOT_THRESHOLD_C}°C).",
                metric_value=telemetry.module_temp_c,
                threshold_value=self.HOTSPOT_THRESHOLD_C
            ))

        # Fault B: Open Circuit String Disconnect (Voltage present, current ~ 0 during sunlight)
        if telemetry.irradiance_w_per_m2 > 300.0 and telemetry.dc_voltage_v > 100.0 and telemetry.dc_current_a < 0.2:
            anomalies.append(TelemetryAnomaly(
                fault_type=FaultType.STRING_DISCONNECT,
                severity=FaultSeverity.CRITICAL,
                message=f"String open-circuit disconnect detected: Voltage is {telemetry.dc_voltage_v}V but Current is {telemetry.dc_current_a}A under {telemetry.irradiance_w_per_m2} W/m² sunlight.",
                metric_value=telemetry.dc_current_a,
                threshold_value=0.2
            ))

        # Fault C: Inverter Derating / Low Efficiency
        if dc_power_kw > 1.0 and efficiency_pct < self.MIN_EFFICIENCY_PCT:
            anomalies.append(TelemetryAnomaly(
                fault_type=FaultType.INVERTER_DERATING,
                severity=FaultSeverity.WARNING,
                message=f"Sub-optimal inverter conversion efficiency ({efficiency_pct}% < {self.MIN_EFFICIENCY_PCT}%).",
                metric_value=efficiency_pct,
                threshold_value=self.MIN_EFFICIENCY_PCT
            ))

        is_healthy = len([a for a in anomalies if a.severity == FaultSeverity.CRITICAL]) == 0

        return TelemetryAnalysisResult(
            inverter_id=telemetry.inverter_id,
            timestamp=telemetry.timestamp,
            metrics=metrics,
            anomalies=anomalies,
            is_healthy=is_healthy
        )
