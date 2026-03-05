#!/usr/bin/env python3
"""
Unit tests for the validator module.

Tests the ReadmeValidator class and ValidationResult dataclass.
"""

import unittest
from validator import ReadmeValidator, ValidationResult


class TestValidationResult(unittest.TestCase):
    """Tests for ValidationResult dataclass."""

    def test_initialization_success(self):
        """Test ValidationResult initializes with success=True by default."""
        result = ValidationResult(success=True)
        self.assertTrue(result.success)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.warnings, [])

    def test_add_error_marks_failure(self):
        """Test that adding an error marks validation as failed."""
        result = ValidationResult(success=True)
        result.add_error("Test error")
        self.assertFalse(result.success)
        self.assertIn("Test error", result.errors)

    def test_add_warning_preserves_success(self):
        """Test that adding a warning doesn't affect success status."""
        result = ValidationResult(success=True)
        result.add_warning("Test warning")
        self.assertTrue(result.success)
        self.assertIn("Test warning", result.warnings)

    def test_multiple_errors(self):
        """Test that multiple errors can be added."""
        result = ValidationResult(success=True)
        result.add_error("Error 1")
        result.add_error("Error 2")
        self.assertEqual(len(result.errors), 2)
        self.assertFalse(result.success)


class TestReadmeValidator(unittest.TestCase):
    """Tests for ReadmeValidator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.validator = ReadmeValidator()

    def test_check_marker_pair_valid(self):
        """Test check_marker_pair with valid markers in correct order."""
        content = """
        Some content
        <!-- GOALS:START -->
        Goals content
        <!-- GOALS:END -->
        More content
        """
        result = self.validator.check_marker_pair(
            content, "<!-- GOALS:START -->", "<!-- GOALS:END -->"
        )
        self.assertTrue(result)

    def test_check_marker_pair_missing_start(self):
        """Test check_marker_pair with missing START marker."""
        content = """
        Some content
        <!-- GOALS:END -->
        More content
        """
        result = self.validator.check_marker_pair(
            content, "<!-- GOALS:START -->", "<!-- GOALS:END -->"
        )
        self.assertFalse(result)

    def test_check_marker_pair_missing_end(self):
        """Test check_marker_pair with missing END marker."""
        content = """
        Some content
        <!-- GOALS:START -->
        More content
        """
        result = self.validator.check_marker_pair(
            content, "<!-- GOALS:START -->", "<!-- GOALS:END -->"
        )
        self.assertFalse(result)

    def test_check_marker_pair_wrong_order(self):
        """Test check_marker_pair with markers in wrong order."""
        content = """
        Some content
        <!-- GOALS:END -->
        Goals content
        <!-- GOALS:START -->
        More content
        """
        result = self.validator.check_marker_pair(
            content, "<!-- GOALS:START -->", "<!-- GOALS:END -->"
        )
        self.assertFalse(result)

    def test_validate_markers_all_present(self):
        """Test validate_markers with all required markers present and valid."""
        content = """
        # README
        
        <!-- GOALS:START -->
        Goals content
        <!-- GOALS:END -->
        
        <!-- UPDATED:START -->
        Updated content
        <!-- UPDATED:END -->
        """
        result = self.validator.validate_markers(content)
        self.assertTrue(result.success)
        self.assertEqual(len(result.errors), 0)

    def test_validate_markers_missing_goals_pair(self):
        """Test validate_markers with missing GOALS markers."""
        content = """
        # README
        
        <!-- UPDATED:START -->
        Updated content
        <!-- UPDATED:END -->
        """
        result = self.validator.validate_markers(content)
        self.assertFalse(result.success)
        self.assertEqual(len(result.errors), 1)
        self.assertIn("GOALS:START", result.errors[0])
        self.assertIn("GOALS:END", result.errors[0])

    def test_validate_markers_missing_updated_pair(self):
        """Test validate_markers with missing UPDATED markers."""
        content = """
        # README
        
        <!-- GOALS:START -->
        Goals content
        <!-- GOALS:END -->
        """
        result = self.validator.validate_markers(content)
        self.assertFalse(result.success)
        self.assertEqual(len(result.errors), 1)
        self.assertIn("UPDATED:START", result.errors[0])
        self.assertIn("UPDATED:END", result.errors[0])

    def test_validate_markers_wrong_order(self):
        """Test validate_markers with markers in wrong order."""
        content = """
        # README
        
        <!-- GOALS:END -->
        Goals content
        <!-- GOALS:START -->
        
        <!-- UPDATED:START -->
        Updated content
        <!-- UPDATED:END -->
        """
        result = self.validator.validate_markers(content)
        self.assertFalse(result.success)
        self.assertEqual(len(result.errors), 1)
        self.assertIn("incorrect order", result.errors[0])
        self.assertIn("GOALS:START", result.errors[0])

    def test_validate_markers_missing_only_start(self):
        """Test validate_markers with only START marker missing."""
        content = """
        # README
        
        <!-- GOALS:END -->
        
        <!-- UPDATED:START -->
        Updated content
        <!-- UPDATED:END -->
        """
        result = self.validator.validate_markers(content)
        self.assertFalse(result.success)
        self.assertIn("GOALS:START", result.errors[0])
        self.assertNotIn("GOALS:END", result.errors[0])

    def test_validate_markers_missing_only_end(self):
        """Test validate_markers with only END marker missing."""
        content = """
        # README
        
        <!-- GOALS:START -->
        
        <!-- UPDATED:START -->
        Updated content
        <!-- UPDATED:END -->
        """
        result = self.validator.validate_markers(content)
        self.assertFalse(result.success)
        self.assertIn("GOALS:END", result.errors[0])
        self.assertNotIn("GOALS:START", result.errors[0])

    def test_validate_markers_multiple_errors(self):
        """Test validate_markers with multiple missing marker pairs."""
        content = """
        # README
        
        Some content
        """
        result = self.validator.validate_markers(content)
        self.assertFalse(result.success)
        self.assertEqual(len(result.errors), 2)

    def test_validate_markers_empty_content(self):
        """Test validate_markers with empty content."""
        content = ""
        result = self.validator.validate_markers(content)
        self.assertFalse(result.success)
        self.assertEqual(len(result.errors), 2)


if __name__ == "__main__":
    unittest.main()
