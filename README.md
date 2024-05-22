# LavaRand Powered Spotify Shuffle 

## Overview
Inspired by Cloudflare's LavaRand, this project aims to improve Spotify's shuffle feature by leveraging true randomness derived from the chaotic motion of lava lamps. 

## Motivation
Entirely a gimmick/fun side project. Since Spotify's shuffling algorithm often feels stale/monotonous, I wanted to create a process that would unequivocally ensure the most random possible shuffle.

## Key Components
- **YOLOv8**: Trained model, detects and tracks lava lamp motion.
- **SHA-256**: Hashes keypoints to produce random numbers.
- **Spotify API**: Queues songs based on generated random indices.
- **tkinter**: Provides a user-friendly GUI for interaction.

## Installation
1. **Clone the repository**:
    ```bash
    git clone https://github.com/rawcsav/LavaShuf.git
    cd LavaShuf
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up Spotify API credentials**:
    - Create a `.env` file with your Spotify client ID, client secret, and redirect URI:
    ```plaintext
    CLIENT_ID=your_spotify_client_id
    CLIENT_SECRET=your_spotify_client_secret
    REDIRECT_URI=your_spotify_redirect_uri
    ```

## Usage
1. **Run the application**:
    ```bash
    python main.py
    ```

2. **Interact with the GUI**:
    - Hit the `Start` button to begin the process, it should open a new window with the camera feed. 
      - I had this setup to work with my phone's camera, so you may need to adjust the camera index in the code.
    - Once you have the camera aligned with the lava lamp(s), and you can see that it's accurately detecting with boundary boxes, press `y` to start the process.
      - The camera feed is strictly for visualization and getting everything aligned properly. Due to threading issues with OpenCV & MacOS, it will need to close this camera feed while actually gathering the images and calculating indices
    - Select a Spotify playlist.
    - Specify the number of songs to queue.
    - The system will then begin capturing lava lamp images and generating random picks
    - View the queued songs & associated blob data for each song queued
   
## Technical Approach
1. **Object Detection**: Uses YOLOv8 to detect and track lava lamp motion.
2. **Keypoint Tracking**: Utilizes ORB to track chaotic motion within the detected lava lamp.
3. **Random Number Generation**: Hashes keypoints using SHA-256 to produce random numbers.
4. **Spotify Integration**: Uses the Spotify API to queue songs based on generated random indices.

## Demonstration
A more exploratory and detailed write-up & demo is available [on my website.](https://rawcsav.com/projects/LavaShuf.html)

## License
This project is licensed under Attribution-ShareAlike 4.0 International

## Acknowledgements

The dataset used in training, validating, and testing the model was a combination of two pre-existing Roboflow datasets: [Lavalamp Dataset 1](https://universe.roboflow.com/frat-niversitesi-6qija/lavalamp) & [Lavalamp Dataset 2](https://universe.roboflow.com/timothe-ewart/lavarandom). All props and credit to the owners/creators of these two datasets :)