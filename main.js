/* =========================================================
   EXAMORA
   Main JavaScript
   ========================================================= */


/* =========================================================
   1. DOM READY
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        initializeMobileMenu();

        initializeFlashMessages();

        initializeFileInputs();

        initializeSmoothLinks();

        initializeAnimations();

    }
);


/* =========================================================
   2. MOBILE MENU
   ========================================================= */

function initializeMobileMenu() {

    const button =
        document.getElementById(
            "mobileMenuButton"
        );

    const menu =
        document.getElementById(
            "mobileMenu"
        );

    if (!button || !menu) {
        return;
    }

    button.addEventListener(
        "click",
        function () {

            menu.classList.toggle(
                "show"
            );

        }
    );


    document.addEventListener(
        "click",
        function (event) {

            const clickedInsideMenu =
                menu.contains(event.target);

            const clickedButton =
                button.contains(event.target);

            if (
                !clickedInsideMenu &&
                !clickedButton
            ) {

                menu.classList.remove(
                    "show"
                );

            }

        }
    );

}


/* =========================================================
   3. FLASH MESSAGE AUTO CLOSE
   ========================================================= */

function initializeFlashMessages() {

    const messages =
        document.querySelectorAll(
            ".flash-message"
        );

    messages.forEach(
        function (message) {

            setTimeout(
                function () {

                    message.style.opacity = "0";

                    message.style.transform =
                        "translateY(-8px)";

                    message.style.transition =
                        "opacity 0.3s ease, transform 0.3s ease";

                    setTimeout(
                        function () {

                            if (
                                message.parentElement
                            ) {

                                message.remove();

                            }

                        },
                        350
                    );

                },
                5000
            );

        }
    );

}


/* =========================================================
   4. FILE INPUT
   ========================================================= */

function initializeFileInputs() {

    const fileInputs =
        document.querySelectorAll(
            'input[type="file"]'
        );

    fileInputs.forEach(
        function (input) {

            input.addEventListener(
                "change",
                function () {

                    const label =
                        input.closest(
                            ".file-drop"
                        );

                    if (!label) {
                        return;
                    }

                    const files =
                        Array.from(
                            input.files
                        );

                    if (files.length === 0) {

                        return;

                    }


                    const textElement =
                        label.querySelector(
                            "span:not(.file-drop-icon)"
                        );

                    if (!textElement) {
                        return;
                    }


                    if (files.length === 1) {

                        textElement.textContent =
                            files[0].name;

                    } else {

                        textElement.textContent =
                            `${files.length} files selected`;

                    }


                    label.classList.add(
                        "file-selected"
                    );

                }
            );

        }
    );

}


/* =========================================================
   5. SMOOTH LINKS
   ========================================================= */

function initializeSmoothLinks() {

    const links =
        document.querySelectorAll(
            'a[href^="#"]'
        );

    links.forEach(
        function (link) {

            link.addEventListener(
                "click",
                function (event) {

                    const targetId =
                        link.getAttribute(
                            "href"
                        );

                    if (
                        !targetId ||
                        targetId === "#"
                    ) {

                        return;

                    }

                    const target =
                        document.querySelector(
                            targetId
                        );

                    if (!target) {
                        return;
                    }

                    event.preventDefault();

                    target.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });

                }
            );

        }
    );

}


/* =========================================================
   6. SIMPLE REVEAL ANIMATION
   ========================================================= */

function initializeAnimations() {

    const elements =
        document.querySelectorAll(
            ".feature-card, " +
            ".module-card, " +
            ".upload-card, " +
            ".question-card, " +
            ".score-card, " +
            ".content-card"
        );

    if (
        !("IntersectionObserver" in window)
    ) {

        return;

    }


    const observer =
        new IntersectionObserver(
            function (entries) {

                entries.forEach(
                    function (entry) {

                        if (
                            entry.isIntersecting
                        ) {

                            entry.target.classList.add(
                                "visible"
                            );

                            observer.unobserve(
                                entry.target
                            );

                        }

                    }
                );

            },
            {
                threshold: 0.08
            }
        );


    elements.forEach(
        function (element) {

            element.classList.add(
                "reveal-element"
            );

            observer.observe(
                element
            );

        }
    );

}


/* =========================================================
   7. NUMBER ANIMATION
   ========================================================= */

function animateNumber(
    element,
    target,
    duration = 800
) {

    if (!element) {
        return;
    }


    const start = 0;

    const startTime =
        performance.now();


    function updateNumber(
        currentTime
    ) {

        const elapsed =
            currentTime - startTime;

        const progress =
            Math.min(
                elapsed / duration,
                1
            );


        const eased =
            1 -
            Math.pow(
                1 - progress,
                3
            );


        const currentValue =
            Math.round(
                start +
                (target - start) *
                eased
            );


        element.textContent =
            currentValue;


        if (progress < 1) {

            requestAnimationFrame(
                updateNumber
            );

        }

    }


    requestAnimationFrame(
        updateNumber
    );

}


/* =========================================================
   8. PREVENT DOUBLE SUBMISSION
   ========================================================= */

document.addEventListener(
    "submit",
    function (event) {

        const form =
            event.target;

        if (
            !form ||
            form.tagName !== "FORM"
        ) {

            return;

        }


        const submitButton =
            form.querySelector(
                'button[type="submit"]'
            );

        if (!submitButton) {
            return;
        }


        if (
            form.dataset.submitting === "true"
        ) {

            event.preventDefault();

            return;

        }


        form.dataset.submitting =
            "true";


        setTimeout(
            function () {

                submitButton.style.opacity =
                    "0.7";

                submitButton.style.pointerEvents =
                    "none";

            },
            0
        );

    }
);


/* =========================================================
   9. ESCAPE KEY
   ========================================================= */

document.addEventListener(
    "keydown",
    function (event) {

        if (
            event.key !== "Escape"
        ) {

            return;

        }


        const menu =
            document.getElementById(
                "mobileMenu"
            );

        if (menu) {

            menu.classList.remove(
                "show"
            );

        }

    }
);


/* =========================================================
   10. CONSOLE MESSAGE
   ========================================================= */

console.log(
    "%cEXAMORA",
    "font-size:24px;font-weight:800;"
);

console.log(
    "AI-Powered Exam Preparation Assistant"
);

console.log(
    "EXAMORA frontend initialized successfully."
);