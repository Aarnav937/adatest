"""
QR Code Generator Plugin
Generate custom styled QR codes with multiple types and bulk generation
"""

import asyncio
import base64
from typing import Dict, List, Any, Optional
from pathlib import Path
import tempfile
from datetime import datetime

# QR Code generation libraries
import qrcode
from PIL import Image, ImageDraw
import io

from . import PluginBase

class QRCodeGeneratorPlugin(PluginBase):
    """Plugin for QR code generation with custom styling"""
    
    def __init__(self):
        self.name = "qr_code_generator"
        self.qr_codes_dir = Path("generated_qr_codes")
        self.qr_codes_dir.mkdir(exist_ok=True)
        
        # QR Code types and their configurations
        self.qr_types = {
            'url': {'error_correction': qrcode.constants.ERROR_CORRECT_L},
            'text': {'error_correction': qrcode.constants.ERROR_CORRECT_M},
            'email': {'error_correction': qrcode.constants.ERROR_CORRECT_M},
            'phone': {'error_correction': qrcode.constants.ERROR_CORRECT_M},
            'wifi': {'error_correction': qrcode.constants.ERROR_CORRECT_M},
            'vcard': {'error_correction': qrcode.constants.ERROR_CORRECT_M}
        }
    
    def get_name(self) -> str:
        return self.name
    
    def get_description(self) -> str:
        return "QR code generation with custom styling and multiple types"
    
    def get_functions(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "generate_qr_code",
                "description": "Generate a QR code with custom styling",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "data": {"type": "string", "description": "Data to encode in QR code"},
                        "qr_type": {"type": "string", "description": "Type of QR code: 'url', 'text', 'email', 'phone', 'wifi', 'vcard'"},
                        "size": {"type": "integer", "description": "QR code size in pixels (default: 400)"},
                        "foreground_color": {"type": "string", "description": "Foreground color (hex code, default: '#000000')"},
                        "background_color": {"type": "string", "description": "Background color (hex code, default: '#FFFFFF')"},
                        "logo_path": {"type": "string", "description": "Path to logo image to embed (optional)"},
                        "border": {"type": "integer", "description": "Border width in pixels (default: 4)"}
                    },
                    "required": ["data", "qr_type"]
                }
            },
            {
                "name": "generate_bulk_qr_codes",
                "description": "Generate multiple QR codes in batch",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "data_list": {"type": "array", "description": "List of data strings to encode", "items": {"type": "string"}},
                        "qr_type": {"type": "string", "description": "Type of QR code for all items"},
                        "size": {"type": "integer", "description": "QR code size in pixels (default: 400)"},
                        "foreground_color": {"type": "string", "description": "Foreground color (hex code)"},
                        "background_color": {"type": "string", "description": "Background color (hex code)"}
                    },
                    "required": ["data_list", "qr_type"]
                }
            },
            {
                "name": "generate_wifi_qr",
                "description": "Generate QR code for WiFi network connection",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ssid": {"type": "string", "description": "WiFi network name"},
                        "password": {"type": "string", "description": "WiFi password"},
                        "encryption": {"type": "string", "description": "Encryption type: 'WPA', 'WEP', 'nopass' (default: 'WPA')"},
                        "hidden": {"type": "boolean", "description": "Whether network is hidden (default: false)"},
                        "size": {"type": "integer", "description": "QR code size in pixels (default: 400)"}
                    },
                    "required": ["ssid"]
                }
            },
            {
                "name": "generate_vcard_qr",
                "description": "Generate QR code for contact information (vCard)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Full name"},
                        "phone": {"type": "string", "description": "Phone number"},
                        "email": {"type": "string", "description": "Email address"},
                        "company": {"type": "string", "description": "Company name"},
                        "title": {"type": "string", "description": "Job title"},
                        "website": {"type": "string", "description": "Website URL"},
                        "address": {"type": "string", "description": "Address"},
                        "size": {"type": "integer", "description": "QR code size in pixels (default: 400)"}
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "list_generated_qr_codes",
                "description": "List all generated QR codes",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        ]
    
    async def execute_function(self, function_name: str, **kwargs) -> Dict[str, Any]:
        if function_name == "generate_qr_code":
            return await self._generate_qr_code(**kwargs)
        elif function_name == "generate_bulk_qr_codes":
            return await self._generate_bulk_qr_codes(**kwargs)
        elif function_name == "generate_wifi_qr":
            return await self._generate_wifi_qr(**kwargs)
        elif function_name == "generate_vcard_qr":
            return await self._generate_vcard_qr(**kwargs)
        elif function_name == "list_generated_qr_codes":
            return await self._list_generated_qr_codes(**kwargs)
        else:
            return {"error": f"Unknown function: {function_name}"}
    
    def get_widget_info(self) -> Optional[Dict[str, Any]]:
        return {
            "component_name": "QRCodeGeneratorWidget",
            "css_file": "QRCodeGeneratorWidget.css",
            "socket_events": ["qr_code_generated", "bulk_qr_codes_generated"]
        }
    
    async def _generate_qr_code(self, data: str, qr_type: str, size: int = 400,
                              foreground_color: str = "#000000", background_color: str = "#FFFFFF",
                              logo_path: str = None, border: int = 4) -> Dict[str, Any]:
        """Generate a single QR code with custom styling"""
        try:
            if qr_type not in self.qr_types:
                return {"error": f"Unsupported QR type: {qr_type}"}
            
            # Validate colors
            if not self._is_valid_hex_color(foreground_color) or not self._is_valid_hex_color(background_color):
                return {"error": "Invalid color format. Use hex codes (e.g., '#FF0000')"}
            
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=self.qr_types[qr_type]['error_correction'],
                box_size=10,
                border=border
            )
            
            qr.add_data(data)
            qr.make(fit=True)
            
            # Create QR code image
            qr_image = qr.make_image(fill_color=foreground_color, back_color=background_color)
            
            # Resize to requested size
            qr_image = qr_image.resize((size, size), Image.Resampling.NEAREST)
            
            # Add logo if provided
            if logo_path:
                qr_image = await self._add_logo_to_qr(qr_image, logo_path)
            
            # Save and convert to base64
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qr_{qr_type}_{timestamp}.png"
            filepath = self.qr_codes_dir / filename
            
            qr_image.save(filepath, "PNG")
            
            # Convert to base64
            buffer = io.BytesIO()
            qr_image.save(buffer, format="PNG")
            qr_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return {
                "filename": filename,
                "filepath": str(filepath),
                "qr_type": qr_type,
                "data": data,
                "size": size,
                "foreground_color": foreground_color,
                "background_color": background_color,
                "qr_base64": qr_base64,
                "generated_at": timestamp
            }
            
        except Exception as e:
            print(f"QR code generation error: {e}")
            return {"error": f"QR code generation failed: {str(e)}"}
    
    async def _generate_bulk_qr_codes(self, data_list: List[str], qr_type: str, size: int = 400,
                                    foreground_color: str = "#000000", background_color: str = "#FFFFFF") -> Dict[str, Any]:
        """Generate multiple QR codes in batch"""
        try:
            if qr_type not in self.qr_types:
                return {"error": f"Unsupported QR type: {qr_type}"}
            
            results = []
            
            for i, data in enumerate(data_list):
                result = await self._generate_qr_code(
                    data=data,
                    qr_type=qr_type,
                    size=size,
                    foreground_color=foreground_color,
                    background_color=background_color
                )
                
                if "error" not in result:
                    result["index"] = i
                    results.append(result)
            
            return {
                "bulk_results": results,
                "total_generated": len(results),
                "total_requested": len(data_list),
                "qr_type": qr_type
            }
            
        except Exception as e:
            print(f"Bulk QR code generation error: {e}")
            return {"error": f"Bulk QR code generation failed: {str(e)}"}
    
    async def _generate_wifi_qr(self, ssid: str, password: str = "", encryption: str = "WPA",
                              hidden: bool = False, size: int = 400) -> Dict[str, Any]:
        """Generate QR code for WiFi network connection"""
        try:
            # Format WiFi data according to standard
            wifi_data = f"WIFI:T:{encryption};S:{ssid};P:{password};H:{str(hidden).lower()};;"
            
            return await self._generate_qr_code(
                data=wifi_data,
                qr_type="wifi",
                size=size
            )
            
        except Exception as e:
            print(f"WiFi QR code generation error: {e}")
            return {"error": f"WiFi QR code generation failed: {str(e)}"}
    
    async def _generate_vcard_qr(self, name: str, phone: str = "", email: str = "", company: str = "",
                               title: str = "", website: str = "", address: str = "", size: int = 400) -> Dict[str, Any]:
        """Generate QR code for contact information (vCard)"""
        try:
            # Build vCard data
            vcard_lines = ["BEGIN:VCARD", "VERSION:3.0"]
            
            if name:
                vcard_lines.append(f"FN:{name}")
                vcard_lines.append(f"N:{name};;;;")
            
            if phone:
                vcard_lines.append(f"TEL:{phone}")
            
            if email:
                vcard_lines.append(f"EMAIL:{email}")
            
            if company:
                vcard_lines.append(f"ORG:{company}")
            
            if title:
                vcard_lines.append(f"TITLE:{title}")
            
            if website:
                vcard_lines.append(f"URL:{website}")
            
            if address:
                vcard_lines.append(f"ADR:;;{address};;;;")
            
            vcard_lines.append("END:VCARD")
            vcard_data = "\n".join(vcard_lines)
            
            return await self._generate_qr_code(
                data=vcard_data,
                qr_type="vcard",
                size=size
            )
            
        except Exception as e:
            print(f"vCard QR code generation error: {e}")
            return {"error": f"vCard QR code generation failed: {str(e)}"}
    
    async def _list_generated_qr_codes(self) -> Dict[str, Any]:
        """List all generated QR codes"""
        try:
            qr_codes = []
            for filepath in self.qr_codes_dir.glob("qr_*.png"):
                stat = filepath.stat()
                qr_codes.append({
                    "filename": filepath.name,
                    "filepath": str(filepath),
                    "size": stat.st_size,
                    "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat()
                })
            
            # Sort by creation time (newest first)
            qr_codes.sort(key=lambda x: x["created_at"], reverse=True)
            
            return {"qr_codes": qr_codes, "total_count": len(qr_codes)}
            
        except Exception as e:
            return {"error": f"Failed to list QR codes: {str(e)}"}
    
    def _is_valid_hex_color(self, color: str) -> bool:
        """Validate hex color format"""
        if not color.startswith('#'):
            return False
        if len(color) != 7:
            return False
        try:
            int(color[1:], 16)
            return True
        except ValueError:
            return False
    
    async def _add_logo_to_qr(self, qr_image: Image.Image, logo_path: str) -> Image.Image:
        """Add logo to center of QR code"""
        try:
            # Load logo
            logo = Image.open(logo_path)
            
            # Calculate logo size (should be about 1/4 of QR code size)
            qr_size = qr_image.size[0]
            logo_size = qr_size // 4
            
            # Resize logo
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # Calculate position to center logo
            pos_x = (qr_size - logo_size) // 2
            pos_y = (qr_size - logo_size) // 2
            
            # Paste logo onto QR code
            qr_image.paste(logo, (pos_x, pos_y))
            
            return qr_image
            
        except Exception as e:
            print(f"Error adding logo to QR code: {e}")
            return qr_image  # Return original QR code if logo addition fails
