#!/usr/bin/env python3

import re
import argparse

def is_valid_email(email):
    """
    Validate an email address using a regular expression.
    This checks for the basic format of an email address: username@domain.tld
    """
    # Regular expression for email validation
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return re.match(email_regex, email) is not None

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Validate an email address.')
    parser.add_argument('email', help='The email address to validate')
    
    # Parse arguments
    args = parser.parse_args()
    
    email = args.email
    
    if is_valid_email(email):
        print(f"✓ {email} is a valid email address.")
        return 0
    else:
        print(f"✗ {email} is NOT a valid email address.")
        return 1

if __name__ == "__main__":
    exit(main())
