
const form = document.getElementById("download-form");

const urlInput = document.getElementById("youtube-url");
const formatInput = document.getElementById("audio-format");

const downloadButton = document.getElementById("download-button");
const statusText = document.getElementById("status");

const BACKEND_URL = "https://soundswap-jrvj.onrender.com";


form.addEventListener("submit", async (event) => {

    event.preventDefault();

    const url = urlInput.value.trim();
    const format = formatInput.value;

    downloadButton.disabled = true;
    downloadButton.textContent = "Converting...";
    statusText.textContent = "Processing your audio...";

    try {

        const response = await fetch(
            `${BACKEND_URL}/api/convert-youtube`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    url: url,
                    format: format
                })
            }
        );

        if (!response.ok) {
    let errorMessage = "Conversion failed";

    try {
        const errorData = await response.json();
        errorMessage = errorData.error || errorMessage;
    } catch {
        // Response was not JSON
    }

    throw new Error(errorMessage);
}

        const audioBlob = await response.blob();

        const downloadUrl = URL.createObjectURL(audioBlob);

        const downloadLink = document.createElement("a");

        downloadLink.href = downloadUrl;
        downloadLink.download = `audio.${format}`;

        document.body.appendChild(downloadLink);
        downloadLink.click();

        downloadLink.remove();

        URL.revokeObjectURL(downloadUrl);

        statusText.textContent = "Download completed!";

    } catch (error) {

        console.error(error);

        statusText.textContent =
    error.message || "Something went wrong. Please try again.";

    } finally {

        downloadButton.disabled = false;
        downloadButton.textContent = "Download";

    }

});