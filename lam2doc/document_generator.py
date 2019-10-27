"""
document_generator.py
Date: 27.10.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com 
"""
from pathlib import Path

import jinja2

from lam2doc.abstract_generator import ContentGenerator


class JinjaGenerator(ContentGenerator):
    """
        generate HTML document from a given data content
    """

    def __init__(self, main_template_name: str, template_folder: Path, data: dict = None,
                 configuration: dict = None, ) -> None:
        """
            Document builder form a template using two top level data contexts: `data` and `configuration`.
        :param main_template_name: the name of the entry point template
        :param template_folder: the folder where to lookup for templates
        :param data: the data to be used in the generation process: `data`
        :param configuration: additional configuration data: `configuration`
        """
        self.data_context = data
        self.config_context = configuration
        self.template_loader = jinja2.FileSystemLoader(searchpath=str(template_folder))
        self.template_env = jinja2.Environment(loader=self.template_loader)
        self.document_template = self.template_env.get_template(main_template_name)

        self.content = None

    def generate(self):
        """
            generate the Jinja document
        :return:
        """
        if not self.content:
            self.content = self.document_template.render(data=self.data_context, configuration=self.config_context)
        return self.content

    def serialise(self, output_file):
        with open(str(output_file), "w", encoding="utf8") as of:
            of.write(self.generate())
