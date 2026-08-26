from pyacessmentai.generation import makePDF, enhance
from pyacessmentai.generation import generate_listening_script, generate_listening_questions

prompt = "Theme a conversation between two friends about their weekend plan and their vacation last month."
print("Generating Listening exercise...")
script = generate_listening_script(
    theme=prompt,
    model_id="gpt-4o",
    level="S4_S6",
    word_count=600,
)
print(script)

result = generate_listening_questions(
    tapescript=script,
    level="S4_S6",
    theme=prompt,
    word_count=800,
)

user_prompt = prompt + "\nTapescript:\n" + script


print(result)

enhanced_result = enhance(result, user_prompt=user_prompt)

print(enhanced_result)

print("Generating PDF...")
pdf = makePDF(
    [result],
    footer="www.acessment.ai",
    header="acessment_production_cropped.png",
    isSolution=True,
    font_size="md",
)
with open("result_before_enhance.pdf", "wb") as f:
    f.write(pdf.read())
print("PDF generated successfully.")

pdf = makePDF(
    [enhanced_result],
    footer="www.acessment.ai",
    header="acessment_production_cropped.png",
    isSolution=True,
    font_size="md",
)
with open("result_after_enhance.pdf", "wb") as f:
    f.write(pdf.read())
print("PDF generated successfully.")
