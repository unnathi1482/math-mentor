# Solution Templates for Common Problem Types

## Quadratic Equation Template

### Problem Type
Solve ax² + bx + c = 0

### Steps
1. Identify coefficients a, b, c
2. Calculate discriminant D = b² - 4ac
3. Analyze discriminant:
   - D > 0: Two real roots
   - D = 0: One repeated root
   - D < 0: Complex roots
4. Apply quadratic formula: x = (-b ± √D) / 2a
5. Simplify the roots
6. Verify by substituting back

### Example
Solve: x² - 5x + 6 = 0
1. a = 1, b = -5, c = 6
2. D = (-5)² - 4(1)(6) = 25 - 24 = 1
3. D > 0, so two real roots
4. x = (5 ± √1) / 2 = (5 ± 1) / 2
5. x = 3 or x = 2
6. Check: 3² - 5(3) + 6 = 9 - 15 + 6 = 0 ✓

---

## Derivative Problem Template

### Problem Type
Find dy/dx for a given function

### Steps
1. Identify the function type
2. Choose appropriate rule:
   - Simple: Power rule, trig rules
   - Product: Product rule
   - Quotient: Quotient rule
   - Composite: Chain rule
3. Apply the rule step by step
4. Simplify the result
5. Factor if possible

### Example
Find d/dx(x² sin x)
1. This is a product of two functions
2. Use product rule: d/dx(uv) = u'v + uv'
3. Let u = x², v = sin x
   - u' = 2x
   - v' = cos x
4. d/dx(x² sin x) = 2x(sin x) + x²(cos x)
5. Final answer: 2x sin x + x² cos x

---

## Integration Problem Template

### Problem Type
Find ∫ f(x) dx

### Steps
1. Identify the integral type
2. Choose technique:
   - Direct: Use standard formulas
   - Substitution: If composite function
   - Parts: If product of different types
3. Apply the technique
4. Don't forget + C for indefinite integrals
5. Verify by differentiating

### Example
Find ∫ x cos(x²) dx
1. Composite function suggests substitution
2. Let u = x², then du = 2x dx, so x dx = du/2
3. ∫ x cos(x²) dx = ∫ cos(u) × (du/2) = (1/2) ∫ cos(u) du
4. = (1/2) sin(u) + C
5. = (1/2) sin(x²) + C
6. Check: d/dx[(1/2)sin(x²)] = (1/2)cos(x²)(2x) = x cos(x²) ✓

---

## Probability Problem Template

### Problem Type
Find probability of event

### Steps
1. Identify the sample space
2. Count total outcomes
3. Identify favorable outcomes
4. Apply appropriate formula:
   - Basic: P = favorable / total
   - Addition: P(A∪B) = P(A) + P(B) - P(A∩B)
   - Multiplication: P(A∩B) = P(A) × P(B|A)
5. Simplify and verify 0 ≤ P ≤ 1

### Example
Two dice are thrown. Find P(sum = 7).
1. Sample space: All pairs (1,1) to (6,6)
2. Total outcomes: 6 × 6 = 36
3. Favorable: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) = 6 outcomes
4. P(sum = 7) = 6/36 = 1/6
5. Check: 0 < 1/6 < 1 ✓

---

## System of Equations Template

### Problem Type
Solve system of linear equations

### Steps
1. Write in matrix form AX = B
2. Check if det(A) ≠ 0
3. Choose method:
   - 2×2: Cramer's rule or inverse
   - 3×3: Gaussian elimination or Cramer's rule
4. Solve for variables
5. Verify by substituting back

### Example
Solve: 2x + 3y = 8
       x - y = 1

1. A = |2  3|, X = |x|, B = |8|
       |1 -1|      |y|      |1|

2. det(A) = 2(-1) - 3(1) = -2 - 3 = -5 ≠ 0

3. Using Cramer's rule:
   x = det|8  3| / det(A) = (-8-3)/(-5) = -11/-5 = 11/5
          |1 -1|
   
   y = det|2  8| / det(A) = (2-8)/(-5) = -6/-5 = 6/5
          |1  1|

4. x = 11/5 = 2.2, y = 6/5 = 1.2

5. Check: 2(2.2) + 3(1.2) = 4.4 + 3.6 = 8 ✓

---

## Limit Problem Template

### Problem Type
Find lim(x→a) f(x)

### Steps
1. Try direct substitution
2. If 0/0 or ∞/∞, try:
   - Factoring and canceling
   - Rationalizing (for square roots)
   - L'Hôpital's rule
   - Standard limits
3. Apply the technique
4. Simplify and get final answer

### Example
Find lim(x→2) (x² - 4)/(x - 2)
1. Direct: (4-4)/(2-2) = 0/0 (indeterminate)
2. Factor numerator: x² - 4 = (x+2)(x-2)
3. (x² - 4)/(x - 2) = (x+2)(x-2)/(x-2) = x + 2
4. lim(x→2) (x + 2) = 2 + 2 = 4

---

## Optimization Problem Template

### Problem Type
Find maximum or minimum value

### Steps
1. Define the variable to optimize
2. Write objective function in one variable
3. Find derivative and set equal to zero
4. Solve for critical points
5. Use second derivative test:
   - f''(x) > 0 → minimum
   - f''(x) < 0 → maximum
6. Check boundary conditions if applicable
7. State the optimal value

### Example
Find the minimum value of f(x) = x² - 4x + 7
1. Objective: minimize f(x)
2. Already in one variable
3. f'(x) = 2x - 4 = 0
4. x = 2 (critical point)
5. f''(x) = 2 > 0, so x = 2 is a minimum
6. No boundaries given
7. f(2) = 4 - 8 + 7 = 3
   Minimum value is 3 at x = 2

---

## Binomial Probability Template

### Problem Type
Find probability of k successes in n trials

### Steps
1. Identify n (trials), k (successes), p (probability of success)
2. Verify binomial conditions:
   - Fixed number of trials
   - Independent trials
   - Constant probability
   - Two outcomes only
3. Apply formula: P(X = k) = nCk × p^k × (1-p)^(n-k)
4. Calculate nCk = n! / (k! × (n-k)!)
5. Compute and simplify

### Example
A coin is tossed 5 times. Find P(exactly 3 heads).
1. n = 5, k = 3, p = 0.5
2. Conditions met (fair coin, independent tosses)
3. P(X = 3) = 5C3 × (0.5)³ × (0.5)²
4. 5C3 = 5!/(3!×2!) = 10
5. P = 10 × 0.125 × 0.25 = 10 × 0.03125 = 0.3125 = 5/16