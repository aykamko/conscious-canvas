const AVG_SEC_TO_CREATE = 10;

function isIOS() {
    if (/iPad|iPhone|iPod/.test(navigator.platform)) {
        return true;
    } else {
        return navigator.maxTouchPoints &&
            navigator.maxTouchPoints > 2 &&
            /MacIntel/.test(navigator.platform);
    }
}

function showElement(element) {
    element.style.visibility = "visible";
}
function hideElement(element) {
    element.style.visibility = "hidden";
}

function undisplayElement(element) {
    element.style.display = "none";
}
function displayElement(element) {
    element.style.display = "block";
}

// Updates the progress bar over N seconds until the 95% mark is reached.
function updateProgressOverNSeconds(progressBar, seconds) {
    const startTime = Date.now();
    const endTime = startTime + seconds * 1000;

    function updateProgress() {
        const now = Date.now();
        if (now > endTime) {
            return;
        }

        const progress = (now - startTime) / (endTime - startTime);
        progressBar.value = progress * 95;

        requestAnimationFrame(updateProgress);
    }

    requestAnimationFrame(updateProgress);
}