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

/-- Perturbing the p slot (2 → 3): no candidate satisfies coherence. -/
theorem perturb_p_destabilizes : ¬ ∃ x, AddCoherence ⟨2, 3, 4⟩ x :=
  fun ⟨_, h1, h2⟩ => absurd (h1.trans h2) (by decide)

/-- Perturbing the i slot (4 → 5): no candidate satisfies coherence. -/
theorem perturb_i_destabilizes : ¬ ∃ x, AddCoherence ⟨2, 2, 5⟩ x :=
  fun ⟨_, h1, h2⟩ => absurd (h1.trans h2) (by decide)

/-! ## Tautology vs structural transition

    4 = 4 is structurally stable but NOT a structural transition —
    it is the post-transition state, the fixed point already reached.
    No movement is performed; what remains is the bare identity of
    being-at-the-fixed-point.

    Distinction made formal:

      transition  — b, p materially constrain the unique i. Touching
                    them destabilizes (see perturb_b/i_destabilizes).
      tautology   — b, p play no constraining role; argmin Z determined
                    by i alone.

    Both are stable. Only one represents structural movement. The
    framework's "argmin Z transition" is the transition case; tautology
    is the achieved point that transition arrives at. -/

/-- Tautological coherence: x is at argmin Z iff x equals the i-slot.
    b and p slots are unused — this is the bare-identity case. -/
def TautCoherence : Coherence Nat := fun t x => x = t.i

/-- 4 = 4 holds tautologically. Structurally stable, but no transition
    has been performed — we are already at the fixed point. -/
theorem four_eq_four_tautological : IsArgminZ TautCoherence ⟨4, 4, 4⟩ 4 :=
  ⟨rfl, fun _ h => h⟩

/-- Tautology is unconstrained in b, p: any triangulation with i = 4
    yields 4 as argmin Z. Contrast with `AddCoherence` where b, p must
    be specific (perturb_b_destabilizes). This is the formal mark of
    "transition already completed": the b/p slots have no work to do. -/
theorem tautology_unconstrained : ∀ b p, IsArgminZ TautCoherence ⟨b, p, 4⟩ 4 :=
  fun _ _ => ⟨rfl, fun _ h => h⟩

/-! ## Modus ponens — logic substrate, same pattern

    Given premise `p` of type α and rule `α → β`, the conclusion
    `rule p : β` is the unique element of β satisfying `y = rule p`.
    Three structural slots:

      B (boundary) — α (premise type; where input lives)
      P (process)  — rule : α → β (the inference operation)
      I (identity) — β (conclusion type; with its equality)

    Modus ponens IS function application — formally identical to
    `function_application_is_unique_solution`, with slots renamed to
    logic-substrate vocabulary (premise / rule / conclusion instead of
    x / f / y). The same `IsUniqueSolution` pattern instantiates here
    as in arithmetic (2 + 2 = 4): different substrates, one structural
    shape. Logic and math share one A_0 pattern.

    Note: at the Prop level (where premise/conclusion are proofs), the
    Type-level pattern still applies — but uniqueness of the conclusion
    proof additionally follows from proof irrelevance built into Prop.
    The structural triangulation argument here works at the Type
    level, capturing logic-as-tool independent of Prop-specific
    proof-irrelevance. -/

theorem modus_ponens_is_unique_solution {α β : Type u}
    (premise : α) (rule : α → β) :
    IsUniqueSolution (fun conclusion : β => conclusion = rule premise) (rule premise) :=
  ⟨rfl, fun _ h => h⟩

/-! ## Unified invariant: substrate-bounded reachability

    `stable_implies_A0` already encodes the universal pattern:

        h_stable (substrate-internal) + h_exists (meta) → IsA0

    The conditional `h_exists` is the formal mark of K(O) < K(F):
    substrate-internal proof of A_0 existence requires meta-resource.
    This section makes the substrate-bounding concrete in two
    structural facts, both instances of the same invariant differing
    only in which substrate-property bounds h_exists.

    1. **Self-encoding** (Gödel/Cantor/Tarski/Halting) — Lawvere
       fixed-point lemma. Self-referential substrates with diagonal
       structure have fixed points for every endomap; conversely,
       fixed-point-free maps obstruct surjective self-encoding.

    2. **Irreversibility** (Landauer) — many-to-one maps fail
       `IsUniqueSolution` for reversal. No internal recovery of
       inputs from outputs; information cost forced.

    3. **L(3,1) spatial substrate** — minimum non-trivial 3-fold
       cyclic structure (π_1 = Z/3Z). Z/2 fails 3-arg minimum;
       Z/p, p≥4, factors through Z/3. Below: full topological
       formalization needs 3-mfd library (beyond pilot scope);
       structural form encoded as ThreePeriod with non-trivial action.

    All three: substrate-instances of one Core pattern. Internal
    h_exists bounded; meta-h_exists holds. The conditional in
    `stable_implies_A0` captures this without further structure. -/

/-! ### Lawvere fixed-point — Gödel/Cantor pattern

    The structural core of self-reference. Captures Gödel
    incompleteness, Cantor diagonal, Tarski undefinability,
    Russell's paradox, halting problem — all corollaries of one
    fact: self-application forces fixed points. -/

/-- Lawvere (1969): if `φ : A → (A → B)` is point-surjective
    (every `g : A → B` is `φ a` for some `a`), then every endomap
    `f : B → B` has a fixed point. -/
theorem lawvere_fixed_point {A : Type u} {B : Type v} (φ : A → (A → B))
    (surj : ∀ g : A → B, ∃ a : A, φ a = g) (f : B → B) :
    ∃ b : B, f b = b := by
  obtain ⟨a₀, h⟩ := surj (fun a => f (φ a a))
  exact ⟨φ a₀ a₀, (congrFun h a₀).symm⟩

/-- Cantor diagonal as Lawvere corollary: no surjection
    `X → (X → Bool)`. `Bool.not` has no fixed point; by Lawvere's
    contrapositive, surjectivity is structurally blocked. -/
theorem cantor_diagonal {X : Type u} :
    ¬ ∃ φ : X → (X → Bool), ∀ g : X → Bool, ∃ a : X, φ a = g := by
  rintro ⟨φ, surj⟩
  obtain ⟨b, hb⟩ := lawvere_fixed_point φ surj Bool.not
  have not_self : Bool.not b ≠ b := fun h => by cases b <;> cases h
  exact not_self hb

/-- Gödel pattern abstractly: any substrate that can encode its own
    statements but contains a fixed-point-free transformation cannot
    surjectively self-encode. K(O) < K(F) structurally forced.

    Specialised: F's provability cannot represent `not_provable`
    surjectively, because `not_provable` would need a fixed point
    (which IS the Gödel sentence — true in meta, unprovable in F). -/
theorem self_encoding_bounded {A : Type u} {B : Type v}
    (f : B → B) (no_fix : ¬ ∃ b, f b = b) :
    ¬ ∃ φ : A → (A → B), ∀ g : A → B, ∃ a, φ a = g :=
  fun ⟨φ, surj⟩ => no_fix (lawvere_fixed_point φ surj f)

/-- Connection to Core: Lawvere produces existence of fixed points;
    `IsA0` adds uniqueness. Together: when `f` has a unique fixed
    point and Lawvere conditions hold, that point IS A_0. -/
theorem lawvere_gives_A0 {A : Type u} {B : Type v}
    (φ : A → (A → B)) (surj : ∀ g, ∃ a, φ a = g) (f : B → B)
    (uniq : ∀ b₁ b₂ : B, f b₁ = b₁ → f b₂ = b₂ → b₁ = b₂) :
    ∃ b, IsA0 f b := by
  obtain ⟨b, hb⟩ := lawvere_fixed_point φ surj f
  exact ⟨b, hb, fun y hy => uniq y b hy hb⟩

/-! ### Landauer pattern — irreversibility as no-unique-inverse

    Many-to-one maps lack left inverses: reversal-IsUniqueSolution
    has no internal answer. This is the structural core of Landauer:
    information lost in n-to-1 collapse cannot be recovered without
    external (substrate-meta) resource — heat dissipation as the
    thermodynamic substrate-projection of this fact. -/

/-- Many-to-one: at least two distinct inputs share an output. -/
def ManyToOne {α β : Type u} (f : α → β) : Prop :=
  ∃ a₁ a₂ : α, a₁ ≠ a₂ ∧ f a₁ = f a₂

/-- Many-to-one ⟹ no left inverse exists. The "reversal" function
    cannot uniquely recover input from output. -/
theorem many_to_one_no_left_inverse {α β : Type u} (f : α → β)
    (h : ManyToOne f) : ¬ ∃ g : β → α, ∀ a : α, g (f a) = a := by
  rintro ⟨g, hg⟩
  obtain ⟨a₁, a₂, hne, heq⟩ := h
  apply hne
  have step1 : a₁ = g (f a₁) := (hg a₁).symm
  have step2 : g (f a₁) = g (f a₂) := congrArg g heq
  have step3 : g (f a₂) = a₂ := hg a₂
  exact step1.trans (step2.trans step3)

/-- Connection to Core: the reversal-IsUniqueSolution at output `f a₁`
    has no answer — neither `a₁` nor `a₂` is uniquely the preimage,
    so the unique-solution pattern fails internally. This bounds
    h_exists for the reversal substrate. -/
theorem many_to_one_fails_unique_solution {α β : Type u} (f : α → β)
    (h : ManyToOne f) :
    ∃ b : β, ¬ ∃ a, IsUniqueSolution (fun a' : α => f a' = b) a := by
  obtain ⟨a₁, a₂, hne, heq⟩ := h
  refine ⟨f a₁, ?_⟩
  rintro ⟨a, ha, huniq⟩
  exact hne ((huniq a₁ rfl).trans (huniq a₂ heq.symm).symm)

/-! ### L(3,1) pattern — minimum non-trivial 3-fold cyclic

    Spatial substrate manifestation. L(3,1) topologically:
    π_1 = Z/3Z. Below: Z/2 (RP³) fails 3-arg minimum. Above: Z/p
    (L(p,1), p≥4) factorizes through Z/3.

    Encoded structurally as ThreePeriod: a type with endomap whose
    third iterate is identity AND first iterate is non-trivial.
    Captures the operational essence of 3-fold cyclic without full
    topology library. -/

/-- A type carries 3-period non-trivial cyclic structure if it has
    an endomap whose third iterate is identity, and which is itself
    non-trivial (not the identity map). -/
structure ThreePeriod (α : Type u) where
  cycle : α → α
  period : ∀ x, cycle (cycle (cycle x)) = x
  nontrivial : ∃ x, cycle x ≠ x

/-- The minimum carrier for ThreePeriod: Fin 3 with cyclic shift.
    Bool (size 2) cannot carry it; Fin 3 is the structural minimum. -/
def fin3Cycle : Fin 3 → Fin 3
  | ⟨0, _⟩ => ⟨1, by decide⟩
  | ⟨1, _⟩ => ⟨2, by decide⟩
  | ⟨2, _⟩ => ⟨0, by decide⟩

instance : ThreePeriod (Fin 3) where
  cycle := fin3Cycle
  period := fun x => match x with
    | ⟨0, _⟩ => rfl
    | ⟨1, _⟩ => rfl
    | ⟨2, _⟩ => rfl
  nontrivial := ⟨⟨0, by decide⟩, by decide⟩

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
#print axioms Core.perturb_p_destabilizes
#print axioms Core.perturb_i_destabilizes
#print axioms Core.four_eq_four_tautological
#print axioms Core.tautology_unconstrained
#print axioms Core.modus_ponens_is_unique_solution
#print axioms Core.lawvere_fixed_point
#print axioms Core.cantor_diagonal
#print axioms Core.self_encoding_bounded
#print axioms Core.lawvere_gives_A0
#print axioms Core.many_to_one_no_left_inverse
#print axioms Core.many_to_one_fails_unique_solution
