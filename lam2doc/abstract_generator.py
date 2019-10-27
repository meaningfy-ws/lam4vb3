"""
contentGenerator
Date: 18.10.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""

from abc import ABC, abstractmethod


class ContentGenerator(ABC):
    """
        generic content generator
    """

    @abstractmethod
    def generate(self):
        """
        Generates the content from a  source
        """

    @abstractmethod
    def serialise(self, output_file):
        """
            write the generated content into a file
        """
