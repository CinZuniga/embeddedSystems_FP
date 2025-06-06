# Simple web server

#Pre-requisites


```
sudo apt instal python3 python3-pip python3/nenv
```


# Create venv
```
python3 -m venv .venv
source .venv/bin/activate
```

# Install requirements 

```requirements.txt
flask
```

install requirements:

```
pip3 install -r requirements.txt
```

# Run the website

```
flask --app main run
```