"""
AI Image Generation Plugin
Local Stable Diffusion image generation with GPU support
"""

import os
import asyncio
import base64
from typing import Dict, List, Any, Optional
from pathlib import Path
import tempfile
from datetime import datetime

# Local AI image generation
import torch
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
from PIL import Image
import io

from . import PluginBase

class ImageGenerationPlugin(PluginBase):
    """Plugin for AI image generation using Stable Diffusion"""
    
    def __init__(self):
        self.name = "image_generation"
        self.pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.generated_images_dir = Path("generated_images")
        self.generated_images_dir.mkdir(exist_ok=True)
        
        # Initialize the model
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize Stable Diffusion XL pipeline"""
        try:
            print("Loading Stable Diffusion XL model...")
            
            # Use Stable Diffusion XL Turbo for faster generation
            model_id = "stabilityai/stable-diffusion-xl-base-1.0"
            
            self.pipeline = StableDiffusionXLPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                use_safetensors=True,
                variant="fp16" if self.device == "cuda" else None
            )
            
            # Optimize for speed
            self.pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipeline.scheduler.config
            )
            
            if self.device == "cuda":
                self.pipeline = self.pipeline.to(self.device)
                # Enable memory efficient attention
                self.pipeline.enable_xformers_memory_efficient_attention()
            
            print(f"Stable Diffusion XL loaded successfully on {self.device}")
            
        except Exception as e:
            print(f"Warning: Could not load Stable Diffusion model: {e}")
            self.pipeline = None
    
    def get_name(self) -> str:
        return self.name
    
    def get_description(self) -> str:
        return "AI image generation using Stable Diffusion XL"
    
    def get_functions(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "generate_image",
                "description": "Generate an image using Stable Diffusion XL based on a text prompt",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "Text description of the image to generate"},
                        "negative_prompt": {"type": "string", "description": "What to avoid in the image (optional)"},
                        "width": {"type": "integer", "description": "Image width (default: 1024)"},
                        "height": {"type": "integer", "description": "Image height (default: 1024)"},
                        "num_inference_steps": {"type": "integer", "description": "Number of denoising steps (default: 20)"},
                        "guidance_scale": {"type": "number", "description": "How closely to follow the prompt (default: 7.5)"}
                    },
                    "required": ["prompt"]
                }
            },
            {
                "name": "list_generated_images",
                "description": "List all previously generated images",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "delete_generated_image",
                "description": "Delete a generated image",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "image_id": {"type": "string", "description": "ID of image to delete"}
                    },
                    "required": ["image_id"]
                }
            }
        ]
    
    async def execute_function(self, function_name: str, **kwargs) -> Dict[str, Any]:
        if function_name == "generate_image":
            return await self._generate_image(**kwargs)
        elif function_name == "list_generated_images":
            return await self._list_generated_images(**kwargs)
        elif function_name == "delete_generated_image":
            return await self._delete_generated_image(**kwargs)
        else:
            return {"error": f"Unknown function: {function_name}"}
    
    def get_widget_info(self) -> Optional[Dict[str, Any]]:
        return {
            "component_name": "ImageGenerationWidget",
            "css_file": "ImageGenerationWidget.css",
            "socket_events": ["image_generation_update", "image_list_update"]
        }
    
    async def _generate_image(self, prompt: str, negative_prompt: str = "", 
                            width: int = 1024, height: int = 1024,
                            num_inference_steps: int = 20, guidance_scale: float = 7.5) -> Dict[str, Any]:
        """Generate image using Stable Diffusion"""
        try:
            if not self.pipeline:
                return {"error": "Image generation model not loaded"}
            
            # Set default negative prompt if not provided
            if not negative_prompt:
                negative_prompt = "blurry, low quality, distorted, deformed, ugly, bad anatomy"
            
            # Validate parameters
            width = max(512, min(width, 1024))
            height = max(512, min(height, 1024))
            num_inference_steps = max(10, min(num_inference_steps, 50))
            guidance_scale = max(1.0, min(guidance_scale, 20.0))
            
            print(f"Generating image: {prompt}")
            print(f"Negative prompt: {negative_prompt}")
            print(f"Size: {width}x{height}, Steps: {num_inference_steps}, Guidance: {guidance_scale}")
            
            # Generate image
            image = await asyncio.to_thread(
                self.pipeline,
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale
            ).images[0]
            
            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_{timestamp}.png"
            filepath = self.generated_images_dir / filename
            
            image.save(filepath, "PNG")
            
            # Convert to base64 for frontend
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            # Generate image ID
            import hashlib
            image_id = hashlib.md5(f"{prompt}_{timestamp}".encode()).hexdigest()
            
            result = {
                "image_id": image_id,
                "filename": filename,
                "filepath": str(filepath),
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "width": width,
                "height": height,
                "num_inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale,
                "image_base64": image_base64,
                "generated_at": timestamp
            }
            
            return result
            
        except Exception as e:
            print(f"Image generation error: {e}")
            return {"error": f"Image generation failed: {str(e)}"}
    
    async def _list_generated_images(self) -> Dict[str, Any]:
        """List all generated images"""
        try:
            images = []
            for filepath in self.generated_images_dir.glob("generated_*.png"):
                stat = filepath.stat()
                images.append({
                    "filename": filepath.name,
                    "filepath": str(filepath),
                    "size": stat.st_size,
                    "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat()
                })
            
            # Sort by creation time (newest first)
            images.sort(key=lambda x: x["created_at"], reverse=True)
            
            return {"images": images}
            
        except Exception as e:
            return {"error": f"Failed to list images: {str(e)}"}
    
    async def _delete_generated_image(self, image_id: str) -> Dict[str, Any]:
        """Delete a generated image"""
        try:
            # For now, we'll delete by filename pattern
            # In a real implementation, you'd store image metadata with IDs
            filename = f"generated_{image_id}.png"
            filepath = self.generated_images_dir / filename
            
            if filepath.exists():
                filepath.unlink()
                return {"success": True, "message": "Image deleted"}
            else:
                return {"error": "Image not found"}
                
        except Exception as e:
            return {"error": f"Failed to delete image: {str(e)}"}
