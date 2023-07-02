from typing import Dict, List, Optional
import openai

import logging

from prompttools.requests.request_queue import RequestQueue
from prompttools.experiment.experiment import Experiment


class OpenAIChatExperiment(Experiment):
    """
    This class defines an experiment for OpenAI's chat completion API.
    It accepts lists for each argument passed into OpenAI's API, then creates
    a cartesian product of those arguments, and gets results for each.
    """

    def __init__(
        self,
        model: List[str],
        messages: List[List[Dict[str, str]]],
        temperature: Optional[List[float]] = [1.0],
        top_p: Optional[List[float]] = [1.0],
        n: Optional[List[int]] = [1],
        stream: Optional[List[bool]] = [False],
        stop: Optional[List[List[str]]] = [None],
        max_tokens: Optional[List[int]] = [float("inf")],
        presence_penalty: Optional[List[float]] = [0],
        frequency_penalty: Optional[List[float]] = [0],
        logit_bias: Optional[Dict] = [None],
    ):
        self.queue = RequestQueue()
        self.completion_fn = openai.ChatCompletion.create
        self.all_args = []
        self.all_args.append(model)
        self.all_args.append(messages)
        self.all_args.append(temperature)
        self.all_args.append(top_p)
        self.all_args.append(n)
        self.all_args.append(stream)
        self.all_args.append(stop)
        self.all_args.append(max_tokens)
        self.all_args.append(presence_penalty)
        self.all_args.append(frequency_penalty)
        self.all_args.append(logit_bias)
        super().__init__()

    @staticmethod
    def _extract_responses(output) -> str:
        return [choice.message.content for choice in output.choices]

    @staticmethod
    def _create_args_dict(args) -> Dict[str, object]:
        args = {
            "model": args[0],
            "messages": args[1],
            "temperature": args[2],
            "top_p": args[3],
            "n": args[4],
            "stream": args[5],
            "stop": args[6],
            "max_tokens": args[7],
            "presence_penalty": args[8],
            "frequency_penalty": args[9],
            "logit_bias": args[10],
        }
        return {name: arg for name, arg in args.items() if arg and arg != float("inf")}