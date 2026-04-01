# Work Breakdown Structure (WBS) in Complex Process Engineering & Land-Based Aquaculture

**Created**: April 2026  
**Sources**: PMI/PMBOK, CSI MasterFormat, FAO Aquaculture Guidelines, AACE International, API Standards, Engineering Textbooks  
**Focus**: Process plants with interconnected subsystems (piping, automation) and recirculating aquaculture systems (RAS)

---

## Part I: WBS Fundamentals for Complex Process Engineering

### 1.1 What Makes Process Engineering WBS Different?

Traditional WBS approaches (phase-based or deliverable-based) often fail for complex process facilities because:

- **Interconnected systems**: Piping networks tie together dozens of equipment packages
- **Integration-heavy**: Automation/control systems cross all physical boundaries
- **Regulatory complexity**: Permits, safety studies, environmental compliance span entire facility
- **Commissioning sequence-dependent**: You can't commission Unit A before Unit B's utilities are ready
- **Multi-discipline coordination**: Civil, structural, mechanical, piping, electrical, instrumentation must align

### 1.2 The 100% Rule Applied to Process Plants

```
Level 1: Complete Facility (100%)
  ├─ Level 2: Major Systems (each sums to 100%)
  │   ├─ Level 3: Subsystems
  │   │   ├─ Level 4: Equipment Packages
  │   │   │   ├─ Level 5: Individual Equipment Items
  │   │   │   │   └─ Level 6: Work Packages (procurement, fabrication, installation, test)
```

**Key**: Every parent element must sum to exactly 100% of its scope across children. No overlap, no gaps.

### 1.3 Common WBS Coding Schemes for Process Industries

#### Scheme A: Process-Unit-Based (Most Common for Plants)

```
1.0  Facility Management
2.0  Utilities (power, steam, cooling water, compressed air)
3.0  Process Units
  3.1  Unit 100 - Raw Materials & Storage
    3.1.1  Tank Farm
      3.1.1.1  Tank TK-101 ( specifications, procurement, installation )
      3.1.1.2  Tank TK-102
      3.1.1.3  Pumps & Transfer System
    3.1.2  Feed Preparation System
  3.2  Unit 200 - Core Process
    3.2.1  Reactor/Processor Vessel System
    3.2.2  Heat Exchanger Network
    3.2.3  Separator/Decanting System
    3.2.4  Process Piping (interconnecting)
  3.3  Unit 300 - Product Recovery
  3.4  Unit 400 - Waste Treatment
4.0  Control & Automation
  4.1  Control System Architecture
  4.2  Field Instruments (sensors, transmitters)
  4.3  Control Valves & Actuators
  4.4  Control Room / SCADA
  4.5  Network & Communications
5.0  Buildings & Civil
  5.1  Process Building
  5.2  Admin/Lab Building
  5.3  Site civil (roads, drainage, fencing)
6.0  Electrical & Power Distribution
7.0  Safety Systems (fire, gas detection, ESD)
8.0  Commissioning & Startup
9.0  Project Management & Engineering
```

#### Scheme B: CSI MasterFormat Integration (Construction-Focused)

```
Division 01 - General Requirements
  ├─ 01 10 00 Summary
  ├─ 01 20 00 Price and Payment Procedures
  ├─ 01 30 00 Administrative Requirements
  ├─ 01 40 00 Quality Requirements
  ├─ 01 50 00 Temporary Facilities and Controls
  ├─ 01 60 00 Product Requirements
  └─ 01 70 00 Execution and Closeout

Division 02 - Existing Conditions
Division 03 - Concrete
Division 04 - Masonry
Division 05 - Metals
Division 06 - Wood, Plastics, and Composites
Division 07 - Thermal and Moisture Protection
Division 08 - Openings
Division 09 - Finishes
Division 10 - Specialties
Division 11 - Equipment
Division 12 - Furnishings
Division 13 - Special Construction (unique process facilities)
Division 14 - Conveying Equipment (material handling)

Division 21 - Fire Suppression
Division 22 - Plumbing
Division 23 - Heating, Ventilating, and Air Conditioning (HVAC)
Division 25 - Integrated Automation (BACnet, etc.)

Division 31 - Earthwork
Division 32 - Exterior Improvements
Division 33 - Utilities (process water, wastewater, storm drainage)

Division 40 - Process Integration
  ├─ 40 05 00 Common Work Results for Process Systems
  ├─ 40 06 00 Schedules for Process Systems
  ├─ 40 07 00 Process Systems Insulation
  ├─ 40 08 00 Process Systems Commissioning
  ├─ 40 09 00 Process Systems Instrumentation
  ├─ 40 10 00 Process Piping
  │   ├─ 40 10 10 Process Piping Specialties
  │   ├─ 40 10 20 Piping Specialties
  │   ├─ 40 10 30 Piping Specialties (valves, fittings)
  │   └─ 40 10 90 Process Piping Tagging and Identification
  ├─ 40 20 00 Process Equipment
  │   ├─ 40 21 00 Pumps
  │   ├─ 40 22 00 Compressors
  │   ├─ 40 23 00 Tanks and Vessels
  │   └─ 40 24 00 Heat Exchangers
  ├─ 40 30 00 Process Specialties
  └─ 40 50 00 Process Mechanical Systems

Division 43 - Process Gas and Liquid Handling
  ├─ 43 11 00 Pumps, General Service
  ├─ 43 13 00 Pumps, Special Service
  ├─ 43 21 00 Compressors, Reciprocating
  └─ ...

Division 44 - Process Control and Analytics
  ├─ 44 10 00 Industrial Control Systems
  ├─ 44 20 00 Process Instrumentation
  │   ├─ 44 21 00 Temperature Instruments
  │   ├─ 44 22 00 Pressure Instruments
  │   ├─ 44 23 00 Flow Instruments
  │   └─ 44 24 00 Level Instruments
  └─ 44 30 00 Analytical Instruments
```

**Use**: CSI MasterFormat when construction execution, procurement, and specification writing are primary drivers. Best for EPC contracts.

#### Scheme C: Hybrid Approach (Recommended for Most)

Combine process unit structure with discipline integration:

```
1.0  Project Management & Engineering
  1.1  Project Management
  1.2  Process Engineering
  1.3  Mechanical Engineering
  1.4  Electrical Engineering
  1.5  Instrumentation & Controls Engineering
  1.6  Civil/Structural Engineering
  1.7  Safety Engineering
  1.8  Procurement
  1.9  Construction Management

2.0  Process Systems (by function)
  2.1  RAS Circulation System
    2.1.1  Intake & Screening
    2.1.2  Pumping System (main circulation pumps)
    2.1.3  Piping Network (main loops)
    2.1.4  Flow Control Valves
  2.2  Biofiltration System
    2.2.1  Biofilter Vessels (moving bed, trickling filter)
    2.2.2  Media & Support Structure
    2.2.3  Air/Water Distribution
  2.3  Temperature Control System
    2.3.1  Chillers/Heaters
    2.3.2  Heat Exchangers
    2.3.3  Temperature Sensors & Controls
  2.4  Oxygenation System
    2.4.1  Oxygen Concentrators/Generators
    2.4.2  Diffusers & Contact Towers
    2.4.3  DO Sensors & Control
  2.5  Solid Waste Removal
    2.5.1  Mechanical Filters (drum, screen)
    2.5.2  Settling Tanks
    2.5.3  Sludge Handling
  2.6  Water Quality Monitoring
    2.6.1  pH Systems
    2.6.2  Alkalinity & Hardness
    2.6.3  Ammonia/Nitrite/Nitrate Sensors
    2.6.4  TSS/Turbidity
  2.7  Disinfection System
    2.7.1  UV Reactors
    2.7.2  Ozone Generators
    2.7.3  Chemical Dosing

3.0  Building & Site Works
  3.1  Building Structure (steel, concrete)
  3.2  Roofing, Doors, Windows
  3.3  HVAC (building comfort)
  3.4  Plumbing (domestic)
  3.5  Electrical Power (main switchgear, distribution)
  3.6  Lighting (interior, exterior, emergency)
  3.7  Fire Protection (sprinklers, detection)
  3.8  Site Work (foundations, paving, drainage)

4.0  Instrumentation, Control & Automation
  4.1  Control System Architecture
    4.1.1  PLC/RTU Hardware
    4.1.2  HMIs & SCADA Software
    4.1.3  Network Infrastructure
  4.2  Field Instruments
    4.2.1  Flow Meters (magnetic, ultrasonic)
    4.2.2  Level Transmitters (ultrasonic, pressure)
    4.2.3  Pressure Transmitters
    4.2.4  Temperature Sensors (RTD, thermocouple)
    4.2.5  pH/ORP/DO Probes
    4.2.6  Water Quality Analyzers
  4.3  Final Control Elements
    4.3.1  Control Valves (size, material)
    4.3.2  Variable Frequency Drives (VFDs)
    4.3.3  Motor Starters
  4.4  Control Logic & Programming
    4.4.1  PLC/RTU Programming
    4.4.2  HMI Screen Development
    4.4.3  Alarm Management
    4.4.4  historian & Reporting
  4.5  Cybersecurity (firewalls, access control)

5.0  Commissioning & Start-up
  5.1  Pre-Commissioning (checkouts, flushing)
  5.2  Cold Commissioning (water-only tests)
  5.3  Biological Start-up (seed stock, bacteria inoculation)
  5.4  Performance Testing
  5.5  Operator Training
  5.6  As-Built Documentation

6.0  Support Systems
  6.1  Backup Power (generators, UPS)
  6.2  Compressed Air System
  6.3  Nitrogen System (if needed)
  6.4  Potable Water
  6.5  Waste Handling (sludge, spent media)
```

---

## Part II: WBS for Land-Based Aquaculture (RAS Focus)

### 2.1 Aquaculture Facility WBS - Functional Breakdown

Based on FAO sustainable aquaculture frameworks and industry best practices:

#### Level 1: Complete RAS Facility

##### Level 2A: Core Production Systems

```
2.1  Recirculating Aquaculture System (RAS)
  2.1.1  Water Intake & Pretreatment
    2.1.1.1  Source Water Supply (well, municipal, surface)
    2.1.1.2  Screening & Filtration (macro debris removal)
    2.1.1.3  Pumping System (intake pumps, redundancy)
  2.1.2  Water Treatment Train
    2.1.2.1  Mechanical Filtration
       - Drum filters / rotary screens
       - Bead filters /TPR filters
       - Settling tanks / clarifiers
    2.1.2.2  Biofiltration
       - Moving Bed Biofilm Reactors (MBBR)
       - Trickling filters / packed towers
       - Fluidized bed reactors
       - Submerged biofilters
    2.1.2.3  Gas Stripping (CO2 removal)
       - Air scouring / cascade systems
       - Packed columns
    2.1.2.4  Temperature Control
       - Heat exchangers (shell & tube, plate)
       - Chillers / refrigeration systems
       - Boilers / heating systems
    2.1.2.5  Oxygenation
       - Oxygen cones / contact tanks
       - Oxygen generators / PSA systems
       - Diffusers
    2.1.2.6  Disinfection (optional)
       - UV systems
       - Ozone generators
       - Chemical dosing
  2.1.3  Recirculation & Distribution
    2.1.3.1  Main circulation pumps (variable speed)
    2.1.3.2  Distribution manifold & headers
    2.1.3.3  Flow control valves (automated)
    2.1.3.4  Raceway / tank inlet structures
  2.1.4  Water Quality Monitoring
    2.1.4.1  Online sensors array
       - Temperature, DO, pH, ORP
       - Ammonia (NH3/NH4+), Nitrite, Nitrate
       - TSS, Turbidity, Alkalinity
    2.1.4.2  Data logging & historian
    2.1.4.3  Calibration equipment & spares
  2.1.5  Drainage & Effluent
    2.1.5.1  Tank drain systems
    2.1.5.2  Sludge collection & dewatering
    2.1.5.3  Effluent polishing (if required)
```

##### Level 2B: Fish Husbandry Systems

```
2.2  Fish Production Units
  2.2.1  Tank Systems
    2.2.1.1  Circular tanks (diameter, material, liners)
    2.2.1.2  Raceways (rectangular flow-through style)
    2.2.1.3  Tank manifolds & plumbing
    2.2.1.4  Tank supports / stands / pads
  2.2.2  Stocking & Harvest
    2.2.2.1  Fish transfer pumps / pumps with fish-safe impellers
    2.2.2.2  Transfer piping & hoses
    2.2.2.3  Anesthesia / staging tanks
    2.2.2.4  Harvest bins & equipment
  2.2.3  Feeding Systems
    2.2.3.1  Feed storage silos / bins
    2.2.3.2  Feed conveyors / pipelines
    2.2.3.3  Distribution dispensers / blowers
    2.2.3.4  Demand feeders (if used)
  2.2.4  Grading & Sorting Equipment
  2.2.5  Broodstock & Larval Rearing Areas (separate systems)

2.3  Fish Health & Biosecurity
  2.3.1  Health Monitoring
    2.3.1.1  Laboratory setup (microscope, water testing kits)
    2.3.1.2  Diagnostic equipment (PCR, etc.)
  2.3.2  Treatment Systems
    2.3.2.1  Quarantine tanks
    2.3.2.2  Bath treatment facilities
    2.3.2.3  Medication storage & handling
  2.3.3  Biosecurity Perimeter
    2.3.3.1  Footbaths, showers, changing rooms
    2.3.3.2  Vehicle disinfection
    2.3.3.3  Pest control (birds, rodents, insects)

2.4  Fish Handling & Processing (if on-site)
  2.4.1  Processing area (kill, gut, filet)
  2.4.2  Chilling / freezing systems
  2.4.3  Packaging equipment
  2.4.4  Cold storage
```

##### Level 2C: Automation & Control

```
3.0  Control & Automation System
  3.1  Control System Architecture
    3.1.1  PLC / RTU hardware specification
    3.1.2  SCADA / HMI software selection
    3.1.3  Network design (Ethernet, fiber, wireless)
    3.1.4  Redundancy design (dual controllers, UPS)
  3.2  Instrumentation Package
    3.2.1  Flow measurement (magnetic, ultrasonic)
    3.2.2  Level detection (ultrasonic, pressure)
    3.2.3  Pressure transmitters
    3.2.4  Temperature sensors (RTDs)
    3.2.5  Dissolved Oxygen probes (optical or polarographic)
    3.2.6  pH / ORP electrodes
    3.2.7  Water quality analyzers (ammonia, nitrite, nitrate)
    3.2.8  Conductivity / salinity
  3.3  Final Control Elements
    3.3.1  Control valves (ball, butterfly, diaphragm) with actuators
    3.3.2  Variable Frequency Drives (VFDs) for pumps
    3.3.3  Motor starters (soft starters)
    3.3.4  Dampers / louvers (if HVAC)
  3.4  Control Logic Development
    3.4.1  PLC programming (ladder logic, structured text)
    3.4.2  HMI screen development
    3.4.3  Alarm philosophy & management
    3.4.4  Data logging & trending
    3.4.5  Recipe management (if multi-species)
  3.5  Cybersecurity Measures
    3.5.1  Industrial firewalls
    3.5.2  Network segmentation (DMZ)
    3.5.3  Access control (AD/LDAP integration)
    3.5.4  Data encryption
```

##### Level 2D: Support Infrastructure

```
4.0  Building & Site Infrastructure
  4.1  Building Shell
    4.1.1  Foundations (piles, spread footings)
    4.1.2  Structural steel frame / concrete structure
    4.1.3  Walls (prefab panels, tilt-up, masonry)
    4.1.4  Roofing (waterproofing, insulation)
    4.1.5  Doors, windows, vents
  4.2  Building Services
    4.2.1  HVAC (heating, ventilation, air conditioning)
    4.2.2  Plumbing (domestic water, toilets, sinks)
    4.2.3  Electrical power distribution within building
    4.2.4  Lighting (high bay, LED)
    4.2.5  Fire protection (sprinklers, extinguishers)
  4.3  Site Development
    4.3.1  Site preparation (clearing, grading)
    4.3.2  Roads, parking, drives
    4.3.3  Drainage & stormwater management
    4.3.4  Fencing, gates, security
    4.3.5  Landscaping / erosion control

5.0  Utilities & Power
  5.1  Electrical Utility Connection
    5.1.1  Utility service application & coordination
    5.1.2  Main transformer / substation (if needed)
    5.1.3  Medium-voltage distribution
    5.1.4  Switchgear & panel boards
    5.1.5  Backup power generation
       - Generator sets (diesel, natural gas)
       - Automatic transfer switches (ATS)
       - Fuel storage (day tank, bulk)
       - Exhaust & ventilation
  5.2  Emergency Power Distribution
    5.2.1  UPS systems (for control systems)
    5.2.2  Critical load panels
    5.2.3  Generator paralleling (if multiple)
  5.3  Compressed Air System
    5.3.1  Air compressors
    5.3.2  Air receivers
    5.3.3  Dryers (refrigerant, desiccant)
    5.3.4  Distribution piping
  5.4  Other Utilities
    5.4.1  Nitrogen generation / storage
    5.4.2  Potable water (well, municipal)
    5.4.3  Wastewater treatment / discharge

6.0  Ancillary Systems
  6.1  Laboratory & Quality Control
  6.2  Storage Areas (feed, chemicals, spare parts)
  6.3  Workshop & Maintenance
  6.4  Office & Staff Amenities
  6.5  Vehicle Parking & Loading
```

---

### 2.2 FAO's Progressive Management Pathway (PMP) as WBS Framework

The FAO's **Progressive Management Pathway for Aquaculture Biosecurity** (2025) provides a structured, phased approach that maps well to WBS:

#### Phase 1: Initiation & Planning (WBS Level 1-2)
- Stakeholder analysis & engagement
- Baseline assessment of current biosecurity status
- Gap analysis against international standards
- Resource mobilization (budget, team)

#### Phase 2: Design & Development (WBS Level 3-4)
- Develop Biosecurity Plan
- Define Standard Operating Procedures (SOPs)
- Infrastructure requirements definition
- Training program design

#### Phase 3: Implementation (WBS Level 5 - Work Packages)
- Physical modifications (buildings, equipment)
- Procurement & installation
- SOP deployment
- Staff training execution
- Documentation system setup

#### Phase 4: Evaluation & Certification (WBS Commissioning)
- Internal audits
- External certification attempts
- Performance metrics review
- Continuous improvement cycle kickoff

**Application**: Use this phased structure as your Level 1-2 breakdown, then drill down into technical systems as Level 3+.

---

### 2.3 RAS-Specific WBS Considerations

#### Critical Path Dependencies

```
Design → Permits → Procurement → Fabrication → Installation → Pre-commissioning → Commissioning

Key constraint: Biofilter media cannot be added until after tank installation and piping pressure tests
Key constraint: Control system cannot be tested until all instruments are installed
Key constraint: Fish cannot be stocked until: 1) Water quality stabilized, 2) All systems commissioned, 3) Staff trained
```

#### Risk-Based WBS Elements

Add risk mitigation as explicit WBS elements:

```
9.0  Risk Mitigation & Contingency
  9.1  Water Quality Failure Prevention
    9.1.1  Redundant pumping (parallel pumps)
    9.1.2  Backup power for all critical systems
    9.1.3  Emergency water storage (reserve tank)
  9.2  Disease Outbreak Prevention
    9.2.1  Quarantine facility (separate system)
    9.2.2  Separate life support for broodstock
    9.2.3  UV/ozone disinfection capability
  9.3  Supply Chain Resilience
    9.3.1  Spare parts inventory (critical pumps, valves, sensors)
    9.3.2  Alternate suppliers identified
    9.3.3  Emergency spares procurement fund
```

---

## Part III: Integrating WBS with Engineering Deliverables

### 3.1 WBS → Document Matrix

Each WBS work package should produce specific deliverables:

| WBS Code | Deliverable | Format | Responsible Discipline |
|----------|-------------|--------|------------------------|
| 2.1.2.1.1 | Drum filter specification | PDF datasheet + P&ID | Mechanical / Process |
| 2.1.2.1.2 | Drum filter procurement package | Vendor drawings, specs, purchase req | Procurement |
| 2.1.2.1.3 | Drum filter installation | Installation record, test report | Mechanical / Construction |
| 4.1.1 | PLC control system architecture | Functional spec, IO list | Instrumentation |
| 4.1.2 | HMI screen mockups | PDF prototype | Controls |
| 4.2.1 | Flow meter calibration certificate | Calibration report | Instrumentation |
| 4.4.1 | PLC program | Source code, comments, version control | Controls |

### 3.2 WBS → Cost Code Alignment

For cost control, map WBS codes to your ERP/cost account structure:

```
Project: AQUA-001 NordicEPOD Trondheim
Cost Code Format: AA-BB-CC-DD-EE
AA = Project (AQUA)
BB = Phase (01=Design, 02=Procurement, 03=Construction, 04=Commissioning)
CC = WBS Level 2 code (01=RAS, 02=Buildings, 03=Control, 04=Utilities)
DD = Discipline (01=Mech, 02=Elec, 03=Inst, 04=Civil, 05=Procurement)
EE = Sequential

Example: AQUA-02-03-04-01-015
Meaning: Procurement phase, Control system, Electrical discipline, 15th cost account (PLC hardware)
```

---

## Part IV: Best Practices from Industry Standards

### 4.1 PMI/PMBOK Guidelines

- **Deliverable-oriented WBS**: Structure around tangible outputs (equipment, documents, systems), not activities
- **Work package**: Smallest unit assigned to a single responsible party; typically 40-80 hours
- **WBS Dictionary**: For each work package, document:
  - Description of work
  - Deliverables
  - Assumptions
  - Constraints
  - Responsible organization
  - Calendar

### 4.2 AACE International TCM Framework

AACE RP 10S-90 recommends:

- **Definition levels**:
  - Level 1: Project (0-2% scope defined)
  - Level 2: Major systems (10-20%)
  - Level 3: Subsystems (30-50%)
  - Level 4: Equipment/packages (60-80%)
  - Level 5: Work packages (90-100%)

- **Cost estimate classes**:
  - Class 5: Concept screening (Level 1-2)
  - Class 4: Feasibility / budget (Level 2-3)
  - Class 3: Controllable (Level 3-4)
  - Class 2: Detailed (Level 4-5)
  - Class 1: Final bid (Level 5)

Match WBS depth to estimate class and project phase.

### 4.3 CSI MasterFormat Principles

- **Divisions** align with construction trades, not process functions
- **Sections** within divisions define specific work results
- **Use 5-digit section numbers** for fine-grained control (e.g., 40 21 13 for centrifugal pumps)
- **Integrate with specifications**: Each WBS element should reference applicable spec sections

---

## Part V: Sample WBS for a 500-ton/year RAS Facility

### Top-Level Structure (4 Levels)

```
1.0  NordicEPOD Trondheim Facility
├─ 2.0  Project Management & Engineering
│   ├─ 2.1  Project Management
│   ├─ 2.2  Process Design Engineering
│   ├─ 2.3  Mechanical Engineering
│   ├─ 2.4  Electrical Engineering
│   ├─ 2.5  Instrumentation & Controls
│   ├─ 2.6  Civil/Structural Engineering
│   ├─ 2.7  Procurement
│   └─ 2.8  Construction Management
├─ 3.0  Recirculating Aquaculture System
│   ├─ 3.1  Water Intake & Pretreatment
│   │   ├─ 3.1.1  Well/pump station (if groundwater)
│   │   ├─ 3.1.2  Intake screens (1µm rotating drum)
│   │   └─ 3.1.3  Pre-filtration (sand/ multimedia)
│   ├─ 3.2  Biofiltration
│   │   ├─ 3.2.1  MBBR reactors (2x parallel, 250m³ each)
│   │   ├─ 3.2.2  Media (Kaldnes K5, 50% fill)
│   │   ├─ 3.2.3  Aeration grid
│   │   └─ 3.2.4  Media retention sieves
│   ├─ 3.3  Temperature Control
│   │   ├─ 3.3.1  Marine-source heat pump system (500kW)
│   │   ├─ 3.3.2  Plate heat exchangers (2x)
│   │   └─ 3.3.3  Control valves & sensors
│   ├─ 3.4  Oxygenation
│   │   ├─ 3.4.1  Oxygen concentrator (PSA, 100kg O₂/day)
│   │   ├─ 3.4.2  Oxygen cone (2000L, 3 units)
│   │   └─ 3.4.3  DO sensors (6x, optical)
│   ├─ 3.5  Solid Waste Removal
│   │   ├─ 3.5.1  Drum filters (200µm, 2x redundant)
│   │   ├─ 3.5.2  Protein skimmers (optional)
│   │   └─ 3.5.3  Sludge collection & storage
│   └─ 3.6  Water Quality Monitoring
│       ├─ 3.6.1  Ammonia/Nitrite/Nitrate analyzers
│       ├─ 3.6.2  pH/ORP system
│       ├─ 3.6.3  TSS/Turbidity sensors
│       └─ 3.6.4  Data historian server
├─ 4.0  Fish Production Systems
│   ├─ 4.1  Production Tanks
│   │   ├─ 4.1.1  Circular tanks (Ø8m, 6 units)
│   │   ├─ 4.1.2  Raceway tanks (25m x 4m, 4 units)
│   │   ├─ 4.1.3  Tank liners (epoxy-coated)
│   │   └─ 4.1.4  Tank plumbing manifolds
│   ├─ 4.2  Recirculation Loops
│   │   ├─ 4.2.1  Main circulation pumps (VFD, 200m³/h x 3)
│   │   ├─ 4.2.2  Piping network (HDPE, 200-400mm)
│   │   ├─ 4.2.3  Automated control valves
│   │   └─ 4.2.4  Flow meters (mag type)
│   ├─ 4.3  Feeding System
│   │   ├─ 4.3.1  Feed silos (20-ton capacity, 2x)
│   │   ├─ 4.3.2  Feed conveyors (screw, pneumatic)
│   │   └─ 4.3.3  Distribution dispensers (12x tanks)
│   └─ 4.4  Fish Handling Equipment
│       ├─ 4.4.1  Fish pumps (airlift, centrifugal)
│       ├─ 4.4.2  Transfer piping
│       └─ 4.4.3  Harvest bins & grading table
├─ 5.0  Control & Automation System
│   ├─ 5.1  Control System Hardware
│   │   ├─ 5.1.1  PLC controllers (Siemens S7-1500, 2x redundant)
│   │   ├─ 5.1.2  RTU I/O modules (distributed I/O cabinets)
│   │   ├─ 5.1.3  HMIs (industrial touch panels, 3x)
│   │   └─ 5.1.4  SCADA server & historian
│   ├─ 5.2  Instrumentation Package
│   │   ├─ 5.2.1  Flow instrumentation (magnetic flowmeters, 20x)
│   │   ├─ 5.2.2  Level transmitters (ultrasonic, 12x)
│   │   ├─ 5.2.3  Pressure transmitters (15x)
│   │   ├─ 5.2.4  Temperature (RTDs, 30x)
│   │   ├─ 5.2.5  DO (optical, 12x)
│   │   ├─ 5.2.6  pH/ORP (10x)
│   │   └─ 5.2.7  Water quality analyzers (ammonia, 2x)
│   ├─ 5.3  Final Control Elements
│   │   ├─ 5.3.1  Control valves (butterfly, 50mm-300mm, 25x)
│   │   ├─ 5.3.2  VFDs (15x, 5-200kW)
│   │   └─ 5.3.3  Motor starters (direct-on-line, 20x)
│   └─ 5.4  Network & Cybersecurity
│       ├─ 5.4.1  Industrial Ethernet switches (managed)
│       ├─ 5.4.2  Firewall / DMZ
│       └─ 5.4.3  Remote access VPN
├─ 6.0  Building & Infrastructure
│   ├─ 6.1  Production Building
│   │   ├─ 6.1.1  Foundations (piles, grade beams)
│   │   ├─ 6.1.2  Structural steel frame (300 tons)
│   │   ├─ 6.1.3  Wall panels (insulated metal)
│   │   ├─ 6.1.4  Roofing (waterproof, insulated)
│   │   └─ 6.1.5  Doors & high bays
│   ├─ 6.2  Building Services
│   │   ├─ 6.2.1  HVAC (unit heaters, exhaust fans)
│   │   ├─ 6.2.2  Electrical lighting (LED high bay)
│   │   ├─ 6.2.3  Fire suppression (ESFR sprinklers)
│   │   └─ 6.2.4  Domestic plumbing
│   └─ 6.3  Site Works
│       ├─ 6.3.1  Site preparation & excavation
│       ├─ 6.3.2  Roads & parking (asphalt)
│       ├─ 6.3.3  Drainage & erosion control
│       └─ 6.3.4  Fencing & gates
├─ 7.0  Power & Utilities
│   ├─ 7.1  Electrical Power
│   │   ├─ 7.1.1  Utility transformer & connection
│   │   ├─ 7.1.2  Main switchgear (12kV)
│   │   ├─ 7.1.3  Distribution panels (400V)
│   │   └─ 7.1.4  Backup generator (500kW diesel)
│   ├─ 7.2  Emergency Systems
│   │   ├─ 7.2.1  UPS (10kVA, 30min)
│   │   └─ 7.2.2  Automatic transfer switch
│   └─ 7.3  Compressed Air
│       ├─ 7.3.1  Air compressor (50kW, 2x)
│       ├─ 7.3.2  Air dryer (desiccant)
│       └─ 7.3.3  Piping distribution
├─ 8.0  Fish Health & Biosecurity
│   ├─ 8.1  Quarantine System
│   │   ├─ 8.1.1  Separate life support (small RAS)
│   │   └─ 8.1.2  Transport tanks & aeration
│   ├─ 8.2  Laboratory
│   │   ├─ 8.2.1  Microscopes & water testing
│   │   ├─ 8.2.2  Growth/health monitoring equipment
│   │   └─ 8.2.3  Sample storage (freezer)
│   └─ 8.3  Biosecurity Perimeter
│       ├─ 8.3.1  Footbaths & showers
│       ├─ 8.3.2  Vehicle disinfection station
│       └─ 8.3.3  Pest control system
├─ 9.0  Commissioning & Start-up
│   ├─ 9.1  Pre-commissioning
│   │   ├─ 9.1.1  Piping pressure tests
│   │   ├─ 9.1.2  Electrical megger tests
│   │   ├─ 9.1.3  Instrument loop checks
│   │   └─ 9.1.4  Control system factory acceptance test (FAT)
│   ├─ 9.2  Cold Commissioning
│   │   ├─ 9.2.1  System flushing & cleaning
│   │   ├─ 9.2.2  Pump tests (flow, head)
│   │   ├─ 9.2.3  Control system site acceptance test (SAT)
│   │   └─ 9.2.4  Alarm & safety function tests
│   ├─ 9.3  Biological Commissioning
│   │   ├─ 9.3.1  System inoculation (nitrifying bacteria)
│   │   ├─ 9.3.2  Nitrification cycle monitoring (4-6 weeks)
│   │   ├─ 9.3.3  Water quality stabilization
│   │   └─ 9.3.4  Test fish stocking (small batch)
│   └─ 9.4  Performance & Ramp-up
│       ├─ 9.4.1  Full stocking
│       ├─ 9.4.2  Production ramp-up plan
│       ├─ 9.4.3  Operator training
│       └─ 9.4.4  Handover documentation
└─ 10.0  Project Indirects
    ├─ 10.1  Insurance & Bonds
    ├─ 10.2  Permits & Fees
    ├─ 10.3  Travel & Living
    └─ 10.4  Contingency (both cost & schedule)
```

---

## Part VI: WBS Development Process for Process/Aquaculture Projects

### Step 1: Define Scope from Process Flow Diagram (PFD)

- Start with PFD that shows major equipment, streams, and operating conditions
- Identify major subsystems that will become Level 2-3 elements
- Include utilities, controls, support systems that PFD may omit

### Step 2: Select Coding System

- If construction-heavy: MasterFormat
- If process-functional: Unit-based hierarchy
- If hybrid: Combine both (process units for Level 2+, disciplines integrated within)
- Ensure compatibility with your cost control system

### Step 3: Decompose to Work Package Level

**Rule**: Work package should be small enough to:
- Be assigned to a single contractor/team
- Have clear completion criteria
- Be estimated with ±10% accuracy
- Take 1-4 weeks to execute

**Example decomposition**:
```
3.2.1 MBBR Reactors (Level 3)
├─ 3.2.1.1 Equipment procurement (work package)
├─ 3.2.1.2 Foundations & civil works (work package)
├─ 3.2.1.3 Reactor installation & assembly (work package)
├─ 3.2.1.4 Piping connections (work package)
├─ 3.2.1.5 Aeration system installation (work package)
├─ 3.2.1.6 Media loading (work package)
└─ 3.2.1.7 Initial testing & certification (work package)
```

### Step 4: Map to Engineering Deliverables

For each work package, identify required drawings, specs, and procedures:
- Procurement: Datasheets, vendor drawings
- Construction: Installation detail drawings, welding procedures
- Commissioning: Test procedures, checklists, punch lists

### Step 5: Integrate with Schedule

Import WBS into scheduling software (MS Project, Primavera P6) as activity codes. Each work package becomes a summary activity; leaf nodes become actual scheduled activities.

### Step 6: Review & Validate

- Walk through with engineering team
- Check 100% rule: every piece of scope is in some WBS element
- Check mutually exclusive: no doublecounting between branches
- Verify alignment with contract WBS if EPC

---

## Part VII: Tools & Templates

### 7.1 MS Project / Primavera P6 WBS Coding

In MS Project:
- Use **Outline Number** field for automatic numbering (1, 1.1, 1.1.1)
- Or use custom **WBS Code** field with manual coding scheme
- Set **WBS Code Mask** to define format (e.g., "AN" for alphanumeric)

In Primavera P6:
- **WBS**tab → define hierarchical structure
- Use **Activity ID** coding separate from WBS
- Export to Excel for reporting

### 7.2 Spreadsheet Template Structure

```
Column A: WBS Code (1.2.3)
Column B: Description
Column C: Discipline
Column D: Deliverable
Column E: Estimated Hours
Column F: Estimated Cost
Column G: Start Date
Column H: Finish Date
Column I: Responsible Party
Column J: Status
Column K: Notes
```

### 7.3 WBS Dictionary Template

One page per work package (leaf node):

```
WBS Code: 3.2.1.4
Description: Piping connections for MBBR reactor to manifold
Discipline: Piping
Scope Includes:
  - All pipe spools from reactor outlet to header
  - Flange connections, gaskets, bolts
  - Pipe supports as per detail drawings
  - Hydrostatic test of installed piping
  - Paint/coating touch-up after installation
Exclusions:
  - Reactor vessel installation (separate WBS)
  - Control valve installation
Deliverables:
  - Installed, tested, painted piping system
  - P&ID markups showing as-built
  - Hydrostatic test report
Acceptance Criteria:
  - No leaks at test pressure (1.5x design)
  - Alignment within ±5mm
  - Paint thickness meets spec
Assumptions:
  - Reactor vessel already installed
  - Piping materials procured under separate WBS
Constraints:
  - Work window: 3-5 days while reactor offline
  - Requires crane access
Resources:
  - Piping crew (4 people, 5 days)
  - Crane (40-ton, 2 days)
  - Hydrotest pump
Related WBS:
  - 3.2.1.1 (reactor procurement)
  - 3.2.1.3 (reactor installation)
  - 5.2.2 (instrumentation on this piping)
```

---

## Part VIII: Common Pitfalls & Solutions

| Pitfall | Cause | Solution |
|---------|-------|----------|
| WBS too shallow (only 3 levels) | Fear of detail, rushed schedule | Decompose to work package level before estimating; use discipline leads to break down |
| WBS too deep (10+ levels) | Micromanagement, poor aggregation | Keep to 4-6 levels; merge work packages that share resources |
| Mixing activities with deliverables | Activity-based WBS instead of deliverable-oriented | Reframe nodes: "Install pump" → "Pump installation package" (includes procurement, testing, docs) |
| Missing systems integration work | Focus on physical equipment over software/controls | Explicitly include "System Integration" WBS elements with verification testing |
| No clear ownership | Multiple disciplines claim same work | Assign single responsible party per work package in WBS dictionary |
| WBS doesn't match contract structure | EPC contractor uses different breakdown | Create mapping table: Contractor WBS code ↔ Your WBS code |
| Change orders create new branches | Uncontrolled scope changes | Use change order process to update WBS baseline, maintain version control |
| Cost accounts misaligned | WBS codes don't match ERP structure | Design WBS hierarchy to match cost code structure from day 1 |

---

## Part IX: References & Further Reading

### Standards & Guidelines
- **PMI Practice Standard for Work Breakdown Structures** (PMI, 2019)
- **AACE International Recommended Practice 10S-90**: Cost Engineering Terminology
- **CSI/CSC MasterFormat 2026** - Construction specifications classification
- **CSI/CSC UniFormat** - Early-stage project classification
- **MIL-STD-881F**: Work Breakdown Structures for Defense Materiel Items (DoD, 2022)
- **FAO Fisheries and Aquaculture Department**: Guidelines for Sustainable Aquaculture (2025)

### Books
- *A Guide to the Project Management Body of Knowledge (PMBOK® Guide)* - 7th Edition
- *Total Cost Management (TCM) Framework* - AACE International
- *Project Management for the Complex Projects* -especially relevant for process plants
- *Recirculating Aquaculture* by Timmons and Ebeling (the RAS bible)

### Industry Resources
- **MPUG.com** - Microsoft Project User Group (case studies)
- **Engineering News-Record (ENR)** - Construction industry practices
- **FAO Fisheries & Aquaculture** - https://www.fao.org/fishery/en
- **World Aquaculture Society** - https://www.world-aquaculture.org

### Software-Specific
- **Microsoft Project**: WBS Code Masks, Outline Numbering, integration with Excel
- **Oracle Primavera P6**: WBS structure, Activity IDs, OBS (Organizational Breakdown Structure)
- **SAP Project System**: WBS elements, network activities

---

## Appendix: Quick Reference - WBS Code Libraries

### Common Process Plant WBS Codes (Recommended)

```
1 - Project Management
2 - Process Engineering
3 - Mechanical / Equipment
4 - Piping
5 - Electrical
6 - Instrumentation
7 - Civil/Structural
8 - Building
9 - Commissioning
10 - Permits & Regulatory
11 - Procurement
12 - Construction Management
13 - Start-up & Training
14 - Closeout
```

### Sample Code to Meaning Mapping

```
3.1.2.1 = Mechanical → Equipment → Pumps → Centrifugal → Specification
3.1.2.2 = Mechanical → Equipment → Pumps → Centrifugal → Procurement
3.1.2.3 = Mechanical → Equipment → Pumps → Centrifugal → Installation
4.2.3 = Piping → Piping Systems → Utility Piping → Instrument Air
6.1.5 = Instrumentation → Control System → PLC Programming
9.2.1 = Commissioning → Pre-commissioning → Piping Pressure Tests
```

---

**End of Document**

*This guide synthesizes industry standards (PMI, AACE, CSI), FAO aquaculture methodologies, and best practices for complex process facility WBS design. For your specific RAS project, adapt the sample WBS in Part V to local conditions, species requirements, and regulatory environment.*