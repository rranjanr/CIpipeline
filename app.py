from flask import Flask

app = Flask(__name__)

@app.route('/')
def webout():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Welcome to DevOps World 🌍</title>
        <style>
            body {
                background: linear-gradient(to right, #1e3c72, #2a5298);
                color: #fff;
                font-family: Arial, sans-serif;
                text-align: center;
                padding-top: 100px;
            }
            h1 {
                font-size: 2.5em;
                margin-bottom: 20px;
                animation: glow 1.5s ease-in-out infinite alternate;
            }
            @keyframes glow {
                from {
                    text-shadow: 0 0 10px #fff, 0 0 20px #0ff, 0 0 30px #0ff;
                }
                to {
                    text-shadow: 0 0 20px #fff, 0 0 30px #0ff, 0 0 40px #0ff;
                }
            }
            p {
                font-size: 1.2em;
                opacity: 0.9;
            }
        </style>
    </head>
    <body>
        <h1>🚀 DevOps is So Much Fun to Learn! 🚀</h1>
        <p>Hello everyone! Welcome to the world of CI/CD, containers, and cloud! ☁️🐳
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)

