from pyacessmentai.generation import makePDF
from pyacessmentai.generation import generate_diy_exercise
from pyacessmentai.generation.ai import enhance

prompt = "Create a english vocabulary exercise include the words 'set off', 'amazing', 'invest', 'discover', 'elf', 'adventure'. Do not provide a word bank (no options). Give 5 fill in the blank questions."
print("Generating DIY exercise...")
result = generate_diy_exercise(prompt)
print(result)
print("Enhancing exercise...")
enhanced_result = enhance(result, user_prompt=prompt)
print(enhanced_result)
print("Generating PDF...")
pdf = makePDF(
    [result],
    footer="www.acessment.ai",
    header="acessment_production_cropped.png",
    font_size="lg",
)
with open("result_before_enhance.pdf", "wb") as f:
    f.write(pdf.read())
print("PDF generated successfully.")

pdf = makePDF(
    [enhanced_result],
    footer="www.acessment.ai",
    header="acessment_production_cropped.png",
    font_size="lg",
)
with open("result_after_enhance.pdf", "wb") as f:
    f.write(pdf.read())
print("PDF generated successfully.")
