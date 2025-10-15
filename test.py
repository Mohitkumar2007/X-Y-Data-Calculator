import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="X-Y Data Calculator", page_icon="icon.png", layout="centered")

st.markdown("""
    <h2 style='text-align: center; color: #4CAF50;'>X-Y Data Calculator</h2>
    <p style='text-align: center; font-size:14px;'>Made by Mohit Kumar A</p>
    """, unsafe_allow_html=True)
st.write("---")

# Single selector for mode
mode = st.radio("Choose calculator:", ("Curve Fitting Data Calculator", "Co-Efficient Co-relation Data Calculator"))

# ddof selector: population (0) or sample (1)
ddof_choice = st.radio("Choose estimator:", ("Population (divide by N)", "Sample (divide by N-1)"))
ddof = 0 if ddof_choice.startswith("Population") else 1

# Helper: parse comma-separated numbers into numpy array of floats
def parse_numbers(text: str) -> np.ndarray:
    if text is None:
        return np.array([])
    parts = [p.strip() for p in text.split(",") if p.strip() != ""]
    if not parts:
        return np.array([])
    try:
        return np.array([float(p) for p in parts])
    except ValueError as ve:
        raise ValueError("Could not parse all values as numbers. Make sure input is comma-separated numbers.") from ve

def round_arr(arr, decimals=4):
    # Keep shape: convert scalars / arrays consistently
    return np.round(arr, decimals)

if mode == "Curve Fitting Data Calculator":
    st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Curve Fitting Data Calculator</h2>", unsafe_allow_html=True)
    st.write("---")

    st.subheader("Enter your data")
    with st.form(key="data_form"):
        x_values = st.text_input("Enter values of X (comma separated):", "1,2,3,4,5")
        y_values = st.text_input("Enter values of Y (comma separated):", "2,4,6,8,10")
        submit = st.form_submit_button("Generate Table")

    if submit:
        try:
            x = parse_numbers(x_values)
            y = parse_numbers(y_values)

            if len(x) == 0 or len(y) == 0:
                st.error("❌ Please enter both X and Y values.")
            elif len(x) != len(y):
                st.error("❌ Number of X and Y values must be the same.")
            else:
                # Calculations (columns rounded to 4 decimals)
                df = pd.DataFrame({
                    "X": round_arr(x),
                    "Y": round_arr(y),
                    "X²": round_arr(x ** 2),
                    "X³": round_arr(x ** 3),
                    "X⁴": round_arr(x ** 4),
                    "X*Y": round_arr(x * y),
                    "X²*Y": round_arr((x ** 2) * y)
                })

                st.subheader("Calculated Table")
                st.dataframe(df, use_container_width=True)

                # Summations (rounded)
                sums = {
                    "ΣX": round(float(np.sum(x)), 4),
                    "ΣY": round(float(np.sum(y)), 4),
                    "ΣX²": round(float(np.sum(x ** 2)), 4),
                    "ΣX³": round(float(np.sum(x ** 3)), 4),
                    "ΣX⁴": round(float(np.sum(x ** 4)), 4),
                    "Σ(X*Y)": round(float(np.sum(x * y)), 4),
                    "Σ(X²*Y)": round(float(np.sum((x ** 2) * y)), 4),
                }
                st.subheader("Summations")
                st.write(pd.DataFrame([sums]))

                # Plot only X vs Y for clarity
                st.subheader("Graphical Representation")
                # Provide a DataFrame with X and Y for line_chart / scatter
                st.line_chart(pd.DataFrame({"X": x, "Y": y}))

                st.info("✅ Table and graph generated successfully!")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

if mode == "Co-Efficient Co-relation Data Calculator":
    st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Co-Efficient Co-relation Data Calculator</h2>", unsafe_allow_html=True)
    st.write("---")
    st.subheader("Enter your data")

    with st.form(key="data1_form"):
        x_values = st.text_input("Enter values of X (comma separated):", "1,2,3,4,5")
        y_values = st.text_input("Enter values of Y (comma separated):", "2,4,6,8,10")
        submit = st.form_submit_button("Generate Table")

    if submit:
        try:
            x = parse_numbers(x_values)
            y = parse_numbers(y_values)

            if len(x) == 0 or len(y) == 0:
                st.error("Please enter valid data for both X and Y.")
            elif len(x) != len(y):
                st.error("The number of X and Y values must be the same.")
            else:
                # Means
                x_bar = round(float(np.mean(x)), 4)
                y_bar = round(float(np.mean(y)), 4)

                # Centered values (X = x - x̄, Y = y - ȳ)
                X = round_arr(x - x_bar)
                Y = round_arr(y - y_bar)
                X2 = round_arr(X ** 2)
                Y2 = round_arr(Y ** 2)
                XY = round_arr(X * Y)

                df = pd.DataFrame({
                    "x": round_arr(x),
                    "y": round_arr(y),
                    "X=x-x̄": X,
                    "Y=y-ȳ": Y,
                    "X²": X2,
                    "Y²": Y2,
                    "XY": XY,
                })
                st.subheader("Generated Data Table")
                st.dataframe(df, use_container_width=True)

                sums = {
                    "Σx": round(float(np.sum(x)), 4),
                    "Σy": round(float(np.sum(y)), 4),
                    "ΣX²": round(float(np.sum(X2)), 4),
                    "ΣY²": round(float(np.sum(Y2)), 4),
                    "ΣXY": round(float(np.sum(XY)), 4)
                }
                st.subheader("Summation Values")
                st.write(pd.DataFrame([sums]))

                # Avoid division by zero in degenerate cases
                denom = sums["ΣX²"]
                denom2 = sums["ΣX²"] * sums["ΣY²"]
                if denom == 0 or denom2 == 0:
                    st.error("Cannot compute coefficients: zero variance in data.")
                else:
                    r = round(sums["ΣXY"] / np.sqrt(denom2), 4)
                    b = round(sums["ΣXY"] / denom, 4)
                    a = round(y_bar - b * x_bar, 4)

                    # Correct labels: std vs variance; also give variance of squared values optionally
                    results = {
                        "Mean of X (x̄)": x_bar,
                        "Mean of Y (ȳ)": y_bar,
                        "Std Dev of X (σ_x)": round(float(np.std(x, ddof=ddof)), 4),
                        "Variance of X (σ²_x)": round(float(np.var(x, ddof=ddof)), 4),
                        # If you really want Var(X²) uncomment next line
                        # "Variance of X² (Var(X²))": round(float(np.var(x**2, ddof=ddof)), 4),
                        "Std Dev of Y (σ_y)": round(float(np.std(y, ddof=ddof)), 4),
                        "Variance of Y (σ²_y)": round(float(np.var(y, ddof=ddof)), 4),
                    }

                    results1 = {
                        "Correlation Coefficient (r)": r,
                        "Regression Coefficient (b)": b,
                        "Y-Intercept (a)": a,
                        "Regression Equation": f"y = {a} + {b}x",
                    }

                    st.subheader("Calculated Results")
                    # Combine both result dicts into one tidy table for compact display
                    combined = {**results, **results1}
                    st.write(pd.DataFrame([combined]))

                    st.info("✅ Results calculated successfully!")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

st.markdown(
    "<p style='text-align: center;'>Created by <a href='https://github.com/Mohitkumar2007'>Mohit Kumar A</a></p>",
    unsafe_allow_html=True)
