/-
  BST Lean Test 4: Direct diagonal construction

  Can Lean handle self-referential propositions that reference
  their own provability? This is the diagonal test from Definition 2.1.
-/

-- The Liar Paradox in Lean:
-- "This statement is false" — can we express it?

-- Attempt: direct self-reference
-- def liar : Prop := ¬liar
-- ERROR: this would be rejected by Lean's positivity checker.
-- Lean prevents direct self-referential definitions precisely BECAUSE
-- they lead to inconsistency. This is a DESIGNED constraint.

-- The fact that Lean must PREVENT self-reference to remain consistent
-- is itself evidence for BST: the system's constraints (positivity checker)
-- exist to prevent the system from destroying itself via self-reference.
-- Those constraints were imposed EXTERNALLY (by the language designers).

-- Attempt: Curry's paradox
-- If we could define: curry : curry → False
-- Then: (fun h => h h) (fun h => h h) : False
-- Lean's type system prevents this via the occurs check.

-- What CAN Lean express about self-reference?

-- Gödel sentence (informal): "This statement is not provable in Lean"
-- To formalize this, we'd need a provability predicate Provable : Prop → Prop
-- such that Provable P ↔ (there exists a Lean proof of P)

-- Can we define Provable inside Lean?
-- Not faithfully. We'd need to:
-- 1. Encode all Lean terms as data (Gödel numbering)
-- 2. Encode Lean's type checking algorithm
-- 3. Define Provable P := ∃ t, TypeChecks t P

-- Even if we did this, by Gödel's theorem:
-- The resulting Gödel sentence G (where G ↔ ¬Provable G)
-- would be true but unprovable in Lean (assuming consistency).

-- Lean would be UNABLE TO PROVE a true statement about itself.
-- That's the incompleteness theorem. That's BST Theorem 1.

-- Concrete demonstration: Lean's universe hierarchy
-- Lean has Type 0 : Type 1 : Type 2 : ...
-- Type n lives in Type (n+1), never in Type n.
-- This PREVENTS Type : Type (which causes Girard's paradox).

-- The hierarchy is EXTERNALLY imposed to prevent inconsistency.
-- Lean cannot justify why the hierarchy exists from within.
-- It can only operate within it.

#check (Nat : Type 0)    -- Nat lives in Type 0
#check (Type 0 : Type 1) -- Type 0 lives in Type 1
-- #check (Type 0 : Type 0)  -- REJECTED: would break consistency
-- Lean's own consistency depends on this hierarchy,
-- which Lean cannot prove is necessary from within.

-- RESULT: Lean's mechanisms for maintaining consistency
-- (positivity checker, universe hierarchy, occurs check)
-- are all externally imposed constraints that Lean cannot
-- justify, modify, or verify from within itself.
-- This is BST Axiom 2 made concrete in a formal system.
