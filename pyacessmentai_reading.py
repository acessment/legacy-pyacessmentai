from pyacessmentai.generation import makePDF
from pyacessmentai.generation import generate_reading_exercise, generate_reading_article

prompt = "creative bingo and resolutions jar"
print("Generating Reading exercise...")
result_dict = generate_reading_article(prompt, model_id="sonar", word_count=500, level="P4_P6")
title = result_dict["title"]
article = result_dict["content"]
result = generate_reading_exercise(
    title=title,
    article=article,
    hasFitB=True,
    hasTFNG=True,
    hasSQ=True,
    level="S4_S6",
    totalNumOfQ=15,
)
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
