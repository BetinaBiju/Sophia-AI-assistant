import eel

@eel.expose
def processTextInput(userInput):
    print(f"Received input: {userInput}")
    # Process the input and return a response
    response = "Hello, you said: " + userInput
    return response

eel.init('www')  # Path to your web folder
eel.start('index.html', size=(800, 600))  # Start the backend server
