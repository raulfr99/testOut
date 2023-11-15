from flask import Flask, render_template, request, session, redirect, url_for
import openai

app = Flask(__name__)
openai.api_key = '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'
app.config["SECRET_KEY"] = "ADSFASDFASDFASDF34A78ADSFHJASDH333"

conversations = []
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    if request.form['genre']:
        # question = 'Yo: ' + request.form['question']
        genre =  request.form['genre']
        character1 =  request.form['character1']
        character2 =  request.form['character2']
        storyline =  request.form['character2']
        # session['user_question'] = genre

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = [
                {
                    "role" : "user",
                    "content" : "write an outline"
                },
                {
                    "role" : "user",
                    "content" : "with a genre of" + genre
                },
                {
                    "role" : "user",
                    "content" : "character 1 name" + character1
                },
                {
                    "role" : "user",
                    "content" : "character 2 name" + character2
                },
                {
                    "role" : "user",
                    "content" : "with a storyline of:" + storyline
                },
                {
                    "role" : "user",
                    "content" : "the outline needs to have 6 short sentences"
                },
                {
                    "role" : "user",
                    "content" : "this an example of the formatting: ,\
                                1. Paco recoge a Lucia en coche.,\
                                2. Hay un conflicto dentro del avión.,\
                                3. Son regidos en China por un extraño.,\
                                4. Llegan a una casa ya de noche.,\
                                5. Su padre se ha convertido en vampiro. ,\
                                6. Quieren convertirlos en vampiros."
                },
                # {
                #     "role" : "user",
                #     "content" : session['user_question']
                # },
                # {
                #     "role" : "assistant",
                #     "content" : session.get('assistant_answer', "")
                # },
                # {
                #     "role" : "user",
                #     "content" : question
                # },
            ],
            temperature = 1,
            max_tokens = 2048,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0
        )

        answer = 'AI: ' + response["choices"][0]["message"]["content"]
        session['assistant_answer'] = answer

        conversations.append('This was my first outline: ')
        conversations.append(answer)

        return render_template('outline.html', chat = conversations)
    else:
        return render_template('index.html')
@app.route('/outline', methods=['POST'])
def outline():
    if request.method == 'GET':
        return render_template('outline.html')
    if request.form['question']:
        question = 'Me: ' + request.form['question']
        session['user_question'] = question

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = [
                {
                    "role" : "user",
                    "content" : session['user_question']
                },
                {
                    "role" : "assistant",
                    "content" : session.get('assistant_answer', "")
                },
                {
                    "role" : "user",
                    "content" : question
                },
            ],
            temperature = 1,
            max_tokens = 2048,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0
        )

        answer = 'AI: ' + response["choices"][0]["message"]["content"]
        session['assistant_answer'] = answer

        conversations.append(question)
        conversations.append(answer)

        return render_template('outline.html', chat = conversations)
    else:
        return render_template('outline.html')
    
@app.route('/reset', methods=['POST'])
def reset():
    global conversations
    conversations = []
    return render_template('index.html')
    

if __name__ == '__main__':
    app.run(debug=True, port=4000)
