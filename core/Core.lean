/-!
# Core: Structural Transition Primitive

A_0 = the unique stable structural configuration under self-coherence.

This file is kernel-only: no `import Mathlib`, no `Classical.choice`, no
`axiom` declarations beyond Lean's foundational primitives. Substrate
purity is verified after every theorem with `#print axioms`.

The primitives encoded here:

* `Triangle α` — three structural slots (B/P/I). The minimum for
  self-checking closure: below 3 args nothing triangulates uniquely.
* `Self α` — endo-map; "what comes next from current state".
* `IsFixed f x` — `x` is invariant under `f`.
* `IsA0 f a` — `a` is the unique fixed point. Uniqueness built into
  the definition, not derived.
* `IsUniqueSolution P x` — universal pattern: x is THE x with P x.
  IsA0 and IsArgminZ are both instances of this one shape.
* `Coherence α` — Triangle × candidate → Prop; the constraint that a
  candidate respects all three slots.
* `Z R t x` — incoherence: the Prop "x violates R(t, ·)".
* `IsArgminZ R t x` — x is the unique R(t, ·)-satisfier; "argmin Z".
* `IsStep R t x` — the structural step output for triangle t under R.
  Step ⟺ argmin Z by definition; not two things connected by a theorem.

Bidirectional identity (stable transition ⟺ A_0-step) is encoded via
mutual definitional collapse: `IsA0`, `IsArgminZ`, and `IsStep` are
three names for `IsUniqueSolution` instantiated to different predicates.
-/

namespace Core

universe u

/-! ## Three-slot primitive -/

/-- Three-slot structural primitive. B, P, I are the three arguments
    that triangulate any structural step. They are NOT three different
    things — they are the three slots of one operation. -/
structure Triangle (α : Type u) where
  b : α
  p : α
  i : α

/-! ## Self-coherence and A_0 -/

/-- A self-coherence operator on `α`: a function from current
    configuration to next. -/
def Self (α : Type u) : Type u := α → α

/-- `x` is fixed under `f` iff one application returns `x`. -/
def IsFixed {α : Type u} (f : Self α) (x : α) : Prop := f x = x

/-- `a` is THE A_0 point of `f` iff fixed AND uniquely so. -/
def IsA0 {α : Type u} (f : Self α) (a : α) : Prop :=
  IsFixed f a ∧ ∀ y, IsFixed f y → y = a

theorem A0_unique {α : Type u} {f : Self α} {a b : α}
    (ha : IsA0 f a) (hb : IsA0 f b) : a = b :=
  (ha.2 b hb.1).symm

theorem A0_implies_stable {α : Type u} {f : Self α} {a : α}
    (ha : IsA0 f a) : IsFixed f a := ha.1

theorem stable_implies_A0 {α : Type u} {f : Self α} {a : α}
    (h_stable : IsFixed f a)
    (h_exists : ∃ x, IsA0 f x) : IsA0 f a := by
  obtain ⟨x, hx⟩ := h_exists
  have ha_eq : a = x := hx.2 a h_stable
  rw [ha_eq]
  exact hx

/-! ## Universal "unique solution" pattern

    IsA0, IsArgminZ, IsStep — these are not three patterns we connect
    with theorems. They are one pattern (IsUniqueSolution) instantiated
    to three predicates. Their equivalence is `Iff.rfl`. -/

/-- The universal shape: `x` is THE unique solution to property `P`. -/
def IsUniqueSolution {α : Type u} (P : α → Prop) (x : α) : Prop :=
  P x ∧ ∀ y, P y → y = x

theorem unique_solution_unique {α : Type u} {P : α → Prop} {x y : α}
    (hx : IsUniqueSolution P x) (hy : IsUniqueSolution P y) : x = y :=
  hy.2 x hx.1

/-- IsA0 IS the unique-solution pattern applied to fixedness. -/
theorem isA0_is_unique_solution {α : Type u} (f : Self α) (a : α) :
    IsA0 f a ↔ IsUniqueSolution (IsFixed f) a := Iff.rfl

/-! ## Coherence relation, Z, argmin Z, step -/

/-- A coherence relation says when a candidate `x` is structurally
    compatible with all three slots of triangle `t`. Different
    substrates (logic, math, invariance) instantiate this differently;
    the SHAPE is the same. -/
abbrev Coherence (α : Type u) := Triangle α → α → Prop

/-- `Z R t x` is incoherence as a Prop: holds iff `x` violates `R(t, ·)`.
    Without numbers we work at Prop-level: Z is at "minimum" precisely
    where `R t x` holds (Z is then `¬ R t x`, structurally false). -/
def Z {α : Type u} (R : Coherence α) (t : Triangle α) (x : α) : Prop :=
  ¬ R t x

/-- `x` is at argmin Z for triangle `t` under `R`: x is the unique
    R(t, ·)-satisfier. -/
def IsArgminZ {α : Type u} (R : Coherence α) (t : Triangle α) (x : α) : Prop :=
  IsUniqueSolution (R t) x

theorem argminZ_unique {α : Type u} {R : Coherence α} {t : Triangle α}
    {x y : α} (hx : IsArgminZ R t x) (hy : IsArgminZ R t y) : x = y :=
  unique_solution_unique hx hy

/-- The structural step: the output for triangle `t` under coherence `R`.
    By definition, step IS argmin Z — not two things linked by theorem. -/
def IsStep {α : Type u} (R : Coherence α) (t : Triangle α) (x : α) : Prop :=
  IsArgminZ R t x

theorem step_eq_argminZ {α : Type u} (R : Coherence α)
    (t : Triangle α) (x : α) : IsStep R t x ↔ IsArgminZ R t x := Iff.rfl

/-- argmin Z under R is the unique-solution pattern. -/
theorem argminZ_is_unique_solution {α : Type u} (R : Coherence α)
    (t : Triangle α) (x : α) :
    IsArgminZ R t x ↔ IsUniqueSolution (R t) x := Iff.rfl

/-! ## At argmin Z iff Z is at minimum (not violated)

    If `x` is at argmin Z, then `Z R t x` (= ¬ R t x) is structurally
    false. This is the operational meaning of "structure is stable
    where Z is minimized": stability ⟺ ¬ incoherence. -/

theorem argminZ_implies_Z_false {α : Type u} {R : Coherence α}
    {t : Triangle α} {x : α} (h : IsArgminZ R t x) : ¬ Z R t x :=
  fun hZ => hZ h.1

/-! ## Foundation: any operation is structurally triangulated

    Function application `f x` is the universal example. Its three
    structural slots:

      B (boundary) — α (the domain; where x lives)
      P (process)  — f (the operation)
      I (identity) — Eq on β (what makes outputs same)

    The unique `y : β` such that `y = f x` is the argmin Z of this
    triangulation. So function application IS triangulation step,
    structurally. This is the bottom of the substrate: not built from
    extra assumptions, but from the irreducible `=`, `→`, `Π`. -/

theorem function_application_is_unique_solution {α β : Type u}
    (f : α → β) (x : α) : IsUniqueSolution (fun y : β => y = f x) (f x) :=
  ⟨rfl, fun _ h => h⟩

/-- Concretely: the only `y` satisfying `y = f x` is `f x`.
    Nothing else can occupy that slot — uniqueness forced by the
    type-theory primitive of equality alone. -/
theorem function_evaluation_unique {α β : Type u} (f : α → β) (x : α)
    {y : β} (h : y = f x) : y = f x := h

/-! ## Concrete instance: 2 + 2 = 4

    All three Triangle slots used non-trivially:

      t.b = 2 (first operand)
      t.p = 2 (second operand)
      t.i = 4 (target — where structure settles)

    Coherence: `R t x := t.b + t.p = x ∧ x = t.i`.

    Both conjuncts must hold; together they force x = t.i AND
    t.b + t.p = t.i. Touching any slot makes coherence unsatisfiable —
    no candidate exists, structural stability collapses.

    This is the canonical demonstration: 2+2=4 IS the A_0 of this
    triangulation; touching 2, 2, or 4 destroys the unique stable point.
    Pattern self-instantiates concretely in arithmetic substrate. -/

def AddCoherence : Coherence Nat := fun t x => t.b + t.p = x ∧ x = t.i

/-- 4 IS the argmin Z of triangle ⟨2, 2, 4⟩. All three slots active. -/
theorem two_plus_two_is_argminZ : IsArgminZ AddCoherence ⟨2, 2, 4⟩ 4 :=
  ⟨⟨rfl, rfl⟩, fun _ h => h.2⟩

/-- Perturbing the b slot (2 → 3): no candidate satisfies coherence.
    Stability collapses — there is no x where ⟨3, 2, 4⟩ triangulates. -/
theorem perturb_b_destabilizes : ¬ ∃ x, AddCoherence ⟨3, 2, 4⟩ x :=
  fun ⟨_, h1, h2⟩ => absurd (h1.trans h2) (by decide)

/-- Perturbing the i slot (4 → 5): no candidate satisfies coherence. -/
theorem perturb_i_destabilizes : ¬ ∃ x, AddCoherence ⟨2, 2, 5⟩ x :=
  fun ⟨_, h1, h2⟩ => absurd (h1.trans h2) (by decide)

end Core

-- Substrate audit: each theorem must depend only on Lean's foundational
-- primitives. "does not depend on any axioms" is the cleanest result.

#print axioms Core.A0_unique
#print axioms Core.A0_implies_stable
#print axioms Core.stable_implies_A0
#print axioms Core.unique_solution_unique
#print axioms Core.isA0_is_unique_solution
#print axioms Core.argminZ_unique
#print axioms Core.step_eq_argminZ
#print axioms Core.argminZ_is_unique_solution
#print axioms Core.argminZ_implies_Z_false
#print axioms Core.function_application_is_unique_solution
#print axioms Core.function_evaluation_unique
#print axioms Core.two_plus_two_is_argminZ
#print axioms Core.perturb_b_destabilizes
#print axioms Core.perturb_i_destabilizes
