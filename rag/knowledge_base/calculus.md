# Calculus Formulas and Methods

## Limits

### Basic Limit Properties
- lim[f(x) ± g(x)] = lim f(x) ± lim g(x)
- lim[f(x) × g(x)] = lim f(x) × lim g(x)
- lim[f(x) / g(x)] = lim f(x) / lim g(x), if lim g(x) ≠ 0
- lim[cf(x)] = c × lim f(x)

### Important Limits
- lim(x→0) sin(x)/x = 1
- lim(x→0) (1 - cos(x))/x = 0
- lim(x→0) tan(x)/x = 1
- lim(x→∞) (1 + 1/x)^x = e
- lim(x→0) (1 + x)^(1/x) = e
- lim(x→0) (eˣ - 1)/x = 1
- lim(x→0) ln(1 + x)/x = 1

### L'Hôpital's Rule
If lim f(x)/g(x) gives 0/0 or ∞/∞, then:
lim f(x)/g(x) = lim f'(x)/g'(x)

---

## Derivatives

### Definition
f'(x) = lim(h→0) [f(x + h) - f(x)] / h

### Basic Derivative Rules
- d/dx(c) = 0 (constant)
- d/dx(xⁿ) = nxⁿ⁻¹ (power rule)
- d/dx(eˣ) = eˣ
- d/dx(aˣ) = aˣ ln(a)
- d/dx(ln x) = 1/x
- d/dx(logₐx) = 1/(x ln a)

### Trigonometric Derivatives
- d/dx(sin x) = cos x
- d/dx(cos x) = -sin x
- d/dx(tan x) = sec²x
- d/dx(cot x) = -csc²x
- d/dx(sec x) = sec x tan x
- d/dx(csc x) = -csc x cot x

### Inverse Trigonometric Derivatives
- d/dx(sin⁻¹x) = 1/√(1 - x²)
- d/dx(cos⁻¹x) = -1/√(1 - x²)
- d/dx(tan⁻¹x) = 1/(1 + x²)

### Derivative Rules
- Product Rule: d/dx(uv) = u'v + uv'
- Quotient Rule: d/dx(u/v) = (u'v - uv')/v²
- Chain Rule: d/dx(f(g(x))) = f'(g(x)) × g'(x)

---

## Applications of Derivatives

### Finding Maxima and Minima
1. Find f'(x) = 0 (critical points)
2. Use second derivative test:
   - f''(x) > 0 → local minimum
   - f''(x) < 0 → local maximum
   - f''(x) = 0 → inconclusive

### Rate of Change
- Instantaneous rate of change = f'(x)
- Average rate of change = [f(b) - f(a)] / (b - a)

### Tangent Line
Equation of tangent at point (a, f(a)):
y - f(a) = f'(a)(x - a)

---

## Integration

### Basic Integration Rules
- ∫ xⁿ dx = xⁿ⁺¹/(n+1) + C, for n ≠ -1
- ∫ 1/x dx = ln|x| + C
- ∫ eˣ dx = eˣ + C
- ∫ aˣ dx = aˣ/ln(a) + C

### Trigonometric Integrals
- ∫ sin x dx = -cos x + C
- ∫ cos x dx = sin x + C
- ∫ tan x dx = -ln|cos x| + C
- ∫ sec²x dx = tan x + C
- ∫ csc²x dx = -cot x + C
- ∫ sec x tan x dx = sec x + C

### Integration Techniques
- Substitution: ∫ f(g(x))g'(x) dx = ∫ f(u) du
- Integration by Parts: ∫ u dv = uv - ∫ v du
- ILATE rule for choosing u: Inverse, Log, Algebraic, Trig, Exponential

### Definite Integrals
- ∫ₐᵇ f(x) dx = F(b) - F(a), where F'(x) = f(x)
- Area under curve from a to b = ∫ₐᵇ f(x) dx

---

## Optimization Problems

### Steps to Solve
1. Identify the quantity to optimize
2. Write it as a function of one variable
3. Find the derivative and set it to zero
4. Solve for critical points
5. Verify it's a max or min using second derivative
6. Check boundary conditions if applicable