"""

## Inspiration

Pit Boss, named after the casino overseer who controls the various blackjack pits, was designed to

## What it does

Pit Boss helps you win at Blackjack by recognizing cards played, and using probability to recommend the action the player should take to maximize winnings

## How I built it

I built it with a Raspberry Pi 3 Model B and a Pi camera. It utilizes OpenCV and some open source playing card recognition software (https://github.com/EdjeElectronics/OpenCV-Playing-Card-Detector)

## Challenges I ran into

Challenges I ran into included how to recognize which cards belong to the player, how to handle the dealer's upside down card, and tracking reshuffles

## Accomplishments that I'm proud of

Using OpenCV and refreshing my knowledge of python, while doing it all on a Raspberry Pi posed significant new hurdles that I'm proud to have attempted

## What I learned

I learned more about OpenCV, and the Pi-Camera.

## What's next for Pit Boss: The Raspberry-Pi Blackjack Helper

Pit Boss needs support for a few more things:

Support for the "Split" action
Support for multiple players
Support for multiple decks

and finally, a head mount in order to make Pit Boss portable

WARNING:

Most card counting devices are illegal to use in a casino, DO NOT use Pit Boss in a casino.

https://en.wikipedia.org/wiki/Card_counting#Devices

"""
