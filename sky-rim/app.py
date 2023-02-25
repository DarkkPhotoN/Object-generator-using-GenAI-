from flask import Flask, render_template, request
import requests
import json
app = Flask(__name__)

# Input
# Cold Drink to refresh in summer. Budget friendly and easily accessible. Tastes in different flavours and comes in a tin can .


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['inptxt']

        sum = summarize(text)

        prompout = prompt(text)

        image = ImageGeneration(prompout)

        name = pname(sum)

        return render_template('index.html', name=name, image=image, sum=sum)

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
    output = json.loads(response.text)["output"]
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
    output = json.loads(response.text)["output"]

    return output


def pname(sum):
    api_url = "https://v1.genr.ai/api/circuit-element/generate-product-name"
    params3 = {"product_description": sum,
               "temperature": 0.8, "keywords": "useful"}

    pname = requests.post(api_url, json=params3)
    output = json.loads(pname.text)["output"]

    return output


if __name__ == '__main__':
    app.run(debug=True)
