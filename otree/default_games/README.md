# Default oTree Games Project

This folder contains the canonical oTree project settings that enable all of the
pre-configured demonstration games distributed with oTree. Once the virtual
environment dependencies are installed you can run the project with:

```bash
source ../../.venv/bin/activate
otree devserver
```

The session configuration enumerates the standard demo apps such as Public
Goods, Trust, Dictator, Cournot Competition, Prisoner's Dilemma, Stag Hunt,
Bertrand Competition, and more. The actual app modules are provided by the
`otree` package and will be accessible after installing the dependencies listed
in the repository `requirements.txt` file.
