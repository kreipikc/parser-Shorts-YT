### What kind of project is this?
This is a script parser for YouTube short films. The work takes place in the console (without a graphical interface). When you enter a link to a page with a brief description of the channel you need, the script analyzes the names, links and the number of views of all shorts on this channel. 

**_It is not working at the moment 23.06.2025_**

### What did I use?
- Python
  - selenium
  - webdriver_manager
  - pandas
  - tqdm
  - art

### Quick start
First of all, we clone the repository to a convenient location for you
```commandline
git clone https://github.com/kreipikc/parser-Shorts-YT.git
```

Next, go to the directory
```commandline
cd <yout_path>/parser-Shorts-YT
```

Download all the necessary packages
```commandline
pip install -r requirements.txt
# or
pip3 install -r requirements.txt
```

Running the script
```commandline
python src/main.py 
# or
python3 src/main.py
```

### Structure project
```commandline
parser-Shorts-YT
├── .gitignore
├── README.md
├── requirements.txt
└── src
    ├── main.py         # Entry point
    ├── model.py        # Model for the 'video'
    ├── parser.py       # Logic parser
    └── utils.py        # Utilities
```

### Why did I even start creating this project?
The project was created for personal use and practice of writing a python parser.
