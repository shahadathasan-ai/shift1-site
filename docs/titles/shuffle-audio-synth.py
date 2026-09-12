"""SHUFFLE title sound design — fully procedural synthesis.

Every sample is computed here from oscillators, damped resonators and a
seeded PRNG. No samples, no library recordings, no stock SFX.

v2 — TONAL palette. v1 built the struggle from white-noise bursts, which
read as hiss and static, and 11 discrete noise ticks over three seconds
read as a Geiger counter. A failing tube does not crackle broadband; it
arcs, and an arc is tonal. So the attempts are now short bursts of the
ballast harmonic stack with a collapsing pitch, and noise is reduced to a
thin edge on transients only.

Half-speed timebase: 196 output frames at 24fps = 8.1667s.
"""
import wave, struct, math, random, sys

SR     = 48000
FPS    = 24
FRAMES = 196
DUR    = FRAMES / FPS
N      = int(SR * DUR)
SPEED  = 2
ef     = lambda f: f / (FPS / SPEED)

T_GLOW  = ef(6)     # 0.500
T_CATCH = ef(42)    # 3.500
T_CLICK = ef(66)    # 5.500

L_BUZZ   = 0.016    # ballast bed
L_STRIKE = 0.058    # arc attempts (tonal, replaces noise crackle)
L_BZZZT  = 0.088    # the catch
L_HUM    = 0.0058   # stable burn
L_CLICK  = 0.520    # the switch

MAINS = 120.0
OUTFILE = sys.argv[1] if len(sys.argv) > 1 else 'shuffle_audio.wav'
rng = random.Random(20260912)

def onepole_lp(buf, fc):
    a = math.exp(-2 * math.pi * fc / SR); y = 0.0
    for i in range(len(buf)):
        y = (1 - a) * buf[i] + a * y; buf[i] = y
    return buf

def onepole_hp(buf, fc):
    a = math.exp(-2 * math.pi * fc / SR); y = 0.0; p = 0.0
    for i in range(len(buf)):
        y = a * (y + buf[i] - p); p = buf[i]; buf[i] = y
    return buf

def smoothstep(x):
    x = 0.0 if x < 0 else (1.0 if x > 1 else x)
    return x * x * (3 - 2 * x)

L = [0.0] * N
R = [0.0] * N

# ── 1. BALLAST BED ───────────────────────────────────────────────────
HARM = [(1, 1.00), (2, 0.52), (3, 0.34), (4, 0.20), (5, 0.13), (6, 0.08)]
i0, i1 = int(T_GLOW * SR), int(T_CATCH * SR)
ph = [0.0] * len(HARM)
for i in range(i0, i1):
    t = i / SR
    p = (t - T_GLOW) / (T_CATCH - T_GLOW)
    drift = 1.0 + 0.0045 * math.sin(2 * math.pi * 0.63 * t)
    s = 0.0
    for k, (mult, amp) in enumerate(HARM):
        ph[k] += 2 * math.pi * MAINS * mult * drift / SR
        s += amp * math.sin(ph[k])
    s /= 2.3
    swell = 0.42 + 0.58 * (0.5 + 0.5 * math.sin(2 * math.pi * 0.47 * t - 1.1))
    swell *= 0.55 + 0.45 * p
    v = s * smoothstep((t - T_GLOW) / 0.30) * swell * L_BUZZ
    L[i] += v; R[i] += v

# ── 2. ARC ATTEMPTS  (tonal — replaces the noise crackle) ────────────
# Each is a short burst of the ballast stack with a fast attack and a
# collapsing pitch, i.e. an arc striking and losing it. Five events at
# irregular gaps: too few and too long to read as particle clicks.
STRIKES = [0.58, 0.94, 1.71, 2.53, 3.08]
for st in STRIKES:
    dec = rng.uniform(0.030, 0.070)
    n = int((dec * 4) * SR)
    s0 = int(st * SR)
    lph = [0.0] * 6
    amp = L_STRIKE * rng.uniform(0.55, 1.0)
    for j in range(n):
        t = j / SR
        a = smoothstep(t / 0.003)                 # 3ms attack
        d = math.exp(-t / dec)
        fall = 1.0 - 0.16 * (1 - d)               # pitch collapses as the arc dies
        s = 0.0
        for k in range(6):
            lph[k] += 2 * math.pi * MAINS * (k + 1) * fall / SR
            s += math.sin(lph[k]) / (k + 1.5)
        edge = rng.uniform(-1, 1) * 0.08 * math.exp(-t / 0.002)   # thin transient edge
        v = (s / 1.7 + edge) * a * d * amp
        if s0 + j < N:
            L[s0 + j] += v; R[s0 + j] += v

# ── 3. THE CATCH ─────────────────────────────────────────────────────
BZ = 0.150
n = int(BZ * SR); s0 = int(T_CATCH * SR)
ph = [0.0] * 8
for j in range(n):
    t = T_CATCH + j / SR
    a = smoothstep(j / (0.004 * SR)); d = math.exp(-j / (n * 0.42))
    s = 0.0
    for k in range(8):
        ph[k] += 2 * math.pi * MAINS * (k + 1) * (1.0 + 0.002 * math.sin(2 * math.pi * 41 * t)) / SR
        s += math.sin(ph[k]) / (k + 1.35)
    nz = rng.uniform(-1, 1) * 0.10 * math.exp(-j / (n * 0.16))    # was 0.33 — less hiss
    v = (s / 2.1 + nz) * a * d * L_BZZZT
    if s0 + j < N:
        L[s0 + j] += v; R[s0 + j] += v

# ── 4. STABLE HUM ────────────────────────────────────────────────────
i0, i1 = int(T_CATCH * SR), int(T_CLICK * SR)
ph = [0.0, 0.0, 0.0]
for i in range(i0, i1):
    t = i / SR
    s = 0.0
    for k, amp in enumerate((1.0, 0.42, 0.13)):
        ph[k] += 2 * math.pi * MAINS * (k + 1) / SR
        s += amp * math.sin(ph[k])
    s /= 1.55
    env = smoothstep((t - T_CATCH) / 0.12) * (1.0 + 0.05 * math.sin(2 * math.pi * 0.9 * t))
    v = s * env * L_HUM
    L[i] += v; R[i] += v

# ── 5. THE CLICK — band-limited mechanical impact ────────────────────
# A switch is an IMPACT, not a tone and not noise:
#   bright contact snick ~3 kHz  +  housing thock ~420 Hz, ~12 ms, dry.
# Filters are real RBJ biquads cascaded to 24 dB/oct. Earlier versions
# used one-pole filters (6 dB/oct), which barely attenuate — that is why
# "filtered noise" stayed full-band and read as static in the speaker.
# Tuned against a spectrum measurement, not by ear-guessing:
#   centroid 3187 Hz · impact band 54% · thock 19% · hiss 0.9%
def biquad_bp(buf, f0, Q):
    w0 = 2 * math.pi * f0 / SR; al = math.sin(w0) / (2 * Q)
    b0, b1, b2 = Q * al, 0.0, -Q * al
    a0, a1, a2 = 1 + al, -2 * math.cos(w0), 1 - al
    b0, b1, b2, a1, a2 = b0/a0, b1/a0, b2/a0, a1/a0, a2/a0
    x1 = x2 = y1 = y2 = 0.0
    for i, x in enumerate(buf):
        y = b0*x + b1*x1 + b2*x2 - a1*y1 - a2*y2
        x2, x1 = x1, x; y2, y1 = y1, y; buf[i] = y
    return buf

def biquad_hp(buf, f0, Q=0.707):
    w0 = 2 * math.pi * f0 / SR; al = math.sin(w0) / (2 * Q); c = math.cos(w0)
    b0, b1, b2 = (1+c)/2, -(1+c), (1+c)/2
    a0, a1, a2 = 1 + al, -2*c, 1 - al
    b0, b1, b2, a1, a2 = b0/a0, b1/a0, b2/a0, a1/a0, a2/a0
    x1 = x2 = y1 = y2 = 0.0
    for i, x in enumerate(buf):
        y = b0*x + b1*x1 + b2*x2 - a1*y1 - a2*y2
        x2, x1 = x1, x; y2, y1 = y1, y; buf[i] = y
    return buf

def make_click(rms_db=-20.0, seed=4242):
    r = random.Random(seed)
    n = int(0.030 * SR)
    snick = [r.uniform(-1, 1) for _ in range(n)]
    biquad_bp(snick, 3000, 0.65); biquad_bp(snick, 3000, 0.65)
    for i in range(n):
        t = i / SR
        snick[i] *= (1 - math.exp(-t / 0.00025)) * math.exp(-t / 0.0055)
    thock = [r.uniform(-1, 1) for _ in range(n)]
    biquad_bp(thock, 420, 1.4)
    for i in range(n):
        t = i / SR
        thock[i] *= (1 - math.exp(-t / 0.0004)) * math.exp(-t / 0.007)
    out = [snick[i] + 0.30 * thock[i] for i in range(n)]
    biquad_hp(out, 170)                       # dry: no rumble
    rms = math.sqrt(sum(v*v for v in out) / n)
    g = (10 ** (rms_db / 20)) / rms           # set by loudness, not peak
    return [v * g for v in out]

CK = 0.030
click = make_click()
s0 = int(T_CLICK * SR)
for j, v in enumerate(click):
    if s0 + j < N:
        L[s0 + j] += v; R[s0 + j] += v

# ── 6. SILENCE AFTER THE CLICK ───────────────────────────────────────
hard = int((T_CLICK + CK + 0.004) * SR)
for i in range(hard, N):
    L[i] = 0.0; R[i] = 0.0

peak = max(max(abs(v) for v in L), max(abs(v) for v in R))
print('peak %.4f  (%.1f dBFS)   arc attempts: %d' % (peak, 20 * math.log10(peak), len(STRIKES)))
assert peak < 0.95, 'clipping'

out = bytearray()
for i in range(N):
    for v in (L[i], R[i]):
        q = int(max(-1.0, min(1.0, v)) * 8388607)
        out += struct.pack('<i', q)[0:3]
w = wave.open(OUTFILE, 'wb')
w.setnchannels(2); w.setsampwidth(3); w.setframerate(SR)
w.writeframes(bytes(out)); w.close()
print('wrote %s  %.4fs  24-bit/48kHz stereo' % (OUTFILE, DUR))
