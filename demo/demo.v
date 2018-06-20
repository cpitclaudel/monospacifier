 λ (n m: ℕ) ⇒
   ∀ p, (p ≠ n → p ≥ m → ⊤ ∨ ⊥) ∨
        (p ⫺ n ⟿ p ≲ n → ⊥)).

 match goal with
 | [ H: False ⊢ _ ]      ⇒ exists x; assumption
 | [ H: _ ∧ _ ⊢ _ ]  ⇒ destruct H
 end.

 abcde  abcde  abcde  abcde
 a ∈ e  a ∨ e  a ⬾ e  a ∘ e
 abcde  abcde  abcde  abcde

 A B C (* regular text *)
 𝓐 𝓑 𝓒 (* bold calligraphy *)
 𝕬 𝕭 𝕮 (* bold fraktur *)
 ⬲ ⩈ ⥵ (* wide symbols *)

 (∧) ∷ 𝔹 ↦ 𝔹 ⟼ 𝔹 (* multi-line *)
                 (* comment *)

