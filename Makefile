DEJAVU=/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansMono.ttf
CONSOLAS=/home/clement/.fonts/Microsoft/Consolas-Fixed.ttf

XITS=/home/clement/.fonts/maths/xits-math.otf
STIX=/home/clement/.fonts/maths/STIXMath-Regular.otf
ASANA=/usr/share/fonts/truetype/asana-math/Asana-Math.otf
SYMBOLA=/usr/share/fonts/truetype/ttf-ancient-scripts/Symbola605.ttf
LATINMODERN=/home/clement/.fonts/maths/latinmodern-math.otf
TEXGYRESCHOLA=/home/clement/.fonts/maths/texgyreschola-math.otf

# DEJAVUSANS=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
# DEJAVUSANSCONDENSED=/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf
# DEJAVUSERIF=/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf
# DEJAVUSERIFCONDENSED=/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerifCondensed.ttf
FREESERIF=/usr/share/fonts/truetype/freefont/FreeSerif.ttf

ttf: monospacifier.py
	rm -f ./fonts/*.ttf
	./monospacifier.py \
		--references ./sources/references/* \
		--inputs ./sources/inputs/* \
		--save-to ./fonts --copy-metrics # 2>&1 # --merge

prepare:
	echo "References"
	rm ./sources/references/*
	cp $(CONSOLAS)				./sources/references/Consolas.ttf
	cp $(DEJAVU)				./sources/references/DejaVuSansMono.ttf
	echo "Inputs"
	rm ./sources/inputs/*
	cp $(XITS)					./sources/inputs/XITSMath.otf
	cp $(STIX)					./sources/inputs/STIXMath.otf
	cp $(ASANA)					./sources/inputs/AsanaMath.otf
	cp $(SYMBOLA)				./sources/inputs/Symbola.ttf
	cp $(LATINMODERN)			./sources/inputs/LatinModernMath.otf
	cp $(TEXGYRESCHOLA)			./sources/inputs/TexGyreScholaMath.otf
	cp $(FREESERIF)				./sources/inputs/FreeSerif.ttf
#   cp $(DEJAVUSANS)			./sources/inputs/DejaVuSans.ttf
#   cp $(DEJAVUSANSCONDENSED)	./sources/inputs/DejaVuSansCondensed.ttf
#   cp $(DEJAVUSERIF)			./sources/inputs/DejaVuSerif.ttf
#   cp $(DEJAVUSERIFCONDENSED)	./sources/inputs/DejaVuSerifCondensed.ttf

install:
	rm ~/.fonts/monospacified/*.ttf
	cp fonts/*.ttf ~/.fonts/monospacified/
	fc-cache

check-sources:
	./coverage.py --glyphs 𝔹 ℝ ℙ ℕ × ≠ ≥ ≤ ± ¬ ∨ ∧ ∃ ∀ λ ⬳ ⟿ ⟸ ⟹ ⇒ ⟷ ↔ ⟵ ← ⟶ → ⊥ ⊤ ⊢ 𝓟 𝓝 ⧺ --fonts ./sources/inputs/*

check-output:
	./coverage.py --glyphs 𝔹 ℝ ℙ ℕ × ≠ ≥ ≤ ± ¬ ∨ ∧ ∃ ∀ λ ⬳ ⟿ ⟸ ⟹ ⇒ ⟷ ↔ ⟵ ← ⟶ → ⊥ ⊤ ⊢ 𝓟 𝓝 ⧺ --fonts ./fonts/*
