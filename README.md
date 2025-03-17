# Email Validator

A simple command-line tool to validate email addresses.

## Usage

```bash
python email_validator.py email@example.com
```

## Examples

Valid email:
```bash
python email_validator.py user@example.com
```
Output: `✓ user@example.com is a valid email address.`

Invalid email:
```bash
python email_validator.py invalid-email
```
Output: `✗ invalid-email is NOT a valid email address.`

## Features

- Validates email addresses against a standard pattern
- Returns exit code 0 for valid emails and 1 for invalid emails
- Simple command-line interface

## Requirements

- Python 3.x (no additional packages required)
