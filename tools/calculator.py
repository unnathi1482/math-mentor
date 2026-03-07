"""
Calculator tool for solving math expressions.
This allows the AI to run actual calculations instead of guessing.
"""

import math
import re


def safe_calculate(expression: str) -> dict:
    """
    Safely evaluate a math expression.
    
    Args:
        expression: A math expression like "2 + 3 * 4" or "sqrt(16)"
    
    Returns:
        dict with 'success', 'result', and 'error' keys
    """
    try:
        # Clean the expression
        cleaned = clean_expression(expression)
        
        # Define safe math functions
        safe_dict = {
            # Basic math
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "sum": sum,
            "pow": pow,
            
            # From math module
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "log10": math.log10,
            "log2": math.log2,
            "exp": math.exp,
            "floor": math.floor,
            "ceil": math.ceil,
            "factorial": math.factorial,
            "gcd": math.gcd,
            
            # Constants
            "pi": math.pi,
            "e": math.e,
            
            # Trig inverses
            "asin": math.asin,
            "acos": math.acos,
            "atan": math.atan,
            
            # Hyperbolic
            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,
        }
        
        # Evaluate safely
        result = eval(cleaned, {"__builtins__": {}}, safe_dict)
        
        return {
            "success": True,
            "result": result,
            "error": None,
            "expression": cleaned
        }
        
    except ZeroDivisionError:
        return {
            "success": False,
            "result": None,
            "error": "Division by zero",
            "expression": expression
        }
    except ValueError as e:
        return {
            "success": False,
            "result": None,
            "error": f"Math error: {str(e)}",
            "expression": expression
        }
    except Exception as e:
        return {
            "success": False,
            "result": None,
            "error": f"Calculation error: {str(e)}",
            "expression": expression
        }


def clean_expression(expression: str) -> str:
    """
    Clean and standardize a math expression.
    
    Converts common notations to Python-compatible format.
    """
    expr = expression.strip()
    
    # Replace common symbols
    replacements = {
        "×": "*",
        "÷": "/",
        "^": "**",
        "√": "sqrt",
        "π": "pi",
        "²": "**2",
        "³": "**3",
    }
    
    for old, new in replacements.items():
        expr = expr.replace(old, new)
    
    # Handle implicit multiplication: 2x → 2*x, 3(4) → 3*(4)
    # Add * between number and letter
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
    # Add * between number and opening parenthesis
    expr = re.sub(r'(\d)\(', r'\1*(', expr)
    # Add * between closing parenthesis and number
    expr = re.sub(r'\)(\d)', r')*\1', expr)
    # Add * between closing and opening parenthesis
    expr = re.sub(r'\)\(', r')*(', expr)
    
    return expr


def solve_quadratic(a: float, b: float, c: float) -> dict:
    """
    Solve quadratic equation ax² + bx + c = 0
    
    Returns both roots (real or complex).
    """
    try:
        discriminant = b**2 - 4*a*c
        
        if discriminant >= 0:
            # Real roots
            sqrt_disc = math.sqrt(discriminant)
            x1 = (-b + sqrt_disc) / (2*a)
            x2 = (-b - sqrt_disc) / (2*a)
            
            return {
                "success": True,
                "discriminant": discriminant,
                "root_type": "real" if discriminant > 0 else "repeated",
                "x1": x1,
                "x2": x2,
                "error": None
            }
        else:
            # Complex roots
            real_part = -b / (2*a)
            imag_part = math.sqrt(abs(discriminant)) / (2*a)
            
            return {
                "success": True,
                "discriminant": discriminant,
                "root_type": "complex",
                "x1": f"{real_part} + {imag_part}i",
                "x2": f"{real_part} - {imag_part}i",
                "error": None
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def calculate_derivative(expression: str, variable: str = "x") -> str:
    """
    Returns a hint about how to find the derivative.
    
    Note: For actual symbolic differentiation, we'd need sympy.
    This provides guidance for common cases.
    """
    rules = []
    
    if "**" in expression or "^" in expression:
        rules.append("Power Rule: d/dx(x^n) = n*x^(n-1)")
    
    if "sin" in expression:
        rules.append("d/dx(sin(x)) = cos(x)")
    
    if "cos" in expression:
        rules.append("d/dx(cos(x)) = -sin(x)")
    
    if "tan" in expression:
        rules.append("d/dx(tan(x)) = sec²(x)")
    
    if "log" in expression or "ln" in expression:
        rules.append("d/dx(ln(x)) = 1/x")
    
    if "exp" in expression or "e**" in expression:
        rules.append("d/dx(e^x) = e^x")
    
    if "*" in expression:
        rules.append("Product Rule: d/dx(f*g) = f'*g + f*g'")
    
    if "/" in expression:
        rules.append("Quotient Rule: d/dx(f/g) = (f'*g - f*g') / g²")
    
    if not rules:
        rules.append("Constant Rule: d/dx(c) = 0")
    
    return "Applicable rules:\n" + "\n".join(f"• {rule}" for rule in rules)