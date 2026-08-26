from pyacessmentai.generation import makePDF
from pyacessmentai.generation import generate_diy_exercise

prompt = "Create a P2 reading exercise with 6 mcq and 2 sq questions about toys. And 100 words reading."
print("Generating DIY exercise...")
result = generate_diy_exercise(prompt)
print(result)
print("Generating PDF...")
pdf = makePDF(
    [result],
    footer="www.acessment.ai",
    header="acessment_production_cropped.png",
    font_size="xl",
)
with open("result.pdf", "wb") as f:
    f.write(pdf.read())
print("PDF generated successfully.")
