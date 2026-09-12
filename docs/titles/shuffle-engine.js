/* SHUFFLE title sequence — timing engine.
   Single source of truth shared by shuffle-sequence.html (approval preview)
   and shuffle-render.html (frame-accurate export). Everything is a pure
   function of time, defined in frames at 24fps. */
(function (root) {

const WORD = 'SHUFFLE', N = WORD.length;
const BATS_TEXT = 'BASED ON A TRUE STORY';

/* Per-letter fixed unevenness — a real tube never lights perfectly evenly.
   Fixed, not random, so any frame is reproducible. */
const UNEVEN = [0.985, 1.0, 0.975, 0.995, 0.965, 1.0, 0.98];

/* ───────────────────────────────────────────────────────────────
   SHUFFLE — Option 6 "Tube" ignition. UNCHANGED.
   Defined in frames at 24fps so every strike and the cut land on a
   whole frame and each flash occupies a known frame count.
   ─────────────────────────────────────────────────────────────── */
const FPS = 24, fr = n => n / FPS;

const IGN = {
  glow: { f0: 6, f1: 9, lvl: 0.07, set: [0, 6], soft: true },   // cathodes warming, outer letters
  strikes: [
    { f0: 11, f1: 13, lvl: 0.58, set: [1, 2, 3] },              // 2f — H U F
    { f0: 15, f1: 17, lvl: 0.82, set: [0, 1, 4, 5, 6] },         // 2f — S H . . F L E
    { f0: 17, f1: 20, lvl: 0.14, set: 'all', soft: true },       // 3f — faint whole-word ghost
    /* ── dead beat: f20 → f25 ── */
    { f0: 25, f1: 27, lvl: 0.92, set: [0, 1, 2, 3, 5, 6] },      // 2f — all but the second F
    { f0: 29, f1: 30, lvl: 1.00, set: 'all' },                   // 1f — full blink
    { f0: 30, f1: 31, lvl: 0.30, set: 'all' },                   // 1f — collapse
    { f0: 31, f1: 33, lvl: 0.86, set: 'all' },                   // 2f — unstable
    { f0: 36, f1: 38, lvl: 0.42, set: [2, 3, 4] },               // 2f — U F F only
    { f0: 38, f1: 40, lvl: 0.95, set: 'all' }                    // 2f — final gasp
    /* ── two black frames f40 → f42 before it truly catches ── */
  ],
  catchF: 42,   // full ignition
  cutF: 66      // the CLICK — burn = 24f = exactly 1.000s
};
IGN.catch = fr(IGN.catchF);
IGN.cut = fr(IGN.cutF);
IGN.strikes.forEach(s => { s.t0 = fr(s.f0); s.t1 = fr(s.f1); });
IGN.glow.t0 = fr(IGN.glow.f0); IGN.glow.t1 = fr(IGN.glow.f1);

/* ───────────────────────────────────────────────────────────────
   THE SWAP — one electrical event, not two cards.
   On cutF exactly: SHUFFLE goes hard to zero (no phosphor tail, or the
   two would be lit on the same frame) and the card switches on at full
   value in the same instant. No black between them, no fade in.
   ─────────────────────────────────────────────────────────────── */
const SEQ = { fps: FPS, holdF: 22, outF: 8, tailF: 2 };
SEQ.swapF     = IGN.cutF;                    // 66 — SHUFFLE off / card on
SEQ.outStartF = SEQ.swapF + SEQ.holdF;       // 88 — card begins to fade
SEQ.endF      = SEQ.outStartF + SEQ.outF;    // 96 — card fully black
SEQ.framesF   = SEQ.endF + SEQ.tailF;        // 98 — total
SEQ.swap = fr(SEQ.swapF);         SEQ.hold = fr(SEQ.holdF);
SEQ.outStart = fr(SEQ.outStartF); SEQ.out = fr(SEQ.outF);
SEQ.end = fr(SEQ.endF);           SEQ.tail = fr(SEQ.tailF);
SEQ.total = fr(SEQ.framesF);                 // 4.0833s
SEQ.frames = SEQ.framesF;                    // 98

const BATS_PEAK = 0.60;   // noticeably dimmer than SHUFFLE's 1.0

function inSet(s, i) { return s === 'all' || s.indexOf(i) !== -1; }
function edge(t, t0, t1, soft) {
  if (t < t0 || t >= t1) return 0;
  if (!soft) return 1;
  const r = Math.min(1 / FPS, (t1 - t0) / 3);   // ~1 frame ramp
  if (t < t0 + r) return (t - t0) / r;
  if (t > t1 - r) return (t1 - t) / r;
  return 1;
}
const smooth = x => x * x * (3 - 2 * x);

/* SHUFFLE brightness, 0 .. ~1.18. Hard zero from the CLICK onward. */
function shuffleAt(t, i) {
  if (t < 0 || t >= IGN.cut) return 0;
  if (t >= IGN.catch) {
    const df = (t - IGN.catch) * FPS;                    // frames, so overshoot is visible
    let b;
    if (df < 1) b = 1.0 + 0.18 * df;                     // 1f rise into overshoot
    else if (df < 4) b = 1.18 - 0.18 * ((df - 1) / 3);   // 3f settle
    else b = 1.0;
    b *= 1 + 0.011 * Math.sin(2 * Math.PI * 100 * t);    // subliminal mains ripple
    return b * UNEVEN[i];
  }
  let lvl = 0;
  if (inSet(IGN.glow.set, i)) lvl = Math.max(lvl, IGN.glow.lvl * edge(t, IGN.glow.t0, IGN.glow.t1, true));
  for (let k = 0; k < IGN.strikes.length; k++) {
    const s = IGN.strikes[k];
    if (inSet(s.set, i)) lvl = Math.max(lvl, s.lvl * edge(t, s.t0, s.t1, s.soft));
  }
  return lvl * UNEVEN[i];
}

/* Card opacity — instant on at the CLICK, hold, then a fairly quick fade. */
function batsAt(t) {
  if (t < SEQ.swap || t >= SEQ.end) return 0;
  if (t < SEQ.outStart) return BATS_PEAK;                                   // instant, no fade in
  return BATS_PEAK * (1 - smooth((t - SEQ.outStart) / SEQ.out));
}

root.ShuffleEngine = {
  WORD: WORD, N: N, BATS_TEXT: BATS_TEXT, UNEVEN: UNEVEN,
  FPS: FPS, fr: fr, IGN: IGN, SEQ: SEQ, BATS_PEAK: BATS_PEAK,
  shuffleAt: shuffleAt, batsAt: batsAt
};
})(typeof window !== 'undefined' ? window : globalThis);
