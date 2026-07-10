"""
ElectricVehicle module - Electric vehicle classes with proper inheritance.

This module fixes the inheritance issues from the original code where
ElectricCar and ElectricBike didn't properly inherit from ElectricVehicle.
Now uses proper inheritance with super() and explicit charging capabilities.
"""

from Vehicle import Vehicle


class ElectricVehicle(Vehicle):
    """
    Base class for electric vehicles with charging capabilities.
    
    Attributes:
        registration_number (str): Vehicle's registration/license plate
        make (str): Vehicle manufacturer/brand
        model (str): Vehicle model name
        color (str): Vehicle color
        charge_level (int): Current battery charge level (0-100%)
    """
    
    def __init__(self, registration_number, make, model, color):
        """
        Initialize an ElectricVehicle instance.
        
        Args:
            registration_number (str): Vehicle's registration/license plate
            make (str): Vehicle manufacturer/brand
            model (str): Vehicle model name
            color (str): Vehicle color
        """
        super().__init__(registration_number, make, model, color)
        self._charge_level = 0
    
    def get_charge_level(self):
        """
        Get the current battery charge level.
        
        Returns:
            int: Charge level as percentage (0-100)
        """
        return self._charge_level
    
    def set_charge_level(self, charge_level):
        """
        Set the battery charge level.
        
        Args:
            charge_level (int): New charge level as percentage (0-100)
            
        Raises:
            ValueError: If charge level is not between 0 and 100
        """
        if not 0 <= charge_level <= 100:
            raise ValueError(f"Charge level must be between 0 and 100, got {charge_level}")
        self._charge_level = charge_level
    
    def charge_vehicle(self, amount):
        """
        Charge the vehicle by the specified amount.
        
        Args:
            amount (int): Amount to charge (will cap at 100%)
        """
        self._charge_level = min(100, self._charge_level + amount)
    
    def discharge_vehicle(self, amount):
        """
        Discharge the vehicle by the specified amount.
        
        Args:
            amount (int): Amount to discharge (will floor at 0%)
        """
        self._charge_level = max(0, self._charge_level - amount)


class ElectricCar(ElectricVehicle):
    """
    Electric car subclass - represents an electric passenger car.
    Properly inherits from ElectricVehicle with charging capabilities.
    """
    
    def get_type(self):
        """
        Get the vehicle type.
        
        Returns:
            str: "ElectricCar"
        """
        return "ElectricCar"


class ElectricBike(ElectricVehicle):
    """
    Electric bike/motorcycle subclass - represents an electric two-wheeler.
    Properly inherits from ElectricVehicle with charging capabilities.
    """
    
    def get_type(self):
        """
        Get the vehicle type.
        
        Returns:
            str: "ElectricBike"
        """
        return "ElectricBike"
