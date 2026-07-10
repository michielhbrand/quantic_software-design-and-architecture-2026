"""
ParkingManager module - Refactored GUI application with separation of concerns.

This module implements the GUI layer with improved separation from business logic.
The original ParkingManager had GUI and business logic tightly coupled.
This version uses the refactored ParkingLot class for clean separation.
Addresses Code Smell 5: Mixing Concerns and Code Smell 7: Global Variables.
"""

import tkinter as tk
from tkinter import messagebox

from ParkingLot import (
    ParkingLot,
    ParkingLotFullException,
    InvalidSlotException,
    VehicleNotFoundException,
)
from VehicleFactory import VehicleFactory


class ParkingManagerGUI:
    """
    GUI controller for the Parking Lot Manager application.
    
    Encapsulates all GUI-related code and interactions, using ParkingLot
    for all business logic. Eliminates global variables by encapsulating
    them in class state.
    """
    
    # Configuration constants (replaces magic numbers from Code Smell 8)
    WINDOW_WIDTH = 650
    WINDOW_HEIGHT = 850
    TEXT_FIELD_WIDTH = 70
    TEXT_FIELD_HEIGHT = 15
    FONT_TITLE = ("Arial", 14, "bold")
    FONT_HEADING = ("Arial", 12, "bold")
    FONT_NORMAL = ("Arial", 12)
    
    def __init__(self):
        """Initialize the GUI application."""
        # Create root window
        self.root = tk.Tk()
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.root.resizable(0, 0)
        self.root.title("Parking Lot Manager (Improved)")
        self.root.config(bg="white")
        
        # Business logic layer (no longer global)
        self._parking_lot = ParkingLot()
        
        # Input variables (encapsulated, no longer global)
        self._num_regular_slots = tk.StringVar()
        self._num_electric_slots = tk.StringVar()
        self._floor_level = tk.StringVar()
        self._floor_level.set("1")
        
        self._vehicle_make = tk.StringVar()
        self._vehicle_model = tk.StringVar()
        self._vehicle_color = tk.StringVar()
        self._vehicle_registration = tk.StringVar()
        self._is_electric = tk.BooleanVar()
        self._is_motorcycle = tk.BooleanVar()
        
        self._remove_slot_number = tk.StringVar()
        self._search_registration = tk.StringVar()
        self._search_color = tk.StringVar()
        
        # Output text widget (encapsulated, no longer global)
        self._output_text = tk.Text(
            self.root,
            width=self.TEXT_FIELD_WIDTH,
            height=self.TEXT_FIELD_HEIGHT,
            bg="white",
            fg="black"
        )
        
        # Build GUI
        self._build_gui()
    
    def _build_gui(self):
        """Build the GUI components."""
        # Title
        title_label = tk.Label(
            self.root,
            text="Parking Lot Manager",
            font=self.FONT_TITLE,
            bg="white",
            fg="black"
        )
        title_label.grid(row=0, column=0, padx=10, columnspan=4, pady=10)
        
        # ==================== LOT CREATION SECTION ====================
        creation_label = tk.Label(
            self.root,
            text="Lot Creation",
            font=self.FONT_HEADING,
            bg="white",
            fg="black"
        )
        creation_label.grid(row=1, column=0, padx=10, columnspan=4)
        
        # Regular slots input
        tk.Label(self.root, text="Regular Slots", font=self.FONT_NORMAL, bg="white", fg="black").grid(
            row=2, column=0, padx=5, sticky="w"
        )
        tk.Entry(
            self.root,
            textvariable=self._num_regular_slots,
            width=6,
            font=self.FONT_NORMAL,
            bg="white",
            fg="black"
        ).grid(row=2, column=1, padx=4, pady=2)
        
        # Electric slots input
        tk.Label(self.root, text="Electric Slots", font=self.FONT_NORMAL, bg="white", fg="black").grid(
            row=2, column=2, padx=5, sticky="w"
        )
        tk.Entry(
            self.root,
            textvariable=self._num_electric_slots,
            width=6,
            font=self.FONT_NORMAL,
            bg="white",
            fg="black"
        ).grid(row=2, column=3, padx=4, pady=2)
        
        # Floor level input
        tk.Label(self.root, text="Floor Level", font=self.FONT_NORMAL, bg="white", fg="black").grid(
            row=3, column=0, padx=5, sticky="w"
        )
        tk.Entry(
            self.root,
            textvariable=self._floor_level,
            width=6,
            font=self.FONT_NORMAL,
            bg="white",
            fg="black"
        ).grid(row=3, column=1, padx=4, pady=4)
        
        # Create parking lot button
        tk.Button(
            self.root,
            command=self._on_create_lot,
            text="Create Parking Lot",
            font=self.FONT_NORMAL,
            padx=5,
            pady=5
        ).grid(row=4, column=0, padx=4, pady=4)
        
        # ==================== VEHICLE PARKING SECTION ====================
        parking_label = tk.Label(
            self.root,
            text="Vehicle Parking",
            font=self.FONT_HEADING,
            bg="white",
            fg="black"
        )
        parking_label.grid(row=5, column=0, padx=10, columnspan=4)
        
        # Vehicle details inputs
        tk.Label(self.root, text="Make", font=self.FONT_NORMAL, bg="white", fg="black").grid(
            row=6, column=0, padx=5, sticky="w"
        )
        tk.Entry(
            self.root,
            textvariable=self._vehicle_make,
            width=12,
            font=self.FONT_NORMAL,
            bg="white",
            fg="black"
        ).grid(row=6, column=1, padx=4, pady=4)
        
        tk.Label(self.root, text="Model", font=self.FONT_NORMAL, bg="white", fg="black").grid(
            row=6, column=2, padx=5, sticky="w"
        )
        tk.Entry(
            self.root,
            textvariable=self._vehicle_model,
            width=12,
            font=self.FONT_NORMAL,
            bg="white",
            fg="black"
        ).grid(row=6, column=3, padx=4, pady=4)
        
        tk.Label(self.root, text="Color", font=self.FONT_NORMAL, bg="white", fg="black").grid(
            row=7, column=0, padx=5, sticky="w"
        )
        tk.Entry(
            self.root,
            textvariable=self._vehicle_color,
            width=12,
            font=self.FONT_NORMAL,
            bg="white",
            fg="black"
        ).grid(row=7, column=1, padx=4, pady=4)
        
        tk.Label(self.root, text="Registration #", font=self.FONT_NORMAL, bg="white", fg="black").grid(
            row=7, column=2, padx=5, sticky="w"
        )
        tk.Entry(
            self.root,
            textvariable=self._vehicle_registration,
            width=12,
            font=self.FONT_NORMAL,
            bg="white",
            fg="black"
        ).grid(row=7, column=3, padx=4, pady=4)
        
        # Checkboxes (replaces magic boolean values 0/1)
        tk.Checkbutton(
            self.root,
            text="Electric Vehicle",
            variable=self._is_electric,
            font=self.FONT_NORMAL,
            bg="white",
            fg="black"
        ).grid(column=0, row=8, padx=4, pady=4, sticky="w")
        
        tk.Checkbutton(
            self.root,
            text="Motorcycle",
            variable=self._is_motorcycle,
            font=self.FONT_NORMAL,
            bg="white",
            fg="black"
        ).grid(column=1, row=8, padx=4, pady=4, sticky="w")
        
        # Park vehicle button
        tk.Button(
            self.root,
            command=self._on_park_vehicle,
            text="Park Vehicle",
            font=self.FONT_NORMAL,
            padx=5,
            pady=5
        ).grid(column=0, row=9, padx=4, pady=4)
        
        # ==================== VEHICLE REMOVAL SECTION ====================
        removal_label = tk.Label(
            self.root,
            text="Vehicle Removal",
            font=self.FONT_HEADING,
            bg="white",
            fg="black"
        )
        removal_label.grid(row=10, column=0, padx=10, columnspan=4)
        
        tk.Label(self.root, text="Slot #", font=self.FONT_NORMAL, bg="white", fg="black").grid(
            row=11, column=0, padx=5, sticky="w"
        )
        tk.Entry(
            self.root,
            textvariable=self._remove_slot_number,
            width=12,
            font=self.FONT_NORMAL,
            bg="white",
            fg="black"
        ).grid(row=11, column=1, padx=4, pady=4)
        
        # Remove vehicle button
        tk.Button(
            self.root,
            command=self._on_remove_vehicle,
            text="Remove Vehicle",
            font=self.FONT_NORMAL,
            padx=5,
            pady=5
        ).grid(column=2, row=11, padx=4, pady=4)
        
        # ==================== SEARCH SECTION ====================
        search_label = tk.Label(
            self.root,
            text="Vehicle Search",
            font=self.FONT_HEADING,
            bg="white",
            fg="black"
        )
        search_label.grid(row=12, column=0, padx=10, columnspan=4)
        
        tk.Button(
            self.root,
            command=self._on_search_by_registration,
            text="Find by Registration",
            font=self.FONT_NORMAL,
            padx=5,
            pady=5
        ).grid(column=0, row=13, padx=4, pady=4)
        
        tk.Entry(
            self.root,
            textvariable=self._search_registration,
            width=12,
            font=self.FONT_NORMAL,
            bg="white",
            fg="black"
        ).grid(row=13, column=1, padx=4, pady=4)
        
        tk.Button(
            self.root,
            command=self._on_search_by_color,
            text="Find by Color",
            font=self.FONT_NORMAL,
            padx=5,
            pady=5
        ).grid(column=2, row=13, padx=4, pady=4)
        
        tk.Entry(
            self.root,
            textvariable=self._search_color,
            width=12,
            font=self.FONT_NORMAL,
            bg="white",
            fg="black"
        ).grid(row=13, column=3, padx=4, pady=4)
        
        # ==================== STATUS SECTION ====================
        status_label = tk.Label(
            self.root,
            text="Status",
            font=self.FONT_HEADING,
            bg="white",
            fg="black"
        )
        status_label.grid(row=14, column=0, padx=10, columnspan=4)
        
        tk.Button(
            self.root,
            command=self._on_show_status,
            text="Show All Vehicles",
            font=self.FONT_NORMAL,
            padx=5,
            pady=5
        ).grid(column=0, row=15, padx=4, pady=4)
        
        tk.Button(
            self.root,
            command=self._on_show_charge_status,
            text="EV Charge Status",
            font=self.FONT_NORMAL,
            padx=5,
            pady=5
        ).grid(column=2, row=15, padx=4, pady=4)
        
        # Output text area
        self._output_text.grid(column=0, row=16, padx=10, pady=10, columnspan=4)
    
    # ==================== EVENT HANDLERS ====================
    
    def _on_create_lot(self):
        """Handle parking lot creation."""
        try:
            regular_str = self._num_regular_slots.get().strip()
            electric_str = self._num_electric_slots.get().strip()
            level_str = self._floor_level.get().strip()
            
            if not all([regular_str, electric_str, level_str]):
                messagebox.showwarning("Error", "All lot creation fields are required")
                return
            
            regular_slots = int(regular_str)
            electric_slots = int(electric_str)
            level = int(level_str)
            
            self._parking_lot.initialize(regular_slots, electric_slots, level)
            
            self._append_output(
                f"✓ Created parking lot with {regular_slots} regular slots, "
                f"{electric_slots} electric slots on level {level}\n"
            )
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create lot: {e}")
    
    def _on_park_vehicle(self):
        """Handle vehicle parking."""
        try:
            # Validate inputs
            make = self._vehicle_make.get().strip()
            model = self._vehicle_model.get().strip()
            color = self._vehicle_color.get().strip()
            registration = self._vehicle_registration.get().strip()
            
            if not all([make, model, color, registration]):
                messagebox.showwarning("Error", "All vehicle fields are required")
                return
            
            # Determine vehicle type
            is_electric = self._is_electric.get()
            is_motorcycle = self._is_motorcycle.get()
            
            if is_electric:
                vehicle_type = (
                    VehicleFactory.ELECTRIC_BIKE
                    if is_motorcycle
                    else VehicleFactory.ELECTRIC_CAR
                )
            else:
                vehicle_type = (
                    VehicleFactory.REGULAR_MOTORCYCLE
                    if is_motorcycle
                    else VehicleFactory.REGULAR_CAR
                )
            
            # Park vehicle
            slot_index, is_ev = self._parking_lot.park_vehicle(
                vehicle_type, registration, make, model, color
            )
            
            slot_type = "Electric" if is_ev else "Regular"
            self._append_output(
                f"✓ Parked {vehicle_type} in {slot_type} Slot #{slot_index + 1}\n"
            )
            
            # Clear inputs
            self._vehicle_make.set("")
            self._vehicle_model.set("")
            self._vehicle_color.set("")
            self._vehicle_registration.set("")
            self._is_electric.set(False)
            self._is_motorcycle.set(False)
            
        except ParkingLotFullException as e:
            messagebox.showwarning("Lot Full", str(e))
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to park vehicle: {e}")
    
    def _on_remove_vehicle(self):
        """Handle vehicle removal."""
        try:
            slot_str = self._remove_slot_number.get().strip()
            if not slot_str:
                messagebox.showwarning("Error", "Enter slot number")
                return
            
            slot_index = int(slot_str) - 1  # Convert to 0-based
            
            # Try to remove from regular slots first
            try:
                self._parking_lot.remove_vehicle(slot_index, is_electric=False)
                self._append_output(f"✓ Removed vehicle from Slot #{slot_str}\n")
            except InvalidSlotException:
                # Try electric slots
                self._parking_lot.remove_vehicle(slot_index, is_electric=True)
                self._append_output(f"✓ Removed vehicle from Electric Slot #{slot_str}\n")
            
            self._remove_slot_number.set("")
            
        except ValueError:
            messagebox.showerror("Error", "Invalid slot number")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _on_search_by_registration(self):
        """Handle search by registration number."""
        try:
            registration = self._search_registration.get().strip()
            if not registration:
                messagebox.showwarning("Error", "Enter registration number")
                return
            
            slot_index, is_electric = self._parking_lot.find_slot_by_registration(
                registration
            )
            
            if slot_index is not None:
                slot_type = "Electric" if is_electric else "Regular"
                self._append_output(
                    f"Found: {slot_type} Slot #{slot_index + 1}\n"
                )
            else:
                self._append_output("Not found\n")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _on_search_by_color(self):
        """Handle search by vehicle color."""
        try:
            color = self._search_color.get().strip()
            if not color:
                messagebox.showwarning("Error", "Enter color")
                return
            
            results = self._parking_lot.find_slots_by_color(color)
            
            if results["regular"]:
                slots_str = ", ".join(str(i + 1) for i in results["regular"])
                self._append_output(f"Regular slots: {slots_str}\n")
            
            if results["electric"]:
                slots_str = ", ".join(str(i + 1) for i in results["electric"])
                self._append_output(f"Electric slots: {slots_str}\n")
            
            if not results["regular"] and not results["electric"]:
                self._append_output("No vehicles found\n")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _on_show_status(self):
        """Display current parking lot status."""
        try:
            self._append_output("\n" + "="*60 + "\n")
            self._append_output("PARKING LOT STATUS\n")
            self._append_output("="*60 + "\n")
            
            occupancy = self._parking_lot.get_occupancy()
            
            self._append_output("\nRegular Vehicles:\n")
            self._append_output("-" * 60 + "\n")
            self._append_output(
                f"Occupied: {occupancy['regular']['occupied']} / "
                f"{occupancy['regular']['total']} "
                f"(Available: {occupancy['regular']['available']})\n"
            )
            
            self._append_output("\nRegular Vehicle Details:\n")
            self._append_output(
                f"{'Slot':<6} {'Make':<12} {'Model':<12} {'Color':<12} {'Reg#':<12}\n"
            )
            self._append_output("-" * 60 + "\n")
            
            for i, vehicle in enumerate(self._parking_lot._regular_slots):
                if vehicle is not None:
                    self._append_output(
                        f"{i + 1:<6} {vehicle.get_make():<12} "
                        f"{vehicle.get_model():<12} {vehicle.get_color():<12} "
                        f"{vehicle.get_registration_number():<12}\n"
                    )
            
            self._append_output("\nElectric Vehicles:\n")
            self._append_output("-" * 60 + "\n")
            self._append_output(
                f"Occupied: {occupancy['electric']['occupied']} / "
                f"{occupancy['electric']['total']} "
                f"(Available: {occupancy['electric']['available']})\n"
            )
            
            self._append_output("\nElectric Vehicle Details:\n")
            self._append_output(
                f"{'Slot':<6} {'Make':<12} {'Model':<12} {'Color':<12} {'Reg#':<12}\n"
            )
            self._append_output("-" * 60 + "\n")
            
            for i, vehicle in enumerate(self._parking_lot._electric_slots):
                if vehicle is not None:
                    self._append_output(
                        f"{i + 1:<6} {vehicle.get_make():<12} "
                        f"{vehicle.get_model():<12} {vehicle.get_color():<12} "
                        f"{vehicle.get_registration_number():<12}\n"
                    )
            
            self._append_output("="*60 + "\n\n")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _on_show_charge_status(self):
        """Display EV charge status."""
        try:
            self._append_output("\n" + "="*60 + "\n")
            self._append_output("ELECTRIC VEHICLE CHARGE STATUS\n")
            self._append_output("="*60 + "\n")
            
            charge_status = self._parking_lot.get_charge_status()
            
            if not charge_status:
                self._append_output("No electric vehicles parked\n")
            else:
                self._append_output(
                    f"{'Slot':<6} {'Registration#':<20} {'Charge %':<10}\n"
                )
                self._append_output("-" * 60 + "\n")
                
                for slot_index, registration, charge in charge_status:
                    self._append_output(
                        f"{slot_index + 1:<6} {registration:<20} {charge}%\n"
                    )
            
            self._append_output("="*60 + "\n\n")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _append_output(self, text):
        """Append text to output widget."""
        self._output_text.insert(tk.END, text)
        self._output_text.see(tk.END)
    
    def run(self):
        """Start the application main loop."""
        self.root.mainloop()


def main():
    """Application entry point."""
    app = ParkingManagerGUI()
    app.run()


if __name__ == "__main__":
    main()
