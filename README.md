# yahoo-finance
CLI python application for retrieving ticker data from yahoo finance.

## Install
Copy repository
```shell
git clone <rep_ref>
cd yahoo-finance
```
*(Optional)* Create and activate virtual environment
```shell
virtualenv venv
./venv/bin/activate
```
Install all dependencies
```shell
pip3 install -r requirement.txt
```
## Run
```shell
python3 yahoo_quotes.py get_quotes <symbols>
```