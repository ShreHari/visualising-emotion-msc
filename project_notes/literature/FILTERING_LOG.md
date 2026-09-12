# Filtering Log — Relevance × Evidence Triage

Read **97 papers** (99 downloaded − 2 wrong-file downloads deleted). Kept **73** as core evidence across **8 themes**; the supervisor's original papers are retained in place. Excluded **24**, of which **23** are in `lit/_excluded/` (the 24th, the supervisor's Ragot paper, is kept in place). The bibliography (`references.bib`) holds 91 entries: the retained papers plus the method references.

Scoring: relevance 0–3 (0 off-topic → 3 directly on-path); evidence 0–3 (0 opinion → 3 strong empirical w/ evaluation). Keep = relevance≥2 AND evidence≥2, or a seminal foundation.

## Excluded (24)

| Paper | rel | ev | Reason |
|---|:--:|:--:|---|
| 3334480.3382892.pdf | 1 | 3 | Only tangential - it measures a general authorship bias against AI paintings (landscapes/portraits) with no connection to emotion, text, or image fidelity - so  (supervisor original — kept in place, not moved) |
| alex-nichol_2021_glide-towards-photorealistic- | 2 | 3 | Empirically strong and topically relevant, but redundant for this project: as the OpenAI diffusion precursor whose architecture and human-eval axes are subsumed  |
| armin-seyeditabari_2018_emotion-detection-in-t | 3 | 1 | Highly relevant as a field map for strand (a), but it is a narrative survey (evidence=1) that fails the empirical/resource bar and is not covered by the seminal  |
| cindy-peng_2025_exploring-opportunities-to-sup | 1 | 2 | Empirical interview/co-design study but off the core path (novice-artist ideation tooling, not emotion extraction or image fidelity); releases no dataset/metric  |
| daniel-hove-paludan_2025_towards-sustainable-c | 1 | 3 | Rigorous within-subjects study with quantitative and CSI human evaluation, but its subject is the energy sustainability of T2I generation, which is only loosely  |
| ewelina-gajewska_2025_the-lovelace-test-of-int | 2 | 2 | A DALL-E-2 Turing/Lovelace detection-plus-aesthetics preprint whose core construct (recognising AI art) is tangential to emotion faithfulness, and it is redunda  |
| hitsuwari_2024_personality-attitudes-ai-art.pd | 2 | 3 | Methodologically solid (pre-registered, N=201, validated scales) but its personality-moderator focus is off-target and it is redundant with Bellaiche and Millet  |
| jeba-rezwana_2022_designing-creative-ai-partne | 1 | 2 | Framework backed by coding 92 systems, but the interaction-design taxonomy is background framing tangential to emotion extraction/image fidelity and redundant w  |
| jingyuan-yang_2024_emoedit-evoking-emotions-th | 2 | 3 | Evidence is strong (CVPR-quality, EmoEditSet, user study, ablations) and it touches the emotion-image intersection, but it is an image-EDITING method whose reus  |
| jonas-oppenlaender_2022_the-creativity-of-text | 1 | 1 | Explicit conceptual position paper (tools=[], no data) offering only co-creation framing; excluded as an opinion/position piece with no reusable emotion or fide  |
| jonas-oppenlaender_2023_the-cultivated-practic | 1 | 1 | Conceptual book chapter with no empirical content, largely restating the author's 2022 position piece; loosely connected framing that is redundant for the core   |
| lisa-feldman-barrett_2017_the-theory-of-constr | 2 | 1 | Relevant as theoretical framing but a pure theory/position paper with no reusable data, taxonomy, or method (evidence 1), and it does not fit the narrow seminal  |
| liu_2024_prompt-journey-is-it-ai-or-is-it-me-C | 1 | 3 | Rigorous CHI study of prompting behaviour/UX, but off the emotion-fidelity path; co-creation theme excluded as tangential.  |
| lotus-team-see-paper_2025_lotus-at-semeval-202 | 2 | 2 | Topically relevant and empirical, but redundant and weak: a mid-ranked (36th) single-system paper whose LLM-explanation-augmentation idea is more rigorously sho  |
| philipp-moe-ner_2024_human-vs-ai-a-novel-bench | 1 | 3 | A strong AI-image-detection benchmark, but detecting generated images is a different construct from emotion faithfulness and off the dissertation's path; the pr  |
| quanzeng-you_2016_building-a-large-scale-datas | 2 | 3 | Empirical and on-topic, but redundant with the retained EmoSet: it is the same natural-photo Mikels 8-category paradigm (its FI dataset explicitly superseded by  |
| rameswar-panda_2018_contemplating-visual-emoti | 1 | 3 | Strong ECCV empirical work but tangential to this dissertation: it addresses training generalizable classifiers from weakly-labelled stock photos and dataset bi  |
| sebastian-deterding_2017_mixed-initiative-crea | 1 | 1 | CHI workshop proposal/position with no empirical content; the MICI framing does not qualify for the seminal exception (reserved for emotion-taxonomy, generative  |
| sebastian-hartwig_2024_a-survey-on-quality-met | 2 | 1 | On-topic as a metric taxonomy for strand (b), but it is a narrative-review preprint (no primary empirical contribution) whose content is already covered by the   |
| sicheng-zhao_2021_affective-image-content-anal | 2 | 1 | Relevant framing of the AICA field but a narrative survey (evidence=1) that is not a seminal-foundation exception type, and it is redundant with the other Zhao   |
| sicheng-zhao_2021_computational-emotion-analys | 2 | 1 | Relevant to strand (b) but a book-chapter narrative survey (evidence=1), not a seminal-foundation exception type, and substantially redundant with the other Zha  |
| thomas-roca_2025_how-good-are-humans-at-detect | 1 | 3 | Large-scale (287k evaluations) but centred on AI-vs-real detection rather than whether images convey the intended emotion; tangential to the faithfulness questi  |
| victor-nikhil-antony_2023_id-8-co-creating-vis | 1 | 3 | Methodologically solid (two user studies, SUS/MICSI) but only loosely connected: it is an HCI creativity-support/co-creation systems paper about multimodal stor  |
| youssef-mohamed_2024_no-culture-left-behind-ar | 2 | 3 | Empirically strong but largely redundant with the foundational 2022 ArtELingo, and its 28-language cross-lingual-transfer focus is tangential to an English-only  |

## Kept (73)

| Paper | role | rel | ev |
|---|---|:--:|:--:|
| minsuk-chang_2023_the-prompt-artists.pdf | context | 2 | 2 |
| NeurIPS-2023-geneval-an-object-focused-framework-f | dataset-resource | 2 | 3 |
| elvis-saravia_2018_carer-contextualized-affect-rep | dataset-resource | 2 | 3 |
| jingyuan-yang_2023_emoset-a-large-scale-visual-emo | dataset-resource | 2 | 3 |
| marchewka_2014_nencki-affective-picture-system-NAP | dataset-resource | 2 | 3 |
| panos-achlioptas_2021_artemis-affective-language-f | dataset-resource | 3 | 3 |
| ronak-kosti_2020_context-based-emotion-recognition | dataset-resource | 3 | 3 |
| saif-m-mohammad_2013_crowdsourcing-a-word-emotion- | dataset-resource | 3 | 3 |
| saif-m-mohammad_2018_obtaining-reliable-human-rati | dataset-resource | 3 | 3 |
| saif-m-mohammad_2018_semeval-2018-task-1-affect-in | dataset-resource | 2 | 3 |
| saif-m-mohammad_2025_nrc-vad-lexicon-v2-norms-for- | dataset-resource | 3 | 3 |
| shamsuddeen-hassan-m_2025_semeval-2025-task-11-bri | dataset-resource | 3 | 3 |
| sven-buechel_2017_emobank-studying-the-impact-of-a | dataset-resource | 3 | 3 |
| youssef-mohamed_2022_artelingo-a-million-emotion-a | dataset-resource | 3 | 3 |
| 2405.18510v1.pdf | emotion-image-intersection | 3 | 3 |
| jingyuan-yang_2024_emogen-emotional-image-content- | emotion-image-intersection | 3 | 3 |
| maneet-mehta_2024_generating-fearful-images-invest | emotion-image-intersection | 3 | 3 |
| qing-lin_2024_make-me-happier-evoking-emotions-thr | emotion-image-intersection | 3 | 3 |
| saif-m-mohammad_2018_wikiart-emotions-an-annotated | emotion-image-intersection | 3 | 3 |
| zibo-zhou_2025_analyzing-image-beyond-visual-aspec | emotion-image-intersection | 3 | 3 |
| 2404.01291v2.pdf | eval-metric | 3 | 3 |
| 2506.08480v1.pdf | eval-metric | 2 | 3 |
| Koo_Evaluating_Text-to-Image_and_Text-to-Video_Syn | eval-metric | 2 | 3 |
| Li_Evaluating_and_Improving_Compositional_Text-to- | eval-metric | 3 | 3 |
| alec-radford_2021_learning-transferable-visual-mod | eval-metric | 3 | 3 |
| chen_2018_reverse-engineering-expressions-into-soc | eval-metric | 3 | 3 |
| jack-hessel_2021_clipscore-a-reference-free-evalua | eval-metric | 3 | 3 |
| jaemin-cho_2024_davidsonian-scene-graph-improving- | eval-metric | 2 | 3 |
| jiazheng-xu_2023_imagereward-learning-and-evaluati | eval-metric | 3 | 3 |
| lancheng-gao_2025_eemo-bench-a-benchmark-for-multi | eval-metric | 3 | 3 |
| martin-heusel_2017_gans-trained-by-a-two-time-scal | eval-metric | 2 | 3 |
| peter-anderson_2016_spice-semantic-propositional-i | eval-metric | 3 | 3 |
| ramakrishna-vedantam_2015_cider-consensus-based-im | eval-metric | 2 | 3 |
| sree-bhattacharyya_2025_evaluating-vision-language | eval-metric | 3 | 3 |
| tony-lee_2023_holistic-evaluation-of-text-to-image | eval-metric | 3 | 3 |
| xiaoshi-wu_2023_human-preference-score-v2-a-solid- | eval-metric | 2 | 3 |
| yushi-hu_2023_tifa-accurate-and-interpretable-text | eval-metric | 3 | 3 |
| yuval-kirstain_2023_pick-a-pic-an-open-dataset-of- | eval-metric | 2 | 3 |
| colin-raffel_2020_exploring-the-limits-of-transfer | foundation | 2 | 3 |
| cowen_2017_self-report-27-emotions.pdf | foundation | 3 | 3 |
| dorottya-demszky_2020_goemotions-a-dataset-of-fine | foundation | 3 | 3 |
| jana-machajdik_2010_affective-image-classification | foundation | 2 | 3 |
| posner_2005_circumplex-model-of-affect.pdf | foundation | 3 | 1 |
| aditya-ramesh_2021_zero-shot-text-to-image-generat | image-model | 3 | 3 |
| aditya-ramesh_2022_hierarchical-text-conditional-i | image-model | 3 | 3 |
| chitwan-saharia_2022_photorealistic-text-to-image- | image-model | 2 | 3 |
| dustin-podell_2023_sdxl-improving-latent-diffusion | image-model | 2 | 3 |
| james-betker_2023_improving-image-generation-with- | image-model | 3 | 3 |
| jufeng-yang_2018_weakly-supervised-coupled-network | image-model | 2 | 3 |
| junnan-li_2022_blip-bootstrapping-language-image-p | image-model | 3 | 3 |
| junnan-li_2023_blip-2-bootstrapping-language-image | image-model | 3 | 3 |
| robin-rombach_2022_high-resolution-image-synthesis | image-model | 2 | 3 |
| shengqi-dang_2025_emoticrafter-text-to-emotional-i | image-model | 3 | 3 |
| bellaiche_2023_bias-against-ai-art-enhances-human- | perception-study | 3 | 3 |
| chen_2018_distinct-expressions-pain-pleasure.pdf | perception-study | 3 | 3 |
| chen_2020_building-culturally-valid-dynamic-expres | perception-study | 3 | 3 |
| chen_2024_cultural-facial-expressions-convey-emoti | perception-study | 3 | 3 |
| jack_2012_facial-expressions-not-universal.pdf | perception-study | 3 | 3 |
| jack_2014_dynamic-facial-expressions-of-emotion-tr | perception-study | 2 | 3 |
| jonas-oppenlaender_2024_artworks-reimagined-explor | perception-study | 2 | 3 |
| miguel-carrasco_2024_level-of-agreement-between-em | perception-study | 3 | 3 |
| millet_2023_anthropocentric-bias-ai-art.pdf | perception-study | 3 | 3 |
| wetzel_2025_color-emotion-associations-t2i.pdf | perception-study | 2 | 3 |
| ani-harutyunyan_2026_fine-grained-emotion-detectio | text-method | 2 | 2 |
| daniel-yang_2023_context-unlocks-emotions-text-bas | text-method | 3 | 3 |
| hyung-won-chung_2022_scaling-instruction-finetuned | text-method | 2 | 3 |
| maarten-grootendorst_2022_bertopic-neural-topic-mo | text-method | 2 | 3 |
| minxue-niu_2025_contrastive-distillation-of-emotio | text-method | 2 | 3 |
| s41599-023-01816-6.pdf | text-method | 3 | 3 |
| see-arxiv-listing_2025_human-vs-llm-based-thematic | text-method | 2 | 3 |
| siddhanth-bhat_2024_emotion-classification-in-shor | text-method | 3 | 3 |
| sourabh-zanwar_2022_improving-the-generalizability | text-method | 3 | 3 |
| yla-r-tausczik_2010_the-psychological-meaning-of-w | text-method | 3 | 2 |

## Data-quality notes

- **2 wrong-file downloads deleted** (URL guesses that resolved to unrelated PDFs): a Hungarian Cultural Studies bibliography (was mislabelled as Chen 2020 IVA) and an astrophysics paper (was mislabelled as a CHI prompt-journey paper). Caught by reading every PDF.
- **1 filename/author mismatch, content correct & kept**: `hitsuwari_2024_personality-attitudes-ai-art.pdf` is actually the Nature Sci Reports 2024 personality/AI-art study (different first author) — correct paper, later judged tangential and excluded on relevance grounds.
- Supervisor's 8 original papers are retained in `RESEARCH PAPERS/` regardless of triage (Ragot et al. 2020 scored tangential but was provided by the supervisor).

## Cited but not downloaded — obtain via University library

A few canonical works are referenced in `RESEARCH_GAP.md` as foundational context but are paywalled with no open preprint (pre-arXiv-era psychology). Get these through the Sheffield library:

- **Ekman, P. (1992). An argument for basic emotions.** *Cognition & Emotion*, 6(3–4). — the discrete basic-emotion tradition.
- **Russell, J. A. (1980). A circumplex model of affect.** *J. Personality & Social Psychology*, 39(6). — the valence–arousal circumplex (the 2005 Posner review of it IS in the library).
- **Plutchik, R. (2001). The nature of emotions.** *American Scientist*, 89(4). — the emotion wheel.

All 6 of the supervisor's own Chen/Jack papers (2012–2024) are in `lit/B_chaona-chen/`, including the recovered IVA 2020 paper (Chen first author).
