"""
Domain models for Solar IoT Telemetry and Performance Analytics.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from datetime import datetime, timezone


class FaultSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    WARNING = "WARNING"
    INFO = "INFO"


class FaultType(str, Enum):
    THERMAL_HOTSPOT = "THERMAL_HOTSPOT"
    STRING_DISCONNECT = "STRING_DISCONNECT"
    INVERTER_DERATING = "INVERTER_DERATING"
    IRRADIANCE_SENSOR_FAULT = "IRRADIANCE_SENSOR_FAULT"
    SYSTEM_NOMINAL = "SYSTEM_NOMINAL"


@dataclass(frozen=True)
class InverterTelemetry:
    inverter_id: str
    timestamp: str
    dc_voltage_v: float
    dc_current_a: float
    ac_active_power_kw: float
    module_temp_c: float
    irradiance_w_per_m2: float
    rated_stc_capacity_kw: float = 10.0


@dataclass(frozen=True)
class PerformanceMetrics:
    dc_power_kw: float
    expected_power_kw: float
    actual_power_kw: float
    inverter_efficiency_pct: float
    performance_ratio_pct: float


@dataclass(frozen=True)
class TelemetryAnomaly:
    fault_type: FaultType
    severity: FaultSeverity
    message: str
    metric_value: float
    threshold_value: float


@dataclass(frozen=True)
class TelemetryAnalysisResult:
    inverter_id: str
    timestamp: str
    metrics: PerformanceMetrics
    anomalies: List[TelemetryAnomaly]
    is_healthy: bool
