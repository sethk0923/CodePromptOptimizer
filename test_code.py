# A simple function
def add_numbers(a, b):
    """Add two numbers and return the result."""
    return a + b

# A class definition
class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, x):
        """Add a number to the current result."""
        self.result += x
        return self.result
    
    def subtract(self, x):
        """Subtract a number from the current result."""
        self.result -= x
        return self.result

# Some example usage
if __name__ == "__main__":
    # Create a calculator
    calc = Calculator()
    
    # Perform some operations
    print(calc.add(5))      # Should print 5
    print(calc.subtract(2)) # Should print 3 