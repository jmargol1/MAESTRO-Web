document.addEventListener("DOMContentLoaded", function () {
    const voiceTypeSelect = document.getElementById("voice_type");
    const customVoiceSection = document.getElementById("custom-voice-section");

    voiceTypeSelect.addEventListener("change", function () {
        if (voiceTypeSelect.value === "custom") {
            customVoiceSection.style.display = "block";
        } else {
            customVoiceSection.style.display = "none";
        }
    });
});