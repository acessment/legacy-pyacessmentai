# README

`pyacessmentai` is an internal package for generating exercise according to the ACEssment standard. The only use of this package are 1. Generate exercise JSONs from prompts and settings; 2. Generate PDFs from a given JSON. It does not contain authentication or authorization mechanisms, and is intended to be used in a trusted environment.

## Testing scripts

`pyacessmentai_debug.py` calls the DIY exercise API and renders the output in PDF
`pyacessmentai_exercise_clone.py` reads `sample_exercise_page1.jpg` and `sample_exercise_page2.jpg`, and calls the clone_exercise function. Then it generates a PDF from the result. Bring your own sample images to test with.
`pyacessment_audio.py` Generates a simple audio.
`pyacessmentai_explain.py` reads `sample_exercise_explain.json` and generates explanations for each question, then generates a PDF from the result.
