# Example Python file for testing the code reviewer
# This file intentionally has some issues to demonstrate the tool

def calculate_average(numbers):
    # Missing input validation
    total = 0
    for i in range(len(numbers)):  # Could use enumerate or direct iteration
        total += numbers[i]
    
    # Potential division by zero
    return total / len(numbers)


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.password = "password123"  # Security issue: hardcoded password
    
    # Missing docstring
    def get_info(self):
        return f"User: {self.name}, Email: {self.email}"
    
    def validate_email(self, email):
        # Weak email validation
        if "@" in email:
            return True
        return False


# Global variable (style issue)
USERS_LIST = []


def add_user(name, email):
    # No input validation
    user = User(name, email)
    USERS_LIST.append(user)  # Modifying global state
    print(f"Added user: {user.get_info()}")


# Unused import (would be caught by a real linter)
import json


if __name__ == "__main__":
    # Example usage with potential issues
    numbers = [1, 2, 3, 4, 5]
    avg = calculate_average(numbers)
    print(f"Average: {avg}")
    
    # This would cause an error but isn't handled
    empty_list = []
    # avg_empty = calculate_average(empty_list)  # Uncomment to see error
    
    add_user("John Doe", "john@example.com")
    add_user("Jane Smith", "invalid-email")  # Invalid email format