import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="X-Y Data Calculator", page_icon="icon.png", layout="centered")

st.markdown("""
    <h2 style='text-align: center; color: #4CAF50;'>X-Y Data Calculator</h2>
    <p style='text-align: center; font-size:14px;'>Made by Mohit Kumar A</p>
    """, unsafe_allow_html=True)
st.write("---")

# Use a single selector instead of two independent checkboxes to avoid both being active
mode = st.radio("Choose calculator:", ("Curve Fitting Data Calculator", "Co-Efficient Co-relation Data Calculator"))


# Helper: parse a comma-separated string into a numpy array of floats with validation
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

if mode == "Curve Fitting Data Calculator":
    st.markdown("""
        <h2 style='text-align: center; color: #4CAF50;'>Curve Fitting Data Calculator</h2>
        """, unsafe_allow_html=True)
    st.write("---")

    # Input Section
    st.subheader("Enter your data")

    with st.form(key="data_form"):
        x_values = st.text_input("Enter values of X (comma separated):", "1,2,3,4,5")
        y_values = st.text_input("Enter values of Y (comma separated):", "2,4,6,8,10")
        submit = st.form_submit_button("Generate Table")

    if submit:
        try:
            # Convert input to lists of numbers using helper
            x = parse_numbers(x_values)
            y = parse_numbers(y_values)

            if len(x) == 0 or len(y) == 0:
                st.error("❌ Please enter both X and Y values.")
            elif len(x) != len(y):
                st.error("❌ Number of X and Y values must be the same.")
            else:
                # Calculations
                df = pd.DataFrame({
                    "X": x,
                    "Y": y,
                    "X²": x ** 2,
                    "X³": x ** 3,
                    "X⁴": x ** 4,
                    "X*Y": x * y,
                    "X²*Y": (x ** 2) * y
                })

                st.subheader("Calculated Table")
                st.dataframe(df, use_container_width=True)

                # Summations
                sums = {
                    "ΣX": np.sum(x),
                    "ΣY": np.sum(y),
                    "ΣX²": np.sum(x ** 2),
                    "ΣX³": np.sum(x ** 3),
                    "ΣX⁴": np.sum(x ** 4),
                    "Σ(X*Y)": np.sum(x * y),
                    "Σ(X²*Y)": np.sum((x ** 2) * y),
                }
                st.subheader("Summations")
                st.write(pd.DataFrame([sums]))

                # Graphical Representation
                st.subheader("Graphical Representation")
                st.line_chart(df[["X", "Y"]])  # Plot only X vs Y for clarity
                # Optional: Let user select columns to plot with st.multiselect

                st.info("✅ Table and graph generated successfully!")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")


if mode == "Co-Efficient Co-relation Data Calculator":
    # Input Section
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
                # Build table only when inputs are valid
                df = pd.DataFrame({
                    "x": x,
                    "y": y,
                    "X=x-x̄": x - np.mean(x),
                    "Y=y-ȳ": y - np.mean(y),
                    "X²": (x - np.mean(x)) ** 2,
                    "Y²": (y - np.mean(y)) ** 2,
                    "XY": (x - np.mean(x)) * (y - np.mean(y)),
                })
                st.subheader("Generated Data Table")
                st.dataframe(df, use_container_width=True)

                sums = {
                    "Σx": np.sum(x),
                    "Σy": np.sum(y),
                    "ΣX²": np.sum((x - np.mean(x)) ** 2),
                    "ΣY²": np.sum((y - np.mean(y)) ** 2),
                    "ΣXY": np.sum((x - np.mean(x)) * (y - np.mean(y)))
                }
                st.subheader("Summation Values")
                st.write(pd.DataFrame([sums]))

                # Avoid division by zero in degenerate cases
                denom = sums["ΣX²"]
                if denom == 0 or (sums["ΣX²"] * sums["ΣY²"]) == 0:
                    st.error("Cannot compute coefficients: zero variance in data.")
                else:
                    r = sums["ΣXY"] / np.sqrt(sums["ΣX²"] * sums["ΣY²"])
                    b = sums["ΣXY"] / sums["ΣX²"]
                    a = np.mean(y) - b * np.mean(x)

                    results = {
                        "Mean of X (x̄)": float(np.mean(x)),
                        "Mean of Y (ȳ)": float(np.mean(y)),
                        "Standard Deviation of X (σx)": float(np.std(x, ddof=1)),
                        "Standard Deviation of Y (σy)": float(np.std(y, ddof=1)),
                        "Correlation Coefficient (r)": float(r),
                        "Regression Coefficient (b)": float(b),
                        "Y-Intercept (a)": float(a)
                    }
                    # Round the displayed results for readability
                    results_rounded = {k: (round(v, 6) if isinstance(v, float) else v) for k, v in results.items()}
                    st.subheader("Calculated Results")
                    st.write(pd.DataFrame([results_rounded]))

                    st.info("✅ Table generated successfully!")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

st.markdown(
    "<p style='text-align: center;'>Created by <a href='https://github.com/Mohitkumar2007'>Mohit Kumar A</a></p>",
    unsafe_allow_html=True)

