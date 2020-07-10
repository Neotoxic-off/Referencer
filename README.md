# Referencer
Get all Href and Src from webpage

## Install:
```BASH
git clone https://github.com/Neotoxic-off/Referencer
cd Referencer
pip3 install -r requirements.txt
```

## Usage:

```BASH
python3 referencer.py -u <URL>
```

## Help:

```
-o / --output    : Directory to store content
-l / --limit     : Exit after number of download
-t / --type      : Extension's content to download
-e / --exception : Extension's content not to download
-u / --url       : Url to extract
```

## Example:

```BASH
python3 referencer.py -u <URL> -l .png .jpg .mp3 -e no.mp3 ..mp3 -o download
```
