# Code Analysis: Original Parking Lot Manager

## Overview of Original Codebase

The original codebase consists of three Python files implementing a parking lot management system with GUI:
- **Vehicle.py** - Base Vehicle class and subclasses (Car, Truck, Motorcycle, Bus)
- **ElectricVehicle.py** - ElectricVehicle base class and subclasses (ElectricCar, ElectricBike)
- **ParkingManager.py** - GUI application with ParkingLot business logic

**Current Architecture Issues:**
- GUI and business logic tightly coupled
- Duplicate code across Vehicle and ElectricVehicle hierarchies
- Complex conditional logic for handling different vehicle types
- Multiple search methods duplicated for regular vs. EV slots
- Global variables throughout application
- Poor naming conventions and magic numbers

---

## Code Smells Identified and Analysis

### Code Smell 1: Poor/Non-Explicit Variable Names

**Location:** Throughout all files
- `slotid` instead of `slot_id` or `slot_number`
- `slotEvId` instead of `electric_vehicle_slot_id`
- `numOfOccupiedSlots` instead of `occupied_slots_count`
- `numOfOccupiedEvSlots` instead of `occupied_electric_slots_count`
- `ev` and `motor` as boolean parameters (cryptic boolean flags)
- `tfield` instead of `text_output_field`
- `regnum` instead of `registration_number`

**Impact:** 
- Reduces code readability and maintainability
- Makes onboarding difficult for new developers
- Increases debugging time

**Example (ParkingManager.py, lines 12-27):**
```python
# Current - unclear naming
command_value = tk.StringVar()
ev_value = tk.StringVar()
ev_car_value = tk.IntVar()
slot1_value = tk.StringVar()
ev_motor_value = tk.IntVar()
```

---

### Code Smell 2: Duplicate Code - Getter Methods

**Location:** Vehicle.py (lines 9-19) and ElectricVehicle.py (lines 10-26)

**Description:** Vehicle and ElectricVehicle classes contain identical getter methods

**Original Code:**
```python
# Vehicle.py
def getMake(self):
    return self.make
def getModel(self):
    return self.model
def getColor(self):
    return self.color
def getRegNum(self):
    return self.regnum

# ElectricVehicle.py (identical methods)
def getMake(self):
    return self.make
def getModel(self):
    return self.model
def getColor(self):
    return self.color
def getRegNum(self):
    return self.regnum
```

**Fix Rationale:** 
- Extract common functionality to a shared base class
- ElectricVehicle should inherit from Vehicle
- Eliminates 8 lines of duplicated code

**Benefits:**
- Single point of maintenance
- Consistent interface across all vehicle types
- Reduces code size and complexity

---

### Code Smell 3: Duplicate Search Methods

**Location:** ParkingManager.py, lines 147-246

**Description:** Separate methods for searching regular vs. EV slots

**Original Code (Examples):**
```python
# Method 1 - Search regular slots by color
def getSlotNumFromColor(self, color): 
    slotnums = []
    for i in range(len(self.slots)):
        if self.slots[i] == -1:
            continue
        if self.slots[i].color == color:
            slotnums.append(str(i+1))
    return slotnums

# Method 2 - Search EV slots by color (identical logic)
def getSlotNumFromColorEv(self, color): 
    slotnums = []
    for i in range(len(self.evSlots)):          
        if self.evSlots[i] == -1:
            continue
        if self.evSlots[i].color == color:
            slotnums.append(str(i+1))
    return slotnums

# Similar duplication for:
# - getSlotNumFromRegNum vs getSlotNumFromRegNumEv
# - getSlotNumFromMake vs getSlotNumFromMakeEv
# - getSlotNumFromModel vs getSlotNumFromModelEv
# - getRegNumFromColor vs getRegNumFromColorEv
```

**Fix Rationale:** 
- Unified search method with strategy pattern
- Query logic should be agnostic to vehicle type
- Eliminate 9 duplicated search methods

**Benefits:**
- Reduced code duplication (100+ lines saved)
- Single point of maintenance for search logic
- Easier to add new search criteria
- Better extensibility for future vehicle types

---

### Code Smell 4: Complex Conditional Logic in park() Method

**Location:** ParkingManager.py, lines 64-89

**Description:** Deeply nested if statements with boolean flag parameters

**Original Code:**
```python
def park(self, regnum, make, model, color, ev, motor):
    if (self.numOfOccupiedEvSlots < self.evCapacity or 
        self.numOfOccupiedSlots < self.capacity):
        slotid = -1
        if (ev == 1):                                    # If electric?
            if self.numOfOccupiedEvSlots < self.evCapacity:
                slotid = self.getEmptyEvSlot()
                if (motor == 1):                         # If motorcycle?
                    self.evSlots[slotid] = ElectricVehicle.ElectricBike(
                        regnum, make, model, color)
                else:
                    self.evSlots[slotid] = ElectricVehicle.ElectricCar(
                        regnum, make, model, color)
                self.slotEvId = self.slotEvId + 1
                self.numOfOccupiedEvSlots = self.numOfOccupiedEvSlots + 1
                slotid = self.slotEvId
        else:                                            # Regular vehicle
            if self.numOfOccupiedSlots < self.capacity:
                slotid = self.getEmptySlot()
                if (motor == 1):                         # If motorcycle?
                    self.slots[slotid] = Vehicle.Car(
                        regnum, make, model, color)
                else:
                    self.slots[slotid] = Vehicle.Motorcycle(
                        regnum, make, model, color)
                # ... rest of logic
```

**Issues:**
- 4 levels of nesting (readability issue)
- Boolean parameters (`ev`, `motor`) are cryptic
- Mixing of concerns: capacity checking, slot allocation, vehicle creation
- Repeated vehicle creation logic
- Logic spread across multiple conditionals

**Fix Rationale:**
- Use Factory Pattern for vehicle creation
- Use Strategy Pattern for vehicle type handling
- Eliminate boolean parameters
- Reduce nesting to single level

**Benefits:**
- Improved readability (easier to follow logic)
- Better testability (each concern separately tested)
- Easier to add new vehicle types
- Eliminates boolean flag anti-pattern

---

### Code Smell 5: Mixing Concerns - GUI and Business Logic

**Location:** ParkingManager.py, lines 117-145 (status methods)

**Description:** Business logic methods directly manipulate GUI text widget

**Original Code:**
```python
def status(self):
    output = "Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
    tfield.insert(tk.INSERT, output)  # <-- GUI manipulation in business logic
    for i in range(len(self.slots)):
        if self.slots[i] != -1:
            output = str(i+1) + "\t" +str(self.level) + "\t" + ...
            tfield.insert(tk.INSERT, output)  # <-- Global variable reference
        else:
            continue
    # ... more GUI updates
```

**Issues:**
- Business logic depends on GUI widget
- Uses global `tfield` variable
- Cannot test business logic without GUI
- Cannot reuse business logic in different UI
- Violates Separation of Concerns

**Fix Rationale:**
- Extract parking lot logic to separate class
- Return data from business methods
- Let GUI handle display logic

**Benefits:**
- Business logic testable independently
- Can use with different UI (web, CLI, etc.)
- Better code organization
- Follows Single Responsibility Principle

---

### Code Smell 6: Inconsistent Inheritance in ElectricVehicle

**Location:** ElectricVehicle.py, lines 28-40

**Description:** ElectricCar and ElectricBike don't properly inherit from ElectricVehicle

**Original Code:**
```python
class ElectricCar:  # <-- Not inheriting from ElectricVehicle!
    def __init__(self, regnum, make, model, color):
        ElectricVehicle.__init__(self, regnum, make, model, color)
        # Manual __init__ call instead of using super()

    def getType(self):
        return "Car"

class ElectricBike:  # <-- Not inheriting from ElectricVehicle!
    def __init__(self, regnum, make, model, color):
        ElectricVehicle.__init__(self, regnum, make, model, color)
        # Manual __init__ call instead of using super()

    def getType(self):
        return "Motorcycle"
```

**Issues:**
- Classes don't use inheritance syntax
- Manual __init__ calls prone to errors
- No inheritance chain established
- Type checking won't work correctly
- Methods from ElectricVehicle not accessible

**Fix Rationale:**
- Proper inheritance hierarchy
- Use super() for cleaner code
- Establish proper type relationships

**Benefits:**
- Proper OOP structure
- Better type checking
- Easier to add new electric vehicle types
- More maintainable code

---

### Code Smell 7: Global Variables

**Location:** ParkingManager.py, lines 6-29

**Description:** Module-level global variables and objects

**Original Code:**
```python
# Global Tkinter window
root = tk.Tk()
root.geometry("650x850")
root.resizable(0,0)
root.title("Parking Lot Manager")

# Global StringVar/IntVar variables
command_value = tk.StringVar()
num_value = tk.StringVar()
ev_value = tk.StringVar()
make_value = tk.StringVar()
model_value = tk.StringVar()
color_value = tk.StringVar()
reg_value = tk.StringVar()
level_value = tk.StringVar()
ev_car_value = tk.IntVar()
ev_car2_value = tk.IntVar()
slot1_value = tk.StringVar()
slot2_value = tk.StringVar()
reg1_value = tk.StringVar()
slot_value = tk.StringVar()
ev_motor_value = tk.IntVar()
level_remove_value = tk.StringVar()

# Global text widget
tfield = tk.Text(root, width=70, height=15)
```

**Issues:**
- 23+ global variables
- Hard to trace dependencies
- Makes testing difficult
- Not thread-safe
- Global state makes code fragile

**Fix Rationale:**
- Encapsulate GUI variables in class
- Pass dependencies as parameters
- Create GUI manager class

**Benefits:**
- Easier to test
- Better code organization
- Eliminates global state
- Thread-safe design

---

### Code Smell 8: Magic Numbers and Hardcoded Values

**Location:** Throughout ParkingManager.py

**Description:** Magic numbers without explanation

**Original Code:**
```python
# Line 37-38: Magic number -1 for empty slots
self.slots = [-1] * capacity
self.evSlots = [-1] * evcapacity

# Lines 67, 81, 92, 100: Comparing with -1
if self.slots[i] == -1:

# Lines 64, 68: Boolean values 1 and 0
if (ev == 1):
if (motor == 1):

# Line 7: Hard-coded window size
root.geometry("650x850")

# Line 29: Hard-coded text widget size
tfield = tk.Text(root, width=70, height=15)
```

**Issues:**
- Unclear what -1 means
- Boolean values as integers
- Hard to change constants
- Reduces readability

**Fix Rationale:**
- Define named constants
- Use proper boolean values
- Extract configuration

**Benefits:**
- More readable code
- Single point of change for constants
- Better self-documenting code

---

### Code Smell 9: Poor Error Handling

**Location:** ParkingManager.py, throughout

**Description:** Silent failures and lack of validation

**Original Code:**
```python
# Returns -1 on failure with no indication why
def park(self, regnum, make, model, color, ev, motor):
    if (self.numOfOccupiedEvSlots < self.evCapacity or 
        self.numOfOccupiedSlots < self.capacity):
        # ... logic ...
        return slotid
    else:
        return -1  # <-- Silent failure

# No input validation
def park(self, regnum, make, model, color, ev, motor):
    # No checks for empty strings, None values, invalid types
```

**Issues:**
- Return values don't indicate why operation failed
- No input validation
- No exception handling
- Magic return value -1

**Fix Rationale:**
- Raise custom exceptions for errors
- Validate input parameters
- Provide meaningful error messages

**Benefits:**
- Better error reporting
- Easier debugging
- More robust application
- Better user experience

---

## Pattern Selection and Justification

### Pattern 1: Factory Pattern (Creational)

**Problem Solved:**
- Eliminates complex conditional logic for vehicle creation (Code Smell 4)
- Decouples vehicle creation from business logic
- Single point of vehicle creation logic

**Implementation Overview:**
Create `VehicleFactory` class with static methods to handle all vehicle creation:
```python
class VehicleFactory:
    @staticmethod
    def create_vehicle(vehicle_type, registration_number, make, model, color):
        """Create appropriate vehicle based on type."""
        if vehicle_type == "electric_car":
            return ElectricCar(registration_number, make, model, color)
        elif vehicle_type == "electric_motorcycle":
            return ElectricBike(registration_number, make, model, color)
        elif vehicle_type == "regular_car":
            return Car(registration_number, make, model, color)
        elif vehicle_type == "regular_motorcycle":
            return Motorcycle(registration_number, make, model, color)
        else:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
```

**How It Addresses Issues:**
- **Code Smell 4 (Complex Conditionals)**: Moves conditional logic to factory
- **Code Smell 6 (Missing Inheritance)**: Factory ensures proper object creation
- **Code Smell 9 (Error Handling)**: Factory validates type and raises exceptions

**Benefits:**
- Centralized vehicle creation logic
- Easy to add new vehicle types without modifying park() method
- Better separation of concerns
- Improved testability
- Eliminates boolean parameters

---

### Pattern 2: Strategy Pattern (Behavioral)

**Problem Solved:**
- Eliminates duplicate search methods (Code Smell 3)
- Encapsulates different vehicle handling algorithms
- Removes need for boolean flags (ev, motor parameters)

**Implementation Overview:**
Create strategy classes for different vehicle types:
```python
class VehicleStrategy:
    """Base strategy for vehicle operations."""
    def get_slots(self):
        pass
    
    def get_empty_slot(self):
        pass
    
    def allocate_slot(self, vehicle, slot_index):
        pass
    
    def deallocate_slot(self, slot_index):
        pass

class RegularVehicleStrategy(VehicleStrategy):
    """Strategy for regular (non-electric) vehicles."""
    def __init__(self, parking_lot):
        self.parking_lot = parking_lot
    
    def get_slots(self):
        return self.parking_lot.slots
    
    def get_empty_slot(self):
        for i in range(len(self.parking_lot.slots)):
            if self.parking_lot.slots[i] is None:
                return i
        return -1
    
    def allocate_slot(self, vehicle, slot_index):
        self.parking_lot.slots[slot_index] = vehicle
        self.parking_lot.occupied_slots_count += 1
    
    def deallocate_slot(self, slot_index):
        self.parking_lot.slots[slot_index] = None
        self.parking_lot.occupied_slots_count -= 1

class ElectricVehicleStrategy(VehicleStrategy):
    """Strategy for electric vehicles."""
    def __init__(self, parking_lot):
        self.parking_lot = parking_lot
    
    def get_slots(self):
        return self.parking_lot.electric_slots
    
    def get_empty_slot(self):
        for i in range(len(self.parking_lot.electric_slots)):
            if self.parking_lot.electric_slots[i] is None:
                return i
        return -1
    
    def allocate_slot(self, vehicle, slot_index):
        self.parking_lot.electric_slots[slot_index] = vehicle
        self.parking_lot.occupied_electric_slots_count += 1
    
    def deallocate_slot(self, slot_index):
        self.parking_lot.electric_slots[slot_index] = None
        self.parking_lot.occupied_electric_slots_count -= 1
```

**How It Addresses Issues:**
- **Code Smell 3 (Duplicate Search Methods)**: Unified search through strategy
- **Code Smell 4 (Complex Conditionals)**: Eliminates if/else chains
- **Code Smell 8 (Magic Numbers)**: Strategies manage slot representation

**Benefits:**
- Eliminates all duplicate search methods
- Removes need for separate EV search methods
- Open/Closed Principle: Easy to add new strategies
- Eliminates boolean parameters
- Improves readability and maintainability

---

## Summary of Improvements

| Issue | Pattern | Improvement |
|-------|---------|-------------|
| Complex vehicle creation | Factory | Centralized, extensible creation logic |
| Duplicate search methods | Strategy | Unified search interface |
| Nested conditionals | Both patterns | Reduced nesting depth to 1-2 levels |
| Global variables | Encapsulation | Improved architecture |
| Poor naming | Refactoring | Explicit, self-documenting names |
| Mixing concerns | Separation | GUI separated from business logic |
| Poor inheritance | Refactoring | Proper OOP hierarchy |
| Magic numbers | Constants | Named constants throughout |
| No error handling | Custom exceptions | Proper exception handling |

---

## Expected Code Metrics Improvement

- **Lines of duplicated code eliminated**: ~120 lines
- **Cyclomatic complexity reduction**: From 8+ to 2-3 per method
- **Code readability improvement**: 50%+ improvement through naming and structure
- **Testability improvement**: 100% (currently untestable, will be fully testable)
- **Maintainability index improvement**: Significant

