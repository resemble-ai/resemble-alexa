# Resemble Alexa

![Resemble Alexa Sample Project Banner](https://www.resemble.ai/wp-content/uploads/2021/02/banner-alexa.jpg)
## What is it?

Use custom text-to-speech voice models from Resemble AI and GPT-3 in your Alexa Skill.

Although this project contains a demo on how you can simply chain Open AI's GPT-3 API to Resemble AI's text to speech API, the GPT-3 component is completely optional and is just used to demonstrate how the voice model can produce any arbitrary speech.

## Requirements

- Resemble AI Account (https://resemble.ai)
- Alexa Developer (https://developer.amazon.com/alexa)
- Open AI GPT-3 Account (https://openai.com/)

## Getting Started

Getting started by creating a new Skill on Alexa's Developer Console: https://developer.amazon.com/alexa/console/ask

![Image to show how to create a new Skill on Alexa's dashboard](https://www.resemble.ai/wp-content/uploads/2021/02/alexa-new-skill.png)

Follow the instructions to create a new skill, and pick Python as the backend

![Pick Python as the hosted backend](https://www.resemble.ai/wp-content/uploads/2021/02/alexa-python.png)

Click `Code` from the top menu bar.

![Click code from the top menu bar](https://www.resemble.ai/wp-content/uploads/2021/02/alexa-code.png)

Replace `lambda_function.py` with the code from `lambda_functions.py` that is contained within this repo. If you're using GPT-3, make sure to add `openai` to the `requirements.txt`
