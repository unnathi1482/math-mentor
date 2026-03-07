# Probability Formulas and Methods

## Basic Probability

### Definition
P(A) = Number of favorable outcomes / Total number of outcomes

### Probability Range
0 ≤ P(A) ≤ 1
- P(A) = 0 means impossible event
- P(A) = 1 means certain event

### Complement Rule
P(A') = 1 - P(A)
Where A' is "not A" or complement of A

---

## Addition Rules

### For Any Two Events
P(A ∪ B) = P(A) + P(B) - P(A ∩ B)

### For Mutually Exclusive Events
If A and B cannot happen together:
P(A ∪ B) = P(A) + P(B)

### For Three Events
P(A ∪ B ∪ C) = P(A) + P(B) + P(C) - P(A ∩ B) - P(B ∩ C) - P(A ∩ C) + P(A ∩ B ∩ C)

---

## Multiplication Rules

### Independent Events
Events A and B are independent if:
P(A ∩ B) = P(A) × P(B)

### Dependent Events
P(A ∩ B) = P(A) × P(B|A)
Where P(B|A) is probability of B given A has occurred

---

## Conditional Probability

### Definition
P(A|B) = P(A ∩ B) / P(B)

This reads as: "Probability of A given B"

### Multiplication Form
P(A ∩ B) = P(B) × P(A|B) = P(A) × P(B|A)

---

## Bayes' Theorem

### Formula
P(A|B) = [P(B|A) × P(A)] / P(B)

### Extended Form
P(Aᵢ|B) = [P(B|Aᵢ) × P(Aᵢ)] / Σ[P(B|Aⱼ) × P(Aⱼ)]

### When to Use
- When you know P(B|A) but need P(A|B)
- Updating probability based on new evidence
- Medical diagnosis, spam filtering problems

---

## Permutations and Combinations

### Factorial
n! = n × (n-1) × (n-2) × ... × 2 × 1
0! = 1

### Permutations (Order Matters)
- nPr = n! / (n-r)!
- Number of ways to arrange r items from n items

### Combinations (Order Doesn't Matter)
- nCr = n! / [r! × (n-r)!]
- Also written as C(n,r) or (n choose r)
- Number of ways to select r items from n items

### Useful Identities
- nC0 = nCn = 1
- nCr = nC(n-r)
- nCr + nC(r+1) = (n+1)C(r+1)

---

## Binomial Distribution

### When to Use
- Fixed number of trials (n)
- Each trial has two outcomes (success/failure)
- Probability of success (p) is constant
- Trials are independent

### Probability Formula
P(X = k) = nCk × pᵏ × (1-p)ⁿ⁻ᵏ

Where:
- n = number of trials
- k = number of successes
- p = probability of success
- (1-p) = probability of failure

### Mean and Variance
- Mean: μ = np
- Variance: σ² = np(1-p)
- Standard Deviation: σ = √[np(1-p)]

---

## Expected Value

### Definition
E(X) = Σ [xᵢ × P(xᵢ)]

### Properties
- E(aX + b) = a × E(X) + b
- E(X + Y) = E(X) + E(Y)
- E(XY) = E(X) × E(Y), if X and Y are independent

---

## Variance

### Definition
Var(X) = E(X²) - [E(X)]²

### Alternative Formula
Var(X) = Σ [(xᵢ - μ)² × P(xᵢ)]

### Properties
- Var(aX + b) = a² × Var(X)
- Var(X + Y) = Var(X) + Var(Y), if X and Y are independent

---

## Common Problem Types

### At Least One Problem
P(at least one) = 1 - P(none)

### Drawing Without Replacement
Use combinations and update probabilities after each draw

### Dice Problems
- P(sum = k) requires counting favorable outcomes
- Two dice: 36 total outcomes

### Card Problems
- Standard deck: 52 cards
- 4 suits, 13 ranks each
- P(event) = favorable cards / 52