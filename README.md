# miniflux-cli [unmaintained]

A small application aimed to allow to read feeds gained by Miniflux2 from a terminal without any browser. Has pretty
not much possibilities yet, but looking through list of articles and removing irrelevant works just fine.


## Requirements

To run an application, you must have installed those things:
 - cpython>=3.6
 - requests>=2.19.1

For Fedora system, you can install `python3-requests` package via `dnf install python3-requests`.

## Installation

To install app, run `sudo python3 setup.py install`. It will do all the things. Then simply run `mcli` and that's all :)

## Things to implement

 - Make display an article, and not just open it (now you can do
     it with using links browser as default way to open arcitles)
 - Make it more user friendly and gain it more possibilities
