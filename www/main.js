$(document).ready(function () {
    // Text Animation using textillate
    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        },
    });

    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true,
        },
    });

    // Start Voice Recognition with Confirmation
    function startVoiceRecognition() {
        let recognition = new webkitSpeechRecognition();
        recognition.lang = 'en-US';
        
        displayMessage("Listening..."); // Inform the user in the UI
        $("#Oval").attr("hidden", true);   // Hide Mic UI
        $("#SiriWave").attr("hidden", false); // Show Siri Wave Animation
        
        recognition.onresult = function (event) {
            let transcript = event.results[0][0].transcript;
            console.log("Recognized: ", transcript);

            // Confirmation Prompt
            let isCorrect = confirm(`Did you say: "${transcript}"?`);
            if (isCorrect) {
                console.log("Confirmed: ", transcript);
                eel.process_command(transcript)(displayResult);
                displayMessage(`Processing: "${transcript}"...`);
            } else {
                alert("Let's try again!");
                startVoiceRecognition();
            }
        };

        recognition.onerror = function (event) {
            alert("Error during recognition: " + event.error);
            displayMessage("Error occurred. Try again.");
        };

        recognition.start();
    }

    // Submit Text from Input Bar
    function submitText() {
        let userInput = $("#textInput").val().trim();
        if (userInput !== "") {
            console.log("User Input: ", userInput);
            eel.process_command(userInput)(displayResult);
            displayMessage(`Processing: "${userInput}"...`);
        } else {
            alert("Please enter a command or query!");
        }
    }

    // Display Backend Response in UI
    function displayResult(response) {
        console.log("Response: ", response);
        $("#output").text(response); // Display response
        $("#SiriWave").attr("hidden", true);
        $("#Oval").attr("hidden", false);
    }

    // Display Messages in Output Section
    function displayMessage(message) {
        $("#output").text(message);
    }

    // Button Click Listeners
    $("#MicBtn").click(function () {
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.playClickSound();
        startVoiceRecognition();
    });

    $("#submitTextBtn").click(function () {
        submitText();
    });

    $("#clearTextBtn").click(function () {
        $("#textInput").val("");
        $("#output").text("Input cleared.");
    });
});
