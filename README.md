pydl
====

CLI file downloader, written in python with selenium.

## Description
CLI file downloader, written in python with selenium.  
You can use the profile of chrome.  

## Version
Ver. 0.0.1

## Dependencies
```
python==3.6.3
selenium==3.11.0
click==6.7
```
    
## Usage

### Generate Template File
```bash
$python pydl init queue.json
$ls
queue.json
$cat queue.json
{
  "queue": [],  <= Input Download URL.
  "downloading": [],
  "finished": []
}
```

### Simple Example
```bash
$python pydl down queue.json     
```

### Options and Commands
```
Options:
  -i, --incomplete TEXT  Incomplete Files Directory.
  -d, --download TEXT    Downloaded Files Directory.
  -p, --profile TEXT     Profile Directory.
  -h, --headless         Running with Headless Browzer.
  --help                 Show this message and exit.

Commands:
  down
  init
```


## Licence

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author

[agranium](https://github.com/agranium)
