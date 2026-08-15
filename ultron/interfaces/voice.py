"""
Voice interface for Ultron Agent Kernel.
"""

import logging
from typing import Optional

from ultron.interfaces.base import BaseInterface
from ultron.utils.errors import VoiceProcessingError
from ultron.utils.logger import setup_logger


class VoiceInterface(BaseInterface):
    """Voice interface for speech processing."""
    
    def __init__(self, agent):
        super().__init__(agent)
        self.logger = setup_logger("ultron.interfaces.voice")
        self.recognizer = None
        self.synthesizer = None
        self._initialize_voice()
    
    def _initialize_voice(self) -> None:
        """Initialize voice processing components."""
        try:
            import speech_recognition
            self.recognizer = speech_recognition.Recognizer()
            self.logger.info("Voice recognizer initialized")
        except ImportError:
            self.logger.warning("speech_recognition not installed")
    
    def process_input(self, audio_data: Optional[bytes] = None) -> str:
        """Process voice input to text.
        
        Args:
            audio_data: Audio data or None to capture from microphone
            
        Returns:
            Transcribed text
        """
        try:
            if self.recognizer is None:
                raise VoiceProcessingError("Voice recognizer not initialized")
            
            if audio_data is None:
                # Capture from microphone
                import speech_recognition
                with speech_recognition.Microphone() as source:
                    self.logger.info("Listening...")
                    audio = self.recognizer.listen(source)
            else:
                audio = audio_data
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio)
            self.logger.info(f"Recognized: {text}")
            return text
        except Exception as e:
            self.logger.error(f"Voice recognition failed: {str(e)}")
            raise VoiceProcessingError(f"Failed to process voice input: {str(e)}")
    
    def process_output(self, text: str) -> bytes:
        """Process text to voice output.
        
        Args:
            text: Text to synthesize
            
        Returns:
            Audio bytes
        """
        try:
            import pyttsx3
            
            if self.synthesizer is None:
                self.synthesizer = pyttsx3.init()
            
            self.synthesizer.say(text)
            self.synthesizer.runAndWait()
            
            self.logger.info(f"Synthesized: {text[:50]}...")
            return b""  # Simplified
        except Exception as e:
            self.logger.error(f"Voice synthesis failed: {str(e)}")
            raise VoiceProcessingError(f"Failed to synthesize voice: {str(e)}")
    
    def speak(self, text: str) -> None:
        """Speak out loud.
        
        Args:
            text: Text to speak
        """
        self.process_output(text)