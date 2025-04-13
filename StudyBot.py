import google.generativeai as genai
import os
from fpdf import FPDF
import tkinter as tk
from tkinter import filedialog
import fitz

root = tk.Tk()
root.withdraw()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
#model = genai.GenerativeModel('gemini-1.5-flash')
model = genai.GenerativeModel('gemini-1.5-flash')
pdf = FPDF()
pdf.add_page()
pdf.add_font(fname='LucidaGrande.ttf')
pdf.set_font("LucidaGrande", size=12)

mode = input("Study mode [e]\nHomework mode [h]\nSummary mode [s]\nQuiz mode[q]\nPDF mode [p]\nSelect a mode >> ").lower()
full_text = ""

if mode == 'e':
    subject = input("Enter your subject >>  ")
    question = input("Enter your question >> ")
    print("\nGenerating response......This may take a while")
    response = model.generate_content(f"You are a highly experienced educator with nearly 20 years of expertise in teaching '{subject}'. Your goal is to provide a clear, well-structured, and insightful response to the following query: '{question}'. Craft comprehensive yet concise notes that simplify complex ideas, enhance understanding, and make learning engaging and effective.")
    print('Generating PDF......')
    response_text = response.text.encode('latin-1','replace').decode('latin-1')
    pdf.multi_cell(0,10,response_text)
    pdf.output(f"Notes_for_{subject}.pdf")

    print("Made a PDF")

if mode == 'h':
    subject = input('Enter your subject >> ')
    print("Select the your homework file")
    file_path = filedialog.askopenfilename(title="Select a File", 
                            filetypes=[("All Files", "*.*"), 
                                       ("PDF Files", "*.pdf")])
    if file_path:
        print("Analysing file......")
        doc = fitz.open(file_path)
        for i in range(len(doc)):
            page = doc[i]
            text = page.get_text()
            full_text += text

        print("\nGenerating response......This may take a while")
        response = model.generate_content(f"You are an expert in the subject '{subject}', you have had nearly 20 years of experience with the subject, easily solving the hardest exam papers like IIT, JEE Advanced,and even Gaokao. Solve and answer the following questions below: {full_text}")
        print('Generating PDF......')
        response_text = response.text.encode('latin-1','replace').decode('latin-1')
        pdf.multi_cell(0,10,response_text)
        pdf.output(f"Homework_Solutions_For_{subject}.pdf")

        print("Made a PDF")

    else:
        print("No file selected")
        exit()

if mode == 'p':
    subject = input('Enter your subject >> ')
    chapter = input('Enter your chapter >> ')
    print("Select the your file")
    file_path = filedialog.askopenfilename(title="Select a File", 
                            filetypes=[("All Files", "*.*"), 
                                       ("PDF Files", "*.pdf")])
    if file_path:
        print("Analysing file......")
        doc = fitz.open(file_path)
        for i in range(len(doc)):
            page = doc[i]
            text = page.get_text()
            full_text += text

        full_text.encode("latin1", "replace").decode("latin1")

        string = """
You are an expert in this subject. Your task is to carefully read and analyze the chapter, then transform it into well-organized, complete, and easy-to-understand notes. These notes should be detailed but also clear, making them perfect for studying and revision.

Guidelines for Creating the Notes:
1. Capture Every Important Detail
Extract all key information from the text, ensuring nothing important is left out.
Include definitions, facts, concepts, explanations, examples, formulas (if any), and key takeaways.
If the chapter contains historical events, processes, scientific principles, or theories, explain them thoroughly.
2. Use Clear, Simple, and Understandable Language
Avoid complex words and make explanations easy to read and understand.
If a topic is complicated, break it down step by step to make it easier to grasp.
Use simple sentences while keeping all the important details intact.
3. Organize the Notes Properly
Use clear headings and subheadings to separate different topics.
Use bullet points, numbered lists, and tables (if helpful) to improve readability.
Arrange the topics in a logical order, making sure everything flows smoothly.
Include summary sections at the end of important topics for quick revision.
4. Explain Concepts Thoroughly
Don’t just list facts—explain how and why things work.
If there are cause-and-effect relationships, processes, or steps, explain them clearly.
Provide real-life examples or comparisons to make difficult concepts easier to understand.
Where necessary, connect ideas to previous knowledge for better understanding.
5. Make the Notes Study-Friendly
Highlight important terms, key points, and commonly asked exam topics.
If there are important formulas, dates, or events, make them stand out.
Use bold or italics where necessary to emphasize critical points.
Summarize the chapter in a few key points at the end to help with revision.
Task:
Now, carefully read and process the following chapter, applying all the above guidelines to create the most effective and complete notes.

Chapter: {}
{}

Write the notes in a way that ensures maximum clarity, understanding, and usefulness for studying and exams.
""".format(chapter, full_text)

        print("\nGenerating response......This may take a while")
        response = model.generate_content(string)
        print('Generating PDF......')
        response_text = response.text.encode('latin-1','replace').decode('latin-1')
        pdf.multi_cell(0,10,response_text)
        pdf.output(f"Notes_For_{subject}.pdf")

        print("Made a PDF")

    else:
        print("No file selected")
        exit()

if mode == 's':
    prompt = input('Enter prompt >> ')
    full_text2 = ""
    print("Select the file..")
    file_path = filedialog.askopenfilename(title="Select a File",
                            filetypes=[("All Files", "*.*"), 
                                       ("PDF Files", "*.pdf")])
    if file_path:
        print("Analysing file.....")
        doc = fitz.open(file_path)
        for i in range(len(doc)):
            page = doc[i]
            text = page.get_text()
            full_text2 += text
        
        print("\nGenerating response.......this may take a while")
        response = model.generate_content(f"Summarise the below text given: {full_text2}, also follow what the following prompt says: {prompt}")
        print(f'\n{response.text}')
    else:
        print("No file selected")
        exit()

if mode == 'q':
    while True:
        chapter = input("Enter the chapter >> ")
        difficulty = input("Easy\nMedium\nHard\nEnter the difficulty >> ").lower()

        print("\nGenerating response......This may take a while")

        question = model.generate_content(f"Create a question for the chapter {chapter}, question difficulty should be '{difficulty}',reply with the question and the question only")
        #answer = model.generate_content(f"You are an experienced teacher that has nearly 20 years of experience. You teach in grade '{grade}' your an expert on the subject '{subject}', Answer the following question for the chapter {chapter}")
        user_ans = input(f"Question: {question.text}\nYour answer >>  ")
        print("\nChecking your answer......")
        real_ans = model.generate_content(f"Check if this answer: {user_ans} is the correct answer for this question: {question.text}. If yes, say 'Correct!', its ok if its doesnt really go that much in depth still say its the correct answer! or else if its no, say 'Wrong answer' then continue with the actual answer and also explain why the answer given was incorrect")
        print(f"Answer: {real_ans.text}")
        
        con = input("Continue? [Y][N] >> ").lower()
        if con == 'y':
            continue
        elif con == 'n':
            break
