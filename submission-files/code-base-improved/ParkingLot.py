"""
ParkingLot module - Refactored parking lot business logic (separation of concerns).

This module extracts parking lot management logic from the GUI layer,
implementing clean business logic that is testable and reusable.
Addresses Code Smell 5: Mixing Concerns - GUI and Business Logic.
"""

from VehicleFactory import VehicleFactory
from ParkingStrategy import RegularVehicleStrategy, ElectricVehicleStrategy


class ParkingLotException(Exception):
    """Base exception for parking lot operations."""
    pass


class ParkingLotFullException(ParkingLotException):
    """Exception raised when parking lot is full."""
    pass


class VehicleNotFoundException(ParkingLotException):
    """Exception raised when vehicle is not found."""
    pass


class InvalidSlotException(ParkingLotException):
    """Exception raised when slot index is invalid."""
    pass


class ParkingLot:
    """
    Refactored ParkingLot class with improved design.
    
    - Uses Strategy Pattern to eliminate duplicate slot handling code
    - Uses Factory Pattern to eliminate complex vehicle creation logic
    - Separates business logic from GUI layer
    - Provides clean API for parking operations
    - Uses explicit naming conventions
    - Includes error handling with custom exceptions
    
    Attributes:
        level (int): Parking lot floor level
        capacity (int): Number of regular vehicle slots
        electric_capacity (int): Number of electric vehicle slots
    """
    
    # Slot representation constants (replaces magic number -1)
    EMPTY_SLOT = None
    
    def __init__(self):
        """Initialize an empty ParkingLot."""
        self._level = 0
        self._capacity = 0
        self._electric_capacity = 0
        self._regular_slots = []
        self._electric_slots = []
        self._occupied_regular_slots = 0
        self._occupied_electric_slots = 0
        
        # Strategies for handling regular and electric slots
        self._regular_strategy = RegularVehicleStrategy(self)
        self._electric_strategy = ElectricVehicleStrategy(self)
    
    def initialize(self, capacity, electric_capacity, level):
        """
        Initialize parking lot with specified capacities.
        
        Args:
            capacity (int): Number of regular vehicle slots
            electric_capacity (int): Number of electric vehicle slots
            level (int): Floor level of this parking lot
            
        Raises:
            ValueError: If capacity values are not positive integers
        """
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError(f"Capacity must be positive integer, got {capacity}")
        
        if not isinstance(electric_capacity, int) or electric_capacity <= 0:
            raise ValueError(f"Electric capacity must be positive integer, got {electric_capacity}")
        
        if not isinstance(level, int) or level <= 0:
            raise ValueError(f"Level must be positive integer, got {level}")
        
        self._capacity = capacity
        self._electric_capacity = electric_capacity
        self._level = level
        
        # Initialize slot arrays with None (replaces -1)
        self._regular_slots = [self.EMPTY_SLOT] * capacity
        self._electric_slots = [self.EMPTY_SLOT] * electric_capacity
        self._occupied_regular_slots = 0
        self._occupied_electric_slots = 0
    
    # ==================== PARKING OPERATIONS ====================
    
    def park_vehicle(self, vehicle_type, registration_number, make, model, color):
        """
        Park a vehicle in the lot using Factory Pattern.
        
        Replaces original park() method's complex nested conditionals.
        Now uses Factory Pattern for vehicle creation and Strategy Pattern
        for slot allocation.
        
        Args:
            vehicle_type (str): Type of vehicle (see VehicleFactory.VALID_TYPES)
            registration_number (str): Vehicle's registration number
            make (str): Vehicle manufacturer
            model (str): Vehicle model
            color (str): Vehicle color
            
        Returns:
            tuple: (slot_index, is_electric) indicating where vehicle was parked
            
        Raises:
            ValueError: If parameters are invalid
            ParkingLotFullException: If appropriate slots are full
        """
        # Use Factory to create vehicle (eliminates nested conditionals)
        vehicle = VehicleFactory.create_vehicle(
            vehicle_type, registration_number, make, model, color
        )
        
        # Determine if electric and choose appropriate strategy
        is_electric = VehicleFactory.is_electric_vehicle(vehicle_type)
        strategy = self._electric_strategy if is_electric else self._regular_strategy
        
        # Check if appropriate slots are full
        if strategy.is_full():
            vehicle_category = "electric" if is_electric else "regular"
            raise ParkingLotFullException(
                f"All {vehicle_category} slots are full (capacity: {len(strategy.get_slots())})"
            )
        
        # Find empty slot and allocate
        slot_index = strategy.find_empty_slot()
        if slot_index == -1:
            raise ParkingLotFullException("No empty slots available")
        
        strategy.allocate_slot(slot_index, vehicle)
        
        return (slot_index, is_electric)
    
    def remove_vehicle(self, slot_index, is_electric):
        """
        Remove a vehicle from the lot.
        
        Args:
            slot_index (int): Index of slot to remove from
            is_electric (bool): Whether this is an electric slot
            
        Raises:
            ValueError: If slot_index is invalid
            VehicleNotFoundException: If slot is empty
        """
        strategy = self._electric_strategy if is_electric else self._regular_strategy
        
        try:
            strategy.deallocate_slot(slot_index)
        except ValueError as e:
            raise InvalidSlotException(str(e))
    
    # ==================== SEARCH OPERATIONS ====================
    
    def find_slot_by_registration(self, registration_number, search_electric=None):
        """
        Find vehicle slot by registration number.
        
        Unified search method (replaces duplicate getSlotNumFromRegNum* methods).
        Uses strategies to search both regular and electric slots.
        
        Args:
            registration_number (str): Registration number to search
            search_electric (bool): Search electric slots only (None=both)
            
        Returns:
            tuple: (slot_index, is_electric) or (None, None) if not found
        """
        # Search regular slots
        if search_electric != True:
            slot_index = self._regular_strategy.search_by_registration(registration_number)
            if slot_index != -1:
                return (slot_index, False)
        
        # Search electric slots
        if search_electric != False:
            slot_index = self._electric_strategy.search_by_registration(registration_number)
            if slot_index != -1:
                return (slot_index, True)
        
        return (None, None)
    
    def find_slots_by_color(self, color, search_electric=None):
        """
        Find all vehicle slots by color.
        
        Unified search method (replaces duplicate getSlotNumFromColor* methods).
        
        Args:
            color (str): Color to search
            search_electric (bool): Search electric slots only (None=both)
            
        Returns:
            dict: {"regular": [indices], "electric": [indices]}
        """
        results = {"regular": [], "electric": []}
        
        if search_electric != True:
            results["regular"] = self._regular_strategy.search_by_color(color)
        
        if search_electric != False:
            results["electric"] = self._electric_strategy.search_by_color(color)
        
        return results
    
    def find_slots_by_make(self, make, search_electric=None):
        """
        Find all vehicle slots by manufacturer.
        
        Unified search method (replaces duplicate getSlotNumFromMake* methods).
        
        Args:
            make (str): Manufacturer to search
            search_electric (bool): Search electric slots only (None=both)
            
        Returns:
            dict: {"regular": [indices], "electric": [indices]}
        """
        results = {"regular": [], "electric": []}
        
        if search_electric != True:
            results["regular"] = self._regular_strategy.search_by_make(make)
        
        if search_electric != False:
            results["electric"] = self._electric_strategy.search_by_make(make)
        
        return results
    
    def find_slots_by_model(self, model, search_electric=None):
        """
        Find all vehicle slots by model.
        
        Unified search method (replaces duplicate getSlotNumFromModel* methods).
        
        Args:
            model (str): Model to search
            search_electric (bool): Search electric slots only (None=both)
            
        Returns:
            dict: {"regular": [indices], "electric": [indices]}
        """
        results = {"regular": [], "electric": []}
        
        if search_electric != True:
            results["regular"] = self._regular_strategy.search_by_model(model)
        
        if search_electric != False:
            results["electric"] = self._electric_strategy.search_by_model(model)
        
        return results
    
    def get_vehicle(self, slot_index, is_electric):
        """
        Get vehicle at specified slot.
        
        Args:
            slot_index (int): Slot index
            is_electric (bool): Whether this is an electric slot
            
        Returns:
            Vehicle: Vehicle object or None if slot empty
        """
        slots = self._electric_slots if is_electric else self._regular_slots
        if 0 <= slot_index < len(slots):
            return slots[slot_index]
        return None
    
    # ==================== STATUS OPERATIONS ====================
    
    def get_status(self):
        """
        Get complete parking lot status.
        
        Returns:
            dict: Status including occupancy and vehicle details
        """
        return {
            "level": self._level,
            "capacity": self._capacity,
            "electric_capacity": self._electric_capacity,
            "occupied_regular": self._occupied_regular_slots,
            "occupied_electric": self._occupied_electric_slots,
            "regular_slots": self._regular_slots,
            "electric_slots": self._electric_slots,
        }
    
    def get_occupancy(self):
        """
        Get occupancy information.
        
        Returns:
            dict: Occupancy details for regular and electric slots
        """
        return {
            "regular": {
                "occupied": self._occupied_regular_slots,
                "total": self._capacity,
                "available": self._capacity - self._occupied_regular_slots,
            },
            "electric": {
                "occupied": self._occupied_electric_slots,
                "total": self._electric_capacity,
                "available": self._electric_capacity - self._occupied_electric_slots,
            },
        }
    
    def get_charge_status(self):
        """
        Get charge status for all electric vehicles.
        
        Returns:
            list: List of tuples (slot_index, registration_number, charge_level)
        """
        return self._electric_strategy.get_charge_status()
    
    def is_empty(self):
        """
        Check if parking lot is completely empty.
        
        Returns:
            bool: True if no vehicles parked
        """
        return self._occupied_regular_slots == 0 and self._occupied_electric_slots == 0
    
    def is_full(self):
        """
        Check if all slots are occupied.
        
        Returns:
            bool: True if no empty slots
        """
        return self._regular_strategy.is_full() and self._electric_strategy.is_full()
    
    # ==================== PROPERTIES ====================
    
    @property
    def level(self):
        """Get parking lot floor level."""
        return self._level
    
    @property
    def capacity(self):
        """Get regular slot capacity."""
        return self._capacity
    
    @property
    def electric_capacity(self):
        """Get electric slot capacity."""
        return self._electric_capacity
    
    @property
    def occupied_regular_slots(self):
        """Get number of occupied regular slots."""
        return self._occupied_regular_slots
    
    @property
    def occupied_electric_slots(self):
        """Get number of occupied electric slots."""
        return self._occupied_electric_slots
