"""SHUFFLE title sound design — fully procedural synthesis.

Every sample is computed from oscillators, seeded pseudo-random noise and
IIR filters written here. No samples, no library recordings, no stock SFX:
nothing enters this file but numbers. Festival-safe by construction.

Half-speed timebase: 196 output frames at 24fps = 8.1667s.
Engine frame f maps to output time f/12.
"""
import wave, struct, math, random

SR      = 48000
FPS     = 24
FRAMES  = 196          # half speed
DUR     = FRAMES / FPS # 8.16667s
N       = int(SR * DUR)
SPEED   = 2            # engine frame -> out time = f / (FPS/SPEED) = f/12
ef      = lambda f: f / (FPS / SPEED)   # engine frame -> output seconds

# ── event times, derived from the engine, not hand-typed ──
T_GLOW   = ef(6)     # 0.500  ignition begins
T_CATCH  = ef(42)    # 3.500  tube finally catches
T_CLICK  = ef(66)    # 5.500  the CLICK — hum stops dead
T_END    = ef(98)    # 8.167

# ── levels (linear). Deliberately low: "subtle and expensive" ──
L_BUZZ    = 0.020    # ballast bed under the failed ignition
L_CRACKLE = 0.034    # irregular struggle crackle
L_BZZZT   = 0.088    # the catch
L_HUM     = 0.0058   # stable burn — almost subliminal
L_CLICK   = 0.230    # the one real transient

MAINS = 120.0        # 60Hz mains -> 120Hz ballast fundamental

rng = random.Random(20260912)   # seeded: identical output every run

# ── helpers ──────────────────────────────────────────────────────────
def onepole_lp(buf, cutoff):
    a = math.exp(-2.0 * math.pi * cutoff / SR); y = 0.0
    for i in range(len(buf)):
        y = (1 - a) * buf[i] + a * y
        buf[i] = y
    return buf

def onepole_hp(buf, cutoff):
    a = math.exp(-2.0 * math.pi * cutoff / SR)
    y = 0.0; prev = 0.0
    for i in range(len(buf)):
        y = a * (y + buf[i] - prev); prev = buf[i]; buf[i] = y
    return buf

def smoothstep(x):
    x = 0.0 if x < 0 else (1.0 if x > 1 else x)
    return x * x * (3 - 2 * x)

L = [0.0] * N
R = [0.0] * N

# ── 1. BALLAST BED  (T_GLOW → T_CATCH) ───────────────────────────────
# Magnetic ballast buzz: 120Hz plus odd-weighted harmonics, slightly
# unstable in pitch. One continuous bed with slow swells — NOT one event
# per visual flicker, so it never mimics the elevator cue.
HARM = [(1, 1.00), (2, 0.52), (3, 0.34), (4, 0.20), (5, 0.13), (6, 0.08)]
i0, i1 = int(T_GLOW * SR), int(T_CATCH * SR)
phase = [0.0] * len(HARM)
for i in range(i0, i1):
    t = i / SR
    p = (t - T_GLOW) / (T_CATCH - T_GLOW)          # 0..1 across the struggle
    drift = 1.0 + 0.0045 * math.sin(2 * math.pi * 0.63 * t)   # pitch instability
    s = 0.0
    for k, (mult, amp) in enumerate(HARM):
        phase[k] += 2 * math.pi * MAINS * mult * drift / SR
        s += amp * math.sin(phase[k])
    s /= 2.3
    # slow swells: the tube trying and losing it, on its own timescale
    swell = (0.42 + 0.58 * (0.5 + 0.5 * math.sin(2 * math.pi * 0.47 * t - 1.1)))
    swell *= (0.55 + 0.45 * p)                      # builds toward the catch
    env = smoothstep((t - T_GLOW) / 0.30) * swell   # ease in, no click-on
    v = s * env * L_BUZZ
    L[i] += v; R[i] += v

# ── 2. STRUGGLE CRACKLE ──────────────────────────────────────────────
# Irregular, sparse, and intentionally NOT aligned to the visual strike
# frames. Gaps are randomised with no repeating interval, so there is no
# rhythm to latch onto.
strike_times = [ef(f) for f in (11, 15, 17, 25, 29, 30, 31, 36, 38)]
events, t = [], T_GLOW + 0.21
while t < T_CATCH - 0.06:
    if all(abs(t - s) > 0.045 for s in strike_times):   # avoid the flicker frames
        events.append(t)
    t += rng.uniform(0.075, 0.34)                       # irregular, non-periodic

for et in events:
    dur = rng.uniform(0.0035, 0.011)
    n = int(dur * SR)
    burst = [rng.uniform(-1, 1) for _ in range(n)]
    burst = onepole_hp(onepole_lp(burst, rng.uniform(2600, 5200)), 900)
    amp = L_CRACKLE * rng.uniform(0.30, 1.0)
    pan = rng.uniform(-0.22, 0.22)                       # a little air, still centred
    s0 = int(et * SR)
    for j in range(n):
        if s0 + j >= N: break
        d = math.exp(-j / (n * 0.34))                   # fast exponential decay
        v = burst[j] * d * amp
        L[s0 + j] += v * (1 - max(0.0, pan))
        R[s0 + j] += v * (1 + min(0.0, pan))

# ── 3. THE CATCH — one stronger, still realistic bzzzt ───────────────
BZ = 0.150
n = int(BZ * SR)
s0 = int(T_CATCH * SR)
ph = [0.0] * 8
for j in range(n):
    t = T_CATCH + j / SR
    a = smoothstep(j / (0.004 * SR))                    # 4ms attack
    d = math.exp(-j / (n * 0.42))
    s = 0.0
    for k in range(8):                                  # richer harmonics than the bed
        ph[k] += 2 * math.pi * MAINS * (k + 1) * (1.0 + 0.002 * math.sin(2 * math.pi * 41 * t)) / SR
        s += math.sin(ph[k]) / (k + 1.35)
    nz = rng.uniform(-1, 1) * 0.33 * math.exp(-j / (n * 0.16))
    v = (s / 2.1 + nz) * a * d * L_BZZZT
    if s0 + j < N:
        L[s0 + j] += v; R[s0 + j] += v

# ── 4. STABLE BURN HUM  (T_CATCH → T_CLICK) ──────────────────────────
# Extremely quiet. Present enough that its removal at the CLICK is felt.
i0, i1 = int(T_CATCH * SR), int(T_CLICK * SR)
ph = [0.0, 0.0, 0.0]
for i in range(i0, i1):
    t = i / SR
    s = 0.0
    for k, amp in enumerate((1.0, 0.42, 0.13)):
        ph[k] += 2 * math.pi * MAINS * (k + 1) / SR
        s += amp * math.sin(ph[k])
    s /= 1.55
    env = smoothstep((t - T_CATCH) / 0.12)              # emerges out of the bzzzt
    env *= 1.0 + 0.05 * math.sin(2 * math.pi * 0.9 * t) # faint breathing
    v = s * env * L_HUM
    L[i] += v; R[i] += v

# ── 5. THE CLICK — dry, electrical, on the exact frame ───────────────
# Relay-style: a sharp broadband transient with a short damped ring.
# No reverb, no tail. Everything after it is silence.
CK = 0.014
n = int(CK * SR)
s0 = int(T_CLICK * SR)
for j in range(n):
    d_fast = math.exp(-j / (0.0011 * SR))               # the snap
    d_ring = math.exp(-j / (0.0042 * SR))               # small mechanical body
    nz = rng.uniform(-1, 1) * d_fast
    ring = math.sin(2 * math.pi * 2150 * j / SR) * 0.42 * d_ring
    ring += math.sin(2 * math.pi * 3400 * j / SR) * 0.20 * d_ring
    v = (nz + ring) * L_CLICK
    if s0 + j < N:
        L[s0 + j] += v; R[s0 + j] += v
# dry it out: remove anything below 220Hz so there is no thump or bass hit
seg0, seg1 = s0, min(N, s0 + int(0.05 * SR))
for buf in (L, R):
    seg = buf[seg0:seg1]
    onepole_hp(seg, 220)
    buf[seg0:seg1] = seg

# ── 6. ENFORCE SILENCE AFTER THE CLICK ───────────────────────────────
hard = int((T_CLICK + CK + 0.004) * SR)
for i in range(hard, N):
    L[i] = 0.0; R[i] = 0.0

# ── write 24-bit / 48kHz stereo WAV ──────────────────────────────────
peak = max(max(abs(v) for v in L), max(abs(v) for v in R))
print('peak linear  %.4f   (%.1f dBFS)' % (peak, 20 * math.log10(peak)))
assert peak < 0.95, 'clipping'

out = bytearray()
for i in range(N):
    for v in (L[i], R[i]):
        q = int(max(-1.0, min(1.0, v)) * 8388607)
        out += struct.pack('<i', q)[0:3]          # 24-bit little-endian

w = wave.open('shuffle_audio.wav', 'wb')
w.setnchannels(2); w.setsampwidth(3); w.setframerate(SR)
w.writeframes(bytes(out)); w.close()

print('crackle events: %d over %.2fs (mean gap %.3fs, no fixed interval)'
      % (len(events), T_CATCH - T_GLOW, (T_CATCH - T_GLOW) / max(1, len(events))))
print('wrote shuffle_audio.wav  %.4fs  %d frames @ %dfps  24-bit/%dkHz stereo'
      % (DUR, FRAMES, FPS, SR // 1000))
