import unittest
import sys
import os

# Add the parent directory to the path so we can import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestMainProgram(unittest.TestCase):

    def test_main_program_runs(self):
        """Test that the main program can run without crashing."""
        try:
            # Import and run the main function
            from main import fetch_earthquake_data

            # Test that we can fetch data (even if it's empty)
            df = fetch_earthquake_data(days_back=1)

            # If we get here, the program didn't crash
            self.assertTrue(True, "Main program ran successfully")

        except Exception as e:
            self.fail(f"Main program crashed with error: {e}")

    def test_state_extraction(self):
        """Test the state extraction function with a simple case."""
        from main import extract_state_from_place

        # Test a simple case
        result = extract_state_from_place("Test location, CA")
        self.assertEqual(result, "CA")

        # Test empty input
        result = extract_state_from_place("")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()


