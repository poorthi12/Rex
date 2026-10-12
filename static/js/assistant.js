
const commandForm = document.getElementById("command-form");
const commandInput = document.getElementById("command-input");
const sendButton = document.getElementById("send-button");

const responseText = document.getElementById("response-text");
const responseBox = document.getElementById("response-box");
const connectionStatus = document.getElementById("connection-status");
const assistantStatus = document.getElementById("assistant-status");

const commandCount = document.getElementById("command-count");
const successCount = document.getElementById("success-count");
const activityList = document.getElementById("activity-list");

const micButton = document.getElementById("mic-button");
const voiceTitle = document.getElementById("voice-title");
const voiceDescription = document.getElementById("voice-description");

let totalCommands = 0;
let successfulCommands = 0;
let recognition = null;
let isListening = false;

const commandHistory = [];

function setConnectionStatus(online) {
    connectionStatus.textContent = online ? "Connected to REX" : "Backend unavailable";
    assistantStatus.textContent = online ? "Online" : "Offline";

    const dot = document.querySelector(".status-dot");
    if (dot) {
        dot.style.background = online ? "#20d69a" : "#ff657a";
        dot.style.boxShadow = online
            ? "0 0 12px #20d69a99"
            : "0 0 12px #ff657a99";
    }
}

async function checkBackend() {
    try {
        const response = await fetch("/api/health");
        if (!response.ok) throw new Error("Health check failed");

        const data = await response.json();
        setConnectionStatus(data.status === "ok");
    } catch (error) {
        setConnectionStatus(false);
        console.error("REX backend health check failed:", error);
    }
}

function addActivity(text, status) {
    const item = {
        text,
        status,
        time: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit"
        })
    };

    commandHistory.unshift(item);

    if (commandHistory.length > 20) {
        commandHistory.pop();
    }

    renderHistory();
}

function renderHistory() {
    activityList.replaceChildren();

    if (commandHistory.length === 0) {
        const empty = document.createElement("p");
        empty.className = "empty-state";
        empty.textContent = "Your command history will appear here.";
        activityList.appendChild(empty);
        return;
    }

    commandHistory.forEach((item) => {
        const row = document.createElement("div");
        row.className = "activity-item";

        const icon = document.createElement("span");
        icon.className = "activity-check";
        icon.textContent = item.status === "success" ? "✓" : "!";
        if (item.status !== "success") {
            icon.style.color = "#ffb6a3";
            icon.style.background = "#40251f";
        }

        const copy = document.createElement("div");
        copy.className = "activity-copy";

        const title = document.createElement("strong");
        title.textContent = item.text;

        const time = document.createElement("span");
        time.textContent = `${item.time} · ${item.status}`;

        copy.append(title, time);
        row.append(icon, copy);
        activityList.appendChild(row);
    });
}

async function sendCommand(text) {
    const cleanedText = text.trim();

    if (!cleanedText) {
        responseText.textContent = "Please type a command first.";
        commandInput.focus();
        return;
    }

    if (cleanedText.length > 2000) {
        responseText.textContent = "Your command is too long.";
        return;
    }

    sendButton.disabled = true;
    commandInput.disabled = true;
    responseText.textContent = "REX is thinking...";
    voiceTitle.textContent = "Processing command";
    voiceDescription.textContent = "Please wait while REX processes your request.";

    try {
        const response = await fetch("/api/command", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: cleanedText })
        });

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const result = await response.json();

        totalCommands++;
        commandCount.textContent = String(totalCommands);

        const message = result.message || "REX returned no message.";
        let details = "";

        if (result.data && Object.keys(result.data).length > 0) {
            if (result.data.result !== undefined) {
                details = ` Result: ${result.data.result}`;
            } else if (result.data.time) {
                details = ` Current time: ${result.data.time}.`;
            } else if (result.data.date) {
                details = ` Today's date: ${result.data.date}.`;
            }
        }

        responseText.textContent = message + details;

        if (result.status === "success") {
            successfulCommands++;
            successCount.textContent = String(successfulCommands);
        }

        addActivity(cleanedText, result.status || "unknown");

        voiceTitle.textContent =
            result.status === "success" ? "Command completed" : "Command processed";

        voiceDescription.textContent = message;
        setConnectionStatus(true);
    } catch (error) {
        console.error("REX command failed:", error);

        responseText.textContent =
            "I couldn't reach the REX backend. Check that the FastAPI server is running, then try again.";

        voiceTitle.textContent = "Connection problem";
        voiceDescription.textContent = "Please check the backend server.";

        setConnectionStatus(false);
        addActivity(cleanedText, "failed");
    } finally {
        sendButton.disabled = false;
        commandInput.disabled = false;
        commandInput.value = "";
        commandInput.focus();
    }
}

commandForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    await sendCommand(commandInput.value);
});

document.querySelectorAll(".quick-action").forEach((button) => {
    button.addEventListener("click", () => {
        sendCommand(button.dataset.command || button.textContent.trim());
    });
});

document.getElementById("clear-history").addEventListener("click", () => {
    commandHistory.length = 0;
    renderHistory();
});

document.getElementById("text-tab").addEventListener("click", () => {
    document.getElementById("text-tab").classList.add("active");
    document.getElementById("voice-tab").classList.remove("active");
    commandInput.focus();
    voiceTitle.textContent = "Type your command";
    voiceDescription.textContent = "Enter a request in the command box below.";
});

document.getElementById("voice-tab").addEventListener("click", () => {
    document.getElementById("voice-tab").classList.add("active");
    document.getElementById("text-tab").classList.remove("active");
    voiceTitle.textContent = "Ready when you are";
    voiceDescription.textContent = "Press the microphone to try voice input, or type below.";
});

const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.lang = "en-IN";
    recognition.interimResults = false;
    recognition.continuous = false;

    recognition.onstart = () => {
        isListening = true;
        micButton.classList.add("listening");
        voiceTitle.textContent = "Listening...";
        voiceDescription.textContent = "Speak your command clearly.";
    };

    recognition.onresult = async (event) => {
        const transcript = event.results[0][0].transcript;
        commandInput.value = transcript;
        voiceDescription.textContent = `You said: "${transcript}"`;
        await sendCommand(transcript);
    };

    recognition.onerror = (event) => {
        voiceTitle.textContent = "Voice input unavailable";
        voiceDescription.textContent =
            event.error === "not-allowed"
                ? "Please allow microphone access in your browser."
                : `Speech recognition error: ${event.error}`;
    };

    recognition.onend = () => {
        isListening = false;
        micButton.classList.remove("listening");
    };

    micButton.addEventListener("click", () => {
        if (isListening) {
            recognition.stop();
        } else {
            try {
                recognition.start();
            } catch (error) {
                console.error("Could not start voice recognition:", error);
                voiceTitle.textContent = "Try again";
                voiceDescription.textContent = "Voice recognition could not start.";
            }
        }
    });
} else {
    micButton.addEventListener("click", () => {
        voiceTitle.textContent = "Voice input not supported";
        voiceDescription.textContent =
            "Try a recent version of Chrome or Edge, or use the text command box.";
    });
}

checkBackend();
renderHistory();
