import qi
import argparse
import sys
import time
from PIL import Image

def main(session):
    # Get a proxy to ALMotion
    motion = session.service("ALMotion")
    tts = session.service("ALTextToSpeech")
    leds = session.service("ALLeds")

    # Set the desired angle for Pepper's head yaw and pitch
    #head_yaw_angle = 0.0  # Keep head facing forward
    #head_pitch_angle = -0.4  # Look up at a pitch angle of -0.5 radians

    # Set the angles for the head yaw and pitch
    #motion.setAngles(["HeadYaw", "HeadPitch"], [head_yaw_angle, head_pitch_angle], 0.1)
    tts.say("Hello, look at me!")
    # Sleep to give time for head movement
    time.sleep(5)

    # Reset head angles to look forward
    # 

    # Get the service ALVideoDevice.
    video_service = session.service("ALVideoDevice")
    resolution = 2    # VGA
    colorSpace = 11   # RGB

    videoClient = video_service.subscribe("python_client", resolution, colorSpace, 5)
    

    t0 = time.time()

    # Get a camera image.
    # image[6] contains the image data passed as an array of ASCII chars.
    naoImage = video_service.getImageRemote(videoClient)

    t1 = time.time()
    # Time the image transfer.
    print("acquisition delay "), t1 - t0

    video_service.unsubscribe(videoClient)
    

    # Now we work with the image returned and save it as a PNG using ImageDraw package.

    # Get the image size and pixel array.
    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    array = naoImage[6]
    image_string = str(bytearray(array))

    # Create a PIL Image from our pixel array.
    im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)

    # Save the image to your host directory
    save_path = '/home/leo/pynaoqi/'  # Replace with your directory path
    image_filename = "camImage.png"
    full_save_path = save_path + image_filename
    im.save(full_save_path, "PNG")
    leds.off("FaceLeds")
    time.sleep(0.2)
    leds.on("FaceLeds")
    time.sleep(0.3)
    leds.off("FaceLeds")
    time.sleep(0.4)
    leds.on("FaceLeds")
    tts.say("Capturing accomplished. The image will be store in your host computer. It might take a little longer, while I am inferencing your emotion")
    motion.setAngles(["HeadYaw", "HeadPitch"], [0.0, 0.0], 0.1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="10.42.0.239",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
              "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)
