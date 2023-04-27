import mido
import time

# Define MIDI CC messages to receive tempo control
TEMPO_CC = 20  # MIDI CC number to receive tempo control
TEMPO_MIN = 30.0  # Minimum tempo in BPM
TEMPO_MAX = 300.0  # Maximum tempo in BPM

# Set up the MIDI output port
mido.set_backend('mido.backends.rtmidi')
output = mido.open_output('clock', virtual=True)

# Set up the MIDI input port for tempo control
input = mido.open_input('clock', virtual=True)
current_tempo = None
tap_tempo = []

# Define the MIDI callback function to receive CC messages
def handle_cc(msg):
    global current_tempo, tap_tempo
    if msg.type == 'control_change' and msg.control == TEMPO_CC:
        # Scale the CC value to the tempo range
        tempo_range = TEMPO_MAX - TEMPO_MIN
        cc_value_scaled = msg.value / 127.0
        tempo = TEMPO_MIN + (tempo_range * cc_value_scaled)
        current_tempo = tempo
    elif msg.type == 'note_on':
        # Store the time of the tap
        tap_tempo.append(time.time())

# Set up the MIDI input callback
input.callback = handle_cc

# Set the initial tempo
current_tempo = 120.0

# Start the clock loop
tick_interval = 60.0 / (current_tempo * 24)  # Calculate the tick interval
tick_time = time.time() + tick_interval  # Set the first tick time
ticks = 0  # Set the initial tick count
while True:
    if time.time() >= tick_time:
        # Send a MIDI clock tick message
        output.send(mido.Message('clock'))
        ticks += 1
        if ticks % 24 == 0:
            # Send a MIDI clock start message every 24 ticks
            output.send(mido.Message('start'))
        if ticks >= 96:
            # Reset the tick count every quarter note
            ticks = 0
        # Calculate the next tick time based on the current tempo
        if len(tap_tempo) >= 2:
            # Calculate the tempo based on the last two taps
            tempo_interval = tap_tempo[-1] - tap_tempo[-2]
            tempo = 60.0 / tempo_interval
            tempo = max(min(tempo, TEMPO_MAX), TEMPO_MIN)  # Clamp the tempo to the range
            current_tempo = tempo
            tap_tempo = tap_tempo[-2:]  # Keep the last two tap times
        tick_interval = 60.0 / (current_tempo * 24)
        tick_time += tick_interval
