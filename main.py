#!/usr/bin/env python3
import argparse
import requests
import sys

from simplytranslate_engines.libretranslate import LibreTranslateEngine
from simplytranslate_engines.googletranslate import GoogleTranslateEngine
from simplytranslate_engines.utils import to_lang_code

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
parser.add_argument("-i", "--instance", help="Instance URL to use (either for libre or server instance)")
parser.add_argument("-o", "--online", default=False, type=bool, action=argparse.BooleanOptionalAction, help="Toggle wether or not to use a SimplyTranslate instance running on a server")

parser.add_argument("-f", "--from", default="auto", help="Language to translate from")
parser.add_argument("-t", "--to", required=True, help="Language to translate to")

parser.add_argument("-d", "--debug", default=False, type=bool, action=argparse.BooleanOptionalAction, help="Toggle Debug Mode")

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
text = " ".join(args["text"])
result = None

# In debug mode, print the value of all cli arguments
if debug:
    print("[DBG] Command-Line Arguments:")
    print(f"Online   \"{online}\"")
    print(f"Engine   \"{engine_name}\"")
    print(f"Instance \"{instance}")
    print(f"From     \"{from_language}\"")
    print(f"To       \"{to_language}\"")
    print(f"Text     \"{text}\"")


if online:
    if instance is None:
        #TODO: load this default instance from a configuration file
        instance = "https://translate.metalune.xyz"
    elif not (instance.startswith("https://") or instance.startswith("http://")):
        instance = f"https://{instance}"

    if debug:
        print(f"[DBG] Contacting Instance {instance}...")

    # Try contacting the server
    try:
        return_value = requests.get(f"{instance}/api/{engine_name}/{from_language}/{to_language}/{text}")

        if return_value.status_code != 200:
            if debug:
                print(f"[DBG] Status Code not Sucessful: {return_value.status_code}")
        else:
            result = return_value.text
    except Exception as e:
        if debug:
            print(f"[DBG] Error sending request to instance \"{instance}\"")
            print(e)
else:
    if engine_name == "libre":
        if instance is None:
            instance = "https://libretranslate.de"
        elif not (instance.startswith("https://") or instance.startswith("http://")):
            instance = f"https://{instance}"

        engine = LibreTranslateEngine(instance)
    elif engine_name == "google":
        if instance is not None:
            parser.error("You can't set instance for Google Translate")

        engine = GoogleTranslateEngine()


    from_language = to_lang_code(from_language, engine)
    to_language = to_lang_code(to_language, engine)

    result = engine.translate(
            text, from_language=from_language, to_language=to_language
            )

############
## Output ##
############

if result == None:
    print("[ERR] Couldn't fetch any result. See Debug Mode for more info")
    sys.exit(1)
else:
    print(result)
