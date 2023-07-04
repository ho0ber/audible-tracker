# audible-tracker
last-heard tracking and charting for audible audiobooks

## Setup
Register device by doing:
* `python register_device.py` and supplying password and OTP
* create secret with `kubectl create secret generic audible-creds --from-file=audible-creds`
