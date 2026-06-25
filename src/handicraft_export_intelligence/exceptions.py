"""Application-specific exceptions."""


class HandicraftExportIntelligenceError(Exception):
    """Base exception for project-specific errors."""


class ConfigurationError(HandicraftExportIntelligenceError):
    """Raised when configuration cannot be loaded or validated."""
