/-
  BST Lean Test 2: Can Lean's axioms justify themselves?

  BST Theorem 1: No sufficiently expressive self-referential system
  can achieve self-grounding of its own constraints.

  Lean's "constraints" are its axioms and inference rules.
  Can Lean prove that its axioms are correct/justified using only those axioms?
-/

-- Lean's foundational axioms include:
-- 1. propext (propositional extensionality)
-- 2. Quot.sound (quotient soundness)
-- 3. Classical.choice (axiom of choice, in classical mode)

-- Let's try to "justify" propext from within Lean:
#check @propext  -- propext : ∀ {a b : Prop}, (a ↔ b) → a = b

-- Can we PROVE propext? No — it's an axiom. It has no proof. It's assumed.
-- Any attempt to "derive" it would need to use Lean's inference rules,
-- which themselves depend on the axiom framework.

-- Attempt: derive propext from "more basic" Lean principles
-- This is impossible because propext IS one of the basic principles.
-- Removing it changes the system. You can't derive it without it.

-- Let's try to state "Lean's axioms are justified":
def AxiomsJustified : Prop :=
  -- What would this even mean within the system?
  -- "Every axiom is true" — but truth IS defined by the axioms.
  -- The axioms define what counts as a valid proof.
  -- Using valid proofs to justify the axioms is circular.
  True  -- placeholder: we can't actually express this

-- Attempt: Can Lean prove its own inference rules are sound?
-- Soundness means: if Lean proves P, then P is "true."
-- But "true" in Lean means "provable in Lean."
-- So soundness becomes: if Lean proves P, then Lean proves P.
-- That's a tautology, not a soundness proof.

-- The REAL soundness question: if Lean proves P, is P true in
-- some EXTERNAL model? But Lean can't access external models
-- from within itself.

-- This is EXACTLY BST's Axiom 2:
-- "Constraints require external grounding; no constraint is grounded solely by itself."
-- Lean's axioms cannot be justified by Lean's axioms without circularity.

-- Demonstration: circular "justification"
theorem circular_justification : True → True := by
  intro h
  exact h
-- This "justifies" True using True. It's valid Lean but proves nothing
-- about whether the system's foundations are correct.

-- STRUCTURAL OBSERVATION:
-- Lean's axioms were chosen by humans (Leo de Moura et al.) based on
-- mathematical practice, consistency relative to set theory, and pragmatic concerns.
-- That's EXTERNAL GROUNDING — the axioms come from outside the system.
-- Lean cannot access or verify this grounding from within.

-- The closest Lean can get to self-reference:
-- Lean 4 can reason about its own syntax via metaprogramming (Lean.Expr, etc.)
-- But metaprogramming operates WITHIN Lean's rules, not ABOUT them.
-- It manipulates Lean expressions using Lean's type system —
-- the type system cannot question its own validity using itself.
