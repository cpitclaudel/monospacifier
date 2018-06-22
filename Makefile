DEJAVU=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf
UBUNTU=/usr/share/fonts/truetype/ubuntu-font-family/UbuntuMono-R.ttf
INCONSOLATA=/home/clement/.fonts/monospace/Inconsolata.otf
INCONSOLATA_LGC=/home/clement/.fonts/monospace/inconsolata-lgc/Inconsolata LGC for Powerline.ttf
TERMINUS=/home/clement/.fonts/monospace/terminus/TerminusTTF-4.39.ttf
MONONOKI=/home/clement/.fonts/monospace/mononoki/mononoki-Regular.ttf
LIBERATION=/home/clement/.fonts/monospace/liberation/LiberationMono-Regular.ttf

XITS=/home/clement/.fonts/maths/xits-math.otf
XITS_BOLD=/home/clement/.fonts/maths/xits-mathbold.otf
STIX=/home/clement/.fonts/maths/STIXMath-Regular.otf
ASANA=/usr/share/fonts/truetype/asana-math/Asana-Math.otf
SYMBOLA=/home/clement/.fonts/maths/Symbola_hint.ttf
LATINMODERN=/home/clement/.fonts/maths/latinmodern-math.otf
TEXGYRESCHOLA=/home/clement/.fonts/maths/texgyreschola-math.otf
FREESERIF=/usr/share/fonts/truetype/freefont/FreeSerif.ttf

ttf: monospacifier.py
	rm -f ./fonts/*.ttf
	./monospacifier.py \
		--references ./sources/references/* \
		--inputs ./sources/inputs/* \
		--rename Asana Asanb \
        --rename STIX STIY \
		--save-to ./fonts --copy-metrics # 2>&1 # --merge

prepare:
	echo "References"
	rm ./sources/references/*
	cp "$(UBUNTU)"					./sources/references/UbuntuMono.ttf
	cp "$(DEJAVU)"					./sources/references/DejaVuSansMono.ttf
	cp "$(INCONSOLATA)"				./sources/references/Inconsolata.ttf
	cp "$(INCONSOLATA_LGC)"			./sources/references/InconsolataLGCForPowerline.ttf
	cp "$(TERMINUS)"				./sources/references/Terminus.ttf
	cp "$(MONONOKI)"				./sources/references/Mononoki.ttf
	cp "$(LIBERATION)"				./sources/references/Liberation.ttf
	echo "Inputs"
	rm								./sources/inputs/*
	cp "$(XITS)"					./sources/inputs/XITSMath.otf
	cp "$(XITS_BOLD)"				./sources/inputs/XITSMath-B.otf
	cp "$(STIX)"					./sources/inputs/STIXMath.otf
	cp "$(ASANA)"					./sources/inputs/AsanaMath.otf
	cp "$(SYMBOLA)"					./sources/inputs/Symbola.ttf
	cp "$(LATINMODERN)"				./sources/inputs/LatinModernMath.otf
	cp "$(TEXGYRESCHOLA)"			./sources/inputs/TexGyreScholaMath.otf
	cp "$(FREESERIF)"				./sources/inputs/FreeSerif.ttf

install:
	rm ~/.fonts/monospacified/*.ttf
	cp fonts/*.ttf ~/.fonts/monospacified/
	fc-cache

check-sources:
	./coverage.py --glyphs 𝔹 ℝ ℙ ℕ × ≠ ≥ ≤ ± ¬ ∨ ∧ ∃ ∀ λ ⬳ ⟿ ⟸ ⟹ ⇒ ⟷ ↔ ⟵ ← ⟶ → ⊥ ⊤ ⊢ 𝓟 𝓝 ⧺ --fonts ./sources/inputs/*

check-output:
	./coverage.py --glyphs 𝔹 ℝ ℙ ℕ × ≠ ≥ ≤ ± ¬ ∨ ∧ ∃ ∀ λ ⬳ ⟿ ⟸ ⟹ ⇒ ⟷ ↔ ⟵ ← ⟶ → ⊥ ⊤ ⊢ 𝓟 𝓝 ⧺ --fonts ./fonts/*
