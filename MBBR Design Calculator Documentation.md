# MBBR Design Calculator for Aquaculture RAS

**Created:** April 4, 2026  
**Purpose:** Technical documentation for an Excel-based MBBR (Moving Bed Biofilm Reactor) dimensioning tool tailored for Recirculating Aquaculture Systems (RAS)

---

## 1. Project Overview

### Objectives
- Develop a deep understanding of MBBR technology in land-based fish farming
- Gather practical data and design specifications
- Create a structured plan for an Excel-based dimensioning tool
- Produce actionable engineering calculations for reactor sizing

### Scope
This calculator is designed for RAS facilities with focus on nitrification performance in cold-water environments (e.g., Norway: 4-10°C winter temperatures).

---

## 2. Core Design Parameters

### Required Inputs

#### Production Parameters
- **Biomass** (kg) - Total fish biomass in system
- **Feed Rate** (kg/day) - Daily feed input
- **Protein Content** (%) - Feed protein percentage
- **Assimilation** (%) - Protein assimilation by fish (typically ~30%)
- **Safety Factor** - Design multiplier (usually 1.2-1.5)

#### Hydraulic Parameters
- **System Flow Rate** (m³/day)
- **Winter Water Temperature** (°C) - Most critical constraint
- **Incoming TAN** (mg/L) - Total Ammonia Nitrogen
- **Desired Effluent TAN** (mg/L) - Target water quality

#### Water Quality Targets
- **Alkalinity** (mg/L CaCO₃) - Buffering capacity
- **TSS** (mg/L) - Total Suspended Solids
- **pH** - Operating range

---

## 3. Design Methodology

### Ammonia Load Calculation (Two Methods)

**Method 1: Nitrogen Balance from Feed**
```
N_load (kg/day) = Feed (kg) × Protein% × 0.16 × (1 - Assimilation%) × 0.8
```
Where:
- 0.16 = nitrogen content in protein (16%)
- 0.8 = factor for uneaten feed + fecal matter (roughly 80% of N excreted as ammonia)
- Assimilation% = fraction of nitrogen retained in fish biomass (typical 25-35%)

**Method 2: Hydraulic Mass Balance**
```
N_load (kg/day) = Flow (m³/day) × (Incoming TAN - Effluent TAN) (mg/L) / 1000
```

**Design Value:** Use the larger of the two methods to ensure sizing safety.

---

### Temperature-Dependent Nitrification Rates

The nitrification rate (ammonia removal per unit media surface area) is highly temperature-sensitive. Use Arrhenius correction or lookup table:

**Reference Rate:** 0.0035 kg N/m²/day at 20°C (optimal)

**Temperature Correction Factor:**
```
Rate(T) = Rate(20°C) × exp[(-Ea/R) × (1/(T+273.15) - 1/(293.15))]
```
Where:
- Ea/R ≈ 6000-7000 K (activation energy parameter)
- T = temperature in °C

**Simplified Lookup Table:**

| Temperature (°C) | Removal Rate (kg N/m²/day) |
|------------------|----------------------------|
| 4                | 0.0008                     |
| 6                | 0.0011                     |
| 8                | 0.0015                     |
| 10               | 0.0018                     |
| 12               | 0.0023                     |
| 15               | 0.0030                     |
| 20               | 0.0035                     |
| 25               | 0.0042                     |

---

### Media Surface Area Requirement

```
Required Surface Area (m²) = N_load (kg/day) / Removal_Rate (kg N/m²/day)
```

**Note:** Use protected surface area (effective biofilm area), not total geometric area. Manufacturer specifications typically provide protected surface area.

---

### Reactor Volume Calculation

```
Reactor Volume (m³) = (Required Surface Area / Media Spec Surface Area) / Filling Fraction
```

Where:
- **Media Spec Surface Area** = protected surface area per m³ of media (typical 800-1500 m²/m³)
- **Filling Fraction** = proportion of reactor occupied by media (typical 0.40-0.70, design 0.50-0.60)

---

### Oxygen Demand Calculation

**Nitrification Oxygen:**
```
O2_nitrification (kg/day) = N_load (kg/day) × 4.57
```
(4.57 mg O₂ per mg NH₄⁺-N oxidized)

**BOD Oxidation (if applicable):**
```
O2_BOD (kg/day) = BOD_load (kg/day) × 1.42
```
(1.42 mg O₂ per mg BOD oxidized)

**Total Oxygen Demand:** Sum of both components + safety factor (1.2-1.5)

---

## 4. Media Selection

### Common MBBR Media Types (Kaldnes examples)

| Media Type | Protected Surface Area (m²/m³) | Dimensions (mm) | Typical Filling Fraction |
|------------|-------------------------------|-----------------|--------------------------|
| K1         | ~900                         | 7×7             | 60%                      |
| K3         | ~800                         | 15×8            | 50-60%                   |
| K5         | ~1500                        | 37×13           | 40-50%                   |

**Selection Criteria:**
- High protected surface area (not just total surface area)
- Appropriate density (floating with slight negative buoyancy)
- abrasion resistance
- bio-film retention under high shear

---

## 5. Excel Workbook Architecture

### Sheet Structure

**1. INPUTS**
- All design parameters (production, hydraulic, water quality)
- Media selection dropdown
- Temperature correction table
- Unit conversion helpers

**2. CALCULATIONS**
- Nitrogen load (both methods)
- Temperature-corrected removal rate (lookup from table)
- Required surface area
- Required reactor volume
- Oxygen demand sizing
- Hydraulic retention time (HRT)

**3. MEDIA_SPECS**
- Manufacturer data table (surface area, density, filling fraction recommendations)
- VLOOKUP formulas to pull properties based on selection

**4. RESULTS**
- Summary of calculated reactor volume
- Media quantity needed (volume × filling fraction)
- Oxygenation requirements
- Capital cost estimate (optional)
- Sensitivity analysis (temperature, filling fraction)

**5. CHECKSTEPS**
- Validation formulas to ensure:
  - No negative values
  - Temperatures within valid range
  - Filling fraction between 40-70%
  - Oxygen supply > demand

**6. OUTPUT_REPORT**
- Clean, printable summary page
- Key formulas displayed
- Recommendations section

---

## 6. Implementation Notes

### Formula Best Practices
- Use named ranges for readability
- Implement data validation for all user inputs (dropdowns, number bounds)
- Add conditional formatting for out-of-range values
- Protect calculation cells to prevent accidental edits

### VBA Features (Optional)
- Export to PDF summary report
- Scenario manager for multiple design options
- Unit converter utility

---

## 7. Advanced Considerations

### Two-Stage Configuration
For high organic loads or high TSS influent:
- **Stage 1:** High filling fraction (60-70%) for BOD removal
- **Stage 2:** High surface area media for nitrification

### Alkalinity Management
- Calculate alkalinity consumption: 7.14 mg CaCO₃ per mg NH₄⁺-N oxidized
- Include sodium bicarbonate dosing calculator

### Standard Oxygen Transfer Efficiency (SOTE)
- Varies with diffuser depth, salinity, water quality
- Use conservative values or site-specific testing

### Start-up Requirements
- Seeding with activated sludge or bio-media from existing system
- Gradual loading to establish biofilm
- Extended startup period in cold water (2-3× longer than warm climates)

---

## 8. Design Checklist

- [ ] Verify all input units (metric vs imperial)
- [ ] Use winter design temperature (minimum expected)
- [ ] Apply safety factor (1.2-1.5)
- [ ] Check media availability and cost
- [ ] Confirm oxygen supply meets demand + safety
- [ ] Include access for maintenance and media retrieval
- [ ] Ensure mixing and flow distribution (avoid short-circuiting)
- [ ] Design for worst-case TAN spikes

---

## 9. References

### Key Data Sources
- Kaldnes K-series media specifications (AnoxKaldnes)
- Peer-reviewed RAS MBBR performance studies
- Commercial RAS facility case studies (Norway, North America)
- Aeration design standards (ASCE, USEPA)

### Typical Performance Ranges
- **Filling fraction:** 40-70% (design 50-60%)
- **Media surface area:** 800-1500 m²/m³ protected
- **Nitrification rate @ 10°C:** 0.0018 kg N/m²/day
- **HRT:** 20-60 minutes for nitrification-only stage

---

## 10. Limitations & Assumptions

- Steady-state design (does not account for peak load transients)
- Assumes complete mixing in reactor zone
- Temperature correction based on empirical data (may need site calibration)
- Does not model biofilm thickness dynamics or sloughing events
- Assumes alkalinity is not limiting (needs separate check)

---

*Document compiled from technical research session on April 4, 2026. For use in Excel-based MBBR dimensioning tool development for aquaculture RAS.*