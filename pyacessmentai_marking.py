from pyacessmentai.generation import mark_work_v2, makePDF
import base64, json
import os

with open("sample_marking_source_3.json", "r", encoding="utf-8") as f:
    exercise_json = json.load(f)


print("Marking exercise...")
image_b64s = []
folder_path = "sample_marking_source_3"
for filename in os.listdir(folder_path):
    if filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "rb") as f:
            image_data = f.read()
            image_b64 = base64.b64encode(image_data).decode("utf-8")
            image_b64s.append(f"data:image/jpg;base64,{image_b64}")
result = mark_work_v2(image_b64s, exercise_json)
for segment in result:
    segment["is_correction"] = True
print(result)
print("Generating PDF...")
pdf = makePDF(
    result,
    footer="www.acessment.ai",
    header="acessment_production_cropped.png",
)
with open("marking_result3.pdf", "wb") as f:
    f.write(pdf.read())
print("PDF generated successfully.")
