#!/usr/bin/env python3
"""
README Validation Module

Validates that README.md contains all required section markers
and that they appear in the correct order (START before END).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Result of README validation with structured error reporting."""

    success: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        """Add an error message and mark validation as failed."""
        self.errors.append(message)
        self.success = False

    def add_warning(self, message: str) -> None:
        """Add a warning message (doesn't affect success status)."""
        self.warnings.append(message)


class ReadmeValidator:
    """Validates README.md structure and section markers."""

    # Required marker pairs that must exist in README
    REQUIRED_MARKERS = [
        ("<!-- GOALS:START -->", "<!-- GOALS:END -->"),
        ("<!-- UPDATED:START -->", "<!-- UPDATED:END -->"),
    ]

    def validate_markers(self, content: str) -> ValidationResult:
        """
        Validates that all required section markers exist and are properly ordered.

        Args:
            content: The README.md file content

        Returns:
            ValidationResult with success status and error messages

        Validates:
            - All required marker pairs exist (Requirements 1.1, 1.2)
            - START markers appear before END markers (Requirement 1.5)
            - Provides descriptive error messages (Requirements 1.3, 1.4, 1.6)
        """
        result = ValidationResult(success=True)

        for start_marker, end_marker in self.REQUIRED_MARKERS:
            if not self.check_marker_pair(content, start_marker, end_marker):
                # Determine which specific issue occurred
                has_start = start_marker in content
                has_end = end_marker in content

                if not has_start and not has_end:
                    result.add_error(
                        f"Missing required markers: {start_marker}, {end_marker}"
                    )
                elif not has_start:
                    result.add_error(f"Missing required marker: {start_marker}")
                elif not has_end:
                    result.add_error(f"Missing required marker: {end_marker}")
                else:
                    # Both exist but in wrong order
                    result.add_error(
                        f"Markers in incorrect order: {start_marker} must appear before {end_marker}"
                    )

        return result

    def check_marker_pair(self, content: str, start: str, end: str) -> bool:
        """
        Checks if a marker pair exists and is in correct order.

        Args:
            content: The README content
            start: Start marker (e.g., "<!-- GOALS:START -->")
            end: End marker (e.g., "<!-- GOALS:END -->")

        Returns:
            True if both markers exist and START appears before END, False otherwise

        Validates:
            - Marker pair exists (Requirements 1.1, 1.2)
            - START appears before END (Requirement 1.5)
        """
        # Check if both markers exist
        if start not in content or end not in content:
            return False

        # Check if START appears before END
        start_pos = content.find(start)
        end_pos = content.find(end)

        return start_pos < end_pos
