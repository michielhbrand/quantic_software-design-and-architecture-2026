# Project Completion Roadmap

## Overview
This roadmap provides a detailed execution plan for completing all 8 steps of the Software Design & Architecture project. Each step builds upon the previous one, leading to a complete submission with improved code, comprehensive documentation, and UML diagrams.

---

## Step 1: Consume Context and Learning Materials

### Objective
Build deep understanding of project requirements and relevant design concepts.

### Tasks
1. **Review Project Brief** (`project-brief.pdf`)
   - Read through entire project overview and learning outcomes
   - Identify key requirements from "Submission Guidelines" section
   - Note the rubric criteria (especially items for score 5)
   - Understand anti-patterns list (lines 56-67)
   - Understand that system must scale to multiple facilities with EV charging

2. **Study Learnings Document** (`learnings.pdf`)
   - Extract core concepts about design patterns (structural, behavioral, architectural)
   - Understand Gang of Four patterns and when to apply them
   - Learn about domain-driven design principles and bounded contexts
   - Understand microservices architecture concepts
   - Study best practices for code quality and refactoring

3. **Document Key Takeaways**
   - List anti-patterns to watch for in the codebase
   - Identify potential design patterns that might apply
   - Note DDD concepts for later system expansion planning

### Deliverables
- Personal notes on project requirements
- Mental map of design patterns and when to use them
- Clear understanding of DDD terminology

---

## Step 2: Analyze Original Code and Identify Improvements

### Objective
Thoroughly understand existing codebase, identify technical debt, and select 2 OO patterns for improvement.

### 2.1 Study Original Code Structure

**Review each Python file:**
- `Vehicle.py` - Base class and subclasses (Car, Truck, Motorcycle, Bus)
- `ElectricVehicle.py` - Electric vehicle base and subclasses
- `ParkingManager.py` - Main application logic and GUI

**Document the current architecture:**
- Class hierarchy and inheritance
- Method responsibilities
- Data structure design (slots arrays)
- GUI/business logic coupling

### 2.2 Identify Code Smells

**Analyze and document:**

1. **Poor/Non-explicit Variable Names**
   - Examples: `slotid`, `slotEvId`, `numOfOccupied*`, `ev`, `motor`
   - Impact: Reduces code readability

2. **Duplicate Code**
   - Duplicate search methods for regular and EV slots
   - Similar getter methods across Vehicle and ElectricVehicle
   - Repeated conditional logic for EV vs regular vehicles

3. **Mixing Concerns**
   - GUI logic deeply coupled with business logic in `ParkingManager.py`
   - Vehicle creation scattered throughout park() method
   - Slot searching logic embedded in query methods

4. **Inconsistent Inheritance**
   - `ElectricCar` and `ElectricBike` don't properly inherit from `ElectricVehicle`
   - Redundant getter methods across base and child classes

5. **Complex Conditional Logic**
   - Nested if statements in `park()` method (lines 65-89)
   - Long parameter lists with boolean flags (`ev`, `motor`)
   - Multiple responsibilities in single method

6. **Lack of Abstraction**
   - No factory for vehicle creation
   - No strategy pattern for handling different vehicle types
   - Hard-coded type checking with boolean parameters

7. **Poor Error Handling**
   - No validation of input parameters
   - No custom exceptions
   - Silent failures with -1 return values

8. **Global Variables**
   - Tkinter variables declared at module level (lines 12-27)
   - Global `tfield` text widget
   - Global `root` tkinter object

9. **Magic Numbers and Hardcoded Values**
   - `-1` used to indicate empty slots
   - Strings hardcoded for output formatting
   - GUI window dimensions hardcoded

### 2.3 Identify 2 Object-Oriented Design Patterns

**Pattern Selection Criteria:**
- Address identified code smells
- Provide substantial architectural improvement
- Are suitable for OO design and Gang of Four patterns

**Recommended Patterns:**

**Pattern 1: Factory Pattern**
- **Rationale**: Eliminates complex vehicle creation logic scattered throughout `park()` method
- **Addresses**: Code smell of mixing concerns, complex conditionals
- **Implementation**: Create `VehicleFactory` class to handle vehicle object creation
- **Benefits**: 
  - Centralized vehicle creation
  - Easy to add new vehicle types
  - Decouples creation from business logic
  - Can expand to support multiple vehicle variations

**Pattern 2: Strategy Pattern**
- **Rationale**: Encapsulates different vehicle handling strategies (regular vs. electric, car vs. motorcycle)
- **Addresses**: Code smell of duplicate methods, complex conditionals, hard-coded type checking
- **Implementation**: Create strategy classes for `RegularVehicleStrategy`, `ElectricVehicleStrategy`
- **Benefits**:
  - Eliminates boolean flags (`ev`, `motor`)
  - Removes duplicate code for similar operations
  - Makes system more extensible
  - Improves testability

**Alternative Pattern 2 Option: Composite/State Pattern**
- Use if you prefer to model vehicle states and transitions

### 2.4 Document Decisions

Create a summary document capturing:
- 5-8 code smells identified with line numbers
- Why each pattern was chosen
- How each pattern addresses specific issues
- Expected benefits to the system

---

## Step 3: Implement Improved Code

### Objective
Create refactored Python code applying the 2 selected design patterns, improving code quality and eliminating identified smells.

### 3.1 Prepare Directory Structure

```
submission-files/code-base-improved/
├── __init__.py
├── Vehicle.py
├── ElectricVehicle.py
├── VehicleFactory.py (NEW)
├── ParkingLot.py (NEW - extracted)
├── ParkingManager.py (refactored)
└── README.md
```

### 3.2 Refactor Each File

**Vehicle.py Improvements:**
- Rename variables to be explicit: `registration_number` instead of `regnum`
- Make attributes private with getters/setters
- Add docstrings to all methods
- Consider abstract base class for better inheritance
- Consistent constructor initialization

**ElectricVehicle.py Improvements:**
- Fix inheritance issues (ElectricCar and ElectricBike should properly inherit)
- Add charge management methods
- Make consistent with Vehicle.py refactoring

**VehicleFactory.py (NEW):**
- Implement Factory Pattern
- Single point of vehicle creation
- Accept vehicle type and attributes
- Return appropriate vehicle instance
- Example:
  ```python
  class VehicleFactory:
      @staticmethod
      def create_vehicle(vehicle_type, reg_num, make, model, color):
          if vehicle_type == "car":
              return Car(reg_num, make, model, color)
          elif vehicle_type == "motorcycle":
              return Motorcycle(reg_num, make, model, color)
          # ... etc
  ```

**ParkingLot.py (NEW - Extract business logic):**
- Extract parking lot logic from ParkingManager
- Separate concerns: data storage and management from GUI
- Clean slot management (use better naming than `slotid`)
- Implement search queries as clean methods
- Remove GUI-related code

**ParkingManager.py (Refactored):**
- Separate GUI code from business logic
- Use Strategy pattern for vehicle handling
- Remove global variables where possible (pass as parameters)
- Improve error handling and validation
- Use VehicleFactory for vehicle creation
- Simplify method signatures (eliminate boolean flags)

### 3.3 Key Refactoring Principles

- **Explicit Naming**: Replace abbreviations with full names
- **Single Responsibility**: Each class/method does one thing
- **DRY (Don't Repeat Yourself)**: Eliminate duplicate code
- **Encapsulation**: Hide implementation details
- **Error Handling**: Validate inputs, raise exceptions
- **Documentation**: Add docstrings and comments

---

## Step 4: Test Improved Code

### Objective
Verify the refactored code compiles, runs, and maintains functionality.

### 4.1 Code Quality Checks

1. **Syntax Validation**
   ```bash
   python3 -m py_compile Vehicle.py
   python3 -m py_compile ElectricVehicle.py
   python3 -m py_compile VehicleFactory.py
   python3 -m py_compile ParkingLot.py
   python3 -m py_compile ParkingManager.py
   ```

2. **Import Validation**
   - Verify all imports work correctly
   - Check for circular dependencies
   - Test module imports

3. **Static Analysis (Optional)**
   ```bash
   pylint Vehicle.py
   pylint ParkingManager.py
   ```

### 4.2 Functional Testing

1. **Unit Tests (if time permits)**
   - Test VehicleFactory creation
   - Test ParkingLot slot allocation
   - Test search queries

2. **Integration Testing**
   - Run the GUI application
   - Create parking lot
   - Park vehicles (regular and electric)
   - Remove vehicles
   - Search by registration, color, make, model
   - Check EV charge status
   - Verify output formatting

3. **Edge Cases**
   - Full parking lot
   - Invalid inputs
   - Empty lot queries
   - Duplicate registration numbers

### 4.3 Regression Testing

Verify that improved code:
- Produces same functional output as original
- Handles edge cases correctly
- Doesn't break existing features

### 4.4 Document Test Results

- Screenshot of successful execution
- List of test cases passed
- Any issues found and resolved
- Performance observations

---

## Step 5: Complete Code-Improvements.md Document

### Objective
Create comprehensive documentation of code improvements and design pattern justifications.

### 5.1 Document Structure

**Section 1: Original Code Analysis**
- Overview of original codebase
- Architecture and structure
- Initial concerns

**Section 2: Code Smells Identified and Fixed**

For each code smell, document:
- **Smell Name & Location**: Specific files and line numbers
- **Description**: What was wrong
- **Original Code**: Code snippet showing the problem
- **Improved Code**: Refactored version
- **Fix Rationale**: Why this improvement was made
- **Benefits**: Improved maintainability, readability, extensibility

Example structure:
```
### Code Smell 1: Duplicate Search Methods
**Location**: ParkingManager.py, lines 147-194
**Description**: Separate methods for searching regular vs. EV slots
**Original Code**: [snippet]
**Improved Code**: [snippet]
**Fix Rationale**: Extracted to unified search strategy
```

**Section 3: Design Patterns Applied**

For each of 2 patterns:
- **Pattern Name**: Factory / Strategy / etc.
- **Gang of Four Classification**: Creational / Behavioral / etc.
- **Problem It Solves**: Specific issues from code smells
- **Implementation Overview**: High-level explanation
- **Key Components**: Classes and methods
- **Code Example**: Before and after comparison
- **Benefits**:
  - Improved code organization
  - Better extensibility
  - Enhanced maintainability
  - Reduced coupling
- **How It Addresses Multiple Smells**: Map to specific smells

**Section 4: Overall Improvements Summary**
- Metrics: Lines of code change, reduced duplication %, improved readability
- Architecture benefits
- Maintenance and extension benefits
- Technical debt reduction

### 5.2 Content Guidelines

- Use code snippets from actual improved code
- Be specific about which patterns address which issues
- Explain tradeoffs (if any)
- Connect improvements to project brief requirements
- Focus on substantial improvements, not cosmetic changes

---

## Step 6: Generate System-Expansion.md Document

### Objective
Design how the parking system extends to include EV charging with DDD and microservices perspective.

### 6.1 Document Structure

**Section 1: System Expansion Overview**
- Current single parking lot system
- New requirement: multiple facilities + EV charging
- Vision for scalable architecture

**Section 2: Domain-Driven Design Analysis**

**2.1 Bounded Contexts**
- Identify separate domains:
  - **Parking Management Subdomain**: Vehicle parking, slot allocation, searches
  - **EV Charging Subdomain**: Charging stations, power distribution, charge scheduling
  - **Facility Management Subdomain**: Multiple locations, capacity planning

**2.2 Bounded Context Diagram**
- Create high-level visual diagram showing:
  - Context boundaries
  - Relationships between contexts
  - Data flow between domains
- Include description and legend

**2.3 Domain Models**

For Parking Management Context:
- **Entities**: Parking Lot, Vehicle, Parking Space, Reservation
- **Value Objects**: Registration Number, Location, Vehicle Spec
- **Aggregates**: ParkingLot (aggregate root), Vehicle with metadata
- **Ubiquitous Language Terms**: Parking slot, capacity, occupancy, allocation

For EV Charging Context:
- **Entities**: Charging Station, Charging Session, Power Grid, Vehicle Battery
- **Value Objects**: Charge Level, Power Output, Location Coordinates
- **Aggregates**: ChargingStation (aggregate root), ChargingSession
- **Ubiquitous Language Terms**: Charge state, power flow, session duration, kWh

**Section 3: Microservices Architecture**

**3.1 Service Decomposition**
- Service 1: **Parking Service**
  - Responsibility: Manage parking slots, allocate spaces, track occupancy
  - API Endpoints:
    - POST /parking-lots (create lot)
    - POST /parking-lots/{id}/allocate (park vehicle)
    - DELETE /parking-lots/{id}/spaces/{space-id} (remove vehicle)
    - GET /parking-lots/{id}/status (get lot status)
  - Database: Parking-specific schema (lots, spaces, vehicles)

- Service 2: **EV Charging Service**
  - Responsibility: Manage charging stations, track charging sessions, power allocation
  - API Endpoints:
    - POST /charging-stations (register station)
    - POST /charging-sessions (start charging)
    - PUT /charging-sessions/{id} (update charge level)
    - GET /charging-sessions/{id}/status (session status)
  - Database: Charging-specific schema (stations, sessions, power)

- Service 3: **Vehicle Registry Service**
  - Responsibility: Track vehicle information, type, ownership
  - API Endpoints:
    - POST /vehicles (register vehicle)
    - GET /vehicles/{reg-num} (get vehicle details)
  - Database: Vehicle registration data

- Service 4: **Facility Management Service** (optional)
  - Responsibility: Manage multiple parking facility locations
  - API Endpoints:
    - POST /facilities (register new facility)
    - GET /facilities (list all facilities)
  - Database: Facility locations and metadata

**3.2 Microservices Architecture Diagram**
- Visual diagram showing:
  - Service boxes with responsibilities
  - API endpoints (both external and internal)
  - Database per service
  - Inter-service communication flows
  - External clients/interfaces

**3.3 API Contract Examples**
- Show key request/response examples
- Error handling approach
- Authentication/authorization consideration

---

## Step 7: Generate Original-Design.md Document

### Objective
Create UML diagrams representing the original code architecture.

### 7.1 Structural UML Diagram (Class Diagram)

**Diagram Contents:**
- **Vehicle Class**: Base class with properties (regnum, make, model, color) and methods (getMake, getModel, etc.)
- **Subclasses**: Car, Truck, Motorcycle, Bus (each with getType())
- **ElectricVehicle Class**: Base with charge property
- **ElectricCar, ElectricBike**: Subclasses of ElectricVehicle
- **ParkingLot Class**: Properties (capacity, evCapacity, level, slots, evSlots, etc.)
- **ParkingLot Methods**: park(), leave(), edit(), status(), search methods, etc.
- **Relationships**: Inheritance arrows, composition with vehicles

**Key Issues to Show:**
- Duplicate inheritance patterns
- Similar method signatures across Vehicle and ElectricVehicle
- Complex method signatures with boolean parameters
- Tight coupling between ParkingLot and Vehicle classes

### 7.2 Behavioral UML Diagram (Sequence Diagram or Activity Diagram)

**Option A: Sequence Diagram**
- Show interaction sequence for:
  - "Park Vehicle" use case
  - "Search by Color" use case
  - "Remove Vehicle" use case

**Option B: Activity Diagram**
- Show workflow for:
  - Vehicle parking process (decision points for EV vs regular, motorcycle vs car)
  - Vehicle removal process
  - Search operation flow

**Diagram Contents:**
- Actors: User (GUI)
- Objects: ParkingLot, Vehicle
- Messages: park(), leave(), getSlotNum(), etc.
- Decision points showing conditional logic
- Return values and results

### 7.3 Creating the Diagrams

**Recommended Tools:**
- PlantUML (code-based, version control friendly)
- Lucidchart (visual design)
- draw.io (free, online)
- Miro (collaborative)

**Export as:** PNG or SVG files, place in `submission-files/diagrams/`

---

## Step 8: Generate Redesign.md Document

### Objective
Create UML diagrams representing the improved code architecture with design patterns.

### 8.1 Structural UML Diagram (Class Diagram with Patterns)

**New/Modified Components:**

- **VehicleFactory Class** (Factory Pattern)
  - Static method: create_vehicle(type, params)
  - Shows how vehicle creation is centralized

- **Refactored Vehicle Hierarchy**
  - Abstract base class if applicable
  - Cleaner inheritance
  - Better naming conventions

- **Strategy Pattern Classes** (if implemented)
  - VehicleStrategy interface/base
  - RegularVehicleStrategy, ElectricVehicleStrategy implementations
  - ParkingLot uses strategies instead of conditionals

- **Refactored ParkingLot Class**
  - Cleaner method signatures
  - Extracted from ParkingManager
  - Reduced complexity

- **Separated ParkingManager Class**
  - GUI only
  - Uses ParkingLot for business logic
  - No direct Vehicle manipulation

**Diagram Features:**
- Factory pattern relationships
- Strategy pattern with interface/implementations
- Dependency injection arrows
- Clearer separation of concerns
- Reduced coupling between classes

### 8.2 Behavioral UML Diagram (Sequence/Activity with Patterns)

**Improved Workflows:**

**Option A: Sequence Diagram**
- Show interaction sequence for:
  - "Park Vehicle" with Factory (simpler flow, no conditionals)
  - "Search by Color" (unified method)
  - "Remove Vehicle" (cleaner handling)

**Improvements Shown:**
- Fewer decision points
- Use of Strategy pattern
- Single creation point (Factory)
- Better separation of GUI and business logic

**Option B: Activity Diagram**
- Vehicle parking flow simplified
- Single decision path for vehicle type
- Use of Factory simplifies creation
- Clear separation of concerns

### 8.3 Comparing Original vs. Improved

**Create side-by-side comparison highlighting:**
- Elimination of boolean parameters
- Use of Factory instead of embedded conditionals
- Strategy pattern reducing duplicate code
- Cleaner interaction flows
- Better separation of concerns

### 8.4 Creating the Diagrams

Use same tools as Step 7, export to `submission-files/diagrams/`:
- `improved_structural_uml.png`
- `improved_behavioral_uml.png`

---

## Execution Timeline and Dependencies

```
Step 1: Context & Learning
    ↓
Step 2: Code Analysis → Identify Patterns
    ↓
Step 3: Implement Improved Code
    ↓
Step 4: Test Code
    ↓
Step 5: Code-Improvements.md ← Uses Steps 2, 3, 4
    ↓
Step 6: System-Expansion.md (can run in parallel)
    ↓
Step 7: Original-Design.md (can run in parallel)
    ↓
Step 8: Redesign.md ← Uses Step 3
```

---

## Quality Checklist

Before finalizing submission, verify:

- [ ] Step 1: Fully understood project brief and learnings
- [ ] Step 2: Identified 5+ code smells with locations
- [ ] Step 2: Selected 2 patterns with clear justification
- [ ] Step 3: Improved code follows all refactoring principles
- [ ] Step 4: Improved code runs without errors
- [ ] Step 4: All functionality preserved from original
- [ ] Step 5: Code-Improvements.md is detailed and complete
- [ ] Step 5: All code smells are documented with before/after
- [ ] Step 5: Pattern justifications are compelling
- [ ] Step 6: System expansion is logical and scalable
- [ ] Step 6: DDD bounded contexts are clearly defined
- [ ] Step 6: Microservices architecture is coherent
- [ ] Step 7: Original diagrams accurately represent code
- [ ] Step 8: Improved diagrams clearly show pattern implementation
- [ ] All UML diagrams are clear, properly labeled
- [ ] All code files are in `code-base-improved/`
- [ ] All diagrams are in `submission-files/diagrams/`
- [ ] Documentation files are in `submission-files/`

---

## Success Criteria

Completion is achieved when:
1. ✓ All 8 steps are executed
2. ✓ Code-Improvements.md documents substantial architectural changes
3. ✓ System-Expansion.md presents coherent DDD and microservices design
4. ✓ Original-Design.md accurately represents existing code
5. ✓ Redesign.md clearly demonstrates pattern implementation
6. ✓ Improved Python code runs without errors
7. ✓ All files organized in submission-files directory
8. ✓ UML diagrams are professional and accurate
