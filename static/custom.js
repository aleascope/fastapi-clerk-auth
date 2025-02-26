window.addEventListener('load', async function () {
    await Clerk.load();
    const currentUrl = window.location.href;
    
    if (Clerk.user) {
        document.querySelector('.auth-wrapper').innerHTML = `<div id="user-button"></div>`;
        const userButtonDiv = document.getElementById('user-button');
        
        Clerk.mountUserButton(userButtonDiv, {
            afterSignOutUrl: currentUrl, // Redirect back to the page user was on
        });
    } else {
        document.querySelector('.auth-wrapper').innerHTML = `<div id="sign-in"></div>`;
        const signInDiv = document.getElementById('sign-in');
        
        Clerk.mountSignIn(signInDiv, {
            forceRedirectUrl: currentUrl, // Redirect back to the page user was on
        });
    }
    
    let authWrapper = document.querySelector(".auth-wrapper");
    if (authWrapper) {
        authWrapper.classList.add("visible-auth");
    }

    const executeButtonContainer = document.querySelector('.swagger-ui');
    
    // Create a MutationObserver to monitor changes in the DOM
    const observer = new MutationObserver(() => {
        const executeButtons = document.querySelectorAll('.execute');
        if (executeButtons.length > 0) {
            executeButtons.forEach(button => {
                button.addEventListener('click', async () => {
                    await setToken();
                });
            });
        }
        const tryoutButtons = document.querySelectorAll('.try-out__btn');
        if (tryoutButtons.length > 0) {
            tryoutButtons.forEach(button => {
                if (Clerk.user) {
                    button.disabled = false;
                } else {
                    button.disabled = true;
                }
            });
        }
    });
    
    // Start observing for added nodes inside the Swagger UI
    observer.observe(executeButtonContainer, {
        childList: true,
        subtree: true,
    });
    
    async function setToken() {
        let token = await Clerk.session.getToken();
        if (token) {
            console.log("Clerk Token Injected into Swagger:", token);
            ui.preauthorizeApiKey("ClerkHTTPBearer", token);
        }
    }
});
