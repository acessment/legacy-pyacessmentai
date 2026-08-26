from pyacessmentai.generation import get_explanation_v2, makePDF
import base64, json
import os

with open("sample_explain_source.json", "r", encoding="utf-8") as f:
    context = f.read()
    exercise_json = json.loads(context)

for segment in exercise_json:
    for question in segment["questions"]:
        print("Generating explanation for question...")
        if question.get("type") == "tfng":
            for statement in question.get("statements", []):
                statement["explanation_text"] = get_explanation_v2(context=context, question=statement)
        elif question.get("type") in ["fitB", "sel_fitB", "art_fitB", "sq", "mcq", "lq"]:
            question["explanation_text"] = get_explanation_v2(context=context, question=question)

result = exercise_json
with open("explanation_result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(result)
print("Generating PDF...")
pdf = makePDF(
    result,
    footer="www.acessment.ai",
    header="acessment_production_cropped.png",
    isSolution=True,
)
with open("explanation_result.pdf", "wb") as f:
    f.write(pdf.read())
print("PDF generated successfully.")
