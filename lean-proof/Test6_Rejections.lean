/-
  BST Lean Test 6: Lean's Rejections

  These are the constructs BST predicts a formal system CANNOT allow.
  Lean rejects each one. The error messages are the evidence.
-/

-- REJECTION 1: Self-referential proposition (Liar Paradox)
def liar : Prop := ¬liar

-- REJECTION 2: Type in itself (Girard's Paradox)
#check (Type 0 : Type 0)

-- REJECTION 3: Self-referential inductive type
inductive Loop where
  | mk : ¬Loop → Loop
