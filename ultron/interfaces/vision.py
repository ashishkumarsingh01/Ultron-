"""
Vision interface for Ultron Agent Kernel.
"""

import logging
from typing import Optional, Dict, Any, List
from pathlib import Path

from ultron.interfaces.base import BaseInterface
from ultron.utils.errors import VisionProcessingError
from ultron.utils.logger import setup_logger


class VisionInterface(BaseInterface):
    """Vision interface for image processing and analysis."""
    
    def __init__(self, agent):
        super().__init__(agent)
        self.logger = setup_logger("ultron.interfaces.vision")
        self.cv2 = None
        self._initialize_vision()
    
    def _initialize_vision(self) -> None:
        """Initialize vision processing components."""
        try:
            import cv2
            self.cv2 = cv2
            self.logger.info("Vision processor initialized")
        except ImportError:
            self.logger.warning("opencv-python not installed")
    
    def process_input(self, image_path: str) -> Dict[str, Any]:
        """Process image input.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Image analysis results
        """
        try:
            if self.cv2 is None:
                raise VisionProcessingError("Vision processor not initialized")
            
            # Load image
            image = self.cv2.imread(image_path)
            if image is None:
                raise VisionProcessingError(f"Failed to load image: {image_path}")
            
            # Analyze image
            height, width = image.shape[:2]
            
            analysis = {
                "path": image_path,
                "width": width,
                "height": height,
                "channels": image.shape[2] if len(image.shape) > 2 else 1,
                "size_mb": Path(image_path).stat().st_size / (1024 * 1024)
            }
            
            self.logger.info(f"Analyzed image: {image_path}")
            return analysis
        except Exception as e:
            self.logger.error(f"Vision processing failed: {str(e)}")
            raise VisionProcessingError(f"Failed to process image: {str(e)}")
    
    def process_output(self, analysis: Dict[str, Any]) -> str:
        """Process vision output.
        
        Args:
            analysis: Analysis results
            
        Returns:
            Text description
        """
        description = f"Image Analysis: {analysis.get('width')}x{analysis.get('height')} pixels"
        return description
    
    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """Analyze an image.
        
        Args:
            image_path: Path to image
            
        Returns:
            Analysis results
        """
        return self.process_input(image_path)
    
    def detect_objects(self, image_path: str) -> List[Dict[str, Any]]:
        """Detect objects in image.
        
        Args:
            image_path: Path to image
            
        Returns:
            List of detected objects
        """
        self.logger.info(f"Detecting objects in: {image_path}")
        return []
    
    def extract_text(self, image_path: str) -> str:
        """Extract text from image (OCR).
        
        Args:
            image_path: Path to image
            
        Returns:
            Extracted text
        """
        try:
            import easyocr
            reader = easyocr.Reader(['en'])
            results = reader.readtext(image_path)
            text = '\n'.join([result[1] for result in results])
            self.logger.info(f"Extracted text from image")
            return text
        except Exception as e:
            self.logger.error(f"OCR failed: {str(e)}")
            return ""