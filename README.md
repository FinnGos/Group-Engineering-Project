# CarboCollect - Sustainability Game

## Description:
🎮 Welcome to **CarboCollect**! This is our task-based collectibles sustainability game. Where, you will be given a few tasks to complete each day on the University of Exeter campus. Each task will relate to a way you can contribute to better sustainability, such as recycling or reducing energy consumption, to help contribute to a greener campus. You can also take part in riddles and treasure hunts visiting significant sites on campus.

All of these will earn you **CarboCoins** that you can spend to unlock **CarboCards** and climb to the top of the leaderboards. These collectibles will highlight key locations, Sustainable Development Goals, and other aspects of our university.

There are many cards to collect, points to earn, and fun facts to be learned, so good luck and have fun!  

**Play now at:** [Our Live Website](https://group-engineering-project.onrender.com/)

Hosted on Render! Compaitable with desktop and mobile devices!

---

## How to Play:
- **Explore**🌍 – Follow the treasure hunts and discover sustainability hotspots.
- **Complete Quests**✅ – Take on eco-friendly challenges daily, weekly, and as part of the larger community, reviewed by our gamemaster Colum.
- **Collect and Learn**🏆 – Earn unique collectibles showing iconic places, SDGs, and sustainability facts.
- **Climb the Leaderboard**🚀 – Compete with friends and prove you’re the ultimate CarboCollector.

---

## 🎨 Team:
- Colum Bailey
- Finn Gosney
- Zeynep Guler
- Daniel Cook
- Jacob Nixon
- Matthew Dawson
- Kadeem Hannan

---

## Key Features 🌟
- **Sustainability Tasks**: Engage in activities like recycling and reducing your energy footprint.
- **Treasure Hunts**: Follow riddles and clues to visit important campus locations.
- **CarboPoints**: Earn points for completing tasks and collecting eco-friendly achievements.
- **CarboCards**: Unlock cards showcasing your progress, SDGs, and key campus spots.
- **Leaderboards**: Track your rank against friends and see who’s most dedicated to sustainability.

---

# How to Set Up and Run Locally ⚙️

Follow these steps to get the app running locally:

1. **Clone the Repository**  
   First, get the code from our GitHub repository:
   ```bash
   git clone https://github.com/FinnGos/Group-Engineering-Project.git
	```


## Setting Up Dependencies 
### 1. **Navigate to "Group-Engineering-Project/"**
 - this is where requirements.txt sits and can be done using cd Group-Engineering-Project

### 2. Create your virtual environment folder
```bash 
python -m venv venv
```

### 3. Load your virtual environment
If you are on macOS or Linux, run the following command 
```bash 
source venv/bin/activate
```
If you are on windows run this instead 
```Powershell 
venv\Scripts\activate
```
- These commands activate the virtual environment so when run it, your terminal should preface every command with (venv)

### 4. Install the dependencies in requirements.txt by running this command 
```bash
pip install -r requirements.txt
```


## Running the Django Server
1. In order to run the server, navigate to the folder with manage.py (Group-Engineering-Project/SustainableApplication)
	and run the following 
	```bash 
	python manage.py runserver
	```
	Please note that if this does not work you may need to change the python keyword at the start that works on your machine
	You could also try:
	```bash 
	python3 manage.py runserver
	```
 	```bash 
	py manage.py runserver
	```
  	or any other python keyword variation

	This starts the app on [http://127.0.0.1:8000](http://127.0.0.1:8000) (localhost).
	
## Accessing the App 
1. Once the server is running, open your preferred web browser.
2. In the address bar, type:  
    [http://127.0.0.1:8000](http://127.0.0.1:8000)
   This will take you to the login page.
3.  From there, you can log in or register to begin playing and completing sustainability tasks!

---
# How to test 💻

- Tests are built modular, and can be run all together
- To run them, follow the instructions under [How to Set Up and Run Locally ⚙️](#how-to-set-up-and-run-locally-⚙️)
- Until you get to [Running the Django Server](##running-the-django-server) where you should stop and run this instead

```bash 
python manage.py test
```
---
# Requirements
- The server runs on **Django** which uses python
- pip needs be installed
- Python 3.11.x should be used
- All other requirements should be accounting for in the virtual environment (venv)
---

# 📩 Contact:
Got questions, issues, or ideas? Direct all queries to our gamemaster: [cb1265@exeter.ac.uk](mailto:cb1265@exeter.ac.uk)
