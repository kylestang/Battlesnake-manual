import os
import time
import keyboard

import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""

def will_collide(board, pos):
    # Check wall collisions
    if  (
        pos["x"] < 0 
        or pos["y"] < 0
        or pos["x"] > board["width"] - 1
        or pos["y"] > board["height"] - 1
        ):
        return True

    # Check snakes for collisions, tail will not collide
    for snake in board["snakes"]:
        if pos in snake["body"][:-1]:
            return True
    
    # If no collisions, return False
    return False


class Battlesnake(object):

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "Kyle",  # TODO: Your Battlesnake Username
            "color": "#E80978",  # TODO: Personalize
            "head": "evil",  # TODO: Personalize
            "tail": "shac-weight",  # TODO: Personalize
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        # TODO: Use this function to decide how your snake is going to look on the board.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        current_time = time.time_ns()

        data = cherrypy.request.json

        timeout = current_time + ((data["game"]["timeout"] - 200) * 1000000)
        
        if data["you"]["body"][0]["y"] < data["you"]["body"][1]["y"]: move = "down"
        elif data["you"]["body"][0]["x"] < data["you"]["body"][1]["x"]: move = "left"
        elif data["you"]["body"][0]["x"] > data["you"]["body"][1]["x"]: move = "right"
        else: move = "up"

        while(time.time_ns() < timeout):
            if keyboard.is_pressed("up"):
                move = "up"
                break
            if keyboard.is_pressed("down"):
                move = "down"
                break
            if keyboard.is_pressed("left"):
                move = "left"
                break
            if keyboard.is_pressed("right"): 
                move = "right"
                break

            time.sleep(0.001)
        
        head = data["you"]["head"]

        down_collision = will_collide(data["board"], {"x" : head["x"], "y" : head["y"] - 1})
        up_collision = will_collide(data["board"], {"x" : head["x"], "y" : head["y"] + 1})
        right_collision = will_collide(data["board"], {"x" : head["x"] + 1, "y" : head["y"]})
        left_collision = will_collide(data["board"], {"x" : head["x"] - 1, "y" : head["y"]})

        if(
            (move == "down" and down_collision)
            or (move == "up" and up_collision)
            or (move == "right" and right_collision)
            or (move == "left" and left_collision)
        ):
            if not down_collision: move = "down"
            elif not up_collision: move = "up"
            elif not right_collision: move = "right"
            elif not left_collision: move = "left"
        
        if timeout > time.time_ns():
            time.sleep((timeout - time.time_ns()) * 0.000000001)

        print(f"MOVE: {move}")
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"

if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "25580")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)