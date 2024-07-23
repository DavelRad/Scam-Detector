# **Scam-Detector**

Detect potential scams with the power of AI! Our Scam Detector Web Application seamlessly integrates Python, OpenAI, Google's Speech-to-Text API, and the Panel framework to provide a simple UI for detecting scam likelihood from audio input.


## **Features**



* **Real-time audio transcription** using Google's Speech-to-Text API
* **Scam likelihood assessment** using OpenAI's GPT-4o model
* **Simple and intuitive web-based user interface** built with Panel


## **Requirements**



* **Python 3.9** or higher
* **pip** (Python package installer)
* **Virtual environment** (recommended)


## **Installation**



1. Clone the repository: \
    ```
    git clone https://github.com/yourusername/scam-detector.git 
    cd scam-detector
    ```


2. Create and activate a virtual environment: \
    ```
    python3 -m venv myenv
    source myenv/bin/activate  # For macOS
    myenv\Scripts\activate     # For Windows
    ```


3. Install the required modules: 
    ```
    pip install panel openai speechrecognition
    ```

## **Setup**


### **macOS**



1. Activate the virtual environment:
   ```
    source myenv/bin/activate
   ```
3. Set your OpenAI API key:
   ```
    export OPENAI_API_KEY="YOUR_API_KEY"
   ```
5. Run the application: 
    ```
    panel serve main.py --show

    ```



### **Windows**



1. Activate the virtual environment:
    ```
    myenv\Scripts\activate
    ```
3. Set your OpenAI API key:
    * **Command Prompt (CMD)**:
    ```
    set OPENAI_API_KEY=YOUR_API_KEY
    ```
    * **PowerShell**:
    ```
    $env:OPENAI_API_KEY="YOUR_API_KEY"
    ```
4. Run the application:
    ```
    panel serve main.py --show
    ```

## **Usage**



* Click on the **Begin listening** button to start the audio transcription.
* The transcribed text will be analyzed for scam likelihood.
* Recommendations will be provided if a potential scam is detected.


## **Contributing**

Contributions are welcome! Please fork the repository and create a pull request with your changes.

---


Replace `YOUR_API_KEY` with your actual OpenAI API key in the instructions. You can also add more sections as needed, such as FAQs, screenshots of the UI, or detailed explanations of the features.
