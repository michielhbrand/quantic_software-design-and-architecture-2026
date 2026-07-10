"""
Vehicle module - Base vehicle classes with improved naming and structure.

This module defines the vehicle hierarchy with explicit names and proper
inheritance patterns to replace the original cryptic variable names.
"""


class Vehicle:
    """
    Base Vehicle class representing a standard parking lot vehicle.
    
    Attributes:
        registration_number (str): Vehicle's registration/license plate
        make (str): Vehicle manufacturer/brand
        model (str): Vehicle model name
        color (str): Vehicle color
    """
    
    def __init__(self, registration_number, make, model, color):
        """
        Initialize a Vehicle instance.
        
        Args:
            registration_number (str): Vehicle's registration/license plate
            make (str): Vehicle manufacturer/brand
            model (str): Vehicle model name
            color (str): Vehicle color
        """
        self._registration_number = registration_number
        self._make = make
        self._model = model
        self._color = color
    
    def get_registration_number(self):
        """
        Get the vehicle's registration number.
        
        Returns:
            str: The vehicle's registration/license plate number
        """
        return self._registration_number
    
    def get_make(self):
        """
        Get the vehicle's manufacturer/brand.
        
        Returns:
            str: The vehicle manufacturer
        """
        return self._make
    
    def get_model(self):
        """
        Get the vehicle's model name.
        
        Returns:
            str: The vehicle model
        """
        return self._model
    
    def get_color(self):
        """
        Get the vehicle's color.
        
        Returns:
            str: The vehicle color
        """
        return self._color
    
    def get_type(self):
        """
        Get the vehicle type.
        
        Returns:
            str: The type of vehicle
        """
        raise NotImplementedError("Subclasses must implement get_type()")


class Car(Vehicle):
    """
    Car subclass - represents a standard passenger car.
    """
    
    def get_type(self):
        """
        Get the vehicle type.
        
        Returns:
            str: "Car"
        """
        return "Car"


class Truck(Vehicle):
    """
    Truck subclass - represents a commercial truck.
    """
    
    def get_type(self):
        """
        Get the vehicle type.
        
        Returns:
            str: "Truck"
        """
        return "Truck"


class Motorcycle(Vehicle):
    """
    Motorcycle subclass - represents a motorcycle or scooter.
    """
    
    def get_type(self):
        """
        Get the vehicle type.
        
        Returns:
            str: "Motorcycle"
        """
        return "Motorcycle"


class Bus(Vehicle):
    """
    Bus subclass - represents a public transport bus.
    """
    
    def get_type(self):
        """
        Get the vehicle type.
        
        Returns:
            str: "Bus"
        """
        return "Bus"
