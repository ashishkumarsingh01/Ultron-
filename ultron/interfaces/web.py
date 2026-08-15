"""
Web interface for Ultron Agent Kernel.
"""

import logging
from typing import Optional, Dict, Any, List
import json

from ultron.interfaces.base import BaseInterface
from ultron.utils.errors import InterfaceException
from ultron.utils.logger import setup_logger


class WebInterface(BaseInterface):
    """Web interface for web scraping and API calls."""
    
    def __init__(self, agent):
        super().__init__(agent)
        self.logger = setup_logger("ultron.interfaces.web")
        self.session = None
        self._initialize_web()
    
    def _initialize_web(self) -> None:
        """Initialize web processing components."""
        try:
            import requests
            self.session = requests.Session()
            self.logger.info("Web interface initialized")
        except ImportError:
            self.logger.warning("requests not installed")
    
    def process_input(self, url: str) -> Dict[str, Any]:
        """Process web input (fetch URL).
        
        Args:
            url: URL to fetch
            
        Returns:
            Response data
        """
        try:
            if self.session is None:
                raise InterfaceException("Web session not initialized")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            result = {
                "url": url,
                "status_code": response.status_code,
                "content_type": response.headers.get('content-type'),
                "content_length": len(response.content)
            }
            
            self.logger.info(f"Fetched: {url}")
            return result
        except Exception as e:
            self.logger.error(f"Web fetch failed: {str(e)}")
            raise InterfaceException(f"Failed to fetch URL: {str(e)}")
    
    def process_output(self, data: Dict[str, Any]) -> str:
        """Process web output.
        
        Args:
            data: Output data
            
        Returns:
            Text representation
        """
        return json.dumps(data, indent=2)
    
    def search(self, query: str, engine: str = "google") -> List[Dict[str, str]]:
        """Search the web.
        
        Args:
            query: Search query
            engine: Search engine (google, bing, etc.)
            
        Returns:
            Search results
        """
        self.logger.info(f"Searching '{query}' on {engine}")
        # Simplified search implementation
        return [
            {"title": f"Result for {query}", "url": f"https://example.com/search?q={query}"}
        ]
    
    def scrape(self, url: str, selectors: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Scrape web page.
        
        Args:
            url: URL to scrape
            selectors: CSS selectors to extract data
            
        Returns:
            Scraped data
        """
        try:
            from bs4 import BeautifulSoup
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            data = {"url": url}
            if selectors:
                for key, selector in selectors.items():
                    elements = soup.select(selector)
                    data[key] = [elem.text for elem in elements]
            
            self.logger.info(f"Scraped: {url}")
            return data
        except Exception as e:
            self.logger.error(f"Web scraping failed: {str(e)}")
            raise InterfaceException(f"Failed to scrape URL: {str(e)}")
    
    def fetch_json(self, url: str) -> Dict[str, Any]:
        """Fetch JSON from API.
        
        Args:
            url: API URL
            
        Returns:
            JSON response
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"JSON fetch failed: {str(e)}")
            raise InterfaceException(f"Failed to fetch JSON: {str(e)}")