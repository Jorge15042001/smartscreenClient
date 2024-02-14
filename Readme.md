# SmartScreenClient

This program handles comunication between different modules (Robotic platform, height estimation module, and realtime state reporting through websockets)

## Config files

* Verify that this is the same as the latest calibration, if not copy the lates calibration files into ./config_files
* In config_files/stereo_config.json make sure "stereo_map_file" is set as an absolute path or relative to root folder of this repository
* In src/main.py make set screen_id to the screen id found at [https://200.10.147.205/](https://200.10.147.205/)

## Dependencies 
```bash
pipenv install # install dependencies
```
## Start
```bash
pipenv shell
python src/main.py
```
