"""A module for rendering templates."""

import os
import sys


class Template:
    """A class representing a template."""

    def __init__(self, template: str):
        self.template = template
        self.template_dir = self._get_template_dir()
        self.template_body = None
        self.template_path = os.path.join(self.template_dir, self.template)
        self._load_template()

    def _get_template_dir(self) -> str:
        """Get the template directory."""
        app_path = sys.path[0]
        if not os.path.exists(app_path):
            return "templates"
        if os.path.exists(app_path + "/templates"):
            return app_path + "/templates"
        return "templates"

    def _load_template(self) -> None:
        """Load the template"""
        if not self._verify_template():
            return None
        with open(self.template_path, "r", encoding="UTF-8") as f:
            self.template_body = f.read()

    def _verify_template(self) -> bool:
        """Verify the template"""
        return os.path.exists(self.template_path) and os.path.isfile(self.template_path)

    def render(self, *args,**kwargs) -> str:
        """Render the template."""
        if self.template_body is None:
            return ""
        return self.template_body.format(*args, **kwargs)
