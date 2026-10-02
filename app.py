from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="workforce_planning"
)


@app.route("/")
def home():
    cursor = db.cursor(dictionary=True)

    # Total Employees
    cursor.execute("SELECT COUNT(*) AS total FROM employees")
    total_employees = cursor.fetchone()["total"]

    # Total Skills
    cursor.execute("SELECT COUNT(*) AS total FROM skills")
    total_skills = cursor.fetchone()["total"]

    # Total Projects
    cursor.execute("SELECT COUNT(*) AS total FROM projects")
    total_projects = cursor.fetchone()["total"]

    # Available Employees
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM employees
        WHERE availability_status = 'Available'
    """)
    available_employees = cursor.fetchone()["total"]

    # Total Forecasts
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM forecasts
    """)
    total_forecasts = cursor.fetchone()["total"]

    # Average Predicted Demand
    cursor.execute("""
        SELECT COALESCE(AVG(predicted_demand), 0) AS average_demand
        FROM forecasts
    """)
    average_demand = cursor.fetchone()["average_demand"]
        # Latest AI Forecasts
    cursor.execute("""
        SELECT
            s.skill_name,
            f.forecast_month,
            f.predicted_demand
        FROM forecasts f
        JOIN skills s
            ON f.skill_id = s.skill_id
        ORDER BY f.forecast_month, s.skill_name
    """)

    forecast_summary = cursor.fetchall()

    cursor.close()

    return render_template(
        "index.html",
        total_employees=total_employees,
        total_skills=total_skills,
        total_projects=total_projects,
        available_employees=available_employees,
        total_forecasts=total_forecasts,
       average_demand=round(average_demand, 2),
      forecast_summary=forecast_summary
    )
@app.route("/employees/delete/<int:employee_id>")
def delete_employee(employee_id):

    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM employees
        WHERE employee_id = %s
    """, (employee_id,))

    db.commit()

    cursor.close()

    return redirect(url_for("employees"))
@app.route("/employees")
def employees():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            employee_id,
            employee_name,
            email,
            department,
            experience_years,
            availability_status
        FROM employees
        ORDER BY employee_id
    """)

    employee_list = cursor.fetchall()

    cursor.close()

    return render_template(
        "employees.html",
        employees=employee_list
    )
@app.route("/employees/add", methods=["GET", "POST"])
def add_employee():

    if request.method == "POST":

        employee_name = request.form["employee_name"]
        email = request.form["email"]
        department = request.form["department"]
        experience_years = request.form["experience_years"]
        availability_status = request.form["availability_status"]

        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO employees
            (employee_name, email, department, experience_years, availability_status)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            employee_name,
            email,
            department,
            experience_years,
            availability_status
        ))

        db.commit()

        cursor.close()

        return redirect(url_for("employees"))

    return render_template("add_employee.html")
@app.route("/employees/edit/<int:employee_id>", methods=["GET", "POST"])
def edit_employee(employee_id):

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        employee_name = request.form["employee_name"]
        email = request.form["email"]
        department = request.form["department"]
        experience_years = request.form["experience_years"]
        availability_status = request.form["availability_status"]

        cursor.execute("""
            UPDATE employees
            SET employee_name = %s,
                email = %s,
                department = %s,
                experience_years = %s,
                availability_status = %s
            WHERE employee_id = %s
        """, (
            employee_name,
            email,
            department,
            experience_years,
            availability_status,
            employee_id
        ))

        db.commit()
        cursor.close()

        return redirect(url_for("employees"))

    cursor.execute("""
        SELECT *
        FROM employees
        WHERE employee_id = %s
    """, (employee_id,))

    employee = cursor.fetchone()

    cursor.close()

    return render_template(
        "edit_employee.html",
        employee=employee
    )
@app.route("/skills")
def skills():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            skill_id,
            skill_name,
            skill_category
        FROM skills
        ORDER BY skill_id
    """)

    skill_list = cursor.fetchall()

    cursor.close()

    return render_template(
        "skills.html",
        skills=skill_list
    )
@app.route("/skills/add", methods=["GET", "POST"])
def add_skill():

    if request.method == "POST":

        skill_name = request.form["skill_name"]
        skill_category = request.form["skill_category"]

        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO skills
            (skill_name, skill_category)
            VALUES (%s, %s)
        """, (
            skill_name,
            skill_category
        ))

        db.commit()

        cursor.close()

        return redirect(url_for("skills"))

    return render_template("add_skill.html")
@app.route("/skills/edit/<int:skill_id>", methods=["GET", "POST"])
def edit_skill(skill_id):

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        skill_name = request.form["skill_name"]
        skill_category = request.form["skill_category"]

        cursor.execute("""
            UPDATE skills
            SET skill_name = %s,
                skill_category = %s
            WHERE skill_id = %s
        """, (
            skill_name,
            skill_category,
            skill_id
        ))

        db.commit()
        cursor.close()

        return redirect(url_for("skills"))

    cursor.execute("""
        SELECT *
        FROM skills
        WHERE skill_id = %s
    """, (skill_id,))

    skill = cursor.fetchone()

    cursor.close()

    return render_template(
        "edit_skill.html",
        skill=skill
    )
@app.route("/skills/delete/<int:skill_id>")
def delete_skill(skill_id):

    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM skills
        WHERE skill_id = %s
    """, (skill_id,))

    db.commit()

    cursor.close()

    return redirect(url_for("skills"))
@app.route("/employee-skills")
def employee_skills():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            es.employee_id,
            es.skill_id,
            e.employee_name,
            s.skill_name,
            es.proficiency_level
        FROM employee_skills es
        JOIN employees e
            ON es.employee_id = e.employee_id
        JOIN skills s
            ON es.skill_id = s.skill_id
        ORDER BY es.employee_id
    """)

    mapping_list = cursor.fetchall()

    cursor.close()

    return render_template(
        "employee_skills.html",
        mappings=mapping_list
    )
@app.route("/employee-skills/add", methods=["GET", "POST"])
def add_employee_skill():

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        employee_id = request.form["employee_id"]
        skill_id = request.form["skill_id"]
        proficiency_level = request.form["proficiency_level"]

        cursor.execute("""
            INSERT INTO employee_skills
            (employee_id, skill_id, proficiency_level)
            VALUES (%s, %s, %s)
        """, (
            employee_id,
            skill_id,
            proficiency_level
        ))

        db.commit()
        cursor.close()

        return redirect(url_for("employee_skills"))

    cursor.execute("""
        SELECT employee_id, employee_name
        FROM employees
        ORDER BY employee_name
    """)

    employees = cursor.fetchall()

    cursor.execute("""
        SELECT skill_id, skill_name
        FROM skills
        ORDER BY skill_name
    """)

    skills = cursor.fetchall()

    cursor.close()

    return render_template(
        "add_employee_skill.html",
        employees=employees,
        skills=skills
    )
@app.route("/employee-skills/edit/<int:employee_id>/<int:skill_id>",
           methods=["GET", "POST"])
def edit_employee_skill(employee_id, skill_id):

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        proficiency_level = request.form["proficiency_level"]

        cursor.execute("""
            UPDATE employee_skills
            SET proficiency_level = %s
            WHERE employee_id = %s
            AND skill_id = %s
        """, (
            proficiency_level,
            employee_id,
            skill_id
        ))

        db.commit()
        cursor.close()

        return redirect(url_for("employee_skills"))

    cursor.execute("""
        SELECT
            e.employee_name,
            s.skill_name,
            es.proficiency_level
        FROM employee_skills es
        JOIN employees e
            ON es.employee_id = e.employee_id
        JOIN skills s
            ON es.skill_id = s.skill_id
        WHERE es.employee_id = %s
        AND es.skill_id = %s
    """, (employee_id, skill_id))

    mapping = cursor.fetchone()

    cursor.close()

    return render_template(
        "edit_employee_skill.html",
        mapping=mapping
    )

@app.route("/employee-skills/delete/<int:employee_id>/<int:skill_id>")
def delete_employee_skill(employee_id, skill_id):

    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM employee_skills
        WHERE employee_id = %s
        AND skill_id = %s
    """, (
        employee_id,
        skill_id
    ))

    db.commit()
    cursor.close()

    return redirect(url_for("employee_skills"))
@app.route("/projects")
def projects():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            project_id,
            project_name,
            client_name,
            start_date,
            end_date,
            required_team_size
        FROM projects
        ORDER BY project_id
    """)

    project_list = cursor.fetchall()

    cursor.close()

    return render_template(
        "projects.html",
        projects=project_list
    )
@app.route("/projects/add", methods=["GET", "POST"])
def add_project():

    if request.method == "POST":

        project_name = request.form["project_name"]
        client_name = request.form["client_name"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        required_team_size = request.form["required_team_size"]

        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO projects
            (
                project_name,
                client_name,
                start_date,
                end_date,
                required_team_size
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            project_name,
            client_name,
            start_date,
            end_date,
            required_team_size
        ))

        db.commit()
        cursor.close()

        return redirect(url_for("projects"))

    return render_template("add_project.html")
@app.route("/projects/edit/<int:project_id>", methods=["GET", "POST"])
def edit_project(project_id):

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        project_name = request.form["project_name"]
        client_name = request.form["client_name"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        required_team_size = request.form["required_team_size"]

        cursor.execute("""
            UPDATE projects
            SET project_name = %s,
                client_name = %s,
                start_date = %s,
                end_date = %s,
                required_team_size = %s
            WHERE project_id = %s
        """, (
            project_name,
            client_name,
            start_date,
            end_date,
            required_team_size,
            project_id
        ))

        db.commit()
        cursor.close()

        return redirect(url_for("projects"))

    cursor.execute("""
        SELECT *
        FROM projects
        WHERE project_id = %s
    """, (project_id,))

    project = cursor.fetchone()

    cursor.close()

    return render_template(
        "edit_project.html",
        project=project
    )
@app.route("/projects/delete/<int:project_id>")
def delete_project(project_id):

    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM projects
        WHERE project_id = %s
    """, (project_id,))

    db.commit()
    cursor.close()

    return redirect(url_for("projects"))
@app.route("/project-requirements")
def project_requirements():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            pr.project_id,
            pr.skill_id,
            p.project_name,
            s.skill_name,
            pr.required_count
        FROM project_requirements pr
        JOIN projects p
            ON pr.project_id = p.project_id
        JOIN skills s
            ON pr.skill_id = s.skill_id
        ORDER BY pr.project_id, s.skill_name
    """)

    requirement_list = cursor.fetchall()

    cursor.close()

    return render_template(
        "project_requirements.html",
        requirements=requirement_list
    )
@app.route("/project-requirements/add", methods=["GET", "POST"])
def add_project_requirement():

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        project_id = request.form["project_id"]
        skill_id = request.form["skill_id"]
        required_count = request.form["required_count"]

        cursor.execute("""
            INSERT INTO project_requirements
            (project_id, skill_id, required_count)
            VALUES (%s, %s, %s)
        """, (
            project_id,
            skill_id,
            required_count
        ))

        db.commit()
        cursor.close()

        return redirect(url_for("project_requirements"))

    cursor.execute("""
        SELECT project_id, project_name
        FROM projects
        ORDER BY project_name
    """)

    projects = cursor.fetchall()

    cursor.execute("""
        SELECT skill_id, skill_name
        FROM skills
        ORDER BY skill_name
    """)

    skills = cursor.fetchall()

    cursor.close()

    return render_template(
        "add_project_requirement.html",
        projects=projects,
        skills=skills
    )
@app.route(
    "/project-requirements/edit/<int:project_id>/<int:skill_id>",
    methods=["GET", "POST"]
)
def edit_project_requirement(project_id, skill_id):

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        required_count = request.form["required_count"]

        cursor.execute("""
            UPDATE project_requirements
            SET required_count = %s
            WHERE project_id = %s
            AND skill_id = %s
        """, (
            required_count,
            project_id,
            skill_id
        ))

        db.commit()
        cursor.close()

        return redirect(url_for("project_requirements"))

    cursor.execute("""
        SELECT
            p.project_name,
            s.skill_name,
            pr.required_count
        FROM project_requirements pr
        JOIN projects p
            ON pr.project_id = p.project_id
        JOIN skills s
            ON pr.skill_id = s.skill_id
        WHERE pr.project_id = %s
        AND pr.skill_id = %s
    """, (project_id, skill_id))

    requirement = cursor.fetchone()

    cursor.close()

    return render_template(
        "edit_project_requirement.html",
        requirement=requirement
    )
@app.route(
    "/project-requirements/delete/<int:project_id>/<int:skill_id>"
)
def delete_project_requirement(project_id, skill_id):

    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM project_requirements
        WHERE project_id = %s
        AND skill_id = %s
    """, (
        project_id,
        skill_id
    ))

    db.commit()
    cursor.close()

    return redirect(url_for("project_requirements"))
@app.route("/assignments")
def assignments():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            ea.assignment_id,
            ea.employee_id,
            ea.project_id,
            e.employee_name,
            p.project_name,
            ea.allocation_percentage,
            ea.assignment_date
        FROM employee_assignments ea
        JOIN employees e
            ON ea.employee_id = e.employee_id
        JOIN projects p
            ON ea.project_id = p.project_id
        ORDER BY ea.assignment_id
    """)

    assignment_list = cursor.fetchall()

    cursor.close()

    return render_template(
        "assignments.html",
        assignments=assignment_list
    )
@app.route("/assignments/add", methods=["GET", "POST"])
def add_assignment():

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        employee_id = request.form["employee_id"]
        project_id = request.form["project_id"]
        allocation_percentage = request.form["allocation_percentage"]
        assignment_date = request.form["assignment_date"]

        cursor.execute("""
            INSERT INTO employee_assignments
            (
                employee_id,
                project_id,
                allocation_percentage,
                assignment_date
            )
            VALUES (%s, %s, %s, %s)
        """, (
            employee_id,
            project_id,
            allocation_percentage,
            assignment_date
        ))

        db.commit()
        cursor.close()

        return redirect(url_for("assignments"))

    cursor.execute("""
        SELECT employee_id, employee_name
        FROM employees
        ORDER BY employee_name
    """)

    employees = cursor.fetchall()

    cursor.execute("""
        SELECT project_id, project_name
        FROM projects
        ORDER BY project_name
    """)

    projects = cursor.fetchall()

    cursor.close()

    return render_template(
        "add_assignment.html",
        employees=employees,
        projects=projects
    )
@app.route("/assignments/edit/<int:assignment_id>", methods=["GET", "POST"])
def edit_assignment(assignment_id):

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        allocation_percentage = request.form["allocation_percentage"]
        assignment_date = request.form["assignment_date"]

        cursor.execute("""
            UPDATE employee_assignments
            SET allocation_percentage = %s,
                assignment_date = %s
            WHERE assignment_id = %s
        """, (
            allocation_percentage,
            assignment_date,
            assignment_id
        ))

        db.commit()
        cursor.close()

        return redirect(url_for("assignments"))

    cursor.execute("""
        SELECT
            ea.assignment_id,
            e.employee_name,
            p.project_name,
            ea.allocation_percentage,
            ea.assignment_date
        FROM employee_assignments ea
        JOIN employees e
            ON ea.employee_id = e.employee_id
        JOIN projects p
            ON ea.project_id = p.project_id
        WHERE ea.assignment_id = %s
    """, (assignment_id,))

    assignment = cursor.fetchone()

    cursor.close()

    return render_template(
        "edit_assignment.html",
        assignment=assignment
    )
@app.route("/assignments/delete/<int:assignment_id>")
def delete_assignment(assignment_id):

    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM employee_assignments
        WHERE assignment_id = %s
    """, (assignment_id,))

    db.commit()
    cursor.close()

    return redirect(url_for("assignments"))
@app.route("/workforce-demand")
def workforce_demand():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            wd.demand_id,
            wd.demand_month,
            s.skill_name,
            wd.required_employees
        FROM workforce_demand wd
        JOIN skills s
            ON wd.skill_id = s.skill_id
        ORDER BY wd.demand_month, s.skill_name
    """)

    demand_list = cursor.fetchall()

    cursor.close()

    return render_template(
        "workforce_demand.html",
        demands=demand_list
    )
@app.route("/workforce-demand/add", methods=["GET", "POST"])
def add_workforce_demand():

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        demand_month = request.form["demand_month"]
        skill_id = request.form["skill_id"]
        required_employees = request.form["required_employees"]

        cursor.execute("""
            INSERT INTO workforce_demand
            (
                demand_month,
                skill_id,
                required_employees
            )
            VALUES (%s, %s, %s)
        """, (
            demand_month,
            skill_id,
            required_employees
        ))

        db.commit()
        cursor.close()

        return redirect(url_for("workforce_demand"))

    cursor.execute("""
        SELECT
            skill_id,
            skill_name
        FROM skills
        ORDER BY skill_name
    """)

    skills = cursor.fetchall()

    cursor.close()

    return render_template(
        "add_workforce_demand.html",
        skills=skills
    )
@app.route("/workforce-demand/edit/<int:demand_id>", methods=["GET", "POST"])
def edit_workforce_demand(demand_id):

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        demand_month = request.form["demand_month"]
        skill_id = request.form["skill_id"]
        required_employees = request.form["required_employees"]

        cursor.execute("""
            UPDATE workforce_demand
            SET demand_month = %s,
                skill_id = %s,
                required_employees = %s
            WHERE demand_id = %s
        """, (
            demand_month,
            skill_id,
            required_employees,
            demand_id
        ))

        db.commit()
        cursor.close()

        return redirect(url_for("workforce_demand"))

    # Get existing demand record
    cursor.execute("""
        SELECT
            demand_id,
            demand_month,
            skill_id,
            required_employees
        FROM workforce_demand
        WHERE demand_id = %s
    """, (demand_id,))

    demand = cursor.fetchone()

    # Get all skills
    cursor.execute("""
        SELECT
            skill_id,
            skill_name
        FROM skills
        ORDER BY skill_name
    """)

    skills = cursor.fetchall()

    cursor.close()

    return render_template(
        "edit_workforce_demand.html",
        demand=demand,
        skills=skills
    )
@app.route("/workforce-demand/delete/<int:demand_id>")
def delete_workforce_demand(demand_id):

    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM workforce_demand
        WHERE demand_id = %s
    """, (demand_id,))

    db.commit()
    cursor.close()

    return redirect(url_for("workforce_demand"))
@app.route("/forecasts")
def forecasts():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            f.forecast_id,
            f.forecast_month,
            s.skill_name,
            f.predicted_demand,
            f.model_name
        FROM forecasts f
        JOIN skills s
            ON f.skill_id = s.skill_id
        ORDER BY f.forecast_month, s.skill_name
    """)

    forecast_list = cursor.fetchall()

    cursor.close()

    return render_template(
        "forecasts.html",
        forecasts=forecast_list
    )
# ==========================================
# RESOURCE GAP ANALYSIS
# ==========================================

@app.route("/resource-gap")
def resource_gap():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            skill_id,
            skill_name,
            required_employees,
            allocated_employees,
            resource_gap
        FROM resource_gap_view
        ORDER BY resource_gap DESC
    """)

    resource_gaps = cursor.fetchall()

    cursor.close()

    return render_template(
        "resource_gap.html",
        resource_gaps=resource_gaps
    )
# ==========================================
# FUTURE WORKFORCE GAP
# ==========================================

@app.route("/future-workforce-gap")
def future_workforce_gap():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            forecast_id,
            forecast_month,
            skill_id,
            skill_name,
            predicted_demand,
            allocated_employees,
            future_resource_gap
        FROM future_workforce_gap_view
        ORDER BY future_resource_gap DESC
    """)

    future_gaps = cursor.fetchall()

    cursor.close()

    return render_template(
        "future_workforce_gap.html",
        future_gaps=future_gaps
    )

# ==========================================
# WORKFORCE ANALYTICS
# ==========================================

@app.route("/analytics")
def analytics():

    cursor = db.cursor(dictionary=True)

    # Total Employees
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM employees
    """)
    total_employees = cursor.fetchone()["total"]

    # Total Historical Demand Records
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM workforce_demand
    """)
    total_demand_records = cursor.fetchone()["total"]

    # Total AI Forecasts
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM forecasts
    """)
    total_forecasts = cursor.fetchone()["total"]

    # Total Future Workforce Gap
    cursor.execute("""
        SELECT COALESCE(SUM(
            CASE
                WHEN future_resource_gap > 0
                THEN future_resource_gap
                ELSE 0
            END
        ), 0) AS total
        FROM future_workforce_gap_view
    """)
    total_future_gap = cursor.fetchone()["total"]

    # Historical Workforce Demand
    cursor.execute("""
        SELECT
            s.skill_name,
            wd.demand_month,
            wd.required_employees
        FROM workforce_demand wd
        JOIN skills s
            ON wd.skill_id = s.skill_id
        ORDER BY wd.demand_month, s.skill_name
    """)

    historical_demand = cursor.fetchall()

    # AI Forecast Data
    cursor.execute("""
        SELECT
            s.skill_name,
            f.forecast_month,
            f.predicted_demand
        FROM forecasts f
        JOIN skills s
            ON f.skill_id = s.skill_id
        ORDER BY f.forecast_month, s.skill_name
    """)

    forecast_data = cursor.fetchall()

    # Future Workforce Gap
    cursor.execute("""
        SELECT
            skill_name,
            predicted_demand,
            allocated_employees,
            future_resource_gap
        FROM future_workforce_gap_view
        ORDER BY future_resource_gap DESC
    """)

    future_gaps = cursor.fetchall()

    cursor.close()

    return render_template(
        "analytics.html",
        total_employees=total_employees,
        total_demand_records=total_demand_records,
        total_forecasts=total_forecasts,
        total_future_gap=round(total_future_gap, 2),
        historical_demand=historical_demand,
        forecast_data=forecast_data,
        future_gaps=future_gaps
    )

# ==========================================
# EMPLOYEE SKILL MATCHING
# ==========================================

@app.route("/skill-matching")
def skill_matching():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            project_id,
            project_name,
            skill_id,
            skill_name,
            required_count,
            employee_id,
            employee_name,
            department,
            experience_years,
            proficiency_level,
            skill_score
        FROM employee_skill_match_view
        ORDER BY
            project_id,
            skill_id,
            skill_score DESC,
            experience_years DESC
    """)

    matching_data = cursor.fetchall()

    cursor.close()

    return render_template(
        "skill_matching.html",
        matching_data=matching_data
    )
if __name__ == "__main__":
    app.run(debug=True)