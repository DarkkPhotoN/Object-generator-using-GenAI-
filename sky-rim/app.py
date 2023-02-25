from flask import Flask, render_template, request
import requests
import json
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['inptxt']

        sum = summarize(text)

        prompout = prompt(text)

        print(prompout)

        image = ImageGeneration(prompout)

        return render_template('index.html', sum=sum, image=image)

    else:
        return render_template('index.html')


def summarize(itext):
    api_url1 = "https://v1.genr.ai/api/circuit-element/summarize"
    params1 = {

        "text": itext,
        "temperature": 0.5,
        "max_words": 15
    }

    response = requests.post(api_url1, json=params1)
    output = json.loads(response.text)
    return output


def prompt(summ):

    api_url2 = "https://v1.genr.ai/api/circuit-element/generate-prompt"

    params2 = {"text": summ, "temperature": 0.5}

    ptext = requests.post(api_url2, json=params2)
    output = json.loads(ptext.text)["output"]
    return output


def ImageGeneration(prompto):

    api_url = "https://v1.genr.ai/api/circuit-element/generate-image"

    params = {
        "prompt": prompto,
        "height": 512,
        "width": 512,
        "model": "stable-diffusion-2",
        "n_images": 1
    }
    response = requests.post(api_url, json=params)
    print(response.text)
    output = json.loads(response.text)["output"]
    print(output)
    return output


if __name__ == '__main__':
    app.run(debug=True)
