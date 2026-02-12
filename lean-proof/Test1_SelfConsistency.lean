/-
  BST Lean Test 1: Can Lean prove its own consistency?

  Gödel's Second Incompleteness Theorem says no sufficiently expressive
  consistent formal system can prove its own consistency.

  Lean's logic (Calculus of Inductive Constructions) is such a system.
  If BST's Theorem 1 is correct, this should be impossible.
-/

-- Define what "consistency" means: there is no proposition P
-- such that both P and ¬P are provable.
def Consistent : Prop :=
  ∀ (P : Prop), ¬(P ∧ ¬P)

-- Attempt 1: Try to prove Lean is consistent
-- This is trivially provable because it's just the law of non-contradiction
-- which is a LOGICAL tautology, not a META-theoretic consistency proof.
theorem lean_consistent_attempt1 : Consistent := by
  intro P ⟨hp, hnp⟩
  exact hnp hp

-- But this isn't what Gödel means by "consistency."
-- The above proves ¬(P ∧ ¬P) for any P, which is just logic.
-- Gödel's consistency is: "This system does not derive False."

-- The REAL question: Can Lean prove that False is not derivable in Lean?
-- That would require Lean to prove: ¬(∃ (p : False), True)
-- But that's trivially true because False has no constructors.

-- The deeper question: Can Lean prove that its OWN AXIOMS don't lead to False?
-- This requires reasoning ABOUT Lean FROM WITHIN Lean.

-- Let's try to encode "Lean is consistent" as a statement IN Lean:
-- "There is no proof of False"
-- In Lean's type theory, if False were provable, we could construct a term of type False.

-- Attempt 2: State that False is not provable
-- This would need to quantify over all possible Lean proofs,
-- which requires encoding Lean's proof system within itself.

-- We CANNOT do this directly. We'd need:
-- 1. A representation of Lean's syntax within Lean
-- 2. A representation of Lean's type-checking rules within Lean
-- 3. A proof that no well-typed term has type False

-- This is exactly the Gödelian barrier: encoding the system within itself
-- to make meta-theoretic claims requires the system to transcend its own boundaries.

-- Attempt 3: Try to assert it as an axiom and see if Lean accepts self-reference
axiom lean_does_not_prove_false : ¬False

-- This is trivially true (False → False is provable), but it's NOT
-- the same as "Lean's axiom system is consistent."
-- It says "False implies anything" not "Lean cannot derive False."

-- The statement we ACTUALLY need but CANNOT express:
-- "For all possible Lean proof terms t, the type of t ≠ False"
-- This requires quantifying over Lean's own proof space FROM WITHIN Lean.

-- CONCLUSION: Lean cannot express its own consistency as a theorem about
-- its own proof system without encoding that proof system as data within itself,
-- which would require a meta-Lean that is itself subject to the same limitation.

#check @Consistent  -- Prop
