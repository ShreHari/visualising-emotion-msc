# Number macros (generated from report/generated/numbers.tex)

Use `\Name{}` in prose. NEVER type these numbers by hand. Value shown is the current rendering.

| macro | value | meaning |
|---|---|---|
| `\nTotal{}` | 1,025 | records processed (incl. pre-tests) |
| `\nPretest{}` | 13 | pre-festival developer test records, excluded |
| `\nAnalysed{}` | 1,012 | records analysed |
| `\nEmotional{}` | 607 | prompts whose GoEmotions top-1 family is not neutral |
| `\nNonEmotional{}` | 405 | prompts the text reader labels neutral |
| `\nFaceAll{}` | 591 | face-classified records, all analysed |
| `\nSceneAll{}` | 421 | scene-classified records, all analysed |
| `\nFaceEmo{}` | 402 | face-classified within emotional |
| `\nSceneEmo{}` | 205 | scene-classified within emotional |
| `\nPositive{}` | 402 | positive-valence prompts (family joy) |
| `\nNegative{}` | 128 | negative-valence prompts |
| `\nDistinct{}` | 763 | distinct prompts (dedup_key groups) |
| `\nRepeats{}` | 249 | records repeating an earlier prompt |
| `\nHappy{}` | 42 | records whose prompt is exactly 'happy' |
| `\nDistinctEmo{}` | 452 | distinct prompts, emotional |
| `\nDistinctNonEmo{}` | 311 | distinct prompts, neutral-labelled |
| `\nDistinctFace{}` | 319 | distinct prompts, emotional, face-classified |
| `\nDistinctScene{}` | 133 | distinct prompts, emotional, scene-classified |
| `\nGroups{}` | 87 | prompts drawn two or more times |
| `\nGroupRecords{}` | 336 | records inside those groups |
| `\nPairGroups{}` | 43 | groups that are pairs |
| `\nullShuffles{}` | 300 | random re-pairings per null |
| `\nullSeed{}` | 7 | random seed of the analysis |
| `\famPromptJoy{}` | 402 | prompt-reader top-1 = joy, all analysed |
| `\famPromptSadness{}` | 99 | prompt-reader top-1 = sadness, all analysed |
| `\famPromptAnger{}` | 12 | prompt-reader top-1 = anger, all analysed |
| `\famPromptFear{}` | 16 | prompt-reader top-1 = fear, all analysed |
| `\famPromptSurprise{}` | 77 | prompt-reader top-1 = surprise, all analysed |
| `\famPromptDisgust{}` | 1 | prompt-reader top-1 = disgust, all analysed |
| `\famPromptNeutral{}` | 405 | prompt-reader top-1 = neutral, all analysed |
| `\famImageJoy{}` | 461 | image-reader top-1 = joy, all analysed |
| `\famImageSadness{}` | 141 | image-reader top-1 = sadness, all analysed |
| `\famImageAnger{}` | 89 | image-reader top-1 = anger, all analysed |
| `\famImageFear{}` | 4 | image-reader top-1 = fear, all analysed |
| `\famImageSurprise{}` | 108 | image-reader top-1 = surprise, all analysed |
| `\famImageDisgust{}` | 0 | image-reader top-1 = disgust, all analysed |
| `\famImageNeutral{}` | 209 | image-reader top-1 = neutral, all analysed |
| `\FullEmoN{}` | 607 | Full block, ALL emotional: n |
| `\FullEmoNSign{}` | 530 | Full block, ALL emotional: valence-sign denominator |
| `\FullEmoVaObs{}` | 83.8\% | Full ALL emotional va: observed |
| `\FullEmoVaNull{}` | 77.3\% | Full ALL emotional va: null mean |
| `\FullEmoVaSd{}` | 0.53\% | Full ALL emotional va: null sd (pp) |
| `\FullEmoVaZ{}` | +12.2 | Full ALL emotional va: z (n/a = degenerate) |
| `\FullEmoVaCi{}` | [82.0, 85.5] | Full ALL emotional va: clustered-bootstrap 95% CI |
| `\FullEmoSignObs{}` | 64.0\% | Full ALL emotional vsign: observed |
| `\FullEmoSignNull{}` | 45.6\% | Full ALL emotional vsign: null mean |
| `\FullEmoSignSd{}` | 1.65\% | Full ALL emotional vsign: null sd (pp) |
| `\FullEmoSignZ{}` | +11.1 | Full ALL emotional vsign: z (n/a = degenerate) |
| `\FullEmoSignCi{}` | [58.6, 68.8] | Full ALL emotional vsign: clustered-bootstrap 95% CI |
| `\FullEmoFamObs{}` | 53.0\% | Full ALL emotional family: observed |
| `\FullEmoFamNull{}` | 38.8\% | Full ALL emotional family: null mean |
| `\FullEmoFamSd{}` | 1.38\% | Full ALL emotional family: null sd (pp) |
| `\FullEmoFamZ{}` | +10.3 | Full ALL emotional family: z (n/a = degenerate) |
| `\FullEmoFamCi{}` | [47.3, 58.7] | Full ALL emotional family: clustered-bootstrap 95% CI |
| `\FullEmoOvlpObs{}` | 50.6\% | Full ALL emotional overlap: observed |
| `\FullEmoOvlpNull{}` | 39.4\% | Full ALL emotional overlap: null mean |
| `\FullEmoOvlpSd{}` | 0.96\% | Full ALL emotional overlap: null sd (pp) |
| `\FullEmoOvlpZ{}` | +11.6 | Full ALL emotional overlap: z (n/a = degenerate) |
| `\FullEmoOvlpCi{}` | [46.5, 54.7] | Full ALL emotional overlap: clustered-bootstrap 95% CI |
| `\FullFaceN{}` | 402 | Full block, face images: n |
| `\FullFaceNSign{}` | 360 | Full block, face images: valence-sign denominator |
| `\FullFaceVaObs{}` | 84.2\% | Full face images va: observed |
| `\FullFaceVaNull{}` | 76.4\% | Full face images va: null mean |
| `\FullFaceVaSd{}` | 0.70\% | Full face images va: null sd (pp) |
| `\FullFaceVaZ{}` | +11.2 | Full face images va: z (n/a = degenerate) |
| `\FullFaceVaCi{}` | [82.3, 86.1] | Full face images va: clustered-bootstrap 95% CI |
| `\FullFaceSignObs{}` | 73.9\% | Full face images vsign: observed |
| `\FullFaceSignNull{}` | 53.5\% | Full face images vsign: null mean |
| `\FullFaceSignSd{}` | 1.97\% | Full face images vsign: null sd (pp) |
| `\FullFaceSignZ{}` | +10.4 | Full face images vsign: z (n/a = degenerate) |
| `\FullFaceSignCi{}` | [68.3, 79.2] | Full face images vsign: clustered-bootstrap 95% CI |
| `\FullFaceFamObs{}` | 61.9\% | Full face images family: observed |
| `\FullFaceFamNull{}` | 45.8\% | Full face images family: null mean |
| `\FullFaceFamSd{}` | 1.57\% | Full face images family: null sd (pp) |
| `\FullFaceFamZ{}` | +10.3 | Full face images family: z (n/a = degenerate) |
| `\FullFaceFamCi{}` | [55.8, 68.0] | Full face images family: clustered-bootstrap 95% CI |
| `\FullFaceOvlpObs{}` | 53.4\% | Full face images overlap: observed |
| `\FullFaceOvlpNull{}` | 40.4\% | Full face images overlap: null mean |
| `\FullFaceOvlpSd{}` | 1.12\% | Full face images overlap: null sd (pp) |
| `\FullFaceOvlpZ{}` | +11.6 | Full face images overlap: z (n/a = degenerate) |
| `\FullFaceOvlpCi{}` | [49.2, 57.7] | Full face images overlap: clustered-bootstrap 95% CI |
| `\FullSceneN{}` | 205 | Full block, scene images: n |
| `\FullSceneNSign{}` | 170 | Full block, scene images: valence-sign denominator |
| `\FullSceneVaObs{}` | 82.9\% | Full scene images va: observed |
| `\FullSceneVaNull{}` | 79.1\% | Full scene images va: null mean |
| `\FullSceneVaSd{}` | 0.64\% | Full scene images va: null sd (pp) |
| `\FullSceneVaZ{}` | +6.0 | Full scene images va: z (n/a = degenerate) |
| `\FullSceneVaCi{}` | [80.4, 85.2] | Full scene images va: clustered-bootstrap 95% CI |
| `\FullSceneSignObs{}` | 42.9\% | Full scene images vsign: observed |
| `\FullSceneSignNull{}` | 29.6\% | Full scene images vsign: null mean |
| `\FullSceneSignSd{}` | 2.30\% | Full scene images vsign: null sd (pp) |
| `\FullSceneSignZ{}` | +5.8 | Full scene images vsign: z (n/a = degenerate) |
| `\FullSceneSignCi{}` | [33.1, 51.1] | Full scene images vsign: clustered-bootstrap 95% CI |
| `\FullSceneFamObs{}` | 35.6\% | Full scene images family: observed |
| `\FullSceneFamNull{}` | 26.2\% | Full scene images family: null mean |
| `\FullSceneFamSd{}` | 2.17\% | Full scene images family: null sd (pp) |
| `\FullSceneFamZ{}` | +4.4 | Full scene images family: z (n/a = degenerate) |
| `\FullSceneFamCi{}` | [26.4, 44.1] | Full scene images family: clustered-bootstrap 95% CI |
| `\FullSceneOvlpObs{}` | 44.9\% | Full scene images overlap: observed |
| `\FullSceneOvlpNull{}` | 38.1\% | Full scene images overlap: null mean |
| `\FullSceneOvlpSd{}` | 1.39\% | Full scene images overlap: null sd (pp) |
| `\FullSceneOvlpZ{}` | +4.9 | Full scene images overlap: z (n/a = degenerate) |
| `\FullSceneOvlpCi{}` | [38.7, 51.0] | Full scene images overlap: clustered-bootstrap 95% CI |
| `\FullPosN{}` | 402 | Full block, positive prompts: n |
| `\FullPosNSign{}` | 402 | Full block, positive prompts: valence-sign denominator |
| `\FullPosVaObs{}` | 86.6\% | Full positive prompts va: observed |
| `\FullPosVaNull{}` | 85.9\% | Full positive prompts va: null mean |
| `\FullPosVaSd{}` | 0.19\% | Full positive prompts va: null sd (pp) |
| `\FullPosVaZ{}` | +3.9 | Full positive prompts va: z (n/a = degenerate) |
| `\FullPosVaCi{}` | -- | Full positive prompts va: clustered-bootstrap 95% CI |
| `\FullPosSignObs{}` | 64.9\% | Full positive prompts vsign: observed |
| `\FullPosSignNull{}` | 64.9\% | Full positive prompts vsign: null mean |
| `\FullPosSignSd{}` | 0.00\% | Full positive prompts vsign: null sd (pp) |
| `\FullPosSignZ{}` | n/a | Full positive prompts vsign: z (n/a = degenerate) |
| `\FullPosSignCi{}` | -- | Full positive prompts vsign: clustered-bootstrap 95% CI |
| `\FullPosFamObs{}` | 64.9\% | Full positive prompts family: observed |
| `\FullPosFamNull{}` | 64.9\% | Full positive prompts family: null mean |
| `\FullPosFamSd{}` | 0.00\% | Full positive prompts family: null sd (pp) |
| `\FullPosFamZ{}` | n/a | Full positive prompts family: z (n/a = degenerate) |
| `\FullPosFamCi{}` | -- | Full positive prompts family: clustered-bootstrap 95% CI |
| `\FullPosOvlpObs{}` | 57.4\% | Full positive prompts overlap: observed |
| `\FullPosOvlpNull{}` | 56.4\% | Full positive prompts overlap: null mean |
| `\FullPosOvlpSd{}` | 0.46\% | Full positive prompts overlap: null sd (pp) |
| `\FullPosOvlpZ{}` | +2.3 | Full positive prompts overlap: z (n/a = degenerate) |
| `\FullPosOvlpCi{}` | -- | Full positive prompts overlap: clustered-bootstrap 95% CI |
| `\FullNegN{}` | 128 | Full block, negative prompts: n |
| `\FullNegNSign{}` | 128 | Full block, negative prompts: valence-sign denominator |
| `\FullNegVaObs{}` | 75.9\% | Full negative prompts va: observed |
| `\FullNegVaNull{}` | 74.5\% | Full negative prompts va: null mean |
| `\FullNegVaSd{}` | 0.66\% | Full negative prompts va: null sd (pp) |
| `\FullNegVaZ{}` | +2.1 | Full negative prompts va: z (n/a = degenerate) |
| `\FullNegVaCi{}` | -- | Full negative prompts va: clustered-bootstrap 95% CI |
| `\FullNegSignObs{}` | 60.9\% | Full negative prompts vsign: observed |
| `\FullNegSignNull{}` | 60.9\% | Full negative prompts vsign: null mean |
| `\FullNegSignSd{}` | 0.00\% | Full negative prompts vsign: null sd (pp) |
| `\FullNegSignZ{}` | n/a | Full negative prompts vsign: z (n/a = degenerate) |
| `\FullNegSignCi{}` | -- | Full negative prompts vsign: clustered-bootstrap 95% CI |
| `\FullNegFamObs{}` | 35.9\% | Full negative prompts family: observed |
| `\FullNegFamNull{}` | 31.0\% | Full negative prompts family: null mean |
| `\FullNegFamSd{}` | 2.30\% | Full negative prompts family: null sd (pp) |
| `\FullNegFamZ{}` | +2.1 | Full negative prompts family: z (n/a = degenerate) |
| `\FullNegFamCi{}` | -- | Full negative prompts family: clustered-bootstrap 95% CI |
| `\FullNegOvlpObs{}` | 35.4\% | Full negative prompts overlap: observed |
| `\FullNegOvlpNull{}` | 30.3\% | Full negative prompts overlap: null mean |
| `\FullNegOvlpSd{}` | 1.68\% | Full negative prompts overlap: null sd (pp) |
| `\FullNegOvlpZ{}` | +3.0 | Full negative prompts overlap: z (n/a = degenerate) |
| `\FullNegOvlpCi{}` | -- | Full negative prompts overlap: clustered-bootstrap 95% CI |
| `\FullNeuN{}` | 405 | Full block, non-emotional: n |
| `\FullNeuNSign{}` | 0 | Full block, non-emotional: valence-sign denominator |
| `\FullNeuVaObs{}` | 76.6\% | Full non-emotional va: observed |
| `\FullNeuVaNull{}` | 76.6\% | Full non-emotional va: null mean |
| `\FullNeuVaSd{}` | 0.16\% | Full non-emotional va: null sd (pp) |
| `\FullNeuVaZ{}` | +0.3 | Full non-emotional va: z (n/a = degenerate) |
| `\FullNeuVaCi{}` | [75.6, 77.6] | Full non-emotional va: clustered-bootstrap 95% CI |
| `\FullNeuSignObs{}` | 0.0\% | Full non-emotional vsign: observed |
| `\FullNeuSignNull{}` | 0.0\% | Full non-emotional vsign: null mean |
| `\FullNeuSignSd{}` | 0.00\% | Full non-emotional vsign: null sd (pp) |
| `\FullNeuSignZ{}` | n/a | Full non-emotional vsign: z (n/a = degenerate) |
| `\FullNeuSignCi{}` | -- | Full non-emotional vsign: clustered-bootstrap 95% CI |
| `\FullNeuFamObs{}` | 28.6\% | Full non-emotional family: observed |
| `\FullNeuFamNull{}` | 28.6\% | Full non-emotional family: null mean |
| `\FullNeuFamSd{}` | 0.00\% | Full non-emotional family: null sd (pp) |
| `\FullNeuFamZ{}` | n/a | Full non-emotional family: z (n/a = degenerate) |
| `\FullNeuFamCi{}` | -- | Full non-emotional family: clustered-bootstrap 95% CI |
| `\FullNeuOvlpObs{}` | 31.6\% | Full non-emotional overlap: observed |
| `\FullNeuOvlpNull{}` | 31.6\% | Full non-emotional overlap: null mean |
| `\FullNeuOvlpSd{}` | 0.35\% | Full non-emotional overlap: null sd (pp) |
| `\FullNeuOvlpZ{}` | +0.0 | Full non-emotional overlap: z (n/a = degenerate) |
| `\FullNeuOvlpCi{}` | -- | Full non-emotional overlap: clustered-bootstrap 95% CI |
| `\DistEmoN{}` | 452 | Dist block, ALL emotional: n |
| `\DistEmoNSign{}` | 394 | Dist block, ALL emotional: valence-sign denominator |
| `\DistEmoVaObs{}` | 83.0\% | Dist ALL emotional va: observed |
| `\DistEmoVaNull{}` | 76.5\% | Dist ALL emotional va: null mean |
| `\DistEmoVaSd{}` | 0.61\% | Dist ALL emotional va: null sd (pp) |
| `\DistEmoVaZ{}` | +10.6 | Dist ALL emotional va: z (n/a = degenerate) |
| `\DistEmoVaCi{}` | [81.5, 84.4] | Dist ALL emotional va: clustered-bootstrap 95% CI |
| `\DistEmoSignObs{}` | 62.2\% | Dist ALL emotional vsign: observed |
| `\DistEmoSignNull{}` | 44.4\% | Dist ALL emotional vsign: null mean |
| `\DistEmoSignSd{}` | 1.80\% | Dist ALL emotional vsign: null sd (pp) |
| `\DistEmoSignZ{}` | +9.9 | Dist ALL emotional vsign: z (n/a = degenerate) |
| `\DistEmoSignCi{}` | [57.2, 67.0] | Dist ALL emotional vsign: clustered-bootstrap 95% CI |
| `\DistEmoFamObs{}` | 51.3\% | Dist ALL emotional family: observed |
| `\DistEmoFamNull{}` | 37.2\% | Dist ALL emotional family: null mean |
| `\DistEmoFamSd{}` | 1.51\% | Dist ALL emotional family: null sd (pp) |
| `\DistEmoFamZ{}` | +9.3 | Dist ALL emotional family: z (n/a = degenerate) |
| `\DistEmoFamCi{}` | [46.7, 56.0] | Dist ALL emotional family: clustered-bootstrap 95% CI |
| `\DistEmoOvlpObs{}` | 48.9\% | Dist ALL emotional overlap: observed |
| `\DistEmoOvlpNull{}` | 37.7\% | Dist ALL emotional overlap: null mean |
| `\DistEmoOvlpSd{}` | 1.03\% | Dist ALL emotional overlap: null sd (pp) |
| `\DistEmoOvlpZ{}` | +10.8 | Dist ALL emotional overlap: z (n/a = degenerate) |
| `\DistEmoOvlpCi{}` | [45.9, 51.9] | Dist ALL emotional overlap: clustered-bootstrap 95% CI |
| `\DistFaceN{}` | 319 | Dist block, face images: n |
| `\DistFaceNSign{}` | 284 | Dist block, face images: valence-sign denominator |
| `\DistFaceVaObs{}` | 83.5\% | Dist face images va: observed |
| `\DistFaceVaNull{}` | 75.5\% | Dist face images va: null mean |
| `\DistFaceVaSd{}` | 0.82\% | Dist face images va: null sd (pp) |
| `\DistFaceVaZ{}` | +9.7 | Dist face images va: z (n/a = degenerate) |
| `\DistFaceVaCi{}` | [81.7, 85.2] | Dist face images va: clustered-bootstrap 95% CI |
| `\DistFaceSignObs{}` | 71.8\% | Dist face images vsign: observed |
| `\DistFaceSignNull{}` | 51.0\% | Dist face images vsign: null mean |
| `\DistFaceSignSd{}` | 2.46\% | Dist face images vsign: null sd (pp) |
| `\DistFaceSignZ{}` | +8.4 | Dist face images vsign: z (n/a = degenerate) |
| `\DistFaceSignCi{}` | [66.4, 77.0] | Dist face images vsign: clustered-bootstrap 95% CI |
| `\DistFaceFamObs{}` | 59.9\% | Dist face images family: observed |
| `\DistFaceFamNull{}` | 43.0\% | Dist face images family: null mean |
| `\DistFaceFamSd{}` | 2.07\% | Dist face images family: null sd (pp) |
| `\DistFaceFamZ{}` | +8.1 | Dist face images family: z (n/a = degenerate) |
| `\DistFaceFamCi{}` | [54.2, 65.2] | Dist face images family: clustered-bootstrap 95% CI |
| `\DistFaceOvlpObs{}` | 51.8\% | Dist face images overlap: observed |
| `\DistFaceOvlpNull{}` | 38.4\% | Dist face images overlap: null mean |
| `\DistFaceOvlpSd{}` | 1.38\% | Dist face images overlap: null sd (pp) |
| `\DistFaceOvlpZ{}` | +9.7 | Dist face images overlap: z (n/a = degenerate) |
| `\DistFaceOvlpCi{}` | [48.1, 55.4] | Dist face images overlap: clustered-bootstrap 95% CI |
| `\DistSceneN{}` | 133 | Dist block, scene images: n |
| `\DistSceneNSign{}` | 110 | Dist block, scene images: valence-sign denominator |
| `\DistSceneVaObs{}` | 81.8\% | Dist scene images va: observed |
| `\DistSceneVaNull{}` | 78.9\% | Dist scene images va: null mean |
| `\DistSceneVaSd{}` | 0.80\% | Dist scene images va: null sd (pp) |
| `\DistSceneVaZ{}` | +3.6 | Dist scene images va: z (n/a = degenerate) |
| `\DistSceneVaCi{}` | [79.5, 83.8] | Dist scene images va: clustered-bootstrap 95% CI |
| `\DistSceneSignObs{}` | 37.3\% | Dist scene images vsign: observed |
| `\DistSceneSignNull{}` | 27.1\% | Dist scene images vsign: null mean |
| `\DistSceneSignSd{}` | 2.92\% | Dist scene images vsign: null sd (pp) |
| `\DistSceneSignZ{}` | +3.5 | Dist scene images vsign: z (n/a = degenerate) |
| `\DistSceneSignCi{}` | [28.1, 46.2] | Dist scene images vsign: clustered-bootstrap 95% CI |
| `\DistSceneFamObs{}` | 30.8\% | Dist scene images family: observed |
| `\DistSceneFamNull{}` | 24.1\% | Dist scene images family: null mean |
| `\DistSceneFamSd{}` | 2.62\% | Dist scene images family: null sd (pp) |
| `\DistSceneFamZ{}` | +2.6 | Dist scene images family: z (n/a = degenerate) |
| `\DistSceneFamCi{}` | [23.3, 38.4] | Dist scene images family: clustered-bootstrap 95% CI |
| `\DistSceneOvlpObs{}` | 41.7\% | Dist scene images overlap: observed |
| `\DistSceneOvlpNull{}` | 36.7\% | Dist scene images overlap: null mean |
| `\DistSceneOvlpSd{}` | 1.63\% | Dist scene images overlap: null sd (pp) |
| `\DistSceneOvlpZ{}` | +3.1 | Dist scene images overlap: z (n/a = degenerate) |
| `\DistSceneOvlpCi{}` | [36.9, 46.5] | Dist scene images overlap: clustered-bootstrap 95% CI |
| `\DistPosN{}` | 293 | Dist block, positive prompts: n |
| `\DistPosNSign{}` | 293 | Dist block, positive prompts: valence-sign denominator |
| `\DistPosVaObs{}` | 85.5\% | Dist positive prompts va: observed |
| `\DistPosVaNull{}` | 84.8\% | Dist positive prompts va: null mean |
| `\DistPosVaSd{}` | 0.22\% | Dist positive prompts va: null sd (pp) |
| `\DistPosVaZ{}` | +3.3 | Dist positive prompts va: z (n/a = degenerate) |
| `\DistPosVaCi{}` | -- | Dist positive prompts va: clustered-bootstrap 95% CI |
| `\DistPosSignObs{}` | 62.1\% | Dist positive prompts vsign: observed |
| `\DistPosSignNull{}` | 62.1\% | Dist positive prompts vsign: null mean |
| `\DistPosSignSd{}` | 0.00\% | Dist positive prompts vsign: null sd (pp) |
| `\DistPosSignZ{}` | n/a | Dist positive prompts vsign: z (n/a = degenerate) |
| `\DistPosSignCi{}` | -- | Dist positive prompts vsign: clustered-bootstrap 95% CI |
| `\DistPosFamObs{}` | 62.1\% | Dist positive prompts family: observed |
| `\DistPosFamNull{}` | 62.1\% | Dist positive prompts family: null mean |
| `\DistPosFamSd{}` | 0.00\% | Dist positive prompts family: null sd (pp) |
| `\DistPosFamZ{}` | n/a | Dist positive prompts family: z (n/a = degenerate) |
| `\DistPosFamCi{}` | -- | Dist positive prompts family: clustered-bootstrap 95% CI |
| `\DistPosOvlpObs{}` | 54.6\% | Dist positive prompts overlap: observed |
| `\DistPosOvlpNull{}` | 53.6\% | Dist positive prompts overlap: null mean |
| `\DistPosOvlpSd{}` | 0.53\% | Dist positive prompts overlap: null sd (pp) |
| `\DistPosOvlpZ{}` | +1.9 | Dist positive prompts overlap: z (n/a = degenerate) |
| `\DistPosOvlpCi{}` | -- | Dist positive prompts overlap: clustered-bootstrap 95% CI |
| `\DistNegN{}` | 101 | Dist block, negative prompts: n |
| `\DistNegNSign{}` | 101 | Dist block, negative prompts: valence-sign denominator |
| `\DistNegVaObs{}` | 76.2\% | Dist negative prompts va: observed |
| `\DistNegVaNull{}` | 74.8\% | Dist negative prompts va: null mean |
| `\DistNegVaSd{}` | 0.85\% | Dist negative prompts va: null sd (pp) |
| `\DistNegVaZ{}` | +1.6 | Dist negative prompts va: z (n/a = degenerate) |
| `\DistNegVaCi{}` | -- | Dist negative prompts va: clustered-bootstrap 95% CI |
| `\DistNegSignObs{}` | 62.4\% | Dist negative prompts vsign: observed |
| `\DistNegSignNull{}` | 62.4\% | Dist negative prompts vsign: null mean |
| `\DistNegSignSd{}` | 0.00\% | Dist negative prompts vsign: null sd (pp) |
| `\DistNegSignZ{}` | n/a | Dist negative prompts vsign: z (n/a = degenerate) |
| `\DistNegSignCi{}` | -- | Dist negative prompts vsign: clustered-bootstrap 95% CI |
| `\DistNegFamObs{}` | 38.6\% | Dist negative prompts family: observed |
| `\DistNegFamNull{}` | 32.9\% | Dist negative prompts family: null mean |
| `\DistNegFamSd{}` | 2.72\% | Dist negative prompts family: null sd (pp) |
| `\DistNegFamZ{}` | +2.1 | Dist negative prompts family: z (n/a = degenerate) |
| `\DistNegFamCi{}` | -- | Dist negative prompts family: clustered-bootstrap 95% CI |
| `\DistNegOvlpObs{}` | 36.7\% | Dist negative prompts overlap: observed |
| `\DistNegOvlpNull{}` | 31.0\% | Dist negative prompts overlap: null mean |
| `\DistNegOvlpSd{}` | 2.11\% | Dist negative prompts overlap: null sd (pp) |
| `\DistNegOvlpZ{}` | +2.7 | Dist negative prompts overlap: z (n/a = degenerate) |
| `\DistNegOvlpCi{}` | -- | Dist negative prompts overlap: clustered-bootstrap 95% CI |
| `\DistNeuN{}` | 311 | Dist block, non-emotional: n |
| `\DistNeuNSign{}` | 0 | Dist block, non-emotional: valence-sign denominator |
| `\DistNeuVaObs{}` | 76.6\% | Dist non-emotional va: observed |
| `\DistNeuVaNull{}` | 76.4\% | Dist non-emotional va: null mean |
| `\DistNeuVaSd{}` | 0.18\% | Dist non-emotional va: null sd (pp) |
| `\DistNeuVaZ{}` | +1.1 | Dist non-emotional va: z (n/a = degenerate) |
| `\DistNeuVaCi{}` | -- | Dist non-emotional va: clustered-bootstrap 95% CI |
| `\DistNeuSignObs{}` | 0.0\% | Dist non-emotional vsign: observed |
| `\DistNeuSignNull{}` | 0.0\% | Dist non-emotional vsign: null mean |
| `\DistNeuSignSd{}` | 0.00\% | Dist non-emotional vsign: null sd (pp) |
| `\DistNeuSignZ{}` | n/a | Dist non-emotional vsign: z (n/a = degenerate) |
| `\DistNeuSignCi{}` | -- | Dist non-emotional vsign: clustered-bootstrap 95% CI |
| `\DistNeuFamObs{}` | 27.7\% | Dist non-emotional family: observed |
| `\DistNeuFamNull{}` | 27.7\% | Dist non-emotional family: null mean |
| `\DistNeuFamSd{}` | 0.00\% | Dist non-emotional family: null sd (pp) |
| `\DistNeuFamZ{}` | n/a | Dist non-emotional family: z (n/a = degenerate) |
| `\DistNeuFamCi{}` | -- | Dist non-emotional family: clustered-bootstrap 95% CI |
| `\DistNeuOvlpObs{}` | 31.4\% | Dist non-emotional overlap: observed |
| `\DistNeuOvlpNull{}` | 31.1\% | Dist non-emotional overlap: null mean |
| `\DistNeuOvlpSd{}` | 0.37\% | Dist non-emotional overlap: null sd (pp) |
| `\DistNeuOvlpZ{}` | +0.8 | Dist non-emotional overlap: z (n/a = degenerate) |
| `\DistNeuOvlpCi{}` | -- | Dist non-emotional overlap: clustered-bootstrap 95% CI |
| `\DiffSignPp{}` | +30.9~pp | face minus scene, valence-sign agreement |
| `\DiffSignCi{}` | [+22.6, +40.6] | its clustered-bootstrap 95% CI (pp) |
| `\DiffSignP{}` | 0.0001 | clustered permutation p (valence sign) |
| `\DiffFamPp{}` | +26.3~pp | face minus scene, family agreement |
| `\DiffFamCi{}` | [+18.4, +35.3] | its clustered-bootstrap 95% CI (pp) |
| `\DiffFamP{}` | 0.0001 | clustered permutation p (family) |
| `\DiffDraws{}` | 10,000 | draws in the clustered bootstrap / permutation |
| `\KappaEmo{}` | 0.23 | Cohen's kappa, family agreement, emotional |
| `\KappaEmoCi{}` | [0.18, 0.29] | its clustered-bootstrap 95% CI |
| `\KappaEmoBand{}` | fair | Landis & Koch (1977) band |
| `\KappaFace{}` | 0.30 | Cohen's kappa, family agreement, face |
| `\KappaFaceCi{}` | [0.23, 0.37] | its clustered-bootstrap 95% CI |
| `\KappaFaceBand{}` | fair | Landis & Koch (1977) band |
| `\KappaScene{}` | 0.13 | Cohen's kappa, family agreement, scene |
| `\KappaSceneCi{}` | [0.06, 0.19] | its clustered-bootstrap 95% CI |
| `\KappaSceneBand{}` | slight | Landis & Koch (1977) band |
| `\KappaAll{}` | 0.21 | Cohen's kappa, family agreement, all_analysed |
| `\KappaAllCi{}` | [0.16, 0.25] | its clustered-bootstrap 95% CI |
| `\KappaAllBand{}` | fair | Landis & Koch (1977) band |
| `\KappaDistEmo{}` | 0.23 | Cohen's kappa, family agreement, distinct_emotional |
| `\KappaDistEmoCi{}` | [0.17, 0.29] | its clustered-bootstrap 95% CI |
| `\KappaDistEmoBand{}` | fair | Landis & Koch (1977) band |
| `\KappaDistFace{}` | 0.29 | Cohen's kappa, family agreement, distinct_face |
| `\KappaDistFaceCi{}` | [0.21, 0.37] | its clustered-bootstrap 95% CI |
| `\KappaDistFaceBand{}` | fair | Landis & Koch (1977) band |
| `\KappaDistScene{}` | 0.09 | Cohen's kappa, family agreement, distinct_scene |
| `\KappaDistSceneCi{}` | [0.01, 0.17] | its clustered-bootstrap 95% CI |
| `\KappaDistSceneBand{}` | slight | Landis & Koch (1977) band |
| `\ConsFam{}` | 68.8\% | mean within-group modal-family agreement |
| `\ConsFamNull{}` | 59.4\% | its permutation-null mean |
| `\ConsFamNullSd{}` | 2.1\% | its null sd |
| `\ConsFamZ{}` | +4.5 | its z |
| `\ConsFamP{}` | $1.0\times10^{-4}$ | its permutation p |
| `\ConsFamCi{}` | [63.8, 73.9] | clustered-bootstrap 95% CI over groups (inference.py) |
| `\ConsVal{}` | 74.5\% | mean within-group modal-valence agreement |
| `\ConsValNull{}` | 63.7\% | its null mean |
| `\ConsValZ{}` | +5.0 | its z |
| `\ConsValP{}` | $1.0\times10^{-4}$ | its permutation p |
| `\ConsFull{}` | 28 | groups where every drawing shares one family |
| `\ConsFullPct{}` | 32.2\% | as a share of the groups |
| `\ConsFullNull{}` | 14.5 | its null mean (count) |
| `\ConsFullZ{}` | +4.2 | its z |
| `\ConsFullP{}` | $2.0\times10^{-4}$ | its permutation p |
| `\ConsDraws{}` | 10,000 | permutation draws |
| `\ConsHappyN{}` | 42 | drawings of the prompt 'happy' |
| `\ConsHappyJoy{}` | 34 | 'happy' drawings read as joy |
| `\ConsHappyNeutral{}` | 7 | 'happy' drawings read as neutral |
| `\ConsHappySurprise{}` | 1 | 'happy' drawings read as surprise |
| `\ZSeedMin{}` | +11.2 | smallest emotional valence-sign z over seeds 1-5 |
| `\ZSeedMax{}` | +12.2 | largest emotional valence-sign z over seeds 1-5 |
| `\McN{}` | 607 | records both image readers cover |
| `\McDeVa{}` | 83.8\% | like-for-like describe_then_extract va (emotional) |
| `\McDeVaNull{}` | 77.3\% | its null mean |
| `\McDeVaZ{}` | +12.2 | its z |
| `\McDeSign{}` | 64.0\% | like-for-like describe_then_extract vsign (emotional) |
| `\McDeSignNull{}` | 45.6\% | its null mean |
| `\McDeSignZ{}` | +11.1 | its z |
| `\McDeFam{}` | 53.0\% | like-for-like describe_then_extract family (emotional) |
| `\McDeFamNull{}` | 38.8\% | its null mean |
| `\McDeFamZ{}` | +10.3 | its z |
| `\McDeOvlp{}` | 50.6\% | like-for-like describe_then_extract overlap (emotional) |
| `\McDeOvlpNull{}` | 39.4\% | its null mean |
| `\McDeOvlpZ{}` | +11.6 | its z |
| `\McDeFaceSign{}` | 73.9\% | like-for-like describe_then_extract face_images vsign |
| `\McDeFaceSignZ{}` | +10.4 | its z |
| `\McDeFaceFam{}` | 61.9\% | like-for-like describe_then_extract face_images family |
| `\McDeFaceFamZ{}` | +10.3 | its z |
| `\McDeSceneSign{}` | 42.9\% | like-for-like describe_then_extract scene_images vsign |
| `\McDeSceneSignZ{}` | +5.8 | its z |
| `\McDeSceneFam{}` | 35.6\% | like-for-like describe_then_extract scene_images family |
| `\McDeSceneFamZ{}` | +4.4 | its z |
| `\McClipVa{}` | 73.3\% | like-for-like direct_clip va (emotional) |
| `\McClipVaNull{}` | 70.1\% | its null mean |
| `\McClipVaZ{}` | +10.2 | its z |
| `\McClipSign{}` | 31.1\% | like-for-like direct_clip vsign (emotional) |
| `\McClipSignNull{}` | 18.6\% | its null mean |
| `\McClipSignZ{}` | +9.9 | its z |
| `\McClipFam{}` | 22.4\% | like-for-like direct_clip family (emotional) |
| `\McClipFamNull{}` | 12.2\% | its null mean |
| `\McClipFamZ{}` | +11.1 | its z |
| `\McClipOvlp{}` | 26.4\% | like-for-like direct_clip overlap (emotional) |
| `\McClipOvlpNull{}` | 20.2\% | its null mean |
| `\McClipOvlpZ{}` | +11.2 | its z |
| `\McClipFaceSign{}` | 36.4\% | like-for-like direct_clip face_images vsign |
| `\McClipFaceSignZ{}` | +7.9 | its z |
| `\McClipFaceFam{}` | 27.4\% | like-for-like direct_clip face_images family |
| `\McClipFaceFamZ{}` | +9.4 | its z |
| `\McClipSceneSign{}` | 20.0\% | like-for-like direct_clip scene_images vsign |
| `\McClipSceneSignZ{}` | +5.4 | its z |
| `\McClipSceneFam{}` | 12.7\% | like-for-like direct_clip scene_images family |
| `\McClipSceneFamZ{}` | +4.1 | its z |
| `\McDiffFamPp{}` | +30.6~pp | describe minus CLIP, family agreement |
| `\McDiffFamCi{}` | [+25.5, +35.6] | its clustered-bootstrap 95% CI (pp) |
| `\McMcNemarFamP{}` | $3.4\times10^{-35}$ | exact McNemar p, unclustered (optimistic) |
| `\McClusterFamP{}` | $<$0.001 | cluster sign-flip p (family) |
| `\McFamB{}` | 218 | records only describe-then-extract agrees on (family) |
| `\McFamC{}` | 32 | records only direct CLIP agrees on (family) |
| `\McFamBoth{}` | 104 | records both agree on (family) |
| `\McFamNeither{}` | 253 | records neither agrees on (family) |
| `\McDiffSignPp{}` | +32.8~pp | describe minus CLIP, valence-sign agreement |
| `\McDiffSignCi{}` | [+27.4, +38.2] | its clustered-bootstrap 95% CI (pp) |
| `\McMcNemarSignP{}` | $5.5\times10^{-33}$ | exact McNemar p, unclustered |
| `\McClusterDraws{}` | 20,000 | cluster sign-flip draws |
| `\McReaderAgree{}` | 32.1\% | top-1 agreement between the two image readers |
| `\McClipNeutral{}` | 283 | emotional-prompt images direct CLIP reads as neutral |
| `\McVOneN{}` | 608 | records in the v1 (NLI prompt side) comparison |
| `\McVOneDeFam{}` | 49.3\% | v1 comparison describe_then_extract family |
| `\McVOneDeOvlp{}` | 48.6\% | v1 comparison describe_then_extract overlap |
| `\McVOneDeVa{}` | 83.7\% | v1 comparison describe_then_extract va |
| `\McVOneClipFam{}` | 25.3\% | v1 comparison direct_clip family |
| `\McVOneClipOvlp{}` | 22.8\% | v1 comparison direct_clip overlap |
| `\McVOneClipVa{}` | 74.2\% | v1 comparison direct_clip va |
| `\CtrlN{}` | 405 | neutral-labelled prompts |
| `\CtrlNameOnly{}` | 2 | records reduced to '[name]' by redaction |
| `\CtrlLexicon{}` | 66 | affect words in the audit lexicon |
| `\CtrlFlagged{}` | 68 | neutral-labelled prompts containing an affect word |
| `\CtrlFlaggedPct{}` | 16.8\% | as a share of the control |
| `\CtrlRemoved{}` | 70 | records removed for the cleaned control |
| `\CtrlCleanN{}` | 335 | cleaned control size |
| `\CtrlTopWords{}` | calm (10), content (8), tired (7), stress (6), relaxed (6), inspired (4), sleepy (4), interested (3), anticipation (3), nostalgic (3) | ten most frequent affect words in the control |
| `\CtrlVaObs{}` | 76.6\% | full control VA observed |
| `\CtrlVaNull{}` | 76.5\% | full control VA null |
| `\CtrlVaSd{}` | 0.15\% | full control VA null sd (pp) |
| `\CtrlVaZ{}` | +0.5 | full control VA z (record-level null) |
| `\CtrlVaZClustered{}` | -0.1 | full control VA z (clustered null) |
| `\CtrlCleanVaObs{}` | 76.6\% | cleaned control VA observed |
| `\CtrlCleanVaNull{}` | 76.6\% | cleaned control VA null |
| `\CtrlCleanVaZ{}` | +0.0 | cleaned control VA z (record-level) |
| `\CtrlCleanVaZClustered{}` | -0.6 | cleaned control VA z (clustered) |
| `\CtrlFamObs{}` | 28.6\% | full control family agreement (degenerate: equals its null) |
| `\DescPeopleExpr{}` | 591 | people>=1 and expression word |
| `\DescPeopleNoExpr{}` | 7 | people>=1, no expression word |
| `\DescNoPeopleExpr{}` | 406 | people=0 yet an expression word |
| `\DescNoPeopleNoExpr{}` | 8 | people=0, no expression word |
| `\DescSceneN{}` | 421 | scene-classified records |
| `\DescScenePeopleZero{}` | 414 | of which people=0 |
| `\DescScenePeopleZeroExpr{}` | 406 | of which people=0 with an expression word |
| `\DescSceneSmile{}` | 332 | people=0 answering smile/smiling/happy |
| `\DescSceneSmilePct{}` | 80.2\% | as a share of the people=0 records |
| `\DescBareStrictN{}` | 418 | expression answers that name an affective state (strict) |
| `\DescBareStrictPct{}` | 41.3\% | as a share of analysed records |
| `\DescBareBroadN{}` | 997 | expression answers that are a single facial-action or affect word (broad) |
| `\DescCopyStrict{}` | 99.8\% | copy rate, strict: image top-1 equals the word's family |
| `\DescCopyBroad{}` | 68.6\% | copy rate, broad |
| `\DescCopyBroadPeopleZero{}` | 48.8\% | copy rate, broad, people=0 |
| `\DescCopyBroadPeople{}` | 82.2\% | copy rate, broad, people>=1 |
| `\DescSmileAll{}` | 66.1\% | smile/smiling/happy share, all analysed |
| `\DescSmileAllN{}` | 669 | count |
| `\DescSmileFace{}` | 57.0\% | smile/smiling/happy share, face-classified |
| `\DescSmileFaceN{}` | 337 | count |
| `\RecJoy{}` | 64.9\% | per-family recall (row = prompt family joy) |
| `\RecJoyCi{}` | [58.7, 70.3] | its clustered-bootstrap 95% CI |
| `\RecJoyN{}` | 402 | prompts in that family |
| `\RecSadness{}` | 40.4\% | per-family recall (row = prompt family sadness) |
| `\RecSadnessCi{}` | [30.9, 51.2] | its clustered-bootstrap 95% CI |
| `\RecSadnessN{}` | 99 | prompts in that family |
| `\RecAnger{}` | 50.0\% | per-family recall (row = prompt family anger) |
| `\RecAngerCi{}` | [22.2, 77.8] | its clustered-bootstrap 95% CI |
| `\RecAngerN{}` | 12 | prompts in that family |
| `\RecFear{}` | 0.0\% | per-family recall (row = prompt family fear) |
| `\RecFearCi{}` | [0.0, 0.0] | its clustered-bootstrap 95% CI |
| `\RecFearN{}` | 16 | prompts in that family |
| `\RecSurprise{}` | 19.5\% | per-family recall (row = prompt family surprise) |
| `\RecSurpriseCi{}` | [11.4, 28.1] | its clustered-bootstrap 95% CI |
| `\RecSurpriseN{}` | 77 | prompts in that family |
| `\RecDisgust{}` | 0.0\% | per-family recall (row = prompt family disgust) |
| `\RecDisgustCi{}` | [0.0, 0.0] | its clustered-bootstrap 95% CI |
| `\RecDisgustN{}` | 1 | prompts in that family |
| `\TaxN{}` | 38 | high-confidence disagreements examined |
| `\TaxDistinct{}` | 37 | distinct prompts among them |
| `\TaxA{}` | 9 | failure mode (a) |
| `\TaxB{}` | 10 | failure mode (b) |
| `\TaxC{}` | 5 | failure mode (c) |
| `\TaxD{}` | 11 | failure mode (d) |
| `\TaxE{}` | 2 | failure mode (e) |
| `\TaxF{}` | 1 | failure mode (f) |
| `\TaxDescriber{}` | 19 | describer faults (a+b) |
| `\TaxReader{}` | 5 | image-reader faults (c) |
| `\TaxPrompt{}` | 12 | prompt-side faults (d+f) |
| `\TaxGenerator{}` | 2 | generator faults (e) |
| `\TaxPeopleZero{}` | 13 | records auto-tagged people=0 |
| `\HolmM{}` | 36 | non-degenerate z-scores tested |
| `\HolmExcluded{}` | 12 | degenerate z-scores excluded |
| `\HolmSurvive{}` | 26 | survive Holm at family-wise 0.05 |
| `\HolmFail{}` | 10 | do not survive |
| `\HolmBonfZ{}` | 3.2 | Bonferroni-equivalent z for the smallest rank |
| `\AblDropExpressionEmoSignObs{}` | 15.3\% | ablation drop_expression, emotional, vsign: observed |
| `\AblDropExpressionEmoSignNull{}` | 11.4\% | ablation drop_expression, emotional, vsign: null mean |
| `\AblDropExpressionEmoSignZ{}` | +5.1 | ablation drop_expression, emotional, vsign: z |
| `\AblDropExpressionEmoFamObs{}` | 20.3\% | ablation drop_expression, emotional, family: observed |
| `\AblDropExpressionEmoFamNull{}` | 16.6\% | ablation drop_expression, emotional, family: null mean |
| `\AblDropExpressionEmoFamZ{}` | +3.8 | ablation drop_expression, emotional, family: z |
| `\AblDropExpressionFaceSignObs{}` | 18.9\% | ablation drop_expression, face, vsign: observed |
| `\AblDropExpressionFaceSignNull{}` | 14.7\% | ablation drop_expression, face, vsign: null mean |
| `\AblDropExpressionFaceSignZ{}` | +3.8 | ablation drop_expression, face, vsign: z |
| `\AblDropExpressionFaceFamObs{}` | 25.9\% | ablation drop_expression, face, family: observed |
| `\AblDropExpressionFaceFamNull{}` | 20.5\% | ablation drop_expression, face, family: null mean |
| `\AblDropExpressionFaceFamZ{}` | +3.8 | ablation drop_expression, face, family: z |
| `\AblDropExpressionSceneSignObs{}` | 7.6\% | ablation drop_expression, scene, vsign: observed |
| `\AblDropExpressionSceneSignNull{}` | 4.7\% | ablation drop_expression, scene, vsign: null mean |
| `\AblDropExpressionSceneSignZ{}` | +2.7 | ablation drop_expression, scene, vsign: z |
| `\AblDropExpressionSceneFamObs{}` | 9.3\% | ablation drop_expression, scene, family: observed |
| `\AblDropExpressionSceneFamNull{}` | 6.4\% | ablation drop_expression, scene, family: null mean |
| `\AblDropExpressionSceneFamZ{}` | +2.2 | ablation drop_expression, scene, family: z |
| `\AblDropActionEmoSignObs{}` | 61.9\% | ablation drop_action, emotional, vsign: observed |
| `\AblDropActionEmoSignNull{}` | 43.9\% | ablation drop_action, emotional, vsign: null mean |
| `\AblDropActionEmoSignZ{}` | +11.0 | ablation drop_action, emotional, vsign: z |
| `\AblDropActionEmoFamObs{}` | 50.6\% | ablation drop_action, emotional, family: observed |
| `\AblDropActionEmoFamNull{}` | 36.7\% | ablation drop_action, emotional, family: null mean |
| `\AblDropActionEmoFamZ{}` | +10.3 | ablation drop_action, emotional, family: z |
| `\AblDropActionFaceSignObs{}` | 72.5\% | ablation drop_action, face, vsign: observed |
| `\AblDropActionFaceSignNull{}` | 52.2\% | ablation drop_action, face, vsign: null mean |
| `\AblDropActionFaceSignZ{}` | +10.4 | ablation drop_action, face, vsign: z |
| `\AblDropActionFaceFamObs{}` | 60.7\% | ablation drop_action, face, family: observed |
| `\AblDropActionFaceFamNull{}` | 44.5\% | ablation drop_action, face, family: null mean |
| `\AblDropActionFaceFamZ{}` | +10.4 | ablation drop_action, face, family: z |
| `\AblDropActionSceneSignObs{}` | 39.4\% | ablation drop_action, scene, vsign: observed |
| `\AblDropActionSceneSignNull{}` | 26.8\% | ablation drop_action, scene, vsign: null mean |
| `\AblDropActionSceneSignZ{}` | +5.6 | ablation drop_action, scene, vsign: z |
| `\AblDropActionSceneFamObs{}` | 30.7\% | ablation drop_action, scene, family: observed |
| `\AblDropActionSceneFamNull{}` | 21.9\% | ablation drop_action, scene, family: null mean |
| `\AblDropActionSceneFamZ{}` | +4.6 | ablation drop_action, scene, family: z |
| `\AblDropPostureEmoSignObs{}` | 62.3\% | ablation drop_posture, emotional, vsign: observed |
| `\AblDropPostureEmoSignNull{}` | 44.5\% | ablation drop_posture, emotional, vsign: null mean |
| `\AblDropPostureEmoSignZ{}` | +10.7 | ablation drop_posture, emotional, vsign: z |
| `\AblDropPostureEmoFamObs{}` | 51.4\% | ablation drop_posture, emotional, family: observed |
| `\AblDropPostureEmoFamNull{}` | 37.9\% | ablation drop_posture, emotional, family: null mean |
| `\AblDropPostureEmoFamZ{}` | +9.7 | ablation drop_posture, emotional, family: z |
| `\AblDropPostureFaceSignObs{}` | 73.1\% | ablation drop_posture, face, vsign: observed |
| `\AblDropPostureFaceSignNull{}` | 53.1\% | ablation drop_posture, face, vsign: null mean |
| `\AblDropPostureFaceSignZ{}` | +10.0 | ablation drop_posture, face, vsign: z |
| `\AblDropPostureFaceFamObs{}` | 61.4\% | ablation drop_posture, face, family: observed |
| `\AblDropPostureFaceFamNull{}` | 45.6\% | ablation drop_posture, face, family: null mean |
| `\AblDropPostureFaceFamZ{}` | +10.1 | ablation drop_posture, face, family: z |
| `\AblDropPostureSceneSignObs{}` | 39.4\% | ablation drop_posture, scene, vsign: observed |
| `\AblDropPostureSceneSignNull{}` | 26.8\% | ablation drop_posture, scene, vsign: null mean |
| `\AblDropPostureSceneSignZ{}` | +5.6 | ablation drop_posture, scene, vsign: z |
| `\AblDropPostureSceneFamObs{}` | 31.7\% | ablation drop_posture, scene, family: observed |
| `\AblDropPostureSceneFamNull{}` | 24.0\% | ablation drop_posture, scene, family: null mean |
| `\AblDropPostureSceneFamZ{}` | +3.6 | ablation drop_posture, scene, family: z |
| `\AblDropPeopleEmoSignObs{}` | 68.5\% | ablation drop_people, emotional, vsign: observed |
| `\AblDropPeopleEmoSignNull{}` | 50.7\% | ablation drop_people, emotional, vsign: null mean |
| `\AblDropPeopleEmoSignZ{}` | +10.8 | ablation drop_people, emotional, vsign: z |
| `\AblDropPeopleEmoFamObs{}` | 57.8\% | ablation drop_people, emotional, family: observed |
| `\AblDropPeopleEmoFamNull{}` | 43.7\% | ablation drop_people, emotional, family: null mean |
| `\AblDropPeopleEmoFamZ{}` | +9.9 | ablation drop_people, emotional, family: z |
| `\AblDropPeopleFaceSignObs{}` | 70.8\% | ablation drop_people, face, vsign: observed |
| `\AblDropPeopleFaceSignNull{}` | 50.7\% | ablation drop_people, face, vsign: null mean |
| `\AblDropPeopleFaceSignZ{}` | +10.4 | ablation drop_people, face, vsign: z |
| `\AblDropPeopleFaceFamObs{}` | 59.7\% | ablation drop_people, face, family: observed |
| `\AblDropPeopleFaceFamNull{}` | 43.6\% | ablation drop_people, face, family: null mean |
| `\AblDropPeopleFaceFamZ{}` | +10.3 | ablation drop_people, face, family: z |
| `\AblDropPeopleSceneSignObs{}` | 63.5\% | ablation drop_people, scene, vsign: observed |
| `\AblDropPeopleSceneSignNull{}` | 50.9\% | ablation drop_people, scene, vsign: null mean |
| `\AblDropPeopleSceneSignZ{}` | +5.0 | ablation drop_people, scene, vsign: z |
| `\AblDropPeopleSceneFamObs{}` | 54.1\% | ablation drop_people, scene, family: observed |
| `\AblDropPeopleSceneFamNull{}` | 44.5\% | ablation drop_people, scene, family: null mean |
| `\AblDropPeopleSceneFamZ{}` | +3.8 | ablation drop_people, scene, family: z |
| `\AblDropSceneEmoSignObs{}` | 64.2\% | ablation drop_scene, emotional, vsign: observed |
| `\AblDropSceneEmoSignNull{}` | 46.0\% | ablation drop_scene, emotional, vsign: null mean |
| `\AblDropSceneEmoSignZ{}` | +10.7 | ablation drop_scene, emotional, vsign: z |
| `\AblDropSceneEmoFamObs{}` | 53.4\% | ablation drop_scene, emotional, family: observed |
| `\AblDropSceneEmoFamNull{}` | 39.2\% | ablation drop_scene, emotional, family: null mean |
| `\AblDropSceneEmoFamZ{}` | +9.8 | ablation drop_scene, emotional, family: z |
| `\AblDropSceneFaceSignObs{}` | 74.4\% | ablation drop_scene, face, vsign: observed |
| `\AblDropSceneFaceSignNull{}` | 53.8\% | ablation drop_scene, face, vsign: null mean |
| `\AblDropSceneFaceSignZ{}` | +10.4 | ablation drop_scene, face, vsign: z |
| `\AblDropSceneFaceFamObs{}` | 62.4\% | ablation drop_scene, face, family: observed |
| `\AblDropSceneFaceFamNull{}` | 46.1\% | ablation drop_scene, face, family: null mean |
| `\AblDropSceneFaceFamZ{}` | +10.1 | ablation drop_scene, face, family: z |
| `\AblDropSceneSceneSignObs{}` | 42.4\% | ablation drop_scene, scene, vsign: observed |
| `\AblDropSceneSceneSignNull{}` | 29.9\% | ablation drop_scene, scene, vsign: null mean |
| `\AblDropSceneSceneSignZ{}` | +5.6 | ablation drop_scene, scene, vsign: z |
| `\AblDropSceneSceneFamObs{}` | 35.6\% | ablation drop_scene, scene, family: observed |
| `\AblDropSceneSceneFamNull{}` | 26.8\% | ablation drop_scene, scene, family: null mean |
| `\AblDropSceneSceneFamZ{}` | +3.9 | ablation drop_scene, scene, family: z |
| `\AblFixedExpressionEmoSignObs{}` | 15.1\% | ablation fixed_expression, emotional, vsign: observed |
| `\AblFixedExpressionEmoSignNull{}` | 10.8\% | ablation fixed_expression, emotional, vsign: null mean |
| `\AblFixedExpressionEmoSignZ{}` | +5.9 | ablation fixed_expression, emotional, vsign: z |
| `\AblFixedExpressionEmoFamObs{}` | 21.3\% | ablation fixed_expression, emotional, family: observed |
| `\AblFixedExpressionEmoFamNull{}` | 17.5\% | ablation fixed_expression, emotional, family: null mean |
| `\AblFixedExpressionEmoFamZ{}` | +3.9 | ablation fixed_expression, emotional, family: z |
| `\AblFixedExpressionFaceSignObs{}` | 17.5\% | ablation fixed_expression, face, vsign: observed |
| `\AblFixedExpressionFaceSignNull{}` | 12.8\% | ablation fixed_expression, face, vsign: null mean |
| `\AblFixedExpressionFaceSignZ{}` | +4.4 | ablation fixed_expression, face, vsign: z |
| `\AblFixedExpressionFaceFamObs{}` | 25.1\% | ablation fixed_expression, face, family: observed |
| `\AblFixedExpressionFaceFamNull{}` | 19.7\% | ablation fixed_expression, face, family: null mean |
| `\AblFixedExpressionFaceFamZ{}` | +4.0 | ablation fixed_expression, face, family: z |
| `\AblFixedExpressionSceneSignObs{}` | 10.0\% | ablation fixed_expression, scene, vsign: observed |
| `\AblFixedExpressionSceneSignNull{}` | 6.6\% | ablation fixed_expression, scene, vsign: null mean |
| `\AblFixedExpressionSceneSignZ{}` | +2.8 | ablation fixed_expression, scene, vsign: z |
| `\AblFixedExpressionSceneFamObs{}` | 13.7\% | ablation fixed_expression, scene, family: observed |
| `\AblFixedExpressionSceneFamNull{}` | 11.2\% | ablation fixed_expression, scene, family: null mean |
| `\AblFixedExpressionSceneFamZ{}` | +1.5 | ablation fixed_expression, scene, family: z |
| `\AblPeopleAwareEmoSignObs{}` | 51.7\% | ablation people_aware, emotional, vsign: observed |
| `\AblPeopleAwareEmoSignNull{}` | 36.9\% | ablation people_aware, emotional, vsign: null mean |
| `\AblPeopleAwareEmoSignZ{}` | +10.1 | ablation people_aware, emotional, vsign: z |
| `\AblPeopleAwareEmoFamObs{}` | 47.1\% | ablation people_aware, emotional, family: observed |
| `\AblPeopleAwareEmoFamNull{}` | 34.5\% | ablation people_aware, emotional, family: null mean |
| `\AblPeopleAwareEmoFamZ{}` | +8.8 | ablation people_aware, emotional, family: z |
| `\AblPeopleAwareFaceSignObs{}` | 73.9\% | ablation people_aware, face, vsign: observed |
| `\AblPeopleAwareFaceSignNull{}` | 53.5\% | ablation people_aware, face, vsign: null mean |
| `\AblPeopleAwareFaceSignZ{}` | +10.4 | ablation people_aware, face, vsign: z |
| `\AblPeopleAwareFaceFamObs{}` | 61.9\% | ablation people_aware, face, family: observed |
| `\AblPeopleAwareFaceFamNull{}` | 45.8\% | ablation people_aware, face, family: null mean |
| `\AblPeopleAwareFaceFamZ{}` | +10.3 | ablation people_aware, face, family: z |
| `\AblPeopleAwareSceneSignObs{}` | 4.7\% | ablation people_aware, scene, vsign: observed |
| `\AblPeopleAwareSceneSignNull{}` | 3.4\% | ablation people_aware, scene, vsign: null mean |
| `\AblPeopleAwareSceneSignZ{}` | +1.6 | ablation people_aware, scene, vsign: z |
| `\AblPeopleAwareSceneFamObs{}` | 18.0\% | ablation people_aware, scene, family: observed |
| `\AblPeopleAwareSceneFamNull{}` | 17.3\% | ablation people_aware, scene, family: null mean |
| `\AblPeopleAwareSceneFamZ{}` | +0.6 | ablation people_aware, scene, family: z |
| `\AblPeopleAwareNoExpressionEmoSignObs{}` | 55.3\% | ablation people_aware_no_expression, emotional, vsign: observed |
| `\AblPeopleAwareNoExpressionEmoSignNull{}` | 39.5\% | ablation people_aware_no_expression, emotional, vsign: null mean |
| `\AblPeopleAwareNoExpressionEmoSignZ{}` | +10.5 | ablation people_aware_no_expression, emotional, vsign: z |
| `\AblPeopleAwareNoExpressionEmoFamObs{}` | 48.1\% | ablation people_aware_no_expression, emotional, family: observed |
| `\AblPeopleAwareNoExpressionEmoFamNull{}` | 35.0\% | ablation people_aware_no_expression, emotional, family: null mean |
| `\AblPeopleAwareNoExpressionEmoFamZ{}` | +9.6 | ablation people_aware_no_expression, emotional, family: z |
| `\AblPeopleAwareNoExpressionFaceSignObs{}` | 73.9\% | ablation people_aware_no_expression, face, vsign: observed |
| `\AblPeopleAwareNoExpressionFaceSignNull{}` | 53.5\% | ablation people_aware_no_expression, face, vsign: null mean |
| `\AblPeopleAwareNoExpressionFaceSignZ{}` | +10.4 | ablation people_aware_no_expression, face, vsign: z |
| `\AblPeopleAwareNoExpressionFaceFamObs{}` | 61.9\% | ablation people_aware_no_expression, face, family: observed |
| `\AblPeopleAwareNoExpressionFaceFamNull{}` | 45.8\% | ablation people_aware_no_expression, face, family: null mean |
| `\AblPeopleAwareNoExpressionFaceFamZ{}` | +10.3 | ablation people_aware_no_expression, face, family: z |
| `\AblPeopleAwareNoExpressionSceneSignObs{}` | 15.9\% | ablation people_aware_no_expression, scene, vsign: observed |
| `\AblPeopleAwareNoExpressionSceneSignNull{}` | 11.6\% | ablation people_aware_no_expression, scene, vsign: null mean |
| `\AblPeopleAwareNoExpressionSceneSignZ{}` | +2.7 | ablation people_aware_no_expression, scene, vsign: z |
| `\AblPeopleAwareNoExpressionSceneFamObs{}` | 21.0\% | ablation people_aware_no_expression, scene, family: observed |
| `\AblPeopleAwareNoExpressionSceneFamNull{}` | 16.8\% | ablation people_aware_no_expression, scene, family: null mean |
| `\AblPeopleAwareNoExpressionSceneFamZ{}` | +2.2 | ablation people_aware_no_expression, scene, family: z |
| `\AblControlEmoSignObs{}` | 64.0\% | ablation control_full_template, emotional, vsign: observed |
| `\AblControlEmoSignNull{}` | 45.6\% | ablation control_full_template, emotional, vsign: null mean |
| `\AblControlEmoSignZ{}` | +11.1 | ablation control_full_template, emotional, vsign: z |
| `\AblControlEmoFamObs{}` | 53.0\% | ablation control_full_template, emotional, family: observed |
| `\AblControlEmoFamNull{}` | 38.8\% | ablation control_full_template, emotional, family: null mean |
| `\AblControlEmoFamZ{}` | +10.3 | ablation control_full_template, emotional, family: z |
| `\AblControlFaceSignObs{}` | 73.9\% | ablation control_full_template, face, vsign: observed |
| `\AblControlFaceSignNull{}` | 53.5\% | ablation control_full_template, face, vsign: null mean |
| `\AblControlFaceSignZ{}` | +10.4 | ablation control_full_template, face, vsign: z |
| `\AblControlFaceFamObs{}` | 61.9\% | ablation control_full_template, face, family: observed |
| `\AblControlFaceFamNull{}` | 45.8\% | ablation control_full_template, face, family: null mean |
| `\AblControlFaceFamZ{}` | +10.3 | ablation control_full_template, face, family: z |
| `\AblControlSceneSignObs{}` | 42.9\% | ablation control_full_template, scene, vsign: observed |
| `\AblControlSceneSignNull{}` | 29.6\% | ablation control_full_template, scene, vsign: null mean |
| `\AblControlSceneSignZ{}` | +5.8 | ablation control_full_template, scene, vsign: z |
| `\AblControlSceneFamObs{}` | 35.6\% | ablation control_full_template, scene, family: observed |
| `\AblControlSceneFamNull{}` | 26.2\% | ablation control_full_template, scene, family: null mean |
| `\AblControlSceneFamZ{}` | +4.4 | ablation control_full_template, scene, family: z |
| `\AblBaselineEmoSignObs{}` | 64.0\% | ablation baseline, emotional, vsign: observed |
| `\AblBaselineEmoSignNull{}` | 45.6\% | ablation baseline, emotional, vsign: null mean |
| `\AblBaselineEmoSignZ{}` | +11.1 | ablation baseline, emotional, vsign: z |
| `\AblBaselineEmoFamObs{}` | 53.0\% | ablation baseline, emotional, family: observed |
| `\AblBaselineEmoFamNull{}` | 38.8\% | ablation baseline, emotional, family: null mean |
| `\AblBaselineEmoFamZ{}` | +10.3 | ablation baseline, emotional, family: z |
| `\AblBaselineFaceSignObs{}` | 73.9\% | ablation baseline, face, vsign: observed |
| `\AblBaselineFaceSignNull{}` | 53.5\% | ablation baseline, face, vsign: null mean |
| `\AblBaselineFaceSignZ{}` | +10.4 | ablation baseline, face, vsign: z |
| `\AblBaselineFaceFamObs{}` | 61.9\% | ablation baseline, face, family: observed |
| `\AblBaselineFaceFamNull{}` | 45.8\% | ablation baseline, face, family: null mean |
| `\AblBaselineFaceFamZ{}` | +10.3 | ablation baseline, face, family: z |
| `\AblBaselineSceneSignObs{}` | 42.9\% | ablation baseline, scene, vsign: observed |
| `\AblBaselineSceneSignNull{}` | 29.6\% | ablation baseline, scene, vsign: null mean |
| `\AblBaselineSceneSignZ{}` | +5.8 | ablation baseline, scene, vsign: z |
| `\AblBaselineSceneFamObs{}` | 35.6\% | ablation baseline, scene, family: observed |
| `\AblBaselineSceneFamNull{}` | 26.2\% | ablation baseline, scene, family: null mean |
| `\AblBaselineSceneFamZ{}` | +4.4 | ablation baseline, scene, family: z |
| `\AblControlChanged{}` | 0 | top-1 readings changed by the control re-run |
| `\AblDropExpressionSurprise{}` | 514 | drop_expression: records read as surprise |
| `\AblDropExpressionNeutral{}` | 368 | drop_expression: records read as neutral |
| `\AblDropExpressionChanged{}` | 671 | drop_expression: top-1 readings changed vs baseline |
| `\AblationAvailable{}` | yes | ablation summary present |
| `\HumanCheckAvailable{}` | no | human check scored |
