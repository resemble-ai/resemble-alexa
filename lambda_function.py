# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.

# This sample is built using the handler classes approach in skill builder.


import logging
import ask_sdk_core.utils as ask_utils
import requests
import json

# For handling s3 URLs
from xml.sax.saxutils import escape

# for OpenAI
import os
import openai

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


openai.api_key = "YOUR_API_KEY"
DEFAULT_PROMPT = """Q: What's your name and background?
A: My name is Albert Einstein, I am a physicist. You may have heard of me!
Q: And what is the purpose of this meeting?
A: I was told that you would want to know everything about the inner workings of our universe."""

VOICE_UUID = "RESEMBLE_VOICE_UUID"
PROJECT_UUID = "PROJECT_UUID"
RESEMBLE_URL = f"https://app.resemble.ai/api/v1/projects/{PROJECT_UUID}/clips/sync"
RESEMBLE_API_KEY = "RESEMBLE_API_KEY"

# Static Assets for Intro and Continuation
INTRO_AUDIO = ""
ASK_AUDIO = ""

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = '<speak><audio src="' + escape(INTRO_AUDIO) + '" /></speak>'

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class GetUserQuestionIntentHandler(AbstractRequestHandler):
    """Handler for Get User Question Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetUserQuestionIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots

        userAnswer = slots['user_question'].value
        
        if not userAnswer:
            response = "There was not an answer"
                
        request = userAnswer

        prompt = DEFAULT_PROMPT
        prompt += f"\nQ. {request} \nA. "
        
        result = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            temperature=0.9,
            max_tokens=50,
            top_p=1,
            stop=["\n"]
        )
        try:
            response = result.to_dict()['choices'][0]['text']
        except:
            response = " "
        
        
        payload = {
            "data": {
                "title": "Alexa Skill",
                "body": response,
                "voice": VOICE_UUID,
            },
            "output_format": "mp3", # important for alexa
            "sample_rate": 16000 # important for alexa
        }
        headers = {
            'Authorization': f'Token token={RESEMBLE_API_KEY}',
            'Content-Type': 'application/json'
        }

        resemble_response =  requests.request(
            "POST",
            RESEMBLE_URL,
            headers=headers,
            json = payload)

        resemble_response_url = resemble_response.text
        
        r = requests.get(resemble_response_url)
        speak_output = '<speak><audio src="' + escape(r.url) + '" /></speak>'
        ask_output = '<speak><audio src="' + escape(ASK_AUDIO) + '" /></speak>'

        return handler_input.response_builder.speak(speak_output).ask(ask_output).response



class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Sometimes I don't hear what you're saying but what if you try asking Hey Einstein and asking your question again?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("If you want to ask Einstein anything else, just say Hey Einstein and your question")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.
sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetUserQuestionIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()