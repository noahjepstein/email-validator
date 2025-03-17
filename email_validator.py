#!/usr/bin/env python3

import sys
import re

def is_valid_email(email):
    """
    Validate an email address using a regular expression.
    This checks for the basic format of an email address: username@domain.tld
    """
    # Regular expression for email validation
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return re.match(email_regex, email) is not None

def main():
    # Check if an email address was provided as an argument
    if len(sys.argv) != 2:
        print("Error: Please provide exactly one email address as an argument.")
        print("Usage: python email_validator.py email@example.com")
        sys.exit(1)
    
    email = sys.argv[1]
    
    if is_valid_email(email):
        print(f"✓ {email} is a valid email address.")
        sys.exit(0)
    else:
        print(f"✗ {email} is NOT a valid email address.")
        sys.exit(1)

if __name__ == "__main__":
    main()
