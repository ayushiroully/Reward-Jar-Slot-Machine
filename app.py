from flask import Flask, jsonify, render_template_string
import random

app = Flask(__name__)

REWARDS = [
    "Take a coffee break ☕", "Go for a walk 🚶", "Do 10 push-ups 💪",
    "Listen to your favorite song 🎶", "Watch a funny video 😂",
    "Meditate 5 min 🧘", "Stretch 🙆", "Healthy snack 🍎", "Read 5 pages 📖",
    "Journal ✍️", "Call a friend 📞", "Plan a trip 🌍", "Play with a pet 🐶",
    "Power nap 😴", "Drink water 💧", "Gratitude 3 things 🙏", "Draw/Doodle 🎨",
    "Deep breathing 🌬️", "Shake it off 🕺", "Chocolate 🍫", "Desk workout 🖥️💪",
    "Fresh air 🌳", "Play game 🎮", "Write note 📝", "Podcast 🎧",
    "Organize desk 🗂️", "Smile 😊", "Weekend plan 📅", "5 min silence 🤫",
    "Kindness act 💝"
]

history = []

@app.route('/')
def index():
    html = """
<!DOCTYPE html>
<html>
<head>
<title>🎰 Slot Machine Reward Jar 🎰</title>
<style>
body { font-family: Arial; text-align:center; margin-top:50px; background:#f0f4f8; }
h1 { color:#2563eb; font-size:2em; }
button { font-size:20px; padding:10px 20px; cursor:pointer; border:none; border-radius:10px; background:#10b981; color:white; }
.slot { display:inline-block; width:150px; height:50px; margin:10px; line-height:50px; font-size:18px; background:white; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.2); overflow:hidden; }
ul { list-style:none; padding:0; margin-top:20px; max-width:500px; margin-left:auto; margin-right:auto; text-align:left; }
li { background:#fff; margin:5px 0; padding:5px 10px; border-radius:5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);}
</style>
</head>
<body>
<h1>🎰 Slot Machine Reward Jar 🎰</h1>
<button onclick="drawReward()">Draw Reward</button>
<div style="margin-top:30px;">
    <div class="slot" id="slot1">🎲</div>
    <div class="slot" id="slot2">🎲</div>
    <div class="slot" id="slot3">🎲</div>
</div>
<h2 id="finalReward" style="color:#f59e0b; margin-top:20px;"></h2>
<h3>History</h3>
<ul id="history"></ul>

<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
<script>
function sleep(ms){return new Promise(r=>setTimeout(r,ms));}

async function drawReward(){
    const slot1=document.getElementById("slot1");
    const slot2=document.getElementById("slot2");
    const slot3=document.getElementById("slot3");
    const final=document.getElementById("finalReward");
    final.innerText="";
    
    // spin animation
    let spins = 15;
    for(let i=0;i<spins;i++){
        slot1.innerText = Math.random().toString(36).substring(2,5);
        slot2.innerText = Math.random().toString(36).substring(2,5);
        slot3.innerText = Math.random().toString(36).substring(2,5);
        await sleep(50);
    }

    // fetch reward
    const response = await fetch("/draw");
    const data = await response.json();
    const reward = data.reward;

    // slot-style reveal one by one
    let parts = reward.split(' ');
    slot1.innerText = parts[0] || reward;
    await sleep(200);
    slot2.innerText = parts[1] || "";
    await sleep(200);
    slot3.innerText = parts.slice(2).join(' ') || "";
    
    final.innerText = "🎉 " + reward + " 🎉";

    // confetti
    confetti({particleCount: 100, spread:70, origin:{y:0.6}});

    // update history
    let histList=document.getElementById("history");
    histList.innerHTML="";
    data.history.slice().reverse().forEach(item=>{
        let li=document.createElement("li");
        li.textContent=item;
        histList.appendChild(li);
    });
}
</script>
</body>
</html>
"""
    return render_template_string(html)

@app.route('/draw', methods=['GET'])
def draw_reward():
    reward = random.choice(REWARDS)
    history.append(reward)
    return jsonify({"reward": reward, "history": history})

if __name__=="__main__":
    app.run(debug=True)
