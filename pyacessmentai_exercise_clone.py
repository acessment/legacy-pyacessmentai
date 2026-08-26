from pyacessmentai.generation import makePDF, clone_exercise
import base64

print("Cloning exercise...")
imageb64s = []
for i in range(1, 3):
    with open(f"sample_exercise_page{i}.jpg", "rb") as f:
        image_data = f.read()
        image_b64 = base64.b64encode(image_data).decode("utf-8")
        imageb64s.append(f"data:image/jpeg;base64,{image_b64}")
result = clone_exercise(imageb64s, "About electric cars")
print(result)
print("Generating PDF...")
pdf = makePDF(
    result,
    footer="www.acessment.ai",
    header="acessment_production_cropped.png",
)
with open("clone_exercise_result.pdf", "wb") as f:
    f.write(pdf.read())
print("PDF generated successfully.")
