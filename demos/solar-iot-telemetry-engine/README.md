# Solar PV Digital Twin & IoT Telemetry Processing Engine Sandbox

**Author:** Norval Mendez (Lead Systems Architect & Senior Software Developer)  
**Context:** Reference CleanTech sandbox architecture modeled from IoT SCADA telemetry pipelines and digital twin analytics (`solar-engineering` and `nht-solar` architecture).

---

## 🎯 Architecture Overview

This sandbox implements the core signal processing and performance analytics algorithms used in solar digital twins and SCADA telemetry systems:

1. **IoT Stream Telemetry Ingestion**:
   - Parses streaming string inverter metrics (DC voltage, DC current, AC active power, module temperature, solar plane-of-array irradiance).
   - Validates physical telemetry bounds and sensor signal integrity.
2. **Standard Test Condition (STC) Yield Modeling**:
   - Computes temperature-derated expected power output:
     $$P_{\text{expected}} = P_{\text{STC}} \times \left( \frac{G}{1000 \, \text{W/m}^2} \right) \times \left[ 1 + \gamma \times (T_{\text{module}} - 25^\circ\text{C}) \right]$$
     *(where $\gamma \approx -0.0038 / ^\circ\text{C}$ for crystalline silicon).*
3. **Performance Ratio (PR) & Inverter Efficiency**:
   - Real-time conversion efficiency $\eta = \frac{P_{AC}}{P_{DC}}$.
   - Site-level Performance Ratio $PR = \frac{P_{\text{actual}}}{P_{\text{expected}}}$.
4. **Automated Fault & Anomaly Classification**:
   - **`THERMAL_HOTSPOT`**: Panel temperature spikes indicating cell degradation or bypass diode failure.
   - **`STRING_DISCONNECT`**: Open circuit voltage present with zero current flow.
   - **`INVERTER_DERATING`**: Thermal throttling or sub-optimal inverter conversion efficiency ($< 90\%$).
5. **Zero External Runtime Dependencies**:
   - Pure Python standard library with complete unit test suite.

---

## 🚀 Running the Tests
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```
