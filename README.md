# Carbo - Sustainability Game

## Description:
🎮 Welcome to **Carbo**! This is our task-based collectibles sustainability game. In this game, you will be given a few tasks to complete each day on the University of Exeter campus. Each task will relate to a way you can contribute to better sustainability, such as recycling or reducing energy consumption, to help contribute to a greener campus. You can also take part in riddles and treasure hunts visiting significant sites on campus.

All of these will earn you **CarboPoints** that you can spend to unlock **CarboCards** and climb to the top of the leaderboards. These collectibles will highlight key locations, Sustainable Development Goals, and other aspects of our university.

There are many cards to collect, points to earn, and fun facts to be learned, so good luck and have fun!  
**Play now at:** [Carbo.com](http://example.com)

---

## How to Play:
- **Explore**🌍 – Follow the treasure hunts and discover sustainability hotspots.
- **Complete Quests**✅ – Take on eco-friendly challenges daily, weekly, and as part of the larger community, reviewed by our gamemaster Colum Bailey.
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

# How to Set Up and Run the Server ⚙️

Follow these steps to get the app running locally:

1. **Clone the Repository**  
   First, get the code from our GitHub repository:
   ```bash
   git clone https://github.com/FinnGos/Group-Engineering-Project.git
```


## Setting Up Dependencies 
1. **Navigate to "SustainableApplication/SustainableApplication"**
 - this is where manage.py sits and can be done using cd SustainableApplication
2. **Create the virtual python environment** 

```bash
python3 -m venv venv
```
- This command creates the virtual environment where our dependencies are stored! 
3. If you are on macOS or Linux, run the following command 
```bash 
source venv/bin/activate
```
If you are on windows run this instead 
```Powershell 
venv\Scripts\activate
```
- These commands are designed to activate the virtual environment, when run your terminal should preface every command with (venv)
4. Install the dependencies in requirements.txt by running this command 
```bash
pip install -r requirements.txt
```


## Running the Django Server
1. In order to run the server, navigate to the folder with manage.py (SustainableApplication/SustainableApplication)
	and run the following 
	```bash 
python3 manage.py runserver
```
	Please note that if this does not work you may need to use python instead of python3

	This starts the app on http://127.0.0.1:8000 (localhost).
	
---
# Accessing the App 
1. Once the server is running, open your preferred web browser.
2. In the address bar, type:  
    `http://127.0.0.1:8000/accounts/login/` This will take you to the login page.
3.  From there, you can log in or register to begin playing and completing sustainability tasks!

---
## Development Notes 💻

- The server runs on **Django**: Make sure you have Python 3.x and pip installed.
- For testing features, make sure to follow the test plan provided in the **docs/** folder (if applicable).

---

## 📩 Contact:
Got questions, issues, or ideas? Direct all queries to our gamemaster: [cb1265@exeter.ac.uk](mailto:email@domain.com)
