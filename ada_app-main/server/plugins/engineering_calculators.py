"""
Engineering Calculators Plugin
13 specialized engineering calculation tools
"""

import asyncio
import math
from typing import Dict, List, Any, Optional
import numpy as np
from scipy import constants

from . import PluginBase

class EngineeringCalculatorsPlugin(PluginBase):
    """Plugin for engineering calculations"""
    
    def __init__(self):
        self.name = "engineering_calculators"
        self.calculators = {
            'electrical': self._electrical_calculations,
            'mechanical': self._mechanical_calculations,
            'structural': self._structural_calculations,
            'thermal': self._thermal_calculations,
            'fluid': self._fluid_calculations,
            'chemical': self._chemical_calculations,
            'optical': self._optical_calculations,
            'acoustic': self._acoustic_calculations,
            'materials': self._materials_calculations,
            'control': self._control_calculations,
            'signal': self._signal_calculations,
            'antenna': self._antenna_calculations,
            'power': self._power_calculations
        }
    
    def get_name(self) -> str:
        return self.name
    
    def get_description(self) -> str:
        return "13 specialized engineering calculation tools"
    
    def get_functions(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "electrical_calculator",
                "description": "Electrical engineering calculations (Ohm's Law, Power, Impedance)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "calculation_type": {"type": "string", "description": "Type: 'ohms_law', 'power', 'impedance', 'resonance'"},
                        "voltage": {"type": "number", "description": "Voltage in volts"},
                        "current": {"type": "number", "description": "Current in amperes"},
                        "resistance": {"type": "number", "description": "Resistance in ohms"},
                        "frequency": {"type": "number", "description": "Frequency in Hz"},
                        "inductance": {"type": "number", "description": "Inductance in henries"},
                        "capacitance": {"type": "number", "description": "Capacitance in farads"}
                    },
                    "required": ["calculation_type"]
                }
            },
            {
                "name": "mechanical_calculator",
                "description": "Mechanical engineering calculations (Stress, Strain, Dynamics)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "calculation_type": {"type": "string", "description": "Type: 'stress', 'strain', 'dynamics', 'kinematics'"},
                        "force": {"type": "number", "description": "Force in newtons"},
                        "area": {"type": "number", "description": "Area in square meters"},
                        "length": {"type": "number", "description": "Length in meters"},
                        "mass": {"type": "number", "description": "Mass in kilograms"},
                        "velocity": {"type": "number", "description": "Velocity in m/s"},
                        "acceleration": {"type": "number", "description": "Acceleration in m/s²"}
                    },
                    "required": ["calculation_type"]
                }
            },
            {
                "name": "structural_calculator",
                "description": "Structural engineering calculations (Beam analysis, Column buckling)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "calculation_type": {"type": "string", "description": "Type: 'beam_analysis', 'column_buckling', 'truss_analysis'"},
                        "load": {"type": "number", "description": "Load in newtons"},
                        "length": {"type": "number", "description": "Length in meters"},
                        "modulus": {"type": "number", "description": "Elastic modulus in Pa"},
                        "moment_of_inertia": {"type": "number", "description": "Moment of inertia in m⁴"}
                    },
                    "required": ["calculation_type"]
                }
            }
        ]
    
    async def execute_function(self, function_name: str, **kwargs) -> Dict[str, Any]:
        if function_name == "electrical_calculator":
            return await self._electrical_calculator(**kwargs)
        elif function_name == "mechanical_calculator":
            return await self._mechanical_calculator(**kwargs)
        elif function_name == "structural_calculator":
            return await self._structural_calculator(**kwargs)
        else:
            return {"error": f"Unknown function: {function_name}"}
    
    def get_widget_info(self) -> Optional[Dict[str, Any]]:
        return {
            "component_name": "EngineeringCalculatorsWidget",
            "css_file": "EngineeringCalculatorsWidget.css",
            "socket_events": ["engineering_calculation_result"]
        }
    
    async def _electrical_calculator(self, calculation_type: str, **kwargs) -> Dict[str, Any]:
        """Electrical engineering calculations"""
        try:
            if calculation_type == "ohms_law":
                voltage = kwargs.get('voltage')
                current = kwargs.get('current')
                resistance = kwargs.get('resistance')
                
                if voltage and current:
                    resistance = voltage / current
                elif voltage and resistance:
                    current = voltage / resistance
                elif current and resistance:
                    voltage = current * resistance
                else:
                    return {"error": "Need at least two of: voltage, current, resistance"}
                
                power = voltage * current
                return {
                    "voltage": voltage,
                    "current": current,
                    "resistance": resistance,
                    "power": power
                }
            
            elif calculation_type == "power":
                voltage = kwargs.get('voltage')
                current = kwargs.get('current')
                resistance = kwargs.get('resistance')
                
                if voltage and current:
                    power = voltage * current
                elif current and resistance:
                    power = current**2 * resistance
                elif voltage and resistance:
                    power = voltage**2 / resistance
                else:
                    return {"error": "Need voltage and current, or current and resistance, or voltage and resistance"}
                
                return {"power": power}
            
            elif calculation_type == "impedance":
                resistance = kwargs.get('resistance', 0)
                frequency = kwargs.get('frequency', 0)
                inductance = kwargs.get('inductance', 0)
                capacitance = kwargs.get('capacitance', 0)
                
                if frequency == 0:
                    return {"error": "Frequency is required for impedance calculation"}
                
                inductive_reactance = 2 * math.pi * frequency * inductance if inductance else 0
                capacitive_reactance = 1 / (2 * math.pi * frequency * capacitance) if capacitance else 0
                reactance = inductive_reactance - capacitive_reactance
                impedance = math.sqrt(resistance**2 + reactance**2)
                
                return {
                    "impedance": impedance,
                    "resistance": resistance,
                    "reactance": reactance,
                    "inductive_reactance": inductive_reactance,
                    "capacitive_reactance": capacitive_reactance
                }
            
            elif calculation_type == "resonance":
                inductance = kwargs.get('inductance')
                capacitance = kwargs.get('capacitance')
                
                if not inductance or not capacitance:
                    return {"error": "Both inductance and capacitance are required"}
                
                resonant_frequency = 1 / (2 * math.pi * math.sqrt(inductance * capacitance))
                return {"resonant_frequency": resonant_frequency}
            
            else:
                return {"error": f"Unknown electrical calculation type: {calculation_type}"}
                
        except Exception as e:
            return {"error": f"Electrical calculation failed: {str(e)}"}
    
    async def _mechanical_calculator(self, calculation_type: str, **kwargs) -> Dict[str, Any]:
        """Mechanical engineering calculations"""
        try:
            if calculation_type == "stress":
                force = kwargs.get('force')
                area = kwargs.get('area')
                
                if not force or not area:
                    return {"error": "Both force and area are required"}
                
                stress = force / area
                return {"stress": stress}
            
            elif calculation_type == "strain":
                original_length = kwargs.get('length')
                change_in_length = kwargs.get('change_in_length', 0)
                
                if not original_length:
                    return {"error": "Original length is required"}
                
                strain = change_in_length / original_length
                return {"strain": strain}
            
            elif calculation_type == "dynamics":
                mass = kwargs.get('mass')
                acceleration = kwargs.get('acceleration')
                velocity = kwargs.get('velocity', 0)
                
                if not mass:
                    return {"error": "Mass is required"}
                
                force = mass * acceleration if acceleration else 0
                kinetic_energy = 0.5 * mass * velocity**2
                
                return {
                    "force": force,
                    "kinetic_energy": kinetic_energy
                }
            
            else:
                return {"error": f"Unknown mechanical calculation type: {calculation_type}"}
                
        except Exception as e:
            return {"error": f"Mechanical calculation failed: {str(e)}"}
    
    async def _structural_calculator(self, calculation_type: str, **kwargs) -> Dict[str, Any]:
        """Structural engineering calculations"""
        try:
            if calculation_type == "beam_analysis":
                load = kwargs.get('load')
                length = kwargs.get('length')
                modulus = kwargs.get('modulus')
                moment_of_inertia = kwargs.get('moment_of_inertia')
                
                if not all([load, length, modulus, moment_of_inertia]):
                    return {"error": "All parameters (load, length, modulus, moment_of_inertia) are required"}
                
                # Simple cantilever beam deflection
                deflection = (load * length**3) / (3 * modulus * moment_of_inertia)
                max_moment = load * length
                
                return {
                    "deflection": deflection,
                    "max_moment": max_moment
                }
            
            elif calculation_type == "column_buckling":
                load = kwargs.get('load')
                length = kwargs.get('length')
                modulus = kwargs.get('modulus')
                moment_of_inertia = kwargs.get('moment_of_inertia')
                
                if not all([load, length, modulus, moment_of_inertia]):
                    return {"error": "All parameters are required"}
                
                # Euler buckling load
                buckling_load = (math.pi**2 * modulus * moment_of_inertia) / length**2
                safety_factor = buckling_load / load if load > 0 else float('inf')
                
                return {
                    "buckling_load": buckling_load,
                    "safety_factor": safety_factor
                }
            
            else:
                return {"error": f"Unknown structural calculation type: {calculation_type}"}
                
        except Exception as e:
            return {"error": f"Structural calculation failed: {str(e)}"}
