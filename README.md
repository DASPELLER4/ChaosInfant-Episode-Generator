# ChaosInfant Episode Generator
A generator for the chaosinfant series I run on my youtube channel also entitled DASPELLER4, they are simple videos with two or more stationary characters on a backdrop of my choice that I can change at any time. It takes in script files of what you want the characters to say and what the scene is, it uses the tettys sapi4 tts api

<a href="https://www.youtube.com/playlist?list=PLWRjq42wIAAA0qxTobCanQzH7b-V8rghK">My videos made with this</a>

## Script.txt
The script.txt file is to be formatted like this:

The scene can be set by having it's name surrounded by square brackets alone on a line like this:

<code>[MyScene]</code>

A character can speak by putting their name in square brackets followed by their speech like this:

<code>[MyCharacter] Hello, World!</code>

## Adding characters to the project
You can add characters to the project by editing chaosinfant.py

You add them my editing the characters variable near the end of the file.

The dictionary is formatted as such <code>{'Name': ['Voice','Character.png'], ...}</code>

## Adding scenes to the project
This the same as adding characters, you now edit the scenes variables

The dictionary is formatted as such <code>{'Name': 'Scene.png', ...}</code>
