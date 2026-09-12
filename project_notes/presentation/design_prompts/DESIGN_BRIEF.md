# EmoViz — Design Brief

*Paste this into Claude Design (claude.ai → Design) to generate UI for the demo app.*

---

## What it is
A public web demo for an MSc research project at the University of Sheffield.
It answers one question: **when an AI draws a feeling someone described, does the drawing
actually feel that way?**

## The story behind it
At a science festival, ~1,000 members of the public typed how they were feeling. An AI
(DALL·E) drew each one as a black-and-white line drawing. This tool lets anyone compare the
feeling in the **words** with the feeling in the **drawing**.

## Who uses it
Complete non-experts — festival visitors, students, the supervisor, anyone given a link.
They know nothing about AI. **Design for someone who lands on it, understands it in 10
seconds, and can use it without instructions.**

## The user flow — 3 steps, one screen
1. **Choose a drawing** — pick one of 6 examples, get a random one, load one by number, or
   upload their own image.
2. **The words** — a text box, pre-filled with what that person actually typed. The user can
   edit it or tap a suggested phrase (e.g. *"tired but happy"*).
3. **Compare** — one button. Results appear below.

## What the results show
- **What the AI saw** — plain observed facts: facial expression, action, posture, how many
  people, what's in the picture. Plus a one-sentence description.
- **The two feelings** — side-by-side readouts: emotion from the **words** vs emotion from the
  **drawing**. Each shows the top 3 emotions with percentages.
- **The verdict** — a similarity score out of 100, a plain-English sentence (e.g. *"The drawing
  carries the same feeling as the words"*), and three facts: same emotion family? same mood
  direction? how much overlap?

## The key idea to communicate visually
It is **not "right or wrong"** — it is **"how close are these two feelings?"** Happy and excited
count as similar. It should feel like a **measurement**, not a pass/fail test.

## Emotions needing visual identity
`joy` · `sadness` · `anger` · `fear` · `surprise` · `disgust` · `neutral`

## Tone
Calm, credible, scientific but friendly. A **research instrument** — not a game, not a SaaS
landing page. Trustworthy enough to show a professor, simple enough for a curious stranger.

## Must-haves
- Works on phone **and** desktop (most people will open it on a phone).
- Touch targets 44px+ (48px on mobile).
- Strong contrast — text passes **WCAG AA (4.5:1)** in light and dark.
- Clear **hover / focus / active** states on every control.
- An honest **waiting state** — results take a few seconds while an AI runs; never a frozen button.
- A small **status indicator** showing whether the AI models are ready.
- A plain-English **"how it works / limits"** section, including: *nothing you type or upload is stored.*

## Avoid
Purple gradients · centered hero text · three-card rows · decorative blobs · jargon ·
anything that looks like a generic AI-generated landing page.

## Components to design
- Page header with live status indicator
- Hero / intro that explains the idea fast
- 3-step process explainer
- Image chooser (example thumbnails + random + upload)
- Text input with suggested phrases
- Primary action button (with loading state)
- Results: observation list · two emotion readouts with bars · similarity score
- Plain-English explainer section
