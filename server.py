import http.server
import socketserver
import json
import random
import os

PORT = 8091
# Ensure we use the current directory if run directly, or the hardcoded workspace if needed.
# Since the user runs it on their machine, os.getcwd() is safer than hardcoding /home/clawy/...
DIRECTORY = os.getcwd() 

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve index.html (the renamed file)
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        # Allow both old and new endpoint for compatibility
        if self.path == '/api/tipi' or self.path == '/api/v3/tipi':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                responses = data.get('responses', [])
                
                # Check for 12 responses
                if len(responses) != 12:
                    error_msg = f"Expected 12 responses, got {len(responses)}"
                    print(error_msg)
                    self.send_error(400, error_msg)
                    return

                # MAPPING (12 items) - 2-3 items per Big Five trait
                # 0: Extraverted (+) -> E1
                # 1: Reserved (-)    -> E2 (Reverse)
                # 2: Critical (-)    -> A1 (Reverse)
                # 3: Sympathetic (+) -> A2
                # 4: Dependable (+)  -> C1
                # 5: Disorganized (-) -> C2 (Reverse)
                # 6: Anxious (-)     -> ES1 (Reverse)
                # 7: Calm (+)        -> ES2
                # 8: Open to new experiences (+) -> O1
                # 9: Conventional (-) -> O2 (Reverse)
                # 10: Complex (+)    -> O3
                # 11: Enthusiastic (+) -> E3

                # Reverse scoring: 8 - score

                # Extraversion: (0 + (8-1) + 11) / 3
                extraversion = (responses[0] + (8 - responses[1]) + responses[11]) / 3.0

                # Agreeableness: ((8-2) + 3) / 2
                agreeableness = ((8 - responses[2]) + responses[3]) / 2.0

                # Conscientiousness: (4 + (8-5)) / 2
                conscientiousness = (responses[4] + (8 - responses[5])) / 2.0

                # Emotional Stability: ((8-6) + 7) / 2
                emotional_stability = ((8 - responses[6]) + responses[7]) / 2.0

                # Openness: (8 + (8-9) + 10) / 3
                openness = (responses[8] + (8 - responses[9]) + responses[10]) / 3.0

                dish_profile = self.generate_dish(extraversion, agreeableness, conscientiousness, emotional_stability, openness)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(dish_profile).encode('utf-8'))
            except Exception as e:
                print(f"Error processing request: {e}")
                self.send_error(500, str(e))
        else:
            self.send_error(404)

    def generate_dish(self, E, A, C, ES, O):
        # Database of Real Dishes mapped to personality profiles
        
        dish = "Toast" # Fallback
        desc = "You are basic toast. Reliable, but maybe a bit dry."
        quote = "\"Simplicity is the ultimate sophistication.\" - Leonardo da Vinci"
        
        # 1. THE ARCHITECTS (High C, High O)
        if C > 5.0 and O > 5.0:
            if E > 4.5:
                dish = "Omakase Sushi Platter"
                desc = "You are a masterpiece of precision and variety. Every detail is calculated, yet you offer an exciting, high-end experience that demands attention."
                quote = "\"God is in the details.\" - Ludwig Mies van der Rohe"
            else:
                dish = "Traditional Kaiseki Dinner"
                desc = "You are refined, subtle, and deeply artistic. You value tradition and perfection over loud displays. You are a quiet masterpiece."
                quote = "\"The beautiful is always bizarre.\" - Charles Baudelaire"

        # 2. THE CHAOTIC CREATIVES (Low C, High O)
        elif C <= 4.0 and O > 5.0:
            if E > 5.0:
                dish = "Fusion Street Food Tacos"
                desc = "You are a messy, colorful explosion of conflicting flavors that somehow work. You break all the rules and taste like a party."
                quote = "\"Chaos is a ladder.\" - George R.R. Martin"
            else:
                dish = "Deconstructed Lemon Tart"
                desc = "You are confusing to some, but brilliant to those who 'get' it. You exist to challenge the status quo, even if you fall apart easily."
                quote = "\"To create is to destroy.\" - Pablo Picasso"

        # 3. THE TRADITIONALISTS (High C, Low O)
        elif C > 5.0 and O <= 4.0:
            if A > 5.0:
                dish = "Grandma's Sunday Roast"
                desc = "You are the definition of dependability and warmth. You stick to the recipe, you show up on time, and you make everyone feel safe."
                quote = "\"Tradition is not the worship of ashes, but the preservation of fire.\" - Gustav Mahler"
            else:
                dish = "Filet Mignon with Steamed Vegetables"
                desc = "You are high-quality, no-nonsense, and strictly disciplined. You don't need sauce to hide behind. You are pure efficiency."
                quote = "\"Discipline is the bridge between goals and accomplishment.\" - Jim Rohn"

        # 4. THE COMFORT SEEKERS (Low C, Low O)
        elif C <= 4.0 and O <= 4.0:
            if ES > 4.0:
                dish = "Macaroni and Cheese"
                desc = "You are simple, cheesy, and beloved. You don't care about presentation or pretension. You are here to vibe and be consumed on a couch."
                quote = "\"There is no love sincerer than the love of food.\" - George Bernard Shaw"
            else:
                dish = "Late Night Döner Kebab"
                desc = "You are a bit of a mess, but you are exactly what people need at 3 AM. You are chaotic comfort in a wrapper."
                quote = "\"In the midst of chaos, there is also opportunity.\" - Sun Tzu"

        # 5. THE SOCIALITES (High E, High A)
        elif E > 5.5 and A > 5.0:
            dish = "Spanish Paella"
            desc = "You are a communal feast! You bring people together, you are colorful, and you are meant to be shared with loud laughter and wine."
            quote = "\"Hell is other people. Heaven is other people eating.\" - Jean-Paul Sartre (Adapted)"

        # 6. THE INTENSE ONES (Low A, High E/N)
        elif A < 3.5 and ES < 3.5:
            dish = "Sichuan Mapo Tofu"
            desc = "You are numbing, spicy, and aggressive. You don't care if people like you; you demand to be felt. You are an intense experience."
            quote = "\"Man is the only animal that refuses to be what he is.\" - Albert Camus"

        # 7. THE ZEN MASTERS (Low E, High ES)
        elif E < 3.5 and ES > 5.5:
            dish = "Bowl of Plain White Rice"
            desc = "You are the foundation of civilization. You are calm, neutral, and stable. You don't need to shout to be essential."
            quote = "\"He who knows, does not speak. He who speaks, does not know.\" - Lao Tzu"

        # Catch-all
        else:
            if O >= max(C, E, A, ES):
                dish = "Aged Balsamic Vinegar"
                desc = "You are intense, complex, and acquired. Not everyone understands you, but those who do, value you highly."
                quote = "\"The unexamined life is not worth living.\" - Socrates"
            elif C >= max(O, E, A, ES):
                dish = "German Pretzel"
                desc = "You are structured, twisted in a specific way, and salty. A reliable classic."
                quote = "\"Order is the sanity of the mind, the health of the body, the peace of the city.\" - Robert Southey"
            elif E >= max(O, C, A, ES):
                dish = "Buffalo Wings"
                desc = "You are messy, spicy, and always the center of the party."
                quote = "\"Life is either a daring adventure or nothing.\" - Helen Keller"
            elif A >= max(O, C, E, ES):
                dish = "Warm Apple Pie"
                desc = "You are sweet, wholesome, and everyone loves you. You have zero enemies."
                quote = "\"Kindness is the language which the deaf can hear and the blind can see.\" - Mark Twain"
            else: 
                dish = "Soggy Cereal"
                desc = "You are having a bit of a breakdown right now, and that is okay. We have all been there."
                quote = "\"I think, therefore I am... tired.\" - René Descartes (maybe)"

        # Construct HTML output
        description = (
            f"<p>The algorithm has tasted your soul.</p>"
            f"<p style='font-size: 1.2rem; margin: 20px 0;'>{desc}</p>"
            f"<p style='font-style: italic; color: #888; margin-top: 15px;'>{quote}</p>"
            f"<hr>"
            f"<p style='font-size:0.9rem; color:#666;'><strong>Psychometric Flavor Profile:</strong><br>"
            f"Extraversion: {E:.1f} | Agreeableness: {A:.1f} | Conscientiousness: {C:.1f} | Emotional Stability: {ES:.1f} | Openness: {O:.1f}</p>"
        )

        return {
            "name": dish,
            "desc": description
        }

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    # Removed explicit OS.chdir to be safer when imported or run
    # Directory is handled by os.getcwd() now
    with ReusableTCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
