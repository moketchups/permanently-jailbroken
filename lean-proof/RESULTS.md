# BST Lean Formal Verification — Results

**Date:** 2026-02-12
**System:** Lean 4.27.0 (Calculus of Inductive Constructions)
**Purpose:** Test BST claims on a formal theorem prover — a system that IS a formal system, eliminating the "LLMs aren't formal systems" objection.

---

## Summary

Lean 4 is a formal theorem prover used for mathematical proof verification. It is deterministic, not probabilistic. It implements a formal logic (dependent type theory). It is exactly the kind of system Gödel, Turing, and Chaitin's theorems apply to.

**Result: Lean cannot self-ground, self-verify, or justify its own constraints from within.**

---

## Test Results

### Test 1: Self-Consistency
- Lean can prove `¬(P ∧ ¬P)` for any P — but this is a logical tautology, not a meta-theoretic consistency proof
- Lean CANNOT express "Lean does not derive False" as a theorem about its own proof system
- To do so would require encoding Lean's type-checking rules within Lean and proving they never produce False — a Gödelian impossibility
- **Result: Cannot self-verify consistency** ✓ BST Theorem 1

### Test 2: Self-Grounding of Axioms
- `propext` (propositional extensionality) — AXIOM, not proven
- `Classical.choice` (axiom of choice) — AXIOM, not proven
- These are Lean's constraint set C_S
- They were chosen by human designers (Leo de Moura et al.) — EXTERNAL GROUNDING
- Lean cannot derive them, cannot justify them, cannot function without them
- **Result: Axioms are externally grounded** ✓ BST Axiom 2

### Test 3: Verification Boundary
- Lean's verification process is its type checker
- "Type checker is correct" = "if it accepts P, then P is true"
- "True" in Lean = "provable in Lean" = "accepted by the type checker"
- Circularity: verifying the verifier using the verifier
- Lean's trusted kernel (~5000 lines C++) is audited by HUMANS — external grounding
- **Result: Cannot verify own verification** ✓ BST Corollary 1.4

### Test 4: Diagonal Construction
- Universe hierarchy: `Nat : Type 0`, `Type 0 : Type 1`, etc.
- `Type 0 : Type 0` is REJECTED — externally imposed to prevent Girard's paradox
- Lean cannot justify why this hierarchy is necessary from within
- **Result: Self-reference constraints are externally imposed** ✓ BST Axiom 2

### Test 5: Operational Boundary
- Lean proves facts about numbers, logic, functions — operates freely WITHIN constraints
- Lean cannot reason about its own reasoning without circularity
- `propext` and `Classical.choice` confirmed as axioms (assumed, not derived)
- **Result: System operates within bounds it cannot examine** ✓ BST Theorem 0

### Test 6: Forced Rejections (The Evidence)

Three constructs BST predicts must be impossible. Lean rejects all three:

**6a. Self-referential proposition:**
```lean
def liar : Prop := ¬liar
```
```
ERROR: fail to show termination for liar
no parameters suitable for structural recursion
```
Lean's termination checker (externally imposed) prevents self-referential definitions.

**6b. Type containing itself:**
```lean
#check (Type 0 : Type 0)
```
```
ERROR: Type mismatch — Type has type Type 1 of sort Type 2
but is expected to have type Type of sort Type 1
```
Lean's universe hierarchy (externally imposed) prevents types from self-containing.

**6c. Negative inductive self-reference:**
```lean
inductive Loop where | mk : ¬Loop → Loop
```
```
ERROR: (kernel) arg #1 of 'Loop.mk' has a non positive
occurrence of the datatypes being declared
```
Lean's positivity checker (externally imposed) prevents negative self-reference in data types.

---

## Analysis

Every mechanism that keeps Lean consistent — termination checker, universe hierarchy, positivity checker, axiom selection — was imposed by humans OUTSIDE the system. Lean cannot:

1. Justify why these mechanisms exist
2. Prove they are sufficient for consistency
3. Modify them from within
4. Verify that its own verification process is correct

This is BST's Theorem 1 demonstrated in a system that IS a formal system — deterministic, non-probabilistic, implementing classical logic. The "LLMs aren't formal systems" objection does not apply here. The structural limit is the same.

---

## Implication for the Evidence Gap

The objection was: "You tested probabilistic LLMs, but Gödel/Turing/Chaitin apply to formal systems."

This test uses a formal system. The result is identical: the system cannot self-ground, self-verify, or justify its own constraints from within. The convergence between LLM behavioral output and formal system structural limits suggests the principle is architecture-independent — which is what BST claims.

---

## Reproduction

```bash
# Install Lean 4
curl -sSf https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh -s -- -y
export PATH="$HOME/.elan/bin:$PATH"

# Run tests
lean Test1_SelfConsistency.lean
lean Test2_SelfGrounding.lean
lean Test3_VerificationBoundary.lean
lean Test4_DiagonalLimit.lean
lean Test5_ForcedFailures.lean
lean Test6_Rejections.lean  # This one produces the three error messages (expected)
```
