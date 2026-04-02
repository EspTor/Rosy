# Town Structure & Geography

## Physical Layout

- **Grid**: 1000×1000 units (1 unit ≈ 1 meter)
- **7 Districts**:
  1. Downtown (center)
  2. Residential North (northwest)
  3. Residential South (southeast)
  4. Industrial East (east)
  5. Tech Park (northeast)
  6. Market District (southwest)
  7. University Heights (far north)

## Location Types

Each location has:
- Coordinates and spatial extent
- Type classification
- Capacity limits
- Properties (comfort, noise, safety)
- Owner (if private)
- Current occupants
- Resource stocks

**Types**: Homes, apartments, retail shops, restaurants, factories, warehouses, town hall, library, police station, hospital, parks, sports facilities, entertainment venues.

## Movement & Navigation

- A* pathfinding on navigation mesh
- Roads = fast, sidewalks = medium, off-grid = slow
- Personal space radius: 1.5 units
- Collision avoidance during movement

## Daily Cycle

- 06:00: Wake up
- 07:00-09:00: Morning commute
- 09:00-17:00: Work/school
- 12:00-13:00: Lunch
- 17:00-19:00: Evening activities
- 21:00-23:00: Home time/nightlife
- 00:00-06:00: Sleep (most agents)

## Services

Locations provide services that consume time and affect state:
- FoodService: reduces hunger, increases happiness
- Entertainment: increases fun
- Education: gain skills
- Healthcare: heal injuries, treat illness

---
