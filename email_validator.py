#!/usr/bin/env python3

import re
import argparse
import socket
from email.utils import parseaddr

def is_valid_format(email):
    """
    Validate an email address format using a regular expression.
    This checks for the basic format of an email address: username@domain.tld
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def validate_domain(domain):
    """
    Validate that the domain exists by attempting to resolve its DNS records.
    Returns a tuple of (is_valid, error_message)
    """
    try:
        socket.getaddrinfo(f"_smtp._tcp.{domain}", None, socket.AF_INET, socket.SOCK_DGRAM)
        return True, None
    except socket.gaierror:
        try:
            socket.getaddrinfo(domain, None)
            return True, None
        except socket.gaierror:
            return False, f"Domain '{domain}' does not have valid DNS records"
    except Exception as e:
        return False, f"Error checking domain: {str(e)}"

def check_disposable_email(domain):
    """
    Check if the domain is a known disposable email provider.
    This is a simple check with a small list of common disposable email domains.
    For production use, consider using a more comprehensive list or API.
    """
    disposable_domains = [
        'mailinator.com', 'guerrillamail.com', 'temp-mail.org', 'fakeinbox.com',
        'tempmail.com', '10minutemail.com', 'yopmail.com', 'throwawaymail.com',
        'getairmail.com', 'mailnesia.com', 'mailcatch.com', 'dispostable.com'
    ]
    return domain.lower() in disposable_domains

def validate_email(email, check_dns=True, check_disposable=True):
    """
    Comprehensive email validation.
    Returns a tuple of (is_valid, messages) where messages is a list of validation results.
    """
    messages = []
    is_valid = True
    if not is_valid_format(email):
        messages.append("✗ Invalid email format")
        return False, messages
    else:
        messages.append("✓ Valid email format")
    _, addr = parseaddr(email)
    try:
        username, domain = addr.split('@', 1)
    except ValueError:
        messages.append("✗ Could not parse email address")
        return False, messages
    if len(username) > 64:
        is_valid = False
        messages.append("✗ Username exceeds maximum length (64 characters)")
    if len(domain) > 255:
        is_valid = False
        messages.append("✗ Domain exceeds maximum length (255 characters)")
    if check_dns:
        domain_valid, error_msg = validate_domain(domain)
        if domain_valid:
            messages.append("✓ Domain has valid DNS records")
        else:
            is_valid = False
            messages.append(f"✗ {error_msg}")
    if check_disposable and check_disposable_email(domain):
        messages.append("! Domain is a known disposable email provider")
    return is_valid, messages

def main():
    parser = argparse.ArgumentParser(description='Validate an email address.')
    parser.add_argument('email', help='The email address to validate')
    parser.add_argument('--no-dns', action='store_true', help='Skip DNS validation')
    parser.add_argument('--no-disposable-check', action='store_true', help='Skip disposable email check')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed validation results')
    args = parser.parse_args()
    is_valid, messages = validate_email(
        args.email, 
        check_dns=not args.no_dns,
        check_disposable=not args.no_disposable_check
    )
    if args.verbose:
        for message in messages:
            print(message)
        if is_valid:
            print(f"\n✓ {args.email} is a valid email address.")
        else:
            print(f"\n✗ {args.email} is NOT a valid email address.")
    else:
        if is_valid:
            print(f"✓ {args.email} is a valid email address.")
        else:
            print(f"✗ {args.email} is NOT a valid email address.")
    return 0 if is_valid else 1

if __name__ == "__main__":
    exit(main())
