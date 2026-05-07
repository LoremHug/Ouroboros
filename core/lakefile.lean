import Lake
open Lake DSL

package core where
  -- kernel-only: no mathlib, no classical extensions
  leanOptions := #[]

lean_lib Core where
  -- single root module Core.lean
  roots := #[`Core]
