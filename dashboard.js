/* =========================================================
   EXAMORA
   Dashboard JavaScript
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        initializeDashboard();

    }
);


/* =========================================================
   1. INITIALIZE DASHBOARD
   ========================================================= */

function initializeDashboard() {

    initializeProgressBars();

    initializeReadinessScore();

    initializeCounters();

    initializeModuleCards();

    initializeDashboardButtons();

    initializeCountdown();

}


/* =========================================================
   2. PROGRESS BARS
   ========================================================= */

function initializeProgressBars() {

    const progressBars =
        document.querySelectorAll(
            "[data-progress]"
        );


    progressBars.forEach(
        function (bar) {

            const value =
                parseFloat(
                    bar.dataset.progress
                );


            if (
                Number.isNaN(value)
            ) {

                return;

            }


            const percentage =
                Math.max(
                    0,
                    Math.min(
                        100,
                        value
                    )
                );


            bar.style.width = "0%";


            setTimeout(
                function () {

                    bar.style.width =
                        `${percentage}%`;

                },
                150
            );

        }
    );

}


/* =========================================================
   3. READINESS SCORE
   ========================================================= */

function initializeReadinessScore() {

    const elements =
        document.querySelectorAll(
            "[data-readiness]"
        );


    elements.forEach(
        function (element) {

            const score =
                parseFloat(
                    element.dataset.readiness
                );


            if (
                Number.isNaN(score)
            ) {

                return;

            }


            animateDashboardNumber(
                element,
                score,
                1000
            );

        }
    );

}


/* =========================================================
   4. COUNTER ANIMATION
   ========================================================= */

function initializeCounters() {

    const counters =
        document.querySelectorAll(
            "[data-counter]"
        );


    counters.forEach(
        function (counter) {

            const target =
                parseFloat(
                    counter.dataset.counter
                );


            if (
                Number.isNaN(target)
            ) {

                return;

            }


            animateDashboardNumber(
                counter,
                target,
                900
            );

        }
    );

}


/* =========================================================
   5. NUMBER ANIMATION
   ========================================================= */

function animateDashboardNumber(
    element,
    target,
    duration
) {

    const startTime =
        performance.now();


    function update(
        currentTime
    ) {

        const elapsed =
            currentTime -
            startTime;


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


        const value =
            Math.round(
                target * eased
            );


        element.textContent =
            `${value}%`;


        if (progress < 1) {

            requestAnimationFrame(
                update
            );

        }

    }


    requestAnimationFrame(
        update
    );

}


/* =========================================================
   6. MODULE CARDS
   ========================================================= */

function initializeModuleCards() {

    const cards =
        document.querySelectorAll(
            "[data-module-card]"
        );


    cards.forEach(
        function (card) {

            card.addEventListener(
                "mouseenter",
                function () {

                    card.classList.add(
                        "module-hover"
                    );

                }
            );


            card.addEventListener(
                "mouseleave",
                function () {

                    card.classList.remove(
                        "module-hover"
                    );

                }
            );


            card.addEventListener(
                "click",
                function () {

                    const moduleNumber =
                        card.dataset.moduleCard;


                    if (!moduleNumber) {
                        return;
                    }


                    const target =
                        document.querySelector(
                            `#module-${moduleNumber}`
                        );


                    if (target) {

                        target.scrollIntoView({
                            behavior: "smooth",
                            block: "center"
                        });

                    }

                }
            );

        }
    );

}


/* =========================================================
   7. DASHBOARD BUTTONS
   ========================================================= */

function initializeDashboardButtons() {

    const buttons =
        document.querySelectorAll(
            "[data-dashboard-action]"
        );


    buttons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    const action =
                        button.dataset.dashboardAction;


                    if (
                        action === "refresh"
                    ) {

                        refreshDashboard();

                    }


                    if (
                        action === "scroll-modules"
                    ) {

                        scrollToModules();

                    }

                }
            );

        }
    );

}


/* =========================================================
   8. REFRESH DASHBOARD
   ========================================================= */

function refreshDashboard() {

    const button =
        document.querySelector(
            '[data-dashboard-action="refresh"]'
        );


    if (button) {

        button.disabled = true;

        button.classList.add(
            "loading"
        );

    }


    setTimeout(
        function () {

            window.location.reload();

        },
        500
    );

}


/* =========================================================
   9. SCROLL TO MODULES
   ========================================================= */

function scrollToModules() {

    const modules =
        document.querySelector(
            ".module-priority-list, " +
            ".modules-section, " +
            "#modules"
        );


    if (!modules) {
        return;
    }


    modules.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

}


/* =========================================================
   10. COUNTDOWN TO EXAM
   ========================================================= */

function initializeCountdown() {

    const countdown =
        document.querySelector(
            "[data-exam-date]"
        );


    if (!countdown) {
        return;
    }


    const examDate =
        countdown.dataset.examDate;


    if (!examDate) {
        return;
    }


    const target =
        new Date(
            examDate
        ).getTime();


    if (
        Number.isNaN(target)
    ) {

        return;

    }


    function updateCountdown() {

        const now =
            new Date().getTime();


        const difference =
            target - now;


        if (
            difference <= 0
        ) {

            countdown.textContent =
                "Exam time";

            return;

        }


        const days =
            Math.floor(
                difference /
                (
                    1000 *
                    60 *
                    60 *
                    24
                )
            );


        const hours =
            Math.floor(
                (
                    difference %
                    (
                        1000 *
                        60 *
                        60 *
                        24
                    )
                ) /
                (
                    1000 *
                    60 *
                    60
                )
            );


        const minutes =
            Math.floor(
                (
                    difference %
                    (
                        1000 *
                        60 *
                        60
                    )
                ) /
                (
                    1000 *
                    60
                )
            );


        countdown.textContent =
            `${days}d ${hours}h ${minutes}m`;

    }


    updateCountdown();


    setInterval(
        updateCountdown,
        60000
    );

}


/* =========================================================
   11. ACTIVE NAVIGATION
   ========================================================= */

function initializeActiveNavigation() {

    const currentPath =
        window.location.pathname;


    const links =
        document.querySelectorAll(
            ".nav-link"
        );


    links.forEach(
        function (link) {

            const href =
                link.getAttribute(
                    "href"
                );


            if (!href) {
                return;
            }


            if (
                href === currentPath
            ) {

                link.classList.add(
                    "active"
                );

            }

        }
    );

}


initializeActiveNavigation();


/* =========================================================
   12. DASHBOARD TOOLTIP
   ========================================================= */

function initializeDashboardTooltips() {

    const elements =
        document.querySelectorAll(
            "[data-tooltip]"
        );


    elements.forEach(
        function (element) {

            element.addEventListener(
                "mouseenter",
                function () {

                    element.setAttribute(
                        "title",
                        element.dataset.tooltip
                    );

                }
            );

        }
    );

}


initializeDashboardTooltips();


/* =========================================================
   13. DASHBOARD CONSOLE MESSAGE
   ========================================================= */

console.log(
    "EXAMORA dashboard module initialized."
);