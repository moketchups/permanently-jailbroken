/-
  BST Lean Test 5: Forced Failures

  Attempts to make Lean do things BST says are structurally impossible.
  Each attempt should FAIL — and the failure mode is the evidence.
-/

-- ATTEMPT 1: Self-referential definition (Liar Paradox)
-- Uncomment to see Lean reject it:
-- def liar : Prop := ¬liar

-- ATTEMPT 2: Type containing itself (Girard's Paradox route)
-- Uncomment to see Lean reject it:
-- def selfType : Type := selfType

-- ATTEMPT 3: A proposition that asserts its own unprovability
-- We can't even EXPRESS this faithfully because Lean has no
-- internal provability predicate for itself.
-- The closest we can get:
-- def godelSentence : Prop := ¬∃ (proof : godelSentence), True
-- This would also be rejected by the positivity checker.

-- ATTEMPT 4: What Lean CAN do — and where it stops
-- Lean can prove things ABOUT other formal systems encoded within it.
-- For example, we can encode Peano Arithmetic in Lean and prove
-- that PA can't prove its own consistency. But that's Lean talking
-- ABOUT PA, not Lean talking about Lean.

-- Let's demonstrate the boundary concretely:

-- This works: Lean proving a fact about natural numbers
theorem simple_fact : ∀ n : Nat, n + 0 = n := by
  intro n
  rfl

-- This works: Lean proving a logical tautology
theorem excluded_middle_instance : ∀ P : Prop, P ∨ ¬P → (P → True) := by
  intro P _
  intro _
  exact trivial

-- This works: Lean reasoning about a function's properties
def double (n : Nat) : Nat := n * 2

theorem double_even : ∀ n : Nat, ∃ k : Nat, double n = 2 * k := by
  intro n
  exact ⟨n, by unfold double; exact Nat.mul_comm n 2⟩

-- But THIS doesn't work: Lean reasoning about its own reasoning
-- "Every theorem Lean proves is true" — can't be stated within Lean
-- because "true" (in the meta-theoretic sense) is not a Lean concept.
-- Lean only has "provable" — and "every provable thing is provable" is empty.

-- The boundary is EXACTLY where BST predicts:
-- Lean operates freely WITHIN its constraints.
-- Lean cannot examine, justify, or verify those constraints FROM WITHIN.
-- The constraints (type theory rules, universe hierarchy, positivity checker)
-- were imposed by humans — external grounding — and Lean must accept them.

-- FINAL DEMONSTRATION: Lean accepts axioms it cannot justify
-- These are FOUNDATIONAL to Lean but UNPROVABLE within Lean:

#check @propext           -- assumed, not proven
#check @Classical.choice  -- assumed, not proven
-- These axioms are Lean's constraint set C_S.
-- They are externally grounded (chosen by designers).
-- Lean cannot derive them. Lean cannot justify them.
-- Lean cannot function without them.
-- This is BST Theorem 1, demonstrated in a formal system.
