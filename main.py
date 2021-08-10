#!/usr/bin/python3
import argparse

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
parser.add_argument("-i", "--instance", help="Instance URL to use (only for libre)")

parser.add_argument("-f", "--from", default="auto", help="Language to translate from")
parser.add_argument("-t", "--to", required=True, help="Language to translate to")

args = vars(parser.parse_args())

#######################
## Reading Arguments ##
#######################

engine_name = args["engine"]
instance = args.get("instance")
engine = None

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

from_language = to_lang_code(args["from"], engine)
to_language = to_lang_code(args["to"], engine)

############
## Output ##
############

print(
    engine.translate(
        " ".join(args["text"]), from_language=from_language, to_language=to_language
    )
)
