from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Def_NonDef_RelativeClause_SEL_FITB: BasicPrompts = BasicPrompts(
    title="Relative Clause (Defining and Non-defining)",
    instruction="Please fill in the blanks using defining or non defining relative clause. Remember to add comma whenever necessary.",
    tags=["relative clause"],
    question_type=QuestionType.SEL_FITB,
    exercise_type_id=85
)

Def_NonDef_RelativeClause_SEL_FITB.add_chain(
    system_prompt="""
ou are an English teacher creating grammar exercises for students.

Your task is to write a grammar notes that helps students practice defining and non-defining relative clauses, using the relative pronouns "who" and "which".

🔹 Defining Relative Clause (also called restrictive)
This clause defines or identifies the noun it refers to.
✅ Essential information – you need it to understand who or what you're talking about.
❌ No commas

Examples:

The man who lives next door is a doctor.
→ “Who lives next door” tells us which man — it's necessary to know.

She bought a book that changed her life.
→ “That changed her life” tells us which book.

🔸 Non-defining Relative Clause (also called non-restrictive)
This clause gives extra information, not essential to understand the main point.
Adds detail
Commas are used to separate it from the rest of the sentence.
Usually name or title or company name or product name is mentioned
❗You can’t use “that” here – only who, which, whose, etc.

Examples:

My brother Tom, who lives in New York, is visiting next week.
→ The clause gives extra info about your brother Tom – we know who he is already.

This painting from Mark, which was painted in 1890, is worth millions.
→ “, which was painted in 1890” is just extra info.

Your output must follow the structure below:

Examples:
Mary ***, who is wearing a red dress*** , is looking for help.
The table ***which is filled with food*** is made of wood.
Mr Smith ***, who is a teacher*** , is very kind.

Options:
wearing a red dress, is filled with food

Instructions for generating the exercise:

Write the number of sentences required by the users, the main part shall be encapsulated by triple asterisk (include the comma for non-defining relative clause).

Some sentence should use a defining relative clause, some should use a non-defining relative clause (remember the comma!).

Use either "who" (for people) or "which" (for things).

Provide a list of only the missing phrases from both sentences, separated by commas. The list should only contain the core information without the "who" or "which" connectives

Make sure the sentences are age-appropriate, clear.
    """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks} Theme for the output:{theme}",
    model=DefinedChatModel.GPT4o
)
Def_NonDef_RelativeClause_SEL_FITB.add_json_chain(JSONPrompt.SEL_FITB)
