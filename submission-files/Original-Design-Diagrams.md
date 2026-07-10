<div align="center">

![Quantic Logo](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjJweCIgaGVpZ2h0PSIyNXB4IiB2aWV3Qm94PSIwIDAgMjIgMjUiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiAgICA8ZyBpZD0iUGFnZS0xIiBzdHJva2U9Im5vbmUiIHN0cm9rZS13aWR0aD0iMSIgZmlsbD0ibm9uZSIgZmlsbC1ydWxlPSJldmVub2RkIj4KICAgICAgICA8ZyBpZD0iTXVsdGlwbGUtUHJvZ3JhbXMtKEdyYWR1YXRlZC1mcm9tLWFjdGl2ZSktLS1PdGhlcnMtdG8tQXBwbHktVG8iIHRyYW5zZm9ybT0idHJhbnNsYXRlKC03NzAuMDAwMDAwLCAtMTI5LjAwMDAwMCkiIGZpbGw9IiNGRjRENjMiPgogICAgICAgICAgICA8ZyBpZD0iRHJvcGRvd24iIHRyYW5zZm9ybT0idHJhbnNsYXRlKDc1NS4wMDAwMDAsIDYyLjAwMDAwMCkiPgogICAgICAgICAgICAgICAgPGcgaWQ9IkFjdGl2ZS1Qcm9ncmFtIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgwLjAwMDAwMCwgNTEuMDAwMDAwKSI+CiAgICAgICAgICAgICAgICAgICAgPHBhdGggZD0iTTI1LjkyMjczOTUsMTYgTDM2Ljg0NTQ3OTEsMjIuMjQ5OTM0NSBMMzYuODQ1NDc5MSwyOC40OTU5MzY1IEwzMS4zODE1OTY0LDMxLjYyMjIxNDUgTDMxLjM4MTU5NjQsMjUuMzc2NzM2OCBMMjUuOTIyNzM5NSwyMi4yNTMwODA0IEwyMC40NjQxNDcyLDI1LjM3NjczNjggTDIwLjQ2NDE0NzIsMzEuNjIzNzg3NSBMMjUuODEsMzQuNjgyIEwyNS44MTA4MTc1LDI4LjQ5NDIzNjMgTDM2LjYxODkzODcsMzQuNzQyODM1NCBMMzYuNjE4OTM4Nyw0MC45OTQ4NDIyIEwyNS45MjIsMzQuODExIEwyNS45MjI0NzUsNDEgTDE1LDM0Ljc1MDMyNzcgTDE1LDIyLjI0OTkzNDUgTDI1LjkyMjczOTUsMTYgWiIgaWQ9IkNvbWJpbmVkLVNoYXBlIj48L3BhdGg+CiAgICAgICAgICAgICAgICA8L2c+CiAgICAgICAgICAgIDwvZz4KICAgICAgICA8L2c+CiAgICA8L2c+Cjwvc3ZnPg==)

# Software Design & Architecture Project

**Original Design - UML Diagrams**

---

**Student:** Michiel Brand
**Student Number:** Q173978195964068764
**Date:** 26 October 2025

---

</div>

# Original Design - UML Diagrams

This document contains UML diagrams representing the original parking lot manager architecture before refactoring.

---

## Structural UML Diagram (Class Diagram) - Original Design

```mermaid
classDiagram
    class Vehicle {
        -string regnum
        -string make
        -string model
        -string color
        +getMake() string
        +getModel() string
        +getColor() string
        +getRegNum() string
        +getType() string
    }

    class Car {
        +getType() string
    }

    class Truck {
        +getType() string
    }

    class Motorcycle {
        +getType() string
    }

    class Bus {
        +getType() string
    }

    class ElectricVehicle {
        -string regnum
        -string make
        -string model
        -string color
        -int charge
        +getMake() string
        +getModel() string
        +getColor() string
        +getRegNum() string
        +getCharge() int
        +setCharge(int) void
    }

    class ElectricCar {
        +getType() string
    }

    class ElectricBike {
        +getType() string
    }

    class ParkingLot {
        -int capacity
        -int evCapacity
        -int level
        -int slotid
        -int slotEvId
        -int numOfOccupiedSlots
        -int numOfOccupiedEvSlots
        -list slots
        -list evSlots
        +createParkingLot(capacity, evcapacity, level)
        +park(regnum, make, model, color, ev, motor)
        +leave(slotid, ev) bool
        +getSlotNumFromColor(color) list
        +getSlotNumFromColorEv(color) list
        +status() void
    }

    Vehicle <|-- Car
    Vehicle <|-- Truck
    Vehicle <|-- Motorcycle
    Vehicle <|-- Bus
    ElectricCar --|> ElectricVehicle
    ElectricBike --|> ElectricVehicle
    ParkingLot --> Vehicle
    ParkingLot --> ElectricVehicle
```

---

## Issues Summary

| Code Smell | Impact |
|-----------|--------|
| **Tight GUI-Business Coupling** | Cannot test business logic without GUI |
| **Global Variables (23+)** | Hard to track state, not thread-safe |
| **9 Duplicate Search Methods** | 100+ lines of copy-paste code |
| **Complex Nested Conditionals** | 4+ nesting levels, hard to understand |
| **Boolean Magic Numbers** | `ev=1`, `motor=1` unclear intent |
| **Magic Number -1** | Silent failures for errors |
| **Inconsistent Inheritance** | ElectricCar/Bike don't properly inherit |
| **Poor Variable Naming** | `slotid`, `regnum`, `numOfOccupiedSlots` cryptic |
| **No Error Handling** | Silent failures, no exceptions |

---

## Activity Diagram - park() Method (Original)

```mermaid
flowchart TD
    Start([User Clicks Park]) --> ReadGlobal["Read Global Variables<br/>make_value, model_value,<br/>color_value, etc."]
    
    ReadGlobal --> Check1{"Is ev == 1?<br/>Magic number"}
    
    Check1 -->|YES| CheckEVCap{"Occupied EV Slots<br/>< Capacity?<br/>4+ nesting levels"}
    Check1 -->|NO| CheckRegCap{"Occupied Reg Slots<br/>< Capacity?"}
    
    CheckEVCap -->|YES| GetEVSlot["Find empty EV slot"]
    CheckEVCap -->|NO| ReturnError1["Return -1<br/>Silent failure"]
    
    CheckRegCap -->|YES| GetRegSlot["Find empty regular slot"]
    CheckRegCap -->|NO| ReturnError2["Return -1"]
    
    GetEVSlot --> CheckMotor1{"motor == 1?<br/>4 levels nesting"}
    GetRegSlot --> CheckMotor2{"motor == 1?"}
    
    CheckMotor1 -->|YES| CreateEVBike["Create ElectricBike<br/>Logic embedded"]
    CheckMotor1 -->|NO| CreateEVCar["Create ElectricCar"]
    
    CheckMotor2 -->|YES| CreateCar["Create Car<br/>WRONG! motor=1<br/>should be Motorcycle"]
    CheckMotor2 -->|NO| CreateMotor["Create Motorcycle<br/>WRONG mapping!"]
    
    CreateEVBike --> UpdateEV["Manual counter updates<br/>slotEvId++<br/>numOfOccupiedEvSlots++"]
    CreateEVCar --> UpdateEV
    CreateCar --> UpdateReg["Manual counter updates"]
    CreateMotor --> UpdateReg
    
    UpdateEV --> ReturnSuccess1["Return slot ID"]
    UpdateReg --> ReturnSuccess2["Return slot ID"]
    
    ReturnError1 --> UIDisplay["GUI update in business logic<br/>tfield.insert()"]
    ReturnError2 --> UIDisplay
    ReturnSuccess1 --> UIDisplay
    ReturnSuccess2 --> UIDisplay
    
    UIDisplay --> End([Done])
    
    style Check1 fill:#ff6b6b,color:#fff
    style CheckEVCap fill:#ff6b6b,color:#fff
    style CheckRegCap fill:#ff6b6b,color:#fff
    style CheckMotor1 fill:#ff6b6b,color:#fff
    style CheckMotor2 fill:#ff6b6b,color:#fff
    style ReturnError1 fill:#ff6b6b,color:#fff
    style ReturnError2 fill:#ff6b6b,color:#fff
    style CreateCar fill:#ff6b6b,color:#fff
    style CreateMotor fill:#ff6b6b,color:#fff
    style UIDisplay fill:#ff6b6b,color:#fff
```

---

## Complexity Metrics - Original Design

```mermaid
graph LR
    subgraph Metrics["Code Quality Metrics"]
        A["Cyclomatic Complexity<br/>park(): 8+"]
        B["Duplicate Code<br/>9 search methods"]
        C["Global Variables<br/>23+"]
        D["Nesting Levels<br/>4+"]
        E["Testability<br/>0%"]
    end
    
    subgraph Consequences["Consequences"]
        F["Hard to Test"]
        G["Hard to Maintain"]
        H["Hard to Extend"]
        L["Bug-Prone"]
        M["Not Reusable"]
    end
    
    A --> F
    B --> G
    C --> F
    D --> G
    E --> F
    
    style Metrics fill:#ff6b6b,color:#fff
    style Consequences fill:#ff4757,color:#fff
    style A fill:#ff6b6b,color:#fff
    style B fill:#ff6b6b,color:#fff
    style C fill:#ff6b6b,color:#fff
    style D fill:#ff6b6b,color:#fff
    style E fill:#ff6b6b,color:#fff
```

---

## Dependency and Coupling Issues

```mermaid
graph TD
    subgraph GUI["GUI Layer - Global Namespace"]
        root["Global: root"]
        vars["23+ Global Variables"]
        tfield["Global: tfield Text Widget"]
    end
    
    subgraph Business["Business Logic Layer<br/>ParkingManager.py"]
        park["park() 4+ nesting<br/>Vehicle creation embedded"]
        search["9 search methods<br/>100+ duplicate lines"]
        status["status() manipulates GUI"]
    end
    
    subgraph Models["Model Layer"]
        vehicle["Vehicle hierarchy<br/>Proper inheritance"]
        evehicle["ElectricVehicle<br/>No proper inheritance"]
    end
    
    root -.->|tight coupling| park
    vars -.->|tight coupling| Business
    tfield -.->|tight coupling| status
    
    park -->|creates| vehicle
    park -->|creates| evehicle
    search -->|accesses| vehicle
    status -->|manipulates| tfield
    
    style GUI fill:#ff6b6b,color:#fff
    style Business fill:#ff4757,color:#fff
    style tfield fill:#ff6b6b,color:#fff
    style root fill:#ff6b6b,color:#fff
    style park fill:#ff4757,color:#fff
    style search fill:#ff4757,color:#fff
    style status fill:#ff4757,color:#fff
    style evehicle fill:#ffb359,color:#fff
```

---

## Key Problems Summary

### High Severity Issues

1. **Tight Coupling**: GUI and business logic intertwined
   - Cannot test business logic independently
   - Cannot reuse logic in different UI

2. **Global State**: 23+ global variables
   - Difficult to track dependencies
   - Not thread-safe
   - Makes code fragile

3. **Duplicate Code**: 9 search methods with identical logic
   - 100+ lines of copy-paste code
   - Maintenance nightmare
   - Bugs need fixing in multiple places

4. **Complex Logic**: park() method has 4+ nesting levels
   - Hard to understand
   - Hard to maintain
   - Difficult to test

### Medium Severity Issues

5. **Boolean Magic Numbers**: `ev=1`, `motor=1`
   - Unclear intent
   - Error-prone
   - Self-documenting code impossible

6. **Silent Failures**: Magic number `-1` for errors
   - No indication of failure reason
   - Hard to debug
   - Poor error handling

7. **Inconsistent Inheritance**: ElectricCar/Bike don't inherit
   - Type checking broken
   - Polymorphism not working
   - Code smell: improper OOP

8. **Poor Naming**: `slotid`, `regnum`, `numOfOccupiedSlots`
   - Reduces readability
   - Faster code rot
   - Hard onboarding

9. **No Exception Handling**
   - Silent failures
   - Unprofessional error handling
   - Poor user experience

---

## Conclusion

The original design shows classic anti-patterns that make the codebase:

- **Monolithic** - Everything in one file
- **Tightly Coupled** - GUI and logic inseparable
- **Untestable** - Cannot test without GUI
- **Duplicated** - Copy-paste code everywhere
- **Complex** - Deep nesting and cryptic logic
- **Not Reusable** - Business logic tied to GUI
- **Hard to Maintain** - Changes needed in multiple places

These issues prompted the need for comprehensive refactoring using design patterns and best practices.
