from naoqi import ALProxy
import os

# IP address and port of your Pepper robot
robot_ip = "10.42.0.239"
robot_port = 9559

# Mapping of class indices to responses
class_responses = {
    '0': "You look angery sir, Terrifying",
    '1': "Are you feeling disgust?",
    '2': "Oh you are happy, I am glad",
    '3': "This might be your neutral face",
    '4': "You look sad sir",
    '5': "You might be feeling surprised"
}

# Create ALTextToSpeech proxy
tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)

# Folder path for .txt files
txt_folder = "/home/leo/pynaoqi"

try:
    # Iterate through .txt files in the folder
    for filename in os.listdir(txt_folder):
        if filename.lower().endswith(".txt"):
            txt_file_path = os.path.join(txt_folder, filename)
            
            # Read the content of the .txt file
            with open(txt_file_path, 'r') as txt_file:
                content = txt_file.read().strip()
                
                # Check if the content is a valid response
                if content in class_responses:
                    response = class_responses[content]
                    tts.say(response)
                else:
                    tts.say("Invalid response")

except Exception as e:
    print("Error:", e)
