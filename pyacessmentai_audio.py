from pyacessmentai.generation import call_tts
import base64

print("Genrating audio...")
audio_b64 = call_tts(
    [["Jenny", "Hello, welcome to the world of electric cars!"], ["Peter", "Hey Jenny."]],
    speed=0.9,
    intro=True,
    premium=True,
    return_b64=True,
    gender=["female", "male"],
)
with open("sample_audio_result.mp3", "wb") as f:
    f.write(base64.b64decode(audio_b64.split(",")[1]))
print("Audio generated successfully.")
