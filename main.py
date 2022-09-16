#!/usr/bin/env python3
import argparse
import requests
import sys
from urllib.parse import urlencode

from simplytranslate_engines.libretranslate import LibreTranslateEngine
from simplytranslate_engines.googletranslate import GoogleTranslateEngine
from simplytranslate_engines.utils import to_lang_code

import asyncio

############################
## Set up Argument Parser ##
############################

parser = argparse.ArgumentParser()

parser.add_argument("text", metavar="TEXT", nargs="+", help="The text to translate")

parser.add_argument(
    "-e",
    "--engine",
    choices=("google", "libre"),
    default="google",
    help="Translation engine to use",
)
parser.add_argument(
    "-i", "--instance", help="Instance URL to use (either for libre or server instance)"
)
parser.add_argument(
    "-o",
    "--online",
    default=False,
    type=bool,
    action=argparse.BooleanOptionalAction,
    help="Toggle whether or not to use a SimplyTranslate instance running on a server",
)

parser.add_argument("-f", "--from", default="auto", help="Language to translate from")
parser.add_argument("-t", "--to", default="en", help="Language to translate to")
parser.add_argument("-p", "--print", default=False, type=bool, action=argparse.BooleanOptionalAction, help="Toggle wether or not to print a shareable link, only works if --online is provided.")

parser.add_argument(
    "-d",
    "--debug",
    default=False,
    type=bool,
    action=argparse.BooleanOptionalAction,
    help="Toggle Debug Mode",
)
parser.add_argument(
    "-a", "--apikey", default=None, help="Optional Api-Key for LibreTranslate"
)

args = vars(parser.parse_args())

#######################
## Reading Arguments ##
#######################

debug = args.get("debug")
online = args.get("online")
engine_name = args["engine"]
instance = args.get("instance")
from_language = args["from"]
to_language = args["to"]
api_key = args.get("apikey")
text = " ".join(args["text"])
print_link = args.get("print")
result = None

# In debug mode, print the value of all cli arguments
if debug:
    print("[DBG] Command-Line Arguments:")
    print(f"Online   {online}")
    print(f'Engine   "{engine_name}"')
    print(f'Instance "{instance}"')
    print(f'From     "{from_language}"')
    print(f'To       "{to_language}"')
    print(f'Text     "{text}"')
    print(f'API Key  "{api_key}"')

# Only used for the --print option
link = ""

if online:
    if instance is None:
        # TODO: load this default instance from a configuration file
        instance = "https://simplytranslate.org"
    elif not (instance.startswith("https://") or instance.startswith("http://")):
        instance = f"https://{instance}"

    if debug:
        print(f"[DBG] Contacting Instance {instance}...")

    # Try contacting the server
    try:
        params = {
            "engine": engine_name,
            "from": from_language,
            "to": to_language,
            "text": text,
        }

        link_params = {
            "engine": engine_name,
            "sl": from_language,
            "tl": to_language,
            "text": text,
        }
        link = f"{instance}?{urlencode(link_params)}"

        return_value = requests.get(f"{instance}/api/translate?{urlencode(params)}")

        if return_value.status_code != 200:
            print(
                f'[ERR] Fetching Translation from server "{instance}" unsuccessful: Return Code {return_value.status_code}',
                file=sys.stderr,
            )
        else:
            result = return_value.text
    except Exception as e:
        print(
            f'[ERR] Fetching Translation from server "{instance}" unsuccessful:',
            file=sys.stderr,
        )
        print(e, file=sys.stderr)
else:
    if engine_name == "libre":
        if instance is None:
            instance = "https://libretranslate.de"
        elif not (instance.startswith("https://") or instance.startswith("http://")):
            instance = f"https://{instance}"

        if api_key is None:
            engine = LibreTranslateEngine(instance)
        else:
            engine = LibreTranslateEngine(instance, api_key=api_key)
    elif engine_name == "google":
        if instance is not None:
            parser.error("You can't set instance for Google Translate")

        engine = GoogleTranslateEngine()

    loop = asyncio.new_event_loop()

    async def asyncio_to_lang_code(from_language, engine):
        return await to_lang_code(from_language, engine)

    async def asyncio_translate(text, from_language, to_language):
        return await engine.translate(text, from_language=from_language, to_language=to_language)

    from_language = loop.run_until_complete(asyncio_to_lang_code(from_language, engine))
    to_language = loop.run_until_complete(asyncio_to_lang_code(from_language, engine))

    result = loop.run_until_complete(asyncio_translate(text, from_language=from_language, to_language=to_language))

############
## Output ##
############

if result is None:
    print(
        "[ERR] Couldn't fetch any result. See Debug Mode for more info", file=sys.stderr
    )
    sys.exit(1)
else:
    print(result)

    if online and print_link:
        print(link)

