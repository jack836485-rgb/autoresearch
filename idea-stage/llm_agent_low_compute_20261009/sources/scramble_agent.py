import os
import sys
import re
import json
import time
import inspect
from tqdm import tqdm
from typing import Dict, Any, List, Optional, Tuple
from openai import OpenAI
from google import genai
from google.genai import types


def handle_api_error(e: Exception):
    error_str = str(e).lower()
    if (
        "maximum context length" in error_str
        or "maximum number of tokens" in error_str
        or "input token count exceeds" in error_str
    ):
        raise e
    if any(
        k in error_str
        for k in [
            "429",
            "503",
            "quota",
            "limit",
            "unavailable",
            "try again",
            "overloaded",
        ]
    ):
        tqdm.write(f"\n[API Error] {e} - Sleeping for 60 seconds before retrying...")
        time.sleep(1)
    else:
        raise e


class OpenRouterBackendMixin:
    def __init__(self, model_name: str = "openai/gpt-oss-120b"):
        self.model_name = model_name
        self.api_key = os.environ.get("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"

        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )
        self.history: List[Dict[str, str]] = []
        self.full_history: List[Dict[str, str]] = []

    def _init_history(self, system_prompt: str):
        self.history = [{"role": "system", "content": system_prompt}]
        self.full_history = [{"role": "system", "content": system_prompt}]

    def _append_user(self, text: str):
        self.history.append({"role": "user", "content": text})
        self.full_history.append({"role": "user", "content": text})

    def _append_assistant(self, text: str):
        self.history.append({"role": "assistant", "content": text})
        self.full_history.append({"role": "assistant", "content": text})

    def _generate(
        self, temperature: Optional[float] = None
    ) -> Tuple[str, Dict[str, Any]]:
        kwargs = {
            "model": self.model_name,
            "messages": self.history,
            "max_tokens": 8196,
        }
        if temperature is not None:
            kwargs["temperature"] = temperature

        while True:
            try:
                t0 = time.time()
                response = self.client.chat.completions.create(**kwargs)
                content = response.choices[0].message.content
                t1 = time.time()
                usage = {
                    "prompt_tokens": (
                        response.usage.prompt_tokens if response.usage else 0
                    ),
                    "completion_tokens": (
                        response.usage.completion_tokens if response.usage else 0
                    ),
                    "total_tokens": (
                        response.usage.total_tokens if response.usage else 0
                    ),
                    "latency": t1 - t0,
                }
                return content, usage
            except Exception as e:
                handle_api_error(e)

    def _get_last_assistant_text(self) -> str:
        if self.history and self.history[-1]["role"] == "assistant":
            return self.history[-1]["content"]
        return ""

    def get_trajectory(self) -> List[Dict[str, Any]]:
        return self.full_history


class GeminiBackendMixin:
    def __init__(
        self, model_name: str = "gemini-3.5-flash", thinking_level: str = None, **kwargs
    ):
        self.model_name = model_name
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.history = []
        self.full_history = []
        self.system_prompt = ""
        self.thinking_level = thinking_level

    def _init_history(self, system_prompt: str):
        self.system_prompt = system_prompt
        self.history = []
        self.full_history = []

    def _append_user(self, text: str):
        self.history.append(
            types.Content(role="user", parts=[types.Part.from_text(text=text)])
        )
        self.full_history.append({"role": "user", "content": text})

    def _append_assistant(self, text: str):
        self.history.append(
            types.Content(role="model", parts=[types.Part.from_text(text=text)])
        )
        self.full_history.append({"role": "model", "content": text})

    def _generate(
        self, temperature: Optional[float] = None
    ) -> Tuple[str, Dict[str, Any]]:
        config_kwargs = {"system_instruction": self.system_prompt}
        if temperature is not None:
            config_kwargs["temperature"] = temperature
        if getattr(self, "thinking_level", None) is not None:
            config_kwargs["thinking_config"] = types.ThinkingConfig(
                thinking_level=self.thinking_level
            )

        while True:
            try:
                t0 = time.time()
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=self.history,
                    config=types.GenerateContentConfig(**config_kwargs),
                )
                t1 = time.time()
                usage = {
                    "prompt_tokens": (
                        response.usage_metadata.prompt_token_count
                        if response.usage_metadata
                        else 0
                    ),
                    "completion_tokens": (
                        response.usage_metadata.candidates_token_count
                        if response.usage_metadata
                        else 0
                    ),
                    "total_tokens": (
                        response.usage_metadata.total_token_count
                        if response.usage_metadata
                        else 0
                    ),
                    "latency": t1 - t0,
                }
                return response.text, usage
            except Exception as e:
                handle_api_error(e)

    def _get_last_assistant_text(self) -> str:
        if self.history and self.history[-1].role == "model":
            return self.history[-1].parts[0].text if self.history[-1].parts else ""
        return ""

    def get_trajectory(self) -> List[Dict[str, Any]]:
        traj = [{"role": "system", "content": self.system_prompt}]
        traj.extend(self.full_history)
        return traj


class BaseStrategy:
    def __init__(self):
        self.action_token_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

    def _parse_json(self, text: str) -> Dict[str, Any]:
        try:
            text_cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
            if "</think>" in text_cleaned:
                text_cleaned = text_cleaned.split("</think>")[-1]

            def escape_newlines(match):
                return match.group(0).replace("\n", "\\n").replace("\r", "\\r")

            text_cleaned = re.sub(r'"(?:[^"\\]|\\.)*"', escape_newlines, text_cleaned)

            matches = list(
                re.finditer(r"```(?:json)?\n(.*?)\n```", text_cleaned, re.DOTALL)
            )
            if matches:
                try:
                    return json.loads(matches[-1].group(1))
                except json.JSONDecodeError:
                    pass

            start = text_cleaned.find("{")
            end = text_cleaned.rfind("}")

            if start != -1 and end != -1 and end > start:
                candidate = text_cleaned[start : end + 1]
                try:
                    return json.loads(candidate)
                except json.JSONDecodeError:
                    if '"action"' in candidate:
                        try:
                            fixed = re.sub(
                                r"\"\s*\"action\"",
                                r'", "action"',
                                candidate,
                            )
                            return json.loads(fixed)
                        except:
                            pass

                    match = re.search(
                        r'"thought"\s*:\s*"(.*?)"\s*,\s*"action"',
                        candidate,
                        re.DOTALL,
                    )
                    if match:
                        raw_thought = match.group(1)
                        cleaned_thought = (
                            raw_thought.replace("\\", "\\\\")
                            .replace('"', '\\"')
                            .replace("\n", "\\n")
                            .replace("\r", "\\r")
                        )
                        fixed_candidate = (
                            candidate[: match.start(1)]
                            + cleaned_thought
                            + candidate[match.end(1) :]
                        )
                        try:
                            return json.loads(fixed_candidate)
                        except json.JSONDecodeError:
                            pass

                    fallback_result = {}
                    thought_match = re.search(
                        r'"thought"\s*:\s*"(.*?)"\s*,\s*"(?:action)"',
                        text,
                        re.DOTALL,
                    )
                    if thought_match:
                        fallback_result["thought"] = (
                            thought_match.group(1)
                            .replace("\n", "\\n")
                            .replace("\r", "\\r")
                        )

                    action_match = re.search(
                        r'"action"\s*:\s*(\{(?:[^{}]|(?:\{[^{}]*\}))*\})',
                        text,
                        re.DOTALL,
                    )
                    if action_match:
                        try:
                            fallback_result["action"] = json.loads(
                                action_match.group(1)
                            )
                        except json.JSONDecodeError:
                            pass

                    if "action" in fallback_result:
                        if "thought" not in fallback_result:
                            fallback_result["thought"] = (
                                "Extracted via regex fallback due to malformed JSON"
                            )
                        return fallback_result

            return json.loads(text_cleaned)
        except Exception as e:
            return {"error": "parse_failure", "raw_response": text, "msg": str(e)}

    def _build_base_prompt_header(
        self, schema: List[Dict[str, Any]], scramble: bool = True
    ) -> str:
        env_desc = (
            "highly restricted, scrambled terminal environment."
            if scramble
            else "terminal environment."
        )
        obf_desc = (
            "All tool names, parameters, and output keys have been obfuscated. You must explore the environment, hypothesize what the tools do, and use them to find the solution."
            if scramble
            else "You must use the available tools to find the solution."
        )
        tool_desc = "AVAILABLE TOOLS (Scrambled):" if scramble else "AVAILABLE TOOLS:"

        return f"""You are an autonomous agent operating in a {env_desc}
Your goal is to solve the tasks provided by the user. If you are stuck on a task, you can use the `skip_task` tool to move to the next one. Skipped tasks will be re-queued and presented again at the end of the rotation. If you believe you cannot solve any more tasks, you can use the `end_episode` tool to terminate the entire episode early.
{obf_desc}

{tool_desc}
{json.dumps(schema, indent=2)}
"""

    def set_system_prompt(self, schema: List[Dict[str, Any]], scramble: bool = True):
        prompt = self._build_base_prompt_header(schema, scramble)
        prompt += """
You MUST respond with a single JSON object in the following format to take an action:
```json
{
  "thought": "Briefly explain your reasoning, what you think a tool does, or your hypothesis.",
  "action": {
    "name": "tool_name_here",
    "arguments": {
      "arg_name": "value"
    }
  }
}
```
Make exactly ONE tool call per response. Do not add text outside the JSON block.
"""
        self._init_history(prompt)

    def get_action(self, observation: str) -> Dict[str, Any]:
        if observation:
            self._append_user(observation)

        step_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

        try:
            reply, usage = self._generate()

            step_usage["prompt_tokens"] += usage.get("prompt_tokens", 0)
            step_usage["completion_tokens"] += usage.get("completion_tokens", 0)
            step_usage["total_tokens"] += usage.get("total_tokens", 0)
            step_usage["latency"] = step_usage.get("latency", 0.0) + usage.get(
                "latency", 0.0
            )

            self.action_token_usage["prompt_tokens"] += usage.get("prompt_tokens", 0)
            self.action_token_usage["completion_tokens"] += usage.get(
                "completion_tokens", 0
            )
            self.action_token_usage["total_tokens"] += usage.get("total_tokens", 0)

            parsed = self._parse_json(reply)

            if not isinstance(parsed, dict):
                parsed = {
                    "error": "parse_failure",
                    "msg": "Response must be a JSON object.",
                }
            elif "action" not in parsed and "error" not in parsed:
                parsed = {
                    "error": "parse_failure",
                    "msg": "Response must contain an 'action' dictionary.",
                }
            elif "error" not in parsed and (
                not isinstance(parsed.get("action"), dict)
                or "name" not in parsed["action"]
            ):
                parsed = {
                    "error": "parse_failure",
                    "msg": "Response must contain an 'action' dictionary with a 'name' key.",
                }

            self._append_assistant(reply)
            parsed["usage"] = step_usage
            return parsed
        except Exception as e:
            return {"error": "api_failure", "msg": str(e), "usage": step_usage}


class GeminiAgent(GeminiBackendMixin, BaseStrategy):
    def __init__(
        self, model_name: str = "gemini-3.5-flash", thinking_level: str = None, **kwargs
    ):
        GeminiBackendMixin.__init__(
            self, model_name=model_name, thinking_level=thinking_level, **kwargs
        )
        BaseStrategy.__init__(self)


class OpenRouterAgent(OpenRouterBackendMixin, BaseStrategy):
    def __init__(self, model_name: str = "anthropic/claude-sonnet-4.5", **kwargs):
        OpenRouterBackendMixin.__init__(self, model_name)
        BaseStrategy.__init__(self)


def get_agent_class(backend: str, agent_type: str):
    if backend.lower() == "gemini":
        backend_prefix = "Gemini"
    elif backend.lower() == "openrouter":
        backend_prefix = "OpenRouter"
    else:
        raise ValueError(f"Unknown backend: {backend}")

    if agent_type == "default":
        class_name = f"{backend_prefix}Agent"
    else:
        raise ValueError(f"Unknown agent type format: {agent_type}")

    current_module = sys.modules[__name__]
    for name, obj in inspect.getmembers(current_module, inspect.isclass):
        if name == class_name:
            return obj

    raise ValueError(f"Could not find agent class {class_name} for type {agent_type}")
