/* =========================================================
   EXAMORA
   Upload Page JavaScript
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        initializeUploadPage();

    }
);


/* =========================================================
   1. INITIALIZE UPLOAD PAGE
   ========================================================= */

function initializeUploadPage() {

    initializeUploadTabs();

    initializeModuleSelector();

    initializeFileDropZones();

    initializeFilePreview();

    initializeUploadValidation();

    initializeDragAndDrop();

}


/* =========================================================
   2. UPLOAD TYPE / TAB SELECTION
   ========================================================= */

function initializeUploadTabs() {

    const tabButtons =
        document.querySelectorAll(
            "[data-upload-kind]"
        );

    const kindInput =
        document.querySelector(
            'input[name="kind"]'
        );

    if (
        !tabButtons.length ||
        !kindInput
    ) {
        return;
    }


    tabButtons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    const kind =
                        button.dataset.uploadKind;

                    if (!kind) {
                        return;
                    }

                    kindInput.value =
                        kind;


                    tabButtons.forEach(
                        function (item) {

                            item.classList.remove(
                                "active"
                            );

                        }
                    );


                    button.classList.add(
                        "active"
                    );


                    updateUploadMode(
                        kind
                    );

                }
            );

        }
    );

}


/* =========================================================
   3. UPDATE UPLOAD MODE
   ========================================================= */

function updateUploadMode(kind) {

    const syllabusSection =
        document.querySelector(
            "[data-syllabus-section]"
        );

    const moduleSection =
        document.querySelector(
            "[data-module-section]"
        );


    if (
        syllabusSection &&
        moduleSection
    ) {

        if (kind === "syllabus") {

            syllabusSection.style.display =
                "block";

            moduleSection.style.display =
                "none";

        } else {

            syllabusSection.style.display =
                "none";

            moduleSection.style.display =
                "block";

        }

    }

}


/* =========================================================
   4. MODULE SELECTOR
   ========================================================= */

function initializeModuleSelector() {

    const moduleSelect =
        document.querySelector(
            'select[name="module_number"]'
        );

    const moduleButtons =
        document.querySelectorAll(
            "[data-module-number]"
        );


    if (moduleSelect) {

        moduleSelect.addEventListener(
            "change",
            function () {

                updateSelectedModule(
                    moduleSelect.value
                );

            }
        );

    }


    moduleButtons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    const number =
                        button.dataset.moduleNumber;

                    if (moduleSelect) {

                        moduleSelect.value =
                            number;

                    }

                    moduleButtons.forEach(
                        function (item) {

                            item.classList.remove(
                                "selected"
                            );

                        }
                    );

                    button.classList.add(
                        "selected"
                    );

                    updateSelectedModule(
                        number
                    );

                }
            );

        }
    );

}


/* =========================================================
   5. UPDATE SELECTED MODULE
   ========================================================= */

function updateSelectedModule(
    moduleNumber
) {

    const selectedLabel =
        document.querySelector(
            "[data-selected-module]"
        );

    if (!selectedLabel) {
        return;
    }


    if (!moduleNumber) {

        selectedLabel.textContent =
            "Select a module";

        return;

    }


    selectedLabel.textContent =
        `Module ${moduleNumber} selected`;

}


/* =========================================================
   6. FILE DROP ZONES
   ========================================================= */

function initializeFileDropZones() {

    const dropZones =
        document.querySelectorAll(
            ".file-drop"
        );


    dropZones.forEach(
        function (zone) {

            const input =
                zone.querySelector(
                    'input[type="file"]'
                );

            if (!input) {
                return;
            }


            zone.addEventListener(
                "click",
                function (event) {

                    if (
                        event.target === input
                    ) {
                        return;
                    }

                    input.click();

                }
            );

        }
    );

}


/* =========================================================
   7. FILE PREVIEW
   ========================================================= */

function initializeFilePreview() {

    const inputs =
        document.querySelectorAll(
            'input[type="file"]'
        );


    inputs.forEach(
        function (input) {

            input.addEventListener(
                "change",
                function () {

                    displaySelectedFiles(
                        input
                    );

                }
            );

        }
    );

}


/* =========================================================
   8. DISPLAY SELECTED FILES
   ========================================================= */

function displaySelectedFiles(
    input
) {

    const files =
        Array.from(
            input.files
        );


    const container =
        input.closest(
            ".upload-card, " +
            ".file-upload-card, " +
            ".upload-form, " +
            "form"
        );


    if (!container) {
        return;
    }


    let preview =
        container.querySelector(
            ".selected-files"
        );


    if (!files.length) {

        if (preview) {

            preview.innerHTML = "";

        }

        return;

    }


    if (!preview) {

        preview =
            document.createElement(
                "div"
            );

        preview.className =
            "selected-files";


        input.parentElement.appendChild(
            preview
        );

    }


    preview.innerHTML = "";


    files.forEach(
        function (file) {

            const item =
                document.createElement(
                    "div"
                );

            item.className =
                "selected-file-item";


            const icon =
                document.createElement(
                    "span"
                );

            icon.className =
                "selected-file-icon";

            icon.textContent =
                getFileIcon(
                    file.name
                );


            const info =
                document.createElement(
                    "div"
                );

            info.className =
                "selected-file-info";


            const name =
                document.createElement(
                    "strong"
                );

            name.textContent =
                file.name;


            const size =
                document.createElement(
                    "small"
                );

            size.textContent =
                formatFileSize(
                    file.size
                );


            info.appendChild(
                name
            );

            info.appendChild(
                size
            );


            item.appendChild(
                icon
            );

            item.appendChild(
                info
            );


            preview.appendChild(
                item
            );

        }
    );

}


/* =========================================================
   9. FILE ICON
   ========================================================= */

function getFileIcon(
    filename
) {

    const extension =
        filename
            .split(".")
            .pop()
            .toLowerCase();


    if (extension === "pdf") {
        return "PDF";
    }

    if (extension === "pptx") {
        return "PPT";
    }

    if (extension === "docx") {
        return "DOC";
    }

    if (extension === "txt") {
        return "TXT";
    }

    return "FILE";

}


/* =========================================================
   10. FILE SIZE
   ========================================================= */

function formatFileSize(
    bytes
) {

    if (!bytes) {
        return "0 KB";
    }


    const units = [
        "Bytes",
        "KB",
        "MB",
        "GB"
    ];


    const index =
        Math.floor(
            Math.log(bytes) /
            Math.log(1024)
        );


    const safeIndex =
        Math.min(
            index,
            units.length - 1
        );


    const value =
        bytes /
        Math.pow(
            1024,
            safeIndex
        );


    return (
        `${value.toFixed(
            safeIndex === 0 ? 0 : 1
        )} ${units[safeIndex]}`
    );

}


/* =========================================================
   11. DRAG AND DROP
   ========================================================= */

function initializeDragAndDrop() {

    const zones =
        document.querySelectorAll(
            ".file-drop"
        );


    zones.forEach(
        function (zone) {

            const input =
                zone.querySelector(
                    'input[type="file"]'
                );


            if (!input) {
                return;
            }


            zone.addEventListener(
                "dragover",
                function (event) {

                    event.preventDefault();

                    zone.classList.add(
                        "drag-over"
                    );

                }
            );


            zone.addEventListener(
                "dragleave",
                function () {

                    zone.classList.remove(
                        "drag-over"
                    );

                }
            );


            zone.addEventListener(
                "drop",
                function (event) {

                    event.preventDefault();

                    zone.classList.remove(
                        "drag-over"
                    );


                    const files =
                        event.dataTransfer.files;


                    if (!files.length) {
                        return;
                    }


                    try {

                        input.files =
                            files;

                        input.dispatchEvent(
                            new Event(
                                "change",
                                {
                                    bubbles: true
                                }
                            )
                        );

                    } catch (error) {

                        console.warn(
                            "Could not attach dropped files.",
                            error
                        );

                    }

                }
            );

        }
    );

}


/* =========================================================
   12. UPLOAD VALIDATION
   ========================================================= */

function initializeUploadValidation() {

    const forms =
        document.querySelectorAll(
            "form"
        );


    forms.forEach(
        function (form) {

            const fileInput =
                form.querySelector(
                    'input[type="file"]'
                );


            if (!fileInput) {
                return;
            }


            form.addEventListener(
                "submit",
                function (event) {

                    const files =
                        Array.from(
                            fileInput.files
                        );


                    if (!files.length) {

                        event.preventDefault();

                        showUploadMessage(
                            "Please select at least one study file.",
                            "error"
                        );

                        return;

                    }


                    const allowedExtensions = [
                        ".pdf",
                        ".pptx",
                        ".docx",
                        ".txt"
                    ];


                    const invalidFiles =
                        files.filter(
                            function (file) {

                                const name =
                                    file.name.toLowerCase();

                                return !allowedExtensions.some(
                                    function (extension) {

                                        return name.endsWith(
                                            extension
                                        );

                                    }
                                );

                            }
                        );


                    if (
                        invalidFiles.length
                    ) {

                        event.preventDefault();

                        showUploadMessage(
                            "Please upload only PDF, PPTX, DOCX or TXT files.",
                            "error"
                        );

                    }

                }
            );

        }
    );

}


/* =========================================================
   13. UPLOAD MESSAGE
   ========================================================= */

function showUploadMessage(
    message,
    type
) {

    let container =
        document.querySelector(
            ".upload-message"
        );


    if (!container) {

        container =
            document.createElement(
                "div"
            );

        container.className =
            "upload-message";


        const firstForm =
            document.querySelector(
                "form"
            );


        if (firstForm) {

            firstForm.prepend(
                container
            );

        }

    }


    container.textContent =
        message;

    container.className =
        `upload-message ${type}`;


    setTimeout(
        function () {

            if (container) {

                container.remove();

            }

        },
        4000
    );

}


/* =========================================================
   14. UPLOAD PROGRESS UI
   ========================================================= */

function showUploadProgress() {

    const progressContainer =
        document.querySelector(
            ".upload-progress"
        );


    if (!progressContainer) {
        return;
    }


    progressContainer.style.display =
        "block";


    let progress =
        0;


    const bar =
        progressContainer.querySelector(
            ".upload-progress-bar"
        );


    const text =
        progressContainer.querySelector(
            ".upload-progress-text"
        );


    const interval =
        setInterval(
            function () {

                progress += 5;


                if (progress > 95) {

                    progress = 95;

                }


                if (bar) {

                    bar.style.width =
                        `${progress}%`;

                }


                if (text) {

                    text.textContent =
                        `Processing ${progress}%`;

                }

            },
            120
        );


    return interval;

}


/* =========================================================
   15. UPLOAD PAGE CONSOLE MESSAGE
   ========================================================= */

console.log(
    "EXAMORA upload module initialized."
);