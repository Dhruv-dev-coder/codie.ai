from flask import Flask, render_template, request, redirect, url_for, session
from together import Together

app = Flask(__name__)
app.secret_key =' Codie AI ChatBox'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')


    session['user'] = email
    return redirect(url_for('chatbox'))



@app.route('/chatbox', methods=['GET', 'POST'])
def chatbox():
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        user = request.form.get('user')
        if user.lower() == 'stop':
            session.pop('history', None)
            return render_template('chatbox.html', message="Chat stopped. You can start again anytime.")

        session['history'].append({"role": "user", "content": user})

        client = Together(
            api_key="5a6ce137fb4b048a950322cc102fc58b7288952c5ee8c63b418f19c5731bfcb6"
        )

        try:

            completion = client.chat.completions.create(
                model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                messages=session['history']
            )


            answer = completion.choices[0].message.content
            session['history'].append({"role": "assistant", "content": answer})
            return render_template('chatbox.html', user=user, response=answer)

        except Exception as e:
            return f"An error occurred: {str(e)}"

    return render_template('chatbox.html',history=session['history'])

if __name__ == "__main__":
    app.run(debug=True)

