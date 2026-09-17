# Images still to add by hand

Each item below is a dashed box in the built PDF, produced by `\placeholderfigure{...}` in the
chapter file named. To fill one: save the image into `figures/`, then replace the whole
`\placeholderfigure` line with a normal figure, for example

```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.9\textwidth]{demo_screenshot}
\caption{The demonstrator after running record 63 (``super tired''): the drawing, the five answers, the two readings and the verdict against the chance band.}
\label{fig:demo}
\end{figure}
```

Keep the `\label{...}` exactly as it is, because the text refers to it.

| # | Label | Chapter file | What to capture | Priority |
|---|---|---|---|---|
| 1 | `fig:demo` | `chapters/chapter3.tex`, section "The demonstrator" | Run `bash emoviz/run_interface.sh`, wait for the models to warm (about 40 s), choose record 63 ("super tired"), press Compare, and screenshot the result panel (drawing, five answers, two readings, verdict with the chance band). Save as `figures/demo_screenshot.png`. | Required |
| 2 | `fig:testsuite` | `chapters/appendixA.tex` | Run `bash emoviz/test.sh` in a terminal, wait for the last summary lines (smoke checks and "numeric checks: 54 passed, 0 failed"), screenshot the terminal. Save as `figures/test_suite.png`. | Recommended |
| 3 | `fig:installation` | `chapters/chapter3.tex`, end of section "The corpus" | A photograph of the installation at the Festival of the Mind 2024, if one exists (the screen, or a visitor's drawing being produced). Credit the photographer in the caption. If no photograph is available, delete the `\placeholderfigure` line; nothing else refers to it. | Optional |

Also worth adding if easy: a second demonstrator screenshot showing an uploaded image (any of your
own line drawings) so the examiner sees the upload path works. Put it next to `fig:demo` as a second
figure with a new label, and add one sentence in the demonstrator section pointing to it.

Images that are already in place and need nothing: the six example records, the pipeline diagram,
the dataset composition bar, the per-day timeline, the prompt-length histogram, the first coding
sheet, and the nine results figures (z by group, face vs scene, method comparison, consistency,
"happy" grid, confusion matrix, no-person examples, taxonomy, ablation).

Before submission: fill the Declaration page (name, signature, date) in `main.tex`; if the
single-coder check has been scored, run `bash sync_generated.sh` and replace the pending paragraph
in `chapters/chapter4.tex` (search for `TODO`) with the numbers; add the outcome of the 10 September
meeting to `chapters/appendixC.tex` (search for `TODO`).
