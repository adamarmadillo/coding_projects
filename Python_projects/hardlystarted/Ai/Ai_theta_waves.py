import numpy as np
import pygame

SAMPLE_RATE = 44100
DURATION = 10          # seconds
CARRIER_HZ = 80        # audible tone
THETA_MIN, THETA_MAX = 4, 10   # theta range to sweep
SWEEP_PERIOD = 5        # seconds for one full 6->10->6 Hz sweep

pygame.mixer.pre_init(SAMPLE_RATE, -16, 2)
pygame.init()

t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)

# Theta modulation frequency oscillates between 6 and 10 Hz over time
mod_freq = THETA_MIN + (THETA_MAX - THETA_MIN) * 0.5 * (
    1 + np.sin(2 * np.pi * t / SWEEP_PERIOD)
)

# Instantaneous phase = integral of mod_freq over time
mod_phase = 2 * np.pi * np.cumsum(mod_freq) / SAMPLE_RATE
theta_envelope = 0.5 * (1 + np.sin(mod_phase))   # 0..1 amplitude envelope

carrier = np.sin(2 * np.pi * CARRIER_HZ * t)
signal = carrier * theta_envelope

audio = np.int16(signal * 32767 * 0.5)
stereo = np.column_stack([audio, audio])

sound = pygame.sndarray.make_sound(np.ascontiguousarray(stereo))
sound.play(-1)

print("Playing theta wave (6-10Hz amplitude modulation on 200Hz tone). Press Enter to stop.")
input()
sound.stop()
pygame.quit()