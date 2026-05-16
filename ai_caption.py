# -----------------------------------
# FLOWPILOT SMART AI CAPTION GENERATOR
# -----------------------------------

topic = input("Enter topic: ")

topic_lower = topic.lower()

print("\n🚀 Generating smart AI captions...\n")

# -----------------------------------
# SPORTS / FIGHTING EVENTS
# -----------------------------------

if (
    "cricket" in topic_lower
    or "football" in topic_lower
    or "sports" in topic_lower
    or "tournament" in topic_lower
    or "boxing" in topic_lower
    or "ufc" in topic_lower
    or "mma" in topic_lower
    or "fight" in topic_lower
    or "wrestling" in topic_lower
    or "competition" in topic_lower
):

    whatsapp_msg = f"""
🏆 {topic} is HERE! 🔥

Get ready for adrenaline-pumping action, fierce competition, roaring crowds, and unforgettable moments! 💥

🔥 Event Highlights:
✅ Intense battles
✅ Competitive spirit
✅ Crowd energy
✅ Ultimate entertainment

📢 Gather your squad and witness the action LIVE!

#GameOn #ChampionMindset
"""

    linkedin_caption = f"""
🏆 Excited to announce {topic}! 🔥

Competitive events inspire discipline, teamwork, resilience, and passion.

This event promises thrilling moments, unforgettable experiences, and an atmosphere full of energy and determination.

Ready for the ultimate showdown? 🚀
"""

    instagram_caption = f"""
🔥 {topic} 🔥

Power. Passion. Performance 💥

Get ready for explosive action, epic moments, and crowd-roaring excitement 🏆

Who’s ready for the battle? 👊
"""

    hashtags = f"""
#{topic.replace(' ', '')}
#Sports
#FightNight
#Boxing
#MMA
#Champion
#GameOn
#Competition
#FlowPilotAI
"""

# -----------------------------------
# MUSIC / DJ / CONCERT
# -----------------------------------

elif (
    "music" in topic_lower
    or "concert" in topic_lower
    or "dj" in topic_lower
    or "dance" in topic_lower
    or "singing" in topic_lower
    or "festival" in topic_lower
):

    whatsapp_msg = f"""
🎵 {topic} is going to be LEGENDARY! 🔥

Feel the beats, enjoy the vibes, and experience an unforgettable night filled with music and energy 🎤✨

🔥 What’s waiting for you:
✅ Live performances
✅ DJ madness
✅ Amazing crowd vibes
✅ Non-stop entertainment

📢 Bring your friends and let the party begin! 🎉
"""

    linkedin_caption = f"""
🎶 Excited for {topic}! 🚀

Music events bring people together through energy, creativity, emotion, and unforgettable experiences.

Looking forward to an electrifying atmosphere and incredible performances! ✨
"""

    instagram_caption = f"""
🎧 BIG VIBES ONLY 🔥

{topic} is about to light up the stage 🎤✨

Music. Lights. Energy. Memories 💯

Who’s ready to lose themselves in the vibes? 🎶
"""

    hashtags = f"""
#{topic.replace(' ', '')}
#Music
#Concert
#DJNight
#LiveMusic
#Dance
#Festival
#Entertainment
#Vibes
#FlowPilotAI
"""

# -----------------------------------
# AI / TECH / CODING
# -----------------------------------

elif (
    "ai" in topic_lower
    or "hackathon" in topic_lower
    or "technology" in topic_lower
    or "coding" in topic_lower
    or "developer" in topic_lower
    or "python" in topic_lower
):

    whatsapp_msg = f"""
💻 {topic} is LIVE! 🚀

Step into the future of innovation, creativity, and technology 🔥

✨ Event Features:
✅ Coding challenges
✅ AI innovation
✅ Networking opportunities
✅ Real-world problem solving

📢 Connect with brilliant minds and build something amazing!
"""

    linkedin_caption = f"""
🚀 Excited to announce {topic}! 💡

Technology continues to transform the world, and this event focuses on innovation, creativity, collaboration, and impactful ideas.

Looking forward to connecting with passionate developers, creators, and innovators!
"""

    instagram_caption = f"""
💻 BUILD. CREATE. INNOVATE 🚀

{topic} is bringing together tech enthusiasts, developers, and innovators for an unforgettable experience 🔥

Ready to change the future? ⚡
"""

    hashtags = f"""
#{topic.replace(' ', '')}
#AI
#Technology
#Programming
#Coding
#Hackathon
#Innovation
#Developer
#Python
#FlowPilotAI
"""

# -----------------------------------
# GAMING / ESPORTS
# -----------------------------------

elif (
    "gaming" in topic_lower
    or "esports" in topic_lower
    or "bgmi" in topic_lower
    or "free fire" in topic_lower
    or "valorant" in topic_lower
    or "pubg" in topic_lower
):

    whatsapp_msg = f"""
🎮 {topic} is ON! 🔥

Get ready for intense battles, insane gameplay, and ultimate gaming action 🚀

🔥 Event Features:
✅ Competitive matches
✅ Team battles
✅ Exciting rewards
✅ Gaming entertainment

📢 Squad up and dominate the arena!
"""

    linkedin_caption = f"""
🎮 Excited to announce {topic}! 🚀

Gaming events encourage teamwork, strategy, leadership, and competitive spirit.

Looking forward to an action-packed esports experience!
"""

    instagram_caption = f"""
🎮 LOCK IN 🔥

{topic} is bringing pure gaming chaos ⚡

Clutch moments. Squad battles. Victory celebrations 🏆

Ready to dominate? 💯
"""

    hashtags = f"""
#{topic.replace(' ', '')}
#Gaming
#Esports
#BGMI
#Valorant
#PUBG
#Gamers
#Tournament
#FlowPilotAI
"""

# -----------------------------------
# BUSINESS / STARTUP
# -----------------------------------

elif (
    "startup" in topic_lower
    or "business" in topic_lower
    or "entrepreneur" in topic_lower
    or "summit" in topic_lower
):

    whatsapp_msg = f"""
📈 {topic} is here! 🚀

Connect with entrepreneurs, innovators, and ambitious minds ready to create impact.

🔥 What to expect:
✅ Networking
✅ Startup ideas
✅ Growth strategies
✅ Business innovation

📢 Let’s build the future together!
"""

    linkedin_caption = f"""
🚀 Excited to announce {topic}! 💼

Entrepreneurship drives innovation, leadership, and growth.

Looking forward to inspiring discussions, networking, and impactful ideas.
"""

    instagram_caption = f"""
💼 DREAM BIG. BUILD BIGGER 🚀

{topic} is where ideas turn into opportunities 🔥

Network. Learn. Grow. Repeat 💯
"""

    hashtags = f"""
#{topic.replace(' ', '')}
#Startup
#Business
#Entrepreneur
#Leadership
#Innovation
#Networking
#Success
#FlowPilotAI
"""

# -----------------------------------
# COLLEGE / FEST
# -----------------------------------

elif (
    "college" in topic_lower
    or "fest" in topic_lower
    or "campus" in topic_lower
):

    whatsapp_msg = f"""
🎉 {topic} is finally here! 🚀

Get ready for fun, excitement, competitions, performances, and unforgettable memories ✨

🔥 Event Highlights:
✅ Music & dance
✅ Fun activities
✅ Amazing performances
✅ Non-stop entertainment

📢 Bring your friends and enjoy the celebration!
"""

    linkedin_caption = f"""
🎉 Excited to announce {topic}! 🚀

College events create opportunities for creativity, leadership, collaboration, and unforgettable experiences.

Looking forward to celebrating talent and energy together!
"""

    instagram_caption = f"""
✨ COLLEGE VIBES = UNMATCHED 🔥

{topic} is bringing unforgettable memories, crazy energy, and nonstop fun 🚀

Who’s ready? 🎉
"""

    hashtags = f"""
#{topic.replace(' ', '')}
#CollegeFest
#CampusLife
#Students
#Fun
#Events
#Celebration
#FlowPilotAI
"""

# -----------------------------------
# DEFAULT CATEGORY
# -----------------------------------

else:

    whatsapp_msg = f"""
🚀 {topic} is happening soon!

Get ready for an exciting experience filled with energy, fun, and unforgettable moments 🔥

📢 Don’t miss out!
"""

    linkedin_caption = f"""
🚀 Excited to announce {topic}!

Looking forward to an engaging experience filled with opportunities, excitement, and meaningful moments.
"""

    instagram_caption = f"""
🔥 {topic} 🔥

Big energy. Big vibes. Big moments 🚀

Stay tuned for something unforgettable ✨
"""

    hashtags = f"""
#{topic.replace(' ', '')}
#Trending
#Events
#Viral
#FlowPilotAI
"""

# -----------------------------------
# OUTPUT
# -----------------------------------

print("========== WHATSAPP MESSAGE ==========")
print(whatsapp_msg)

print("\n========== LINKEDIN CAPTION ==========")
print(linkedin_caption)

print("\n========== INSTAGRAM CAPTION ==========")
print(instagram_caption)

print("\n========== HASHTAGS ==========")
print(hashtags)