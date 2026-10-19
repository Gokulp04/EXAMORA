from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify
)

from pathlib import Path
from datetime import datetime
import json

from config import (
    SECRET_KEY,
    UPLOAD_DIR,
    EXTRACTED_DIR,
    PROCESSED_DIR,
    MAX_CONTENT_LENGTH,
    create_required_directories
)

from services.file_service import (
    save_uploaded_file,
    extract_uploaded_file,
    allowed_file
)

from services.syllabus_service import (
    detect_modules
)

from services.module_service import (
    calculate_module_percentages,
    create_module_dashboard_data
)

from services.analysis_service import (
    analyze_module,
    generate_questions,
    create_study_plan,
    create_revision,
    calculate_readiness
)


# =========================================================
# EXAMORA APPLICATION
# =========================================================

app = Flask(__name__)

app.secret_key = SECRET_KEY

app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


# =========================================================
# CREATE REQUIRED DIRECTORIES
# =========================================================

create_required_directories()


# =========================================================
# DATA FILES
# =========================================================

MODULES_FILE = (
    PROCESSED_DIR /
    "modules.json"
)

ANALYSIS_FILE = (
    PROCESSED_DIR /
    "latest_analysis.json"
)


# =========================================================
# GLOBAL TEMPLATE DATA
# =========================================================

@app.context_processor
def inject_globals():

    return {
        "app_name": "EXAMORA",
        "app_tagline":
            "AI-Powered Exam Preparation Assistant",
        "year": datetime.now().year
    }


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route(
    "/dashboard",
    methods=["GET", "POST"]
)
def dashboard():

    if request.method == "POST":

        subject = request.form.get(
            "subject",
            ""
        ).strip()

        exam_date = request.form.get(
            "exam_date",
            ""
        ).strip()

        study_hours = request.form.get(
            "study_hours",
            "2"
        ).strip()


        # -------------------------------------------------
        # Validate Subject
        # -------------------------------------------------

        if not subject:

            flash(
                "Please enter your subject.",
                "error"
            )

            return redirect(
                url_for("dashboard")
            )


        # -------------------------------------------------
        # Validate Study Hours
        # -------------------------------------------------

        try:

            hours = float(
                study_hours
            )

            hours = max(
                0.5,
                min(hours, 24)
            )

        except (
            TypeError,
            ValueError
        ):

            hours = 2.0


        # -------------------------------------------------
        # Store Student Information
        # -------------------------------------------------

        session["subject"] = subject

        session["exam_date"] = (
            exam_date
        )

        session["study_hours"] = hours


        return redirect(
            url_for("upload")
        )


    return render_template(
        "dashboard.html",

        subject=session.get(
            "subject",
            ""
        ),

        exam_date=session.get(
            "exam_date",
            ""
        ),

        study_hours=session.get(
            "study_hours",
            2
        )
    )


# =========================================================
# UPLOAD PAGE
# =========================================================

@app.route(
    "/upload",
    methods=["GET", "POST"]
)
def upload():

    if request.method == "POST":

        kind = request.form.get(
            "kind",
            "module"
        )


        # -------------------------------------------------
        # Get Module Number
        # -------------------------------------------------

        module_number = request.form.get(
            "module_number",
            "1"
        )


        try:

            module_number = int(
                module_number
            )

        except (
            TypeError,
            ValueError
        ):

            module_number = 1


        if module_number not in range(1, 6):

            flash(
                "Invalid module number.",
                "error"
            )

            return redirect(
                url_for("upload")
            )


        # -------------------------------------------------
        # Select Target Directory
        # -------------------------------------------------

        if kind == "syllabus":

            target_directory = (
                UPLOAD_DIR /
                "syllabus"
            )

        else:

            target_directory = (
                UPLOAD_DIR /
                f"module_{module_number}"
            )


        # -------------------------------------------------
        # Get Uploaded Files
        # -------------------------------------------------

        uploaded_files = (
            request.files.getlist(
                "study_files"
            )
        )


        if (
            not uploaded_files
            or all(
                not file.filename
                for file in uploaded_files
            )
        ):

            flash(
                "Please choose at least one file.",
                "error"
            )

            return redirect(
                url_for("upload")
            )


        saved_files = []

        errors = []


        # -------------------------------------------------
        # Process Each File
        # -------------------------------------------------

        for file in uploaded_files:

            if not file.filename:
                continue


            # ---------------------------------------------
            # Validate File Type
            # ---------------------------------------------

            if not allowed_file(
                file.filename
            ):

                errors.append(
                    f"{file.filename}: "
                    "unsupported file type"
                )

                continue


            try:

                # -----------------------------------------
                # Save File
                # -----------------------------------------

                saved_path = (
                    save_uploaded_file(
                        file,
                        target_directory
                    )
                )


                # -----------------------------------------
                # Extract Text
                # -----------------------------------------

                extracted_text = (
                    extract_uploaded_file(
                        saved_path
                    )
                )


                # -----------------------------------------
                # Save Extracted Text
                # -----------------------------------------

                text_path = (
                    EXTRACTED_DIR /
                    f"{saved_path.stem}.txt"
                )


                text_path.write_text(
                    extracted_text,
                    encoding="utf-8"
                )


                saved_files.append({

                    "name":
                        saved_path.name,

                    "path":
                        str(saved_path),

                    "text_file":
                        str(text_path),

                    "text_length":
                        len(extracted_text)

                })


            except Exception as error:

                errors.append(
                    f"{file.filename}: {error}"
                )


        # =================================================
        # SYLLABUS PROCESSING
        # =================================================

        if (
            kind == "syllabus"
            and saved_files
        ):

            syllabus_text_parts = []


            for item in saved_files:

                text_path = Path(
                    item["text_file"]
                )


                if text_path.exists():

                    syllabus_text_parts.append(
                        text_path.read_text(
                            encoding="utf-8"
                        )
                    )


            combined_syllabus = (
                "\n\n".join(
                    syllabus_text_parts
                )
            )


            # ---------------------------------------------
            # Detect Modules
            # ---------------------------------------------

            modules = detect_modules(
                combined_syllabus
            )


            save_modules_data(
                modules
            )


            session[
                "syllabus_uploaded"
            ] = True


            flash(
                "Syllabus processed successfully.",
                "success"
            )


        # =================================================
        # MODULE MATERIAL PROCESSING
        # =================================================

        elif saved_files:

            current_files = session.get(
                "module_files",
                {}
            )


            module_key = str(
                module_number
            )


            current_files.setdefault(
                module_key,
                []
            )


            current_files[
                module_key
            ].extend(
                [
                    item["name"]
                    for item in saved_files
                ]
            )


            session[
                "module_files"
            ] = current_files


            # ---------------------------------------------
            # Merge Material With Module
            # ---------------------------------------------

            merge_module_material(
                module_number,
                saved_files
            )


            flash(
                f"{len(saved_files)} file(s) "
                f"uploaded for Module "
                f"{module_number}.",
                "success"
            )


        # =================================================
        # DISPLAY ERRORS
        # =================================================

        for error in errors:

            flash(
                error,
                "error"
            )


        return redirect(
            url_for("modules")
        )


    # =====================================================
    # GET REQUEST
    # =====================================================

    modules = load_modules_data()


    return render_template(
        "upload.html",
        modules=modules
    )


# =========================================================
# MODULES PAGE
# =========================================================

@app.route("/modules")
def modules():

    modules_data = (
        load_modules_data()
    )


    percentages = (
        calculate_module_percentages(
            modules_data
        )
    )


    dashboard_data = (
        create_module_dashboard_data(
            modules_data
        )
    )


    return render_template(
        "modules.html",

        modules=modules_data,

        percentages=percentages,

        dashboard_data=dashboard_data,

        syllabus_uploaded=session.get(
            "syllabus_uploaded",
            False
        )
    )


# =========================================================
# MODULE PREPARATION
# =========================================================

@app.route(
    "/prepare/<int:module_number>",
    methods=["GET", "POST"]
)
def prepare(module_number):

    # -----------------------------------------------------
    # Validate Module
    # -----------------------------------------------------

    if module_number not in range(1, 6):

        flash(
            "Invalid module.",
            "error"
        )

        return redirect(
            url_for("modules")
        )


    modules_data = (
        load_modules_data()
    )


    module = modules_data.get(
        str(module_number),
        {}
    )


    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        study_hours = request.form.get(
            "study_hours",
            session.get(
                "study_hours",
                2
            )
        )


        try:

            hours = float(
                study_hours
            )

            hours = max(
                0.5,
                min(hours, 24)
            )

        except (
            TypeError,
            ValueError
        ):

            hours = 2.0


        # -----------------------------------------------
        # Store Selected Module
        # -----------------------------------------------

        session[
            "selected_module"
        ] = module_number


        session[
            "study_hours"
        ] = hours


        return redirect(
            url_for("analysis")
        )


    # =====================================================
    # GET
    # =====================================================

    return render_template(
        "preparation.html",

        module_number=module_number,

        module=module,

        study_hours=session.get(
            "study_hours",
            2
        )
    )


# =========================================================
# ANALYSIS PAGE
# =========================================================

@app.route("/analysis")
def analysis():

    module_number = session.get(
        "selected_module"
    )


    if not module_number:

        flash(
            "Please select a module first.",
            "error"
        )

        return redirect(
            url_for("modules")
        )


    modules_data = (
        load_modules_data()
    )


    selected_module = (
        modules_data.get(
            str(module_number),
            {}
        )
    )


    # -----------------------------------------------------
    # Analyze ONLY Selected Module
    # -----------------------------------------------------

    analysis_result = (
        analyze_module(
            selected_module
        )
    )


    save_analysis_data(
        analysis_result
    )


    return render_template(
        "analysis.html",

        result=analysis_result,

        module_number=module_number
    )


# =========================================================
# QUESTIONS PAGE
# =========================================================

@app.route("/questions")
def questions():

    analysis_result = (
        load_analysis_data()
    )


    module_number = session.get(
        "selected_module"
    )


    if not analysis_result:

        flash(
            "Please analyze a module first.",
            "error"
        )

        return redirect(
            url_for("modules")
        )


    questions_data = (
        generate_questions(
            analysis_result
        )
    )


    return render_template(
        "questions.html",

        questions=questions_data,

        module_number=module_number
    )


# =========================================================
# RESULTS PAGE
# =========================================================

@app.route("/results")
def results():

    module_number = session.get(
        "selected_module"
    )


    analysis_result = (
        load_analysis_data()
    )


    if (
        not module_number
        or not analysis_result
    ):

        flash(
            "Please complete module analysis first.",
            "error"
        )

        return redirect(
            url_for("modules")
        )


    hours = session.get(
        "study_hours",
        2
    )


    # -----------------------------------------------------
    # Generate Study Plan
    # -----------------------------------------------------

    plan = create_study_plan(
        analysis_result,
        hours
    )


    # -----------------------------------------------------
    # Generate Revision
    # -----------------------------------------------------

    revision = create_revision(
        analysis_result
    )


    # -----------------------------------------------------
    # Calculate Readiness
    # -----------------------------------------------------

    readiness = calculate_readiness(
        analysis_result,
        hours
    )


    return render_template(
        "results.html",

        module_number=module_number,

        plan=plan,

        revision=revision,

        readiness=readiness,

        analysis=analysis_result
    )


# =========================================================
# HEALTH CHECK API
# =========================================================

@app.route("/api/health")
def health():

    return jsonify({

        "status":
            "ok",

        "service":
            "EXAMORA",

        "version":
            "1.0.0",

        "ai_mode":
            "local-intelligence",

        "timestamp":
            datetime.now().isoformat()

    })


# =========================================================
# SAVE MODULE DATA
# =========================================================

def save_modules_data(
    modules
):

    MODULES_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    with open(
        MODULES_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(

            modules,

            file,

            indent=4,

            ensure_ascii=False

        )


# =========================================================
# LOAD MODULE DATA
# =========================================================

def load_modules_data():

    # -----------------------------------------------------
    # If file doesn't exist
    # -----------------------------------------------------

    if not MODULES_FILE.exists():

        return {

            str(i): {

                "number": i,

                "title":
                    f"Module {i}",

                "content":
                    "",

                "topics":
                    []

            }

            for i in range(1, 6)

        }


    # -----------------------------------------------------
    # Read Existing Data
    # -----------------------------------------------------

    try:

        with open(
            MODULES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            modules = json.load(
                file
            )


        return modules


    except (
        json.JSONDecodeError,
        OSError
    ):

        return {

            str(i): {

                "number": i,

                "title":
                    f"Module {i}",

                "content":
                    "",

                "topics":
                    []

            }

            for i in range(1, 6)

        }


# =========================================================
# MERGE MODULE MATERIAL
# =========================================================

def merge_module_material(
    module_number,
    saved_files
):

    modules = (
        load_modules_data()
    )


    key = str(
        module_number
    )


    # -----------------------------------------------------
    # Create Module If Missing
    # -----------------------------------------------------

    if key not in modules:

        modules[key] = {

            "number":
                module_number,

            "title":
                f"Module {module_number}",

            "content":
                "",

            "topics":
                []

        }


    existing_content = (
        modules[key].get(
            "content",
            ""
        )
    )


    material_parts = []


    # -----------------------------------------------------
    # Read Extracted Text
    # -----------------------------------------------------

    for item in saved_files:

        text_file = Path(
            item["text_file"]
        )


        if text_file.exists():

            text = (
                text_file.read_text(
                    encoding="utf-8"
                ).strip()
            )


            if text:

                material_parts.append(
                    text
                )


    # -----------------------------------------------------
    # Merge Text
    # -----------------------------------------------------

    if material_parts:

        combined = (
            "\n\n".join(
                material_parts
            )
        )


        if existing_content.strip():

            modules[key][
                "content"
            ] = (

                existing_content

                + "\n\n"

                + combined

            )

        else:

            modules[key][
                "content"
            ] = combined


        # -----------------------------------------------
        # Detect Topics
        # -----------------------------------------------

        detected = detect_modules(

            f"MODULE {module_number}\n"
            +
            modules[key]["content"]

        )


        modules[key][
            "topics"
        ] = (

            detected[key][
                "topics"
            ]

        )


    # -----------------------------------------------------
    # Save Updated Module Data
    # -----------------------------------------------------

    save_modules_data(
        modules
    )


# =========================================================
# SAVE ANALYSIS DATA
# =========================================================

def save_analysis_data(
    analysis_result
):

    ANALYSIS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    with open(
        ANALYSIS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(

            analysis_result,

            file,

            indent=4,

            ensure_ascii=False

        )


# =========================================================
# LOAD ANALYSIS DATA
# =========================================================

def load_analysis_data():

    if not ANALYSIS_FILE.exists():

        return {}


    try:

        with open(
            ANALYSIS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )


    except (
        json.JSONDecodeError,
        OSError
    ):

        return {}


# =========================================================
# FILE TOO LARGE
# =========================================================

@app.errorhandler(413)
def file_too_large(error):

    flash(
        "File is too large. Maximum size is 50 MB.",
        "error"
    )


    return redirect(
        url_for("upload")
    )


# =========================================================
# PAGE NOT FOUND
# =========================================================

@app.errorhandler(404)
def page_not_found(error):

    return (
        render_template(
            "index.html"
        ),
        404
    )


# =========================================================
# GENERAL SERVER ERROR
# =========================================================

@app.errorhandler(500)
def internal_server_error(error):

    return (
        """
        <h1>EXAMORA Server Error</h1>
        <p>
            Something went wrong while processing
            your request.
        </p>
        <p>
            Check the terminal for the exact error.
        </p>
        """,
        500
    )


# =========================================================
# RUN EXAMORA
# =========================================================

if __name__ == "__main__":

    print()

    print(
        "=" * 60
    )

    print(
        "              WELCOME TO EXAMORA"
    )

    print(
        "=" * 60
    )

    print(
        "      AI-Powered Exam Preparation Assistant"
    )

    print(
        "=" * 60
    )

    print()

    print(
        "EXAMORA is starting..."
    )

    print(
        "Open your browser at:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print()

    print(
        "Press CTRL+C to stop the server."
    )

    print()


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )