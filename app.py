from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>DevOps Learning Journey</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                text-align: center;
                background-color: #f0f8ff;
            }
            h1 {
                color: #2c3e50;
                margin-bottom: 20px;
            }
            p {
                color: #34495e;
                font-size: 18px;
                line-height: 1.6;
            }
        </style>
    </head>
    <body>
        <h1>🚀 DevOps is So Much Fun to Learn! 🚀</h1>
        <p>Hello everyone! Welcome to the world of CI/CD, containers, and cloud! ☁️🐳</p>
        <h2>This is a test</h2>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)

