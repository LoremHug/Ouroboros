/-!
# Core: Structural Transition Primitive

A_0 = the unique stable structural configuration under self-coherence.

This file is kernel-only: no `import Mathlib`, no `Classical.choice`, no
`axiom` declarations beyond Lean's foundational primitives. Substrate
purity is verified after every theorem with `#print axioms`.

The primitives encoded here:

* `Triangle α` — three structural slots (B/P/I). The minimum for
  self-checking closure: below 3 args nothing triangulates uniquely.
* `Self α` — endo-map; structurally, "what comes next from current state".
* `IsFixed f x` — `x` is invariant under `f` (one structural step
  preserves it).
* `IsA0 f a` — `a` is the unique fixed point of `f`. Uniqueness is
  built into the definition, not a separate theorem.

The bidirectional identity (stable transition ⟺ A_0-step) is encoded
via mutual definitional collapse: `IsA0` is `IsFixed` plus uniqueness,
so any stable point is by construction the A_0 point — there is no
"alternative stable point" as a category.
-/

namespace Core

universe u

/-- Three-slot structural primitive. B, P, I are the three arguments that
    triangulate any structural step. They are NOT three different things
    — they are the three slots of one operation. -/
structure Triangle (α : Type u) where
  b : α
  p : α
  i : α

/-- A self-coherence operator on `α`: a function from current
    configuration to next. No assumption that it is total / continuous /
    well-ordered — just an endo-map. -/
def Self (α : Type u) : Type u := α → α

/-- `x` is fixed under `f` iff one application of `f` returns `x`. -/
def IsFixed {α : Type u} (f : Self α) (x : α) : Prop := f x = x

/-- `a` is THE A_0 point of `f` iff:
    (1) `a` is fixed, and
    (2) any other fixed point coincides with `a`.

    Uniqueness is part of the definition — not derived afterward. The
    statement "alternative stable points exist" is not false but
    structurally vacuous: by this definition, anything fixed = `a`. -/
def IsA0 {α : Type u} (f : Self α) (a : α) : Prop :=
  IsFixed f a ∧ ∀ y, IsFixed f y → y = a

/-- Direct corollary: any two A_0 points of the same operator coincide. -/
theorem A0_unique {α : Type u} {f : Self α} {a b : α}
    (ha : IsA0 f a) (hb : IsA0 f b) : a = b :=
  (ha.2 b hb.1).symm

/-- Bidirectional identity (forward): if `a` is A_0, it is fixed.
    Trivially built into the definition. -/
theorem A0_implies_stable {α : Type u} {f : Self α} {a : α}
    (ha : IsA0 f a) : IsFixed f a :=
  ha.1

/-- Bidirectional identity (inverse): if `a` is fixed AND `f` admits an
    A_0 point, then `a` IS that A_0 point. There is no "other stability"
    to speak of — any stable point coincides with A_0 by construction. -/
theorem stable_implies_A0 {α : Type u} {f : Self α} {a : α}
    (h_stable : IsFixed f a)
    (h_exists : ∃ x, IsA0 f x) : IsA0 f a := by
  obtain ⟨x, hx⟩ := h_exists
  have ha_eq : a = x := hx.2 a h_stable
  rw [ha_eq]
  exact hx

end Core

-- Axiom audit: each theorem must depend only on Lean's foundational
-- primitives. Anything beyond signals an extra entity in our sense.
#print axioms Core.A0_unique
#print axioms Core.A0_implies_stable
#print axioms Core.stable_implies_A0
