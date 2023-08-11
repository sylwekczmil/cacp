function waitForElm(selector) {
    return new Promise(resolve => {
        if (document.querySelector(selector)) {
            return resolve(document.querySelector(selector));
        }

        const observer = new MutationObserver(mutations => {
            if (document.querySelector(selector)) {
                resolve(document.querySelector(selector));
                observer.disconnect();
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });
}

function disableAllNavLinks() {
    document.querySelectorAll('.nav-link').forEach(navLink => {
        navLink.classList.add("disabled");
    })
}

function enableAllNavLinks() {
    document.querySelectorAll('.nav-link').forEach(navLink => {
        navLink.classList.remove("disabled");
    })
}

function runNavLinksRoutine() {
    setTimeout(() => {
        disableAllNavLinks()
        setTimeout(() => {
            enableAllNavLinks()
        }, 1000)
    }, 1)
}


var pushState = history.pushState;
history.pushState = function () {
    pushState.apply(history, arguments);
    runNavLinksRoutine()
};

waitForElm(".nav").then(() => {
    runNavLinksRoutine()
});
