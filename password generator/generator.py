import random
import string

class PasswordGenerator:
    def __init__(self):
        self.uppercase = string.ascii_uppercase
        self.lowercase = string.ascii_lowercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    def generate(self, length=12, use_upper=True, use_lower=True, use_digits=True, use_symbols=True, exclude_chars=""):
        """
        Generates a password based on the specified criteria.
        """
        if not any([use_upper, use_lower, use_digits, use_symbols]):
            return "Error: Select at least one character type."

        # Filter pools based on exclusion list
        pool_upper = "".join([c for c in self.uppercase if c not in exclude_chars])
        pool_lower = "".join([c for c in self.lowercase if c not in exclude_chars])
        pool_digits = "".join([c for c in self.digits if c not in exclude_chars])
        pool_symbols = "".join([c for c in self.symbols if c not in exclude_chars])

        char_pool = ""
        password = []

        # Ensure at least one character from each selected category is included
        try:
            if use_upper:
                if not pool_upper: raise ValueError("No uppercase characters available.")
                char_pool += pool_upper
                password.append(random.choice(pool_upper))
            if use_lower:
                if not pool_lower: raise ValueError("No lowercase characters available.")
                char_pool += pool_lower
                password.append(random.choice(pool_lower))
            if use_digits:
                if not pool_digits: raise ValueError("No digits available.")
                char_pool += pool_digits
                password.append(random.choice(pool_digits))
            if use_symbols:
                if not pool_symbols: raise ValueError("No symbols available.")
                char_pool += pool_symbols
                password.append(random.choice(pool_symbols))
        except ValueError as e:
            return f"Error: {str(e)}"

        if not char_pool:
            return "Error: No characters available to generate password."

        # Fill the rest of the password length
        remaining_length = length - len(password)
        if remaining_length > 0:
            for _ in range(remaining_length):
                password.append(random.choice(char_pool))

        # Shuffle the password to avoid predictable patterns
        random.shuffle(password)
        
        return "".join(password)

    def check_strength(self, password):
        """
        Returns a strength score (0-4) and a label.
        """
        score = 0
        if len(password) >= 8:
            score += 1
        if any(c in self.uppercase for c in password):
            score += 1
        if any(c in self.lowercase for c in password):
            score += 1
        if any(c in self.digits for c in password):
            score += 1
        if any(c in self.symbols for c in password):
            score += 1
            
        # Adjust for length
        if len(password) >= 12:
            score += 1
            
        # Cap score at 4 for simplicity in this context, or map to labels
        # Let's do a simple mapping
        if score < 3:
            return "Weak", "#ff4d4d" # Red
        elif score < 5:
            return "Medium", "#ffa64d" # Orange
        else:
            return "Strong", "#4dff88" # Green
