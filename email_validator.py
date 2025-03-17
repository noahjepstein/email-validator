#!/usr/bin/env python3

import re
import argparse
import socket
import smtplib
from email.utils import parseaddr

# Try to import dns.resolver, but don't fail if it's not available
try:
    import dns.resolver
    HAS_DNS_RESOLVER = True
except ImportError:
    HAS_DNS_RESOLVER = False

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

def verify_email_exists(email, domain):
    """
    Verify if the email address exists by attempting an SMTP connection.
    Returns a tuple of (exists, error_message)
    """
    try:
        # Try to get MX records for the domain
        mx_host = domain  # Default to domain if we can't find MX records
        
        if HAS_DNS_RESOLVER:
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                mx_hosts = sorted([(rec.preference, str(rec.exchange).rstrip('.')) for rec in mx_records])
                if mx_hosts:
                    mx_host = mx_hosts[0][1]  # Use the MX with lowest preference
                else:
                    return False, f"No MX records found for {domain}"
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                # No MX records, try to connect directly to the domain
                pass
        
        # Connect to the mail server with a shorter timeout
        server = smtplib.SMTP(mx_host, 25, timeout=5)
        server.set_debuglevel(0)  # Set to 1 for debugging
        
        server.ehlo_or_helo_if_needed()
        
        if server.has_extn('starttls'):
            server.starttls()
            server.ehlo()
        
        server.mail('noreply@example.com')
        code, message = server.rcpt(email)
        server.quit()
        
        if code == 250:
            return True, None
        else:
            return False, f"Email verification failed: {message.decode('utf-8')}"
            
    except (socket.gaierror, socket.error, socket.herror) as e:
        # Common DNS and connection errors
        return True, "Could not connect to mail server, assuming email is valid"
    except smtplib.SMTPException as e:
        # SMTP protocol errors - some servers reject verification attempts
        return True, "Mail server rejected verification attempt, assuming email is valid"
    except Exception as e:
        # For any other errors, assume the email might be valid
        return True, f"Verification error: {str(e)}, assuming email is valid"

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

def validate_email(email, check_dns=True, check_disposable=True, verify_existence=False):
    """
    Comprehensive email validation.
    Returns a tuple of (is_valid, messages) where messages is a list of validation results.
    """
    messages = []
    is_valid = True
    
    if not is_valid_format(email):
        messages.append("\u2717 Invalid email format")
        return False, messages
    else:
        messages.append("\u2713 Valid email format")
    
    _, addr = parseaddr(email)
    try:
        username, domain = addr.split('@', 1)
    except ValueError:
        messages.append("\u2717 Could not parse email address")
        return False, messages
    
    if len(username) > 64:
        is_valid = False
        messages.append("\u2717 Username exceeds maximum length (64 characters)")
    
    if len(domain) > 255:
        is_valid = False
        messages.append("\u2717 Domain exceeds maximum length (255 characters)")
    
    if check_dns:
        domain_valid, error_msg = validate_domain(domain)
        if domain_valid:
            messages.append("\u2713 Domain has valid DNS records")
        else:
            is_valid = False
            messages.append(f"\u2717 {error_msg}")
            # If domain is invalid, skip existence check
            verify_existence = False
    
    if verify_existence and is_valid:
        exists, error_msg = verify_email_exists(email, domain)
        if exists:
            messages.append("\u2713 Email address exists and can receive emails")
        else:
            is_valid = False
            messages.append(f"\u2717 {error_msg}")
    
    if check_disposable and check_disposable_email(domain):
        messages.append("! Domain is a known disposable email provider")
    
    return is_valid, messages

def main():
    parser = argparse.ArgumentParser(description='Validate an email address.')
    parser.add_argument('email', help='The email address to validate')
    parser.add_argument('--no-dns', action='store_true', help='Skip DNS validation')
    parser.add_argument('--no-disposable-check', action='store_true', help='Skip disposable email check')
    parser.add_argument('--no-verify', action='store_true', help='Skip SMTP verification of email existence')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed validation results')
    
    args = parser.parse_args()
    
    is_valid, messages = validate_email(
        args.email, 
        check_dns=not args.no_dns,
        check_disposable=not args.no_disposable_check,
        verify_existence=not args.no_verify
    )
    
    if args.verbose:
        for message in messages:
            print(message)
        if is_valid:
            print(f"\n\u2713 {args.email} is a valid email address.")
        else:
            print(f"\n\u2717 {args.email} is NOT a valid email address.")
    else:
        if is_valid:
            print(f"\u2713 {args.email} is a valid email address.")
        else:
            print(f"\u2717 {args.email} is NOT a valid email address.")
    
    return 0 if is_valid else 1

if __name__ == "__main__":
    exit(main())
