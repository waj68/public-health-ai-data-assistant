
import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

# ----------------------------------------------------
# Page setup
# ----------------------------------------------------

st.set_page_config(
    page_title="Public Health AI Data Assistant",
    page_icon="🩺",
    layout="wide"
)

st.title("Public Health AI Data Assistant")
st.caption("Phase 3 preview: predefined questions plus safe free-text question capture")

st.markdown(
    """
    This prototype uses semi-synthetic outbreak and respiratory surveillance data.
    Users can select a predefined public health question and view the corresponding SQL query,
    result table, plain-language summary, and chart.

    Phase 3 begins by adding a free-text question box. At this stage, the free-text question
    is captured but not yet converted into SQL automatically.

    **Note:** These data are fictional and used only for demonstration.
    """
)

# ----------------------------------------------------
# DuckDB connection
# ----------------------------------------------------

con = duckdb.connect()

# ----------------------------------------------------
# Schema context for future AI SQL generation
# ----------------------------------------------------

SCHEMA_CONTEXT = """
You are a public health analytics SQL assistant.

Dataset:
This app uses semi-synthetic public health outbreak and respiratory surveillance data.
The data are fictional and used only for demonstration.

Tables:

1. facilities
- facility_id: unique facility identifier
- facility_name: fictional facility name
- facility_type: type of facility, such as long-term care, acute care, school, shelter, community clinic, or childcare centre
- health_zone: health region or zone
- city: city associated with the health zone
- capacity: approximate facility capacity

2. outbreak_events
- outbreak_id: unique outbreak identifier
- facility_id: links to facilities.facility_id
- disease: disease or syndrome associated with the outbreak
- outbreak_start_date: date the outbreak started
- outbreak_end_date: date the outbreak ended
- number_of_cases: total outbreak-associated cases
- number_hospitalized: outbreak-associated hospitalizations
- number_deaths: outbreak-associated deaths
- outbreak_status: open or closed outbreak status

3. weekly_respiratory_activity
- week_start_date: start date of the surveillance week
- health_zone: health region or zone
- virus: respiratory virus, such as Influenza, RSV, or COVID-19
- percent_positive: percent of tests positive for the virus
- test_volume: number of tests performed during the week
- activity_level: low, moderate, or high activity level

4. lab_testing
- week_start_date: start date of the testing week
- health_zone: health region or zone
- test_type: type of lab test
- tests_performed: number of tests performed
- positive_tests: number of positive tests

Relationships:
- outbreak_events.facility_id joins to facilities.facility_id
- weekly_respiratory_activity.health_zone can be compared with facilities.health_zone
- lab_testing.health_zone can be compared with weekly_respiratory_activity.health_zone
- lab_testing.week_start_date can be compared with weekly_respiratory_activity.week_start_date

Important interpretation rule:
The weekly_respiratory_activity table represents aggregate respiratory virus surveillance indicators. test_volume means number of tests performed, not number of outbreaks.

Safety rules:
- Generate DuckDB-compatible SQL only.
- Use SELECT queries only.
- Do not generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, or other modifying statements.
- Use only the tables and columns listed above.
- Do not expose real patient or confidential information.
"""

con = duckdb.connect()

SCHEMA_CONTEXT = """
...
"""

# ----------------------------------------------------
# SQL safety checker
# ----------------------------------------------------

def is_safe_select_query(sql_query):
    """
    Basic SQL safety checker for the prototype.
    Allows only read-only SELECT queries and blocks common modifying statements.
    """

    if not sql_query or not isinstance(sql_query, str):
        return False, "SQL query is empty or invalid."

    sql_lower = sql_query.strip().lower()

    if not sql_lower.startswith("select"):
        return False, "Only SELECT queries are allowed."

    blocked_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "truncate",
        "merge",
        "grant",
        "revoke"
    ]

    for keyword in blocked_keywords:
        if keyword in sql_lower:
            return False, f"Blocked keyword detected: {keyword}"

    return True, "SQL query passed the basic safety check."


# ----------------------------------------------------
# Rule-based SQL generator for Phase 3 prototype
# ----------------------------------------------------


def generate_rule_based_sql(user_question):
    """
    Rule-based SQL generator for a small set of supported free-text questions.
    This is not a real AI model yet.
    """

    question = user_question.strip().lower()

    if "facility type" in question and "highest" in question and "cases" in question:
        return """
            SELECT
                f.facility_type,
                SUM(o.number_of_cases) AS total_cases,
                COUNT(*) AS number_of_outbreaks,
                ROUND(AVG(o.number_of_cases), 1) AS average_cases_per_outbreak
            FROM 'data/outbreak_events.csv' o
            JOIN 'data/facilities.csv' f
                ON o.facility_id = f.facility_id
            GROUP BY f.facility_type
            ORDER BY total_cases DESC
            LIMIT 1;
        """

    elif "disease" in question and "most outbreaks" in question:
        return """
            SELECT
                disease,
                COUNT(*) AS number_of_outbreaks
            FROM 'data/outbreak_events.csv'
            GROUP BY disease
            ORDER BY number_of_outbreaks DESC
            LIMIT 1;
        """

    elif "rsv" in question and "health zone" in question and "positivity" in question:
        return """
            SELECT
                health_zone,
                ROUND(AVG(percent_positive), 1) AS average_rsv_percent_positive,
                SUM(test_volume) AS total_rsv_test_volume
            FROM 'data/weekly_respiratory_activity.csv'
            WHERE virus = 'RSV'
            GROUP BY health_zone
            ORDER BY average_rsv_percent_positive DESC
            LIMIT 1;
        """

    else:
        return None

# ----------------------------------------------------
# Predefined questions and SQL queries
# ----------------------------------------------------

queries = {
    "How many outbreaks occurred by disease?": """
        SELECT
            disease,
            COUNT(*) AS number_of_outbreaks
        FROM 'data/outbreak_events.csv'
        GROUP BY disease
        ORDER BY number_of_outbreaks DESC;
    """,

    "Which health zones had the most outbreaks?": """
        SELECT
            f.health_zone,
            COUNT(*) AS number_of_outbreaks,
            SUM(o.number_of_cases) AS total_cases
        FROM 'data/outbreak_events.csv' o
        JOIN 'data/facilities.csv' f
            ON o.facility_id = f.facility_id
        GROUP BY f.health_zone
        ORDER BY number_of_outbreaks DESC;
    """,

    "Which facilities reported the most outbreaks?": """
        SELECT
            f.facility_name,
            f.facility_type,
            f.health_zone,
            COUNT(*) AS number_of_outbreaks,
            SUM(o.number_of_cases) AS total_cases
        FROM 'data/outbreak_events.csv' o
        JOIN 'data/facilities.csv' f
            ON o.facility_id = f.facility_id
        GROUP BY
            f.facility_name,
            f.facility_type,
            f.health_zone
        ORDER BY number_of_outbreaks DESC, total_cases DESC
        LIMIT 10;
    """,

    "Which facility types had the most outbreaks?": """
        SELECT
            f.facility_type,
            COUNT(*) AS number_of_outbreaks,
            SUM(o.number_of_cases) AS total_cases,
            ROUND(AVG(o.number_of_cases), 1) AS average_cases_per_outbreak
        FROM 'data/outbreak_events.csv' o
        JOIN 'data/facilities.csv' f
            ON o.facility_id = f.facility_id
        GROUP BY f.facility_type
        ORDER BY number_of_outbreaks DESC;
    """,

    "How did outbreak activity change over time by disease?": """
        SELECT
            DATE_TRUNC('month', CAST(outbreak_start_date AS DATE)) AS outbreak_month,
            disease,
            COUNT(*) AS number_of_outbreaks,
            SUM(number_of_cases) AS total_cases
        FROM 'data/outbreak_events.csv'
        GROUP BY outbreak_month, disease
        ORDER BY outbreak_month, disease;
    """,

    "Which health zone had the highest average RSV percent positivity?": """
        SELECT
            health_zone,
            ROUND(AVG(percent_positive), 1) AS average_rsv_percent_positive,
            SUM(test_volume) AS total_rsv_test_volume
        FROM 'data/weekly_respiratory_activity.csv'
        WHERE virus = 'RSV'
        GROUP BY health_zone
        ORDER BY average_rsv_percent_positive DESC;
    """
}

# ----------------------------------------------------
# Section 1: Predefined question workflow
# ----------------------------------------------------

st.header("1. Predefined public health questions")

st.info(
    "Phase 2 uses predefined questions from the dropdown. "
    "These questions already have approved SQL queries connected to them."
)

selected_question = st.selectbox(
    "Choose a question:",
    list(queries.keys())
)

sql = queries[selected_question]

st.subheader("Generated SQL")
st.code(sql, language="sql")

if st.button("Run predefined query"):
    try:
        result = con.execute(sql).fetchdf()

        st.subheader("Results")
        st.dataframe(result, use_container_width=True)

        # ----------------------------------------------------
        # Plain-language summary
        # ----------------------------------------------------

        st.subheader("Plain-language summary")

        if selected_question == "How many outbreaks occurred by disease?":
            top_row = result.iloc[0]
            total_outbreaks = result["number_of_outbreaks"].sum()

            st.write(
                f"The dataset contains **{total_outbreaks} outbreaks** in total. "
                f"The disease with the highest number of outbreaks is **{top_row['disease']}**, "
                f"with **{top_row['number_of_outbreaks']} outbreaks**."
            )

        elif selected_question == "Which health zones had the most outbreaks?":
            top_row = result.iloc[0]

            st.write(
                f"The health zone with the highest number of outbreaks is **{top_row['health_zone']}**, "
                f"with **{top_row['number_of_outbreaks']} outbreaks** and "
                f"**{top_row['total_cases']} total outbreak-associated cases**."
            )

        elif selected_question == "Which facilities reported the most outbreaks?":
            top_row = result.iloc[0]

            st.write(
                f"The facility with the highest number of outbreaks is **{top_row['facility_name']}** "
                f"({top_row['facility_type']}, {top_row['health_zone']}), "
                f"with **{top_row['number_of_outbreaks']} outbreaks** and "
                f"**{top_row['total_cases']} total outbreak-associated cases**."
            )

        elif selected_question == "Which facility types had the most outbreaks?":
            top_row = result.iloc[0]

            st.write(
                f"The facility type with the highest number of outbreaks is **{top_row['facility_type']}**, "
                f"with **{top_row['number_of_outbreaks']} outbreaks**, "
                f"**{top_row['total_cases']} total cases**, and an average of "
                f"**{top_row['average_cases_per_outbreak']} cases per outbreak**."
            )

        elif selected_question == "How did outbreak activity change over time by disease?":
            top_row = result.sort_values("number_of_outbreaks", ascending=False).iloc[0]

            st.write(
                f"The highest monthly disease-specific outbreak count occurred for **{top_row['disease']}** "
                f"in **{top_row['outbreak_month']}**, with **{top_row['number_of_outbreaks']} outbreaks** "
                f"and **{top_row['total_cases']} total cases**."
            )

        elif selected_question == "Which health zone had the highest average RSV percent positivity?":
            top_row = result.iloc[0]

            st.write(
                f"The health zone with the highest average RSV percent positivity is "
                f"**{top_row['health_zone']}**, with an average RSV percent positivity of "
                f"**{top_row['average_rsv_percent_positive']}%** and "
                f"**{top_row['total_rsv_test_volume']} RSV tests**."
            )

        else:
            st.write("A plain-language summary is not configured for this question yet.")

        # ----------------------------------------------------
        # Visualization
        # ----------------------------------------------------

        st.subheader("Visualization")

        if selected_question == "How many outbreaks occurred by disease?":
            fig = px.bar(
                result,
                x="disease",
                y="number_of_outbreaks",
                title="Number of Outbreaks by Disease"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif selected_question == "Which health zones had the most outbreaks?":
            fig = px.bar(
                result,
                x="health_zone",
                y="number_of_outbreaks",
                title="Number of Outbreaks by Health Zone"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif selected_question == "Which facilities reported the most outbreaks?":
            fig = px.bar(
                result,
                x="facility_name",
                y="number_of_outbreaks",
                color="facility_type",
                title="Top Facilities by Number of Outbreaks"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif selected_question == "Which facility types had the most outbreaks?":
            fig = px.bar(
                result,
                x="facility_type",
                y="number_of_outbreaks",
                title="Number of Outbreaks by Facility Type"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif selected_question == "How did outbreak activity change over time by disease?":
            fig = px.line(
                result,
                x="outbreak_month",
                y="number_of_outbreaks",
                color="disease",
                markers=True,
                title="Monthly Outbreak Trends by Disease"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif selected_question == "Which health zone had the highest average RSV percent positivity?":
            fig = px.bar(
                result,
                x="health_zone",
                y="average_rsv_percent_positive",
                title="Average RSV Percent Positivity by Health Zone"
            )
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("No chart configured for this question yet.")

    except Exception as e:
        st.error("The query could not be executed.")
        st.exception(e)


# ----------------------------------------------------
# Section 2: Phase 3 free-text question workflow
# ----------------------------------------------------

st.divider()

st.header("2. Try your own question — Phase 3 rule-based preview")

st.warning(
    "This section is a controlled Phase 3 prototype. "
    "It can answer a small set of supported free-text questions using rule-based SQL generation. "
    "A real AI model is not connected yet."
)

supported_questions = [
    "Which facility type had the highest total number of cases?",
    "Which disease had the most outbreaks?",
    "Which health zone had the highest average RSV percent positivity?"
]

with st.expander("View supported free-text questions"):
    for q in supported_questions:
        st.write(f"- {q}")

user_question = st.text_input(
    "Type your own public health data question:",
    placeholder="Example: Which facility type had the highest total number of cases?"
)

if st.button("Generate and run safe SQL"):
    if user_question.strip() == "":
        st.error("Please type a public health data question first.")

    else:
        st.subheader("Captured question")
        st.write(user_question)

        st.subheader("Schema context available to the assistant")
        with st.expander("View schema context"):
            st.text(SCHEMA_CONTEXT)

        generated_sql = generate_rule_based_sql(user_question)

        if generated_sql is None:
            st.error(
                "This question is not yet supported by the rule-based prototype. "
                "Try one of the supported questions listed above."
            )

        else:
            st.subheader("Generated SQL")
            st.code(generated_sql, language="sql")

            is_safe, safety_message = is_safe_select_query(generated_sql)

            st.subheader("SQL safety check")
            if is_safe:
                st.success(safety_message)
            else:
                st.error(safety_message)

            if is_safe:
                try:
                    result = con.execute(generated_sql).fetchdf()

                    st.subheader("Results")
                    st.dataframe(result, use_container_width=True)

                    st.subheader("Plain-language summary")

                    if "facility_type" in result.columns and "total_cases" in result.columns:
                        top_row = result.iloc[0]
                        st.write(
                            f"The facility type with the highest total number of cases is "
                            f"**{top_row['facility_type']}**, with **{top_row['total_cases']} total cases** "
                            f"across **{top_row['number_of_outbreaks']} outbreaks**."
                        )

                    elif "disease" in result.columns and "number_of_outbreaks" in result.columns:
                        top_row = result.iloc[0]
                        st.write(
                            f"The disease with the highest number of outbreaks is "
                            f"**{top_row['disease']}**, with **{top_row['number_of_outbreaks']} outbreaks**."
                        )

                    elif "health_zone" in result.columns and "average_rsv_percent_positive" in result.columns:
                        top_row = result.iloc[0]
                        st.write(
                            f"The health zone with the highest average RSV percent positivity is "
                            f"**{top_row['health_zone']}**, with an average RSV positivity of "
                            f"**{top_row['average_rsv_percent_positive']}%**."
                        )

                    else:
                        st.write("The query ran successfully. Please review the result table above.")

                except Exception as e:
                    st.error("The generated SQL could not be executed.")
                    st.exception(e)
