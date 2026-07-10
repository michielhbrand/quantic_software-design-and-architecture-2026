"""
ParkingStrategy module - Strategy Pattern implementation for vehicle slot handling.

This module implements the Strategy Pattern to eliminate duplicate code for
handling regular vs. electric vehicle slots. Addresses Code Smell 3:
Duplicate Search Methods for regular and EV slots.
"""

from abc import ABC, abstractmethod


class ParkingStrategy(ABC):
    """
    Abstract base class for parking slot management strategies.
    
    Implements the Strategy Pattern (Behavioral) to encapsulate different
    algorithms for managing regular and electric vehicle slots.
    """
    
    @abstractmethod
    def get_slots(self):
        """Get the slots managed by this strategy."""
        pass
    
    @abstractmethod
    def find_empty_slot(self):
        """Find next empty slot. Returns index or -1 if full."""
        pass
    
    @abstractmethod
    def allocate_slot(self, slot_index, vehicle):
        """Allocate a vehicle to a slot."""
        pass
    
    @abstractmethod
    def deallocate_slot(self, slot_index):
        """Deallocate/remove vehicle from a slot."""
        pass
    
    @abstractmethod
    def get_occupied_count(self):
        """Get count of occupied slots."""
        pass
    
    @abstractmethod
    def is_full(self):
        """Check if all slots are occupied."""
        pass
    
    @abstractmethod
    def search_by_registration(self, registration_number):
        """
        Find slot index by registration number.
        Returns slot index (0-based) or -1 if not found.
        """
        pass
    
    @abstractmethod
    def search_by_color(self, color):
        """
        Find all slot indices by vehicle color.
        Returns list of slot indices (0-based).
        """
        pass
    
    @abstractmethod
    def search_by_make(self, make):
        """
        Find all slot indices by vehicle make.
        Returns list of slot indices (0-based).
        """
        pass
    
    @abstractmethod
    def search_by_model(self, model):
        """
        Find all slot indices by vehicle model.
        Returns list of slot indices (0-based).
        """
        pass


class RegularVehicleStrategy(ParkingStrategy):
    """
    Strategy for managing regular (non-electric) vehicle parking slots.
    
    Handles all operations for regular vehicle slots without special
    charging requirements.
    """
    
    def __init__(self, parking_lot):
        """
        Initialize the regular vehicle strategy.
        
        Args:
            parking_lot: Reference to ParkingLot instance
        """
        self._parking_lot = parking_lot
    
    def get_slots(self):
        """
        Get the slots managed by this strategy.
        
        Returns:
            list: Array of regular vehicle slots
        """
        return self._parking_lot._regular_slots
    
    def find_empty_slot(self):
        """
        Find next empty regular slot.
        
        Returns:
            int: Index of empty slot or -1 if full
        """
        for i in range(len(self._parking_lot._regular_slots)):
            if self._parking_lot._regular_slots[i] is None:
                return i
        return -1
    
    def allocate_slot(self, slot_index, vehicle):
        """
        Allocate a vehicle to a regular slot.
        
        Args:
            slot_index (int): Slot index to allocate
            vehicle: Vehicle instance to park
            
        Raises:
            ValueError: If slot is out of bounds or already occupied
        """
        if slot_index < 0 or slot_index >= len(self._parking_lot._regular_slots):
            raise ValueError(f"Slot index {slot_index} out of bounds")
        
        if self._parking_lot._regular_slots[slot_index] is not None:
            raise ValueError(f"Slot {slot_index} is already occupied")
        
        self._parking_lot._regular_slots[slot_index] = vehicle
        self._parking_lot._occupied_regular_slots += 1
    
    def deallocate_slot(self, slot_index):
        """
        Remove vehicle from a regular slot.
        
        Args:
            slot_index (int): Slot index to deallocate
            
        Raises:
            ValueError: If slot is out of bounds or empty
        """
        if slot_index < 0 or slot_index >= len(self._parking_lot._regular_slots):
            raise ValueError(f"Slot index {slot_index} out of bounds")
        
        if self._parking_lot._regular_slots[slot_index] is None:
            raise ValueError(f"Slot {slot_index} is already empty")
        
        self._parking_lot._regular_slots[slot_index] = None
        self._parking_lot._occupied_regular_slots -= 1
    
    def get_occupied_count(self):
        """
        Get count of occupied regular slots.
        
        Returns:
            int: Number of occupied slots
        """
        return self._parking_lot._occupied_regular_slots
    
    def is_full(self):
        """
        Check if all regular slots are occupied.
        
        Returns:
            bool: True if full, False otherwise
        """
        return self._parking_lot._occupied_regular_slots >= len(
            self._parking_lot._regular_slots
        )
    
    def search_by_registration(self, registration_number):
        """
        Find slot index by vehicle registration number.
        
        Args:
            registration_number (str): Registration number to search
            
        Returns:
            int: Slot index (0-based) or -1 if not found
        """
        for i, vehicle in enumerate(self._parking_lot._regular_slots):
            if vehicle is not None and vehicle.get_registration_number() == registration_number:
                return i
        return -1
    
    def search_by_color(self, color):
        """
        Find all slot indices by vehicle color.
        
        Args:
            color (str): Color to search
            
        Returns:
            list: Slot indices (0-based) where vehicles of this color are parked
        """
        results = []
        for i, vehicle in enumerate(self._parking_lot._regular_slots):
            if vehicle is not None and vehicle.get_color() == color:
                results.append(i)
        return results
    
    def search_by_make(self, make):
        """
        Find all slot indices by vehicle make.
        
        Args:
            make (str): Make to search
            
        Returns:
            list: Slot indices (0-based) where vehicles of this make are parked
        """
        results = []
        for i, vehicle in enumerate(self._parking_lot._regular_slots):
            if vehicle is not None and vehicle.get_make() == make:
                results.append(i)
        return results
    
    def search_by_model(self, model):
        """
        Find all slot indices by vehicle model.
        
        Args:
            model (str): Model to search
            
        Returns:
            list: Slot indices (0-based) where vehicles of this model are parked
        """
        results = []
        for i, vehicle in enumerate(self._parking_lot._regular_slots):
            if vehicle is not None and vehicle.get_model() == model:
                results.append(i)
        return results


class ElectricVehicleStrategy(ParkingStrategy):
    """
    Strategy for managing electric vehicle parking slots.
    
    Handles all operations for electric vehicle slots, including
    charging station management and charge tracking.
    """
    
    def __init__(self, parking_lot):
        """
        Initialize the electric vehicle strategy.
        
        Args:
            parking_lot: Reference to ParkingLot instance
        """
        self._parking_lot = parking_lot
    
    def get_slots(self):
        """
        Get the slots managed by this strategy.
        
        Returns:
            list: Array of electric vehicle slots
        """
        return self._parking_lot._electric_slots
    
    def find_empty_slot(self):
        """
        Find next empty electric vehicle slot.
        
        Returns:
            int: Index of empty slot or -1 if full
        """
        for i in range(len(self._parking_lot._electric_slots)):
            if self._parking_lot._electric_slots[i] is None:
                return i
        return -1
    
    def allocate_slot(self, slot_index, vehicle):
        """
        Allocate an electric vehicle to a slot.
        
        Args:
            slot_index (int): Slot index to allocate
            vehicle: Electric vehicle instance to park
            
        Raises:
            ValueError: If slot is out of bounds or already occupied
        """
        if slot_index < 0 or slot_index >= len(self._parking_lot._electric_slots):
            raise ValueError(f"Slot index {slot_index} out of bounds")
        
        if self._parking_lot._electric_slots[slot_index] is not None:
            raise ValueError(f"Slot {slot_index} is already occupied")
        
        self._parking_lot._electric_slots[slot_index] = vehicle
        self._parking_lot._occupied_electric_slots += 1
    
    def deallocate_slot(self, slot_index):
        """
        Remove electric vehicle from a slot.
        
        Args:
            slot_index (int): Slot index to deallocate
            
        Raises:
            ValueError: If slot is out of bounds or empty
        """
        if slot_index < 0 or slot_index >= len(self._parking_lot._electric_slots):
            raise ValueError(f"Slot index {slot_index} out of bounds")
        
        if self._parking_lot._electric_slots[slot_index] is None:
            raise ValueError(f"Slot {slot_index} is already empty")
        
        self._parking_lot._electric_slots[slot_index] = None
        self._parking_lot._occupied_electric_slots -= 1
    
    def get_occupied_count(self):
        """
        Get count of occupied electric slots.
        
        Returns:
            int: Number of occupied electric slots
        """
        return self._parking_lot._occupied_electric_slots
    
    def is_full(self):
        """
        Check if all electric slots are occupied.
        
        Returns:
            bool: True if full, False otherwise
        """
        return self._parking_lot._occupied_electric_slots >= len(
            self._parking_lot._electric_slots
        )
    
    def search_by_registration(self, registration_number):
        """
        Find slot index by vehicle registration number.
        
        Args:
            registration_number (str): Registration number to search
            
        Returns:
            int: Slot index (0-based) or -1 if not found
        """
        for i, vehicle in enumerate(self._parking_lot._electric_slots):
            if vehicle is not None and vehicle.get_registration_number() == registration_number:
                return i
        return -1
    
    def search_by_color(self, color):
        """
        Find all slot indices by vehicle color.
        
        Args:
            color (str): Color to search
            
        Returns:
            list: Slot indices (0-based) where vehicles of this color are parked
        """
        results = []
        for i, vehicle in enumerate(self._parking_lot._electric_slots):
            if vehicle is not None and vehicle.get_color() == color:
                results.append(i)
        return results
    
    def search_by_make(self, make):
        """
        Find all slot indices by vehicle make.
        
        Args:
            make (str): Make to search
            
        Returns:
            list: Slot indices (0-based) where vehicles of this make are parked
        """
        results = []
        for i, vehicle in enumerate(self._parking_lot._electric_slots):
            if vehicle is not None and vehicle.get_make() == make:
                results.append(i)
        return results
    
    def search_by_model(self, model):
        """
        Find all slot indices by vehicle model.
        
        Args:
            model (str): Model to search
            
        Returns:
            list: Slot indices (0-based) where vehicles of this model are parked
        """
        results = []
        for i, vehicle in enumerate(self._parking_lot._electric_slots):
            if vehicle is not None and vehicle.get_model() == model:
                results.append(i)
        return results
    
    def get_charge_status(self):
        """
        Get charge status for all parked electric vehicles.
        
        Returns:
            list: List of tuples (slot_index, registration_number, charge_level)
        """
        status = []
        for i, vehicle in enumerate(self._parking_lot._electric_slots):
            if vehicle is not None:
                status.append((
                    i,
                    vehicle.get_registration_number(),
                    vehicle.get_charge_level()
                ))
        return status
