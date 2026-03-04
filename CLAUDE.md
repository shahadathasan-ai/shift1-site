# CLAUDE.md — Shift1 Productions

This file provides context to Claude Code when working on the Shift1 project.

## What Shift1 Is

A creative production company. Portfolio site for original writing across formats — screenplays, novels, animation, short stories. Not a studio with employees, more like a personal creative brand / production label.

**Brand name origin:** "Shift1" — the "1" replaces the "I" in SHIFT. Hidden easter egg: "SH" = Shahadat Hasan's initials. Don't point this out anywhere on the site — it's a discovery, not a declaration.

**Domain:** shift1.co (live, Cloudflare registrar, auto-renewing)
**Email:** stories@shift1.co (forwards to personal Gmail via Cloudflare Email Routing)
**Hosting:** GitHub Pages (repo: shahadathasan-ai/shift1-site), HTTPS enforced
**GitHub:** shahadathasan-ai

## Brand & Design

- **Style:** Dark, minimal, sleek, cinematic. Not techy, not corporate.
- **Colour palette:** Near-black background (#0b0b0b), off-white text (#e8e4de), bright gold accent (#e8d5a3)
- **Fonts:** Space Grotesk (headings, logo), Inter (body)
- **Logo:** "SH1FT" in Space Grotesk Bold, the "1" in accent colour. TM symbol in footer only.
- **Favicon:** SVG, black square with "S" white + "1" gold
- **Background effect:** Firefly particles — warm gold dots that pulse and wander.

## Site Structure

### index.html (main page)
- Hero: Full-screen logo + "Productions" subtitle + "Stories" scroll hint with bouncing arrow
- Projects section: "Selected Stories" heading, "Features, pilots, novels, short stories — the best fit for the idea."
- 7 project cards: NYC Midnight (flip, links to nyc-midnight.html), Icarus (flip), Shuffle (flip), Lion Street (flip), Bombshell (no-flip), God has No Family (no-flip), Nostradamus (no-flip)
- Contact: stories@shift1.co
- Footer: copyright with TM

### nyc-midnight.html
- NYC Midnight competition entries page
- Left sidebar: competition list (Scary Story, Short Story, Screenwriting 2026, Screenwriting 2025)
- Click a competition → rounds panel on right with constraints, loglines, "Read the story" links
- Scary Story rounds 1 & 2 show green "Advanced" badge
- On mobile, tapping a competition auto-scrolls to the rounds panel

### read/viewer.html
- Single PDF.js viewer replacing all individual reader pages
- Hash-based routing: viewer.html#story-id
- PDF.js v3.11.174 from CDN, renders to canvas with retina support
- Navigation: arrow buttons, keyboard arrows, swipe on mobile, Escape to go back
- Click outside PDF goes back to nyc-midnight.html
- Constraint pills stacked vertically, left-aligned on desktop, hidden on mobile

### read/pdfs/
- 6 PDFs with clean filenames: dont-answer.pdf, oops.pdf, confession-114.pdf, feed.pdf, first-words.pdf, eau-de-prince.pdf

## Files in This Folder

```
shift1/
├── CLAUDE.md               ← this file
├── index.html              ← main site (dark, fireflies)
├── nyc-midnight.html       ← competition entries page
├── favicon.svg             ← S1 browser tab icon
├── read/
│   ├── viewer.html         ← PDF.js reader (hash-routed)
│   └── pdfs/               ← 6 story PDFs
├── Writing /
│   ├── Writing Ideas.xlsx  ← master list of all story ideas
│   └── NYC Midnight/       ← competition PDFs (source copies) + judge feedback PDFs
├── index-light.html        ← light mode version (reference only)
├── logo-options.html       ← logo variations (reference only)
├── particle-options.html   ← particle effects (reference only)
```

## Writing Ideas (from Writing Ideas.xlsx)

Master spreadsheet of all story concepts. Last column has comments from Rose (RG).

### On the website (with synopses visible)
| Title | Genre | Format | Status |
|-------|-------|--------|--------|
| **Icarus** | Comedy / Sci-Fi | Animated Series | In Progress |
| **Shuffle** | Horror | Feature | In Progress |
| **Lion Street** | Biopic | Novel | In Progress |

### On the website (title + genre only, no synopsis shown)
| Title | Genre | Format |
|-------|-------|--------|
| **Bombshell** | Comedy | Feature |
| **God has No Family** | Thriller / Sci-Fi | Feature |
| **Nostradamus** | Romantic Comedy | Feature |

### Not on the website
| Title | Genre | Format | Seed |
|-------|-------|--------|------|
| **Asphodel Meadows** | Psychological | Feature | False memories, not knowing if what you see is real |
| **Melting Point** | Thriller | Series | Women in non-traditional roles; wife becomes firefighter after husband dies on duty |
| **21grams** | Drama / Comedy | Feature/Series | 21.3g = weight lost at death (weight of a soul); spirits force suicidal loner to fix their unresolved issues |
| **Rot** | Psychological / Horror | Feature | Based on Zaqqum (Islamic tree of hell); newlyweds move to idyllic town, things go wrong |
| **Maalik** | Thriller | Feature/Series | Infiltrating a terrorist org from inside; how much soul do you lose |
| **Griot** | Psychological | Feature | 500-year space journey, last man who remembers Earth |
| **Abacus** | Thriller / Sci-Fi | Feature | Karma as scientific formula; Orwellian future where good/bad is calculated |
| **Dreams** | Sci-Fi | Feature/Series | Alternate life during sleep; addiction to dream lives |
| **Take a Ticket** | Comedy | Feature | DMV that licenses superpowers; pencil pushers vs villains after clerical error |
| **Unlikely Sequels** | Comedy | Animated Episodic | Taking movie endings and making unlikely sequels |
| **Caller Unknown** | Comedy | Feature | Anonymous helpful phone calls from unknown number |
| **Hope** | Comedy | Feature | Woman searching for lost daughter; actually in a coma, must delve through past to escape |
| **Untitled (Proxima)** | Sci-Fi | Feature | Spacecraft sent to distant star will be overtaken by later, faster ships — would early crews sabotage? |
| **Shots Fired** | — | — | Title only |
| **Turn off the lights** | — | — | Title only |

### Rose's comments (RG)
- **Bombshell:** "LOVE, very Sartre 'No Exit'"
- **Shuffle:** "Use your actual story, needle pokes him and then an entity materializes and starts following him"
- **God has No Family:** "Like this one, what if it's a son he didn't know about? He kills his family but doesn't feel the power he should, then he finds out he actually has a bastard out there somewhere. In the process of seeking him out to kill him, he has a change of heart?"
- **Nostradamus:** "If you leaned into the nihilism of this, could be very interesting"
- **Lion Street:** "I want to know more!"

## Writing Craft Profile

Confirmed strengths and weaknesses from NYC Midnight judge feedback across multiple entries. Reference these when developing or reviewing any writing in this project.

### Confirmed Strengths
- **Format innovation / structural experimentation:** Diary entries, case file interleaving, timestamped confessional footage. Judges consistently praise structural choices as differentiators.
- **Atmospheric writing and sensory detail:** "Wind scrapes the stone like teeth," "Cold air tastes like pond water." Judges highlight specific sensory lines as standout moments.
- **Psychological tension and dread:** Strongest when horror comes from implication and absence, not explicit threat.
- **Language economy and punchy prose:** Clipped sentence structure, breathless pacing, "form that reads almost like poetry."
- **Strong high-concept premises:** "What if" hooks that reveal something true about human nature.
- **Characterisation in few words:** "Approval? We demand. We receive." — judges note ability to establish character swiftly.
- **Comedy voice:** "Eau de Prince" demonstrates sharp comedic voice, world-building, and romantic structure with wit and warmth.

### Known Weaknesses (flag these actively)
- **Over-explaining / exposition dumping:** Tends to tell what the scene should show. Judges flagged this in "Don't Answer" (told outright someone is there when it can be inferred) and "Feed" (prose describing internal states the audience can't see on screen). #1 thing to catch.
- **Subtlety calibration:** Plants clever, subtle clues but sometimes they're too invisible. In "Oops," the title's meaning wasn't clear to all judges, and one felt the connection between cases and the protagonist's affair didn't land. Active craft tension: how to make something discoverable without being invisible.
- **Tonal consistency:** When mixing darkness with humour/irony, tone can tip too far. In "Oops," one judge felt the ending planted the story in comedy when that wasn't the intention.
- **Pacing rushes:** Transitions can feel unearned or compressed. "Feed" needed earlier notes of dread rather than front-loading the reveal.
- **Screenwriting-specific — unfilmable prose:** Poetic language that describes things the audience won't see or hear. In screenwriting, every line needs to translate to screen.
- **Can get too clever with format:** Format innovation is a genuine strength but can tip into being clever for its own sake.

### Style & Taste
- Darkness, moral complexity, psychological horror over gore
- Where literary fiction meets genre
- Stories that work on multiple levels — surface plot plus deeper thematic resonance
- Values craft, structure, and economy of language

## NYC Midnight Competitions

Competition data stored as JS object in nyc-midnight.html. Loglines match the actual PDF title pages.

| Competition | Format | Rounds | Stories |
|-------------|--------|--------|---------|
| Scary Story Challenge 2025 | 400 words, 48 hours | 3 | Don't Answer (R1, Advanced), Oops (R2, Advanced), Confession 114 (Final) |
| Short Story Challenge 2026 | 2,000 words, 8 days (R1) | 1 | Eau de Prince |
| Screenwriting Challenge 2026 | 10 pages, 8 days (R1) | 1 | First Words |
| Screenwriting Challenge 2025 | 12 pages, 8 days (R1) | 1 | Feed |

### Judge Feedback Summaries

Feedback PDFs stored alongside story PDFs in `Writing /NYC Midnight/` subfolders.

**Don't Answer (Scary Story R1) — Advanced**
- Praised: eerie atmosphere, sensory writing, diary format as structural innovation, absence of physical presence creating more terror than explicit threat, ending packs a punch, "breathless" and "reads almost like poetry"
- Flagged: could further address *why* he killed Meg (more on the resentment), redundancies to trim (e.g. being told outright someone is there), could vary sentence fragment length more, protagonist recognises "her" too quickly

**Oops (Scary Story R2) — Advanced**
- Praised: compelling mystery, clean formatting, punchy noir voice, deft shifts between cases/insight/phone calls, original and eerie concept, dread has room to build
- Flagged: needs more hint of detective's personal paranoia driving him, "oops" title meaning wasn't clear to all judges, confusing images near the end ("The door is open..." paragraph), one judge felt ending tipped into unintended comedy, connection between cases and protagonist's affair didn't fully land

**Feed (Screenwriting 2025) — Did not advance**
- Praised: immediate intriguing hook, language economy in characterisation, strong character intros (Ashcombe, Aunt Maeve), doppelganger twist well-executed, contrast between luxury and danger, ending leaves resolution to imagination
- Flagged: too much poetic/unfilmable prose (internal states audience can't see on screen), needs earlier notes of dread and horror (too straightforward until Thomas conversation), lords could express different "flavours" of bigotry, minor grammar/formatting errors

**Confession 114 (Scary Story Final) — Feedback not yet received**
**Eau de Prince (Short Story 2026) — Feedback not yet received**
**First Words (Screenwriting 2026) — Feedback not yet received**

## Upcoming Competitions

Potential sources of new site content. Deadlines relevant to Shift1.

| Competition | Deadline | Format |
|-------------|----------|--------|
| PAGE Awards | Apr 15, 2026 | Screenplays (10 genre categories) |
| Bridport Prize | May 31, 2026 | Short story up to 5,000 words |
| Austin Film Festival | May 27, 2026 (late) | Features, TV pilots, shorts |
| Zoetrope Screenplay | Sep 9, 2026 | Features, TV/streaming pilots |
| Zoetrope Short Fiction | ~Oct 2026 | Up to 5,000 words |
| Sundance Episodic Lab | ~Summer 2026 | Pilot script + series proposal (target: Icarus) |

## Deployment Workflow

1. Edit files locally in `/Users/shahadat.hasan/claude-projects/shift1/`
2. `git add` + `git commit` + `git push` from the shift1 folder
3. GitHub Pages auto-deploys in ~30 seconds
4. Hard refresh browser to see changes (Cmd+Shift+R on desktop)
