"""
VehicleFactory module - Factory Pattern implementation for vehicle creation.

This module implements the Factory Pattern to centralize vehicle creation logic,
eliminating complex conditionals scattered throughout the application.
Addresses Code Smell 4: Complex Conditional Logic in park() method.
"""

from Vehicle import Car, Truck, Motorcycle, Bus
from ElectricVehicle import ElectricCar, ElectricBike


class VehicleFactory:
    """
    Factory class for creating vehicle instances.
    
    Implements the Factory Pattern (Creational) to:
    - Centralize vehicle creation logic
    - Eliminate complex conditional logic from business methods
    - Provide a single point for vehicle instantiation
    - Make it easy to add new vehicle types without modifying park() logic
    """
    
    # Vehicle type constants
    REGULAR_CAR = "regular_car"
    REGULAR_TRUCK = "regular_truck"
    REGULAR_MOTORCYCLE = "regular_motorcycle"
    REGULAR_BUS = "regular_bus"
    ELECTRIC_CAR = "electric_car"
    ELECTRIC_BIKE = "electric_bike"
    
    # All valid vehicle types
    VALID_TYPES = {
        REGULAR_CAR,
        REGULAR_TRUCK,
        REGULAR_MOTORCYCLE,
        REGULAR_BUS,
        ELECTRIC_CAR,
        ELECTRIC_BIKE,
    }
    
    @staticmethod
    def create_vehicle(vehicle_type, registration_number, make, model, color):
        """
        Create a vehicle instance of the specified type.
        
        Factory method that handles all vehicle creation logic, replacing the
        complex nested conditionals that were previously in park() method.
        
        Args:
            vehicle_type (str): Type of vehicle to create (see VALID_TYPES)
            registration_number (str): Vehicle's registration/license plate
            make (str): Vehicle manufacturer/brand
            model (str): Vehicle model name
            color (str): Vehicle color
            
        Returns:
            Vehicle: An instance of the requested vehicle type
            
        Raises:
            ValueError: If vehicle_type is not recognized
            TypeError: If required parameters are not strings
            
        Example:
            >>> car = VehicleFactory.create_vehicle(
            ...     VehicleFactory.REGULAR_CAR,
            ...     "ABC123",
            ...     "Toyota",
            ...     "Camry",
            ...     "Blue"
            ... )
            >>> car.get_type()
            'Car'
        """
        # Validate input parameters
        VehicleFactory._validate_parameters(
            registration_number, make, model, color
        )
        
        # Validate vehicle type
        if vehicle_type not in VehicleFactory.VALID_TYPES:
            raise ValueError(
                f"Invalid vehicle type: {vehicle_type}. "
                f"Valid types: {', '.join(sorted(VehicleFactory.VALID_TYPES))}"
            )
        
        # Create and return appropriate vehicle instance
        if vehicle_type == VehicleFactory.REGULAR_CAR:
            return Car(registration_number, make, model, color)
        
        elif vehicle_type == VehicleFactory.REGULAR_TRUCK:
            return Truck(registration_number, make, model, color)
        
        elif vehicle_type == VehicleFactory.REGULAR_MOTORCYCLE:
            return Motorcycle(registration_number, make, model, color)
        
        elif vehicle_type == VehicleFactory.REGULAR_BUS:
            return Bus(registration_number, make, model, color)
        
        elif vehicle_type == VehicleFactory.ELECTRIC_CAR:
            return ElectricCar(registration_number, make, model, color)
        
        elif vehicle_type == VehicleFactory.ELECTRIC_BIKE:
            return ElectricBike(registration_number, make, model, color)
    
    @staticmethod
    def create_regular_vehicle(vehicle_subtype, registration_number, make, model, color):
        """
        Create a regular (non-electric) vehicle.
        
        Convenience method for creating regular vehicles without needing to know
        the exact type constant.
        
        Args:
            vehicle_subtype (str): "car", "truck", "motorcycle", or "bus"
            registration_number (str): Vehicle's registration/license plate
            make (str): Vehicle manufacturer/brand
            model (str): Vehicle model name
            color (str): Vehicle color
            
        Returns:
            Vehicle: A regular vehicle instance
            
        Raises:
            ValueError: If vehicle_subtype is not recognized
        """
        subtype_map = {
            "car": VehicleFactory.REGULAR_CAR,
            "truck": VehicleFactory.REGULAR_TRUCK,
            "motorcycle": VehicleFactory.REGULAR_MOTORCYCLE,
            "bus": VehicleFactory.REGULAR_BUS,
        }
        
        if vehicle_subtype not in subtype_map:
            raise ValueError(
                f"Invalid regular vehicle subtype: {vehicle_subtype}. "
                f"Valid subtypes: {', '.join(sorted(subtype_map.keys()))}"
            )
        
        return VehicleFactory.create_vehicle(
            subtype_map[vehicle_subtype],
            registration_number,
            make,
            model,
            color
        )
    
    @staticmethod
    def create_electric_vehicle(vehicle_subtype, registration_number, make, model, color):
        """
        Create an electric vehicle.
        
        Convenience method for creating electric vehicles without needing to know
        the exact type constant.
        
        Args:
            vehicle_subtype (str): "car" or "bike"
            registration_number (str): Vehicle's registration/license plate
            make (str): Vehicle manufacturer/brand
            model (str): Vehicle model name
            color (str): Vehicle color
            
        Returns:
            ElectricVehicle: An electric vehicle instance
            
        Raises:
            ValueError: If vehicle_subtype is not recognized
        """
        subtype_map = {
            "car": VehicleFactory.ELECTRIC_CAR,
            "bike": VehicleFactory.ELECTRIC_BIKE,
        }
        
        if vehicle_subtype not in subtype_map:
            raise ValueError(
                f"Invalid electric vehicle subtype: {vehicle_subtype}. "
                f"Valid subtypes: {', '.join(sorted(subtype_map.keys()))}"
            )
        
        return VehicleFactory.create_vehicle(
            subtype_map[vehicle_subtype],
            registration_number,
            make,
            model,
            color
        )
    
    @staticmethod
    def _validate_parameters(registration_number, make, model, color):
        """
        Validate vehicle creation parameters.
        
        Args:
            registration_number (str): Vehicle's registration/license plate
            make (str): Vehicle manufacturer/brand
            model (str): Vehicle model name
            color (str): Vehicle color
            
        Raises:
            TypeError: If any parameter is not a string
            ValueError: If any parameter is empty
        """
        params = {
            "registration_number": registration_number,
            "make": make,
            "model": model,
            "color": color,
        }
        
        for param_name, param_value in params.items():
            if not isinstance(param_value, str):
                raise TypeError(
                    f"{param_name} must be a string, got {type(param_value).__name__}"
                )
            
            if not param_value.strip():
                raise ValueError(f"{param_name} cannot be empty")
    
    @staticmethod
    def get_valid_types():
        """
        Get list of all valid vehicle types.
        
        Returns:
            list: Sorted list of valid vehicle type constants
        """
        return sorted(VehicleFactory.VALID_TYPES)
    
    @staticmethod
    def is_electric_vehicle(vehicle_type):
        """
        Check if a vehicle type is electric.
        
        Args:
            vehicle_type (str): The vehicle type to check
            
        Returns:
            bool: True if vehicle is electric, False otherwise
        """
        return vehicle_type in {
            VehicleFactory.ELECTRIC_CAR,
            VehicleFactory.ELECTRIC_BIKE,
        }
