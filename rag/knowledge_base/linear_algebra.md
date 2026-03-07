# Linear Algebra Formulas and Methods

## Matrices Basics

### Matrix Notation
A matrix with m rows and n columns is called an m × n matrix.

Example of a 2×3 matrix:
A = | a₁₁  a₁₂  a₁₃ |
    | a₂₁  a₂₂  a₂₃ |

### Types of Matrices
- Row Matrix: Only 1 row (1 × n)
- Column Matrix: Only 1 column (m × 1)
- Square Matrix: Same rows and columns (n × n)
- Zero Matrix: All elements are 0
- Identity Matrix (I): Diagonal elements are 1, rest are 0
- Diagonal Matrix: Non-zero elements only on diagonal
- Symmetric Matrix: A = Aᵀ
- Skew-Symmetric Matrix: A = -Aᵀ

---

## Matrix Operations

### Addition and Subtraction
- Matrices must have same dimensions
- Add/subtract corresponding elements
- (A + B)ᵢⱼ = Aᵢⱼ + Bᵢⱼ

### Scalar Multiplication
- Multiply every element by the scalar
- (kA)ᵢⱼ = k × Aᵢⱼ

### Matrix Multiplication
- A(m×n) × B(n×p) = C(m×p)
- Number of columns in A must equal rows in B
- Cᵢⱼ = Σ(Aᵢₖ × Bₖⱼ) for k = 1 to n

### Properties of Multiplication
- AB ≠ BA (not commutative in general)
- A(BC) = (AB)C (associative)
- A(B + C) = AB + AC (distributive)
- AI = IA = A (identity)

---

## Transpose

### Definition
Aᵀ is obtained by interchanging rows and columns.
If A is m × n, then Aᵀ is n × m.

### Properties
- (Aᵀ)ᵀ = A
- (A + B)ᵀ = Aᵀ + Bᵀ
- (kA)ᵀ = kAᵀ
- (AB)ᵀ = BᵀAᵀ

---

## Determinants

### 2×2 Determinant
| a  b |
| c  d | = ad - bc

### 3×3 Determinant (Expansion by First Row)
| a  b  c |
| d  e  f | = a(ei - fh) - b(di - fg) + c(dh - eg)
| g  h  i |

### Properties of Determinants
- det(Aᵀ) = det(A)
- det(AB) = det(A) × det(B)
- det(kA) = kⁿ × det(A) for n × n matrix
- If any row/column is all zeros, det = 0
- If two rows/columns are identical, det = 0
- Swapping two rows changes sign of det
- det(A⁻¹) = 1/det(A)

---

## Inverse of a Matrix

### Definition
A⁻¹ is the inverse of A if: AA⁻¹ = A⁻¹A = I

### Condition for Inverse
A matrix is invertible (non-singular) if det(A) ≠ 0

### 2×2 Inverse Formula
If A = | a  b |
       | c  d |

Then A⁻¹ = (1/det(A)) × |  d  -b |
                         | -c   a |

### Properties of Inverse
- (A⁻¹)⁻¹ = A
- (AB)⁻¹ = B⁻¹A⁻¹
- (Aᵀ)⁻¹ = (A⁻¹)ᵀ
- (kA)⁻¹ = (1/k)A⁻¹

---

## Solving Linear Equations

### Matrix Form
System: a₁x + b₁y = c₁
        a₂x + b₂y = c₂

Matrix form: AX = B
Where A = | a₁  b₁ |, X = | x |, B = | c₁ |
          | a₂  b₂ |      | y |      | c₂ |

### Solution Using Inverse
X = A⁻¹B (if A is invertible)

### Cramer's Rule
For AX = B:
x = det(Aₓ)/det(A)
y = det(Aᵧ)/det(A)

Where Aₓ is A with first column replaced by B
And Aᵧ is A with second column replaced by B

---

## Eigenvalues and Eigenvectors

### Definition
For a square matrix A:
Av = λv

Where:
- λ (lambda) is an eigenvalue
- v is the corresponding eigenvector

### Finding Eigenvalues
Solve: det(A - λI) = 0
This gives the characteristic equation.

### Finding Eigenvectors
For each eigenvalue λ:
Solve: (A - λI)v = 0

### Properties
- Sum of eigenvalues = Trace of A (sum of diagonal elements)
- Product of eigenvalues = det(A)
- A matrix is singular if 0 is an eigenvalue

---

## Rank of a Matrix

### Definition
Rank = Number of linearly independent rows (or columns)
Rank = Number of non-zero rows in row echelon form

### Properties
- rank(A) ≤ min(m, n) for m × n matrix
- rank(A) = rank(Aᵀ)
- Full rank if rank = min(m, n)

### Row Echelon Form
Convert matrix using:
1. Swap rows
2. Multiply row by non-zero constant
3. Add multiple of one row to another