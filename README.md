# Email Validator

A comprehensive command-line tool to validate email addresses. It's completely self-contained with no external dependencies.

## Features

- Format validation using regular expressions
- DNS validation to verify domain existence
- Detection of disposable email providers
- Length validation for username and domain parts
- Detailed verbose output mode
- Configurable validation options
- Returns exit code 0 for valid emails and 1 for invalid emails
- No external dependencies - uses only Python standard library

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/email-validator.git
cd email-validator

# Make the script executable
chmod +x email_validator.py
```

## Usage

```bash
# Basic usage
./email_validator.py email@example.com

# Show detailed validation results
./email_validator.py email@example.com --verbose

# Skip DNS validation
./email_validator.py email@example.com --no-dns

# Skip disposable email check
./email_validator.py email@example.com --no-disposable-check

# Get help
./email_validator.py -h
```

## Examples

### Basic validation

```bash
./email_validator.py user@example.com
```
Output: 
```
√ user@example.com is a valid email address.
```

### Verbose validation

```bash
./email_validator.py user@example.com --verbose
```
Output:
```
√ Valid email format
√ Domain has valid DNS records

√ user@example.com is a valid email address.
```

### Invalid email

```bash
./email_validator.py invalid-email --verbose
```
Output:
```
× Invalid email format

× invalid-email is NOT a valid email address.
```

### Disposable email detection

```bash
./email_validator.py user@mailinator.com --verbose
```
Output:
```
√ Valid email format
√ Domain has valid DNS records
! Domain is a known disposable email provider

√ user@mailinator.com is a valid email address.
```

## Requirements

- Python 3.x (standard library only)
