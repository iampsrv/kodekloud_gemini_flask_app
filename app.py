from flask import Flask, render_template, request
import google.generativeai as genai
import os

app = Flask(__name__)

# A dictionary to store tasks with an ID
tasks = {}
task_id_counter = 1

@app.route('/', methods=['GET', 'POST'])
def index():
    global task_id_counter
    response_text = ""

    if request.method == 'POST':
        if 'add_task' in request.form:
            task_content = request.form.get('task_content')
            if task_content:
                tasks[task_id_counter] = task_content
                task_id_counter += 1

        elif 'delete_task' in request.form:
            task_id_to_delete = int(request.form.get('task_id_to_delete'))
            tasks.pop(task_id_to_delete, None)

        elif 'generate_content' in request.form:
            task_list = "\n".join(tasks.values())

            # Your code to integrate
            gemini_api_key = os.environ.get('SECRET_KEY')
            genai.configure(api_key=gemini_api_key)
            

            # Set up the model
            generation_config = {
                "temperature": 0.9,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 2048,
            }

            safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
        ]
            prompt_parts =[]
            model = genai.GenerativeModel(model_name="gemini-pro",
                                          generation_config=generation_config,
                                          safety_settings=safety_settings)

            prompt_parts = [
                f"Please list the following tasks in a logical order from which task to start, without adding any commentary or suggestions:\n\n{task_list}"
            ]

            response = model.generate_content(prompt_parts)
            response_text = response.text

    return render_template('index.html', tasks=tasks, response=response_text)

if __name__ == '__main__':
    app.run(port=5000,debug=True)
    # app.run(host='0.0.0.0',port=5000,debug=True)
