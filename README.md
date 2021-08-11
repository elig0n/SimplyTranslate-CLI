# SimplyTranslate CLI

This is a simple CLI for SimplyTranslate.

## Usage Examples

For the following examples we're always going to translate the german word "Krankenwagen", which means "ambulance" in english

Translate using the default translation engine (google) locally to the default output language (english)
```bash
$ python3 main.py "Krankenwagen"
ambulance
```

Translate using the libretranslate translation engine from german to french
```bash
$ python3 main.py --engine libre --from de -to fr "Krankenwagen"
ambulance
```

Translate using the google engine online with the default SimplyTranslate instance (https://translate.metalune.xyz)

```bash
$ python3 main.py "Krankenwagen" --online
ambulance
```

Translate using the google engine online and specify a custom SimplyTranslate instance
```bash
$ python3 main.py "Krankenwagen" --online --instance "translate.example.com"
ambulance
```




## Contact

To get in contact with the developers, visit us on the #simple-web IRC channel on [Libera.Chat](https://libera.chat).

## License

simplytranslate_cli is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

simplytranslate_cli is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
