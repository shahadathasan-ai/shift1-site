/* SHUFFLE title sequence — timing engine.
   Single source of truth shared by shuffle-sequence.html (approval preview)
   and shuffle-render.html (frame-accurate export). Everything is a pure
   function of time, defined in frames at 24fps. */
(function (root) {
/* ══════════════════════════════════════════════════════════════════
   SEQUENCE ENGINE — pure function of time, shared by preview + render
   ══════════════════════════════════════════════════════════════════ */
const WORD = 'SHUFFLE', N = 7;
const BATS_TEXT = 'BASED ON A TRUE STORY';
const UNEVEN = [0.985, 1.0, 0.975, 0.995, 0.965, 1.0, 0.98];

/* Option 6 "Tube" / stubborn ignition.
   Defined in FRAMES at 24fps, not seconds: every strike and the electrical cut
   land exactly on a frame boundary, so each flash occupies a known whole number
   of frames and the CLICK can be cut to frame in Resolve. The rhythm is the
   approved Option 6 choreography, snapped to the grid. */
const FPS = 24, fr = n => n / FPS;

const IGN = {
  glow: { f0: 6, f1: 9, lvl: 0.07, set: [0, 6], soft: true },   // cathodes warming, outer letters
  strikes: [
    { f0: 11, f1: 13, lvl: 0.58, set: [1, 2, 3] },              // 2f — H U F
    { f0: 15, f1: 17, lvl: 0.82, set: [0, 1, 4, 5, 6] },         // 2f — S H . . F L E
    { f0: 17, f1: 20, lvl: 0.14, set: 'all', soft: true },       // 3f — faint whole-word ghost
    /* ── dead beat: f19 → f25, six black frames (0.25s) ── */
    { f0: 25, f1: 27, lvl: 0.92, set: [0, 1, 2, 3, 5, 6] },      // 2f — all but the second F
    { f0: 29, f1: 30, lvl: 1.00, set: 'all' },                   // 1f — full blink
    { f0: 30, f1: 31, lvl: 0.30, set: 'all' },                   // 1f — collapse
    { f0: 31, f1: 33, lvl: 0.86, set: 'all' },                   // 2f — unstable
    { f0: 36, f1: 38, lvl: 0.42, set: [2, 3, 4] },               // 2f — U F F only
    { f0: 38, f1: 40, lvl: 0.95, set: 'all' }                    // 2f — final gasp
    /* ── two black frames f40 → f42 before it truly catches ── */
  ],
  catchF: 42,   // full ignition
  cutF: 66      // hard electrical cut (burn = 24f = exactly 1.000s)
};
IGN.catch = fr(IGN.catchF);
IGN.cut = fr(IGN.cutF);
IGN.strikes.forEach(s => { s.t0 = fr(s.f0); s.t1 = fr(s.f1); });
IGN.glow.t0 = fr(IGN.glow.f0); IGN.glow.t1 = fr(IGN.glow.f1);

/* Downstream timing in frames too, so the whole sequence is grid-locked:
   beat 11f = 0.458s · fade-in 11f · hold 36f = 1.500s · fade-out 12f = 0.500s */
const SEQ = { fps: FPS, beatF: 11, inF: 11, holdF: 36, outF: 12, tailF: 2 };
SEQ.cutF      = IGN.cutF;                    // 66
SEQ.batsT0F   = SEQ.cutF + SEQ.beatF;        // 77
SEQ.batsFullF = SEQ.batsT0F + SEQ.inF;       // 88
SEQ.batsOutF  = SEQ.batsFullF + SEQ.holdF;   // 124
SEQ.batsEndF  = SEQ.batsOutF + SEQ.outF;     // 136
SEQ.framesF   = SEQ.batsEndF + SEQ.tailF;    // 138
SEQ.cut = fr(SEQ.cutF);          SEQ.beat = fr(SEQ.beatF);
SEQ.batsT0 = fr(SEQ.batsT0F);    SEQ.batsIn = fr(SEQ.inF);
SEQ.batsFull = fr(SEQ.batsFullF);SEQ.batsHold = fr(SEQ.holdF);
SEQ.batsOutT = fr(SEQ.batsOutF); SEQ.batsOut = fr(SEQ.outF);
SEQ.batsEnd = fr(SEQ.batsEndF);  SEQ.tail = fr(SEQ.tailF);
SEQ.total  = fr(SEQ.framesF);                // 5.750s
SEQ.frames = SEQ.framesF;                    // 138
const BATS_PEAK = 0.62;

function inSet(s, i) { return s === 'all' || s.indexOf(i) !== -1; }
function edge(t, t0, t1, soft) {
  if (t < t0 || t >= t1) return 0;
  if (!soft) return 1;
  const r = Math.min(1 / FPS, (t1 - t0) / 3);   // ~1 frame ramp
  if (t < t0 + r) return (t - t0) / r;
  if (t > t1 - r) return (t1 - t) / r;
  return 1;
}
const smooth   = x => x * x * (3 - 2 * x);
const smoother = x => x * x * x * (x * (x * 6 - 15) + 10);

/* SHUFFLE brightness, 0 .. ~1.18 */
function shuffleAt(t, i) {
  if (t < 0) return 0;
  if (t >= IGN.cut) {
    const tail = 1 / FPS;                           // single-frame phosphor tail
    if (t < IGN.cut + tail) return 0.10 * (1 - (t - IGN.cut) / tail) * UNEVEN[i];
    return 0;
  }
  if (t >= IGN.catch) {
    const df = (t - IGN.catch) * FPS;   // in frames, so the overshoot is visible
    let b;
    if (df < 1) b = 1.0 + 0.18 * df;                     // 1f rise into overshoot
    else if (df < 4) b = 1.18 - 0.18 * ((df - 1) / 3);   // 3f settle
    else b = 1.0;
    b *= 1 + 0.011 * Math.sin(2 * Math.PI * 100 * t);        // subliminal mains ripple
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

/* Second card opacity — no flicker, gentle in, smooth out */
function batsAt(t) {
  if (t < SEQ.batsT0 || t >= SEQ.batsEnd) return 0;
  if (t < SEQ.batsFull) return BATS_PEAK * smoother((t - SEQ.batsT0) / SEQ.batsIn);
  if (t < SEQ.batsOutT) return BATS_PEAK;
  return BATS_PEAK * (1 - smooth((t - SEQ.batsOutT) / SEQ.batsOut));
}

  root.ShuffleEngine = {
    WORD: WORD, N: N, BATS_TEXT: BATS_TEXT, UNEVEN: UNEVEN,
    FPS: FPS, fr: fr, IGN: IGN, SEQ: SEQ, BATS_PEAK: BATS_PEAK,
    shuffleAt: shuffleAt, batsAt: batsAt
  };
})(typeof window !== 'undefined' ? window : globalThis);
