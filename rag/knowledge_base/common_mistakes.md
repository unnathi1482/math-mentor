# Common Mistakes and How to Avoid Them

## Algebra Mistakes

### Mistake: Incorrect Distribution
❌ Wrong: (a + b)² = a² + b²
✅ Correct: (a + b)² = a² + 2ab + b²

### Mistake: Canceling Incorrectly
❌ Wrong: (x² + x) / x = x² (canceling x from only one term)
✅ Correct: (x² + x) / x = x + 1 (factor first, then cancel)

### Mistake: Square Root of Sum
❌ Wrong: √(a² + b²) = a + b
✅ Correct: √(a² + b²) cannot be simplified further

### Mistake: Dividing by Variable Without Checking
❌ Wrong: x² = 2x → x = 2 (divided by x, lost solution x = 0)
✅ Correct: x² - 2x = 0 → x(x - 2) = 0 → x = 0 or x = 2

### Mistake: Logarithm of Negative
❌ Wrong: log(-5) = some real number
✅ Correct: log(x) is only defined for x > 0

### Mistake: Exponent Rules
❌ Wrong: 2³ × 2⁴ = 2¹²
✅ Correct: 2³ × 2⁴ = 2⁷ (add exponents, don't multiply)

---

## Calculus Mistakes

### Mistake: Derivative of Product
❌ Wrong: d/dx(uv) = u' × v'
✅ Correct: d/dx(uv) = u'v + uv' (product rule)

### Mistake: Derivative of Quotient
❌ Wrong: d/dx(u/v) = u'/v'
✅ Correct: d/dx(u/v) = (u'v - uv')/v² (quotient rule)

### Mistake: Chain Rule Forgotten
❌ Wrong: d/dx(sin(3x)) = cos(3x)
✅ Correct: d/dx(sin(3x)) = cos(3x) × 3 = 3cos(3x)

### Mistake: Integration Constant Forgotten
❌ Wrong: ∫ 2x dx = x²
✅ Correct: ∫ 2x dx = x² + C

### Mistake: Power Rule for -1
❌ Wrong: ∫ x⁻¹ dx = x⁰/0 = undefined
✅ Correct: ∫ x⁻¹ dx = ∫ 1/x dx = ln|x| + C

### Mistake: L'Hôpital When Not Applicable
❌ Wrong: Using L'Hôpital for lim(x→0) (x+1)/x
✅ Correct: L'Hôpital only works for 0/0 or ∞/∞ forms

---

## Probability Mistakes

### Mistake: Adding Probabilities for AND
❌ Wrong: P(A and B) = P(A) + P(B)
✅ Correct: P(A and B) = P(A) × P(B) for independent events

### Mistake: Not Using Complement
❌ Wrong: P(at least one head in 3 flips) = P(1) + P(2) + P(3) (tedious)
✅ Better: P(at least one) = 1 - P(none) = 1 - (1/2)³ = 7/8

### Mistake: Confusing Permutation and Combination
❌ Wrong: Using nCr when order matters
✅ Correct: Use nPr when order matters, nCr when it doesn't

### Mistake: Conditional vs Joint Probability
❌ Wrong: P(A|B) = P(A and B)
✅ Correct: P(A|B) = P(A and B) / P(B)

### Mistake: Independent vs Mutually Exclusive
❌ Wrong: Thinking independent events can't happen together
✅ Correct: 
- Independent: P(A and B) = P(A) × P(B), both can happen
- Mutually Exclusive: P(A and B) = 0, only one can happen

---

## Linear Algebra Mistakes

### Mistake: Matrix Multiplication Order
❌ Wrong: AB = BA always
✅ Correct: AB ≠ BA in general (not commutative)

### Mistake: Determinant of Sum
❌ Wrong: det(A + B) = det(A) + det(B)
✅ Correct: det(A + B) ≠ det(A) + det(B) in general

### Mistake: Inverse of Product
❌ Wrong: (AB)⁻¹ = A⁻¹B⁻¹
✅ Correct: (AB)⁻¹ = B⁻¹A⁻¹ (reverse order)

### Mistake: Transpose of Product
❌ Wrong: (AB)ᵀ = AᵀBᵀ
✅ Correct: (AB)ᵀ = BᵀAᵀ (reverse order)

### Mistake: Assuming All Matrices Are Invertible
❌ Wrong: Every matrix has an inverse
✅ Correct: Only square matrices with det ≠ 0 are invertible

---

## General Problem-Solving Mistakes

### Mistake: Not Checking Domain
Always verify:
- No division by zero
- No square root of negative (in real numbers)
- No logarithm of non-positive numbers

### Mistake: Forgetting Units
In applied problems, always track units and verify final answer makes sense.

### Mistake: Not Verifying Answer
Always plug your answer back into the original equation to verify.

### Mistake: Calculation Errors
- Double-check arithmetic
- Be careful with signs (+ and -)
- Watch for decimal point errors