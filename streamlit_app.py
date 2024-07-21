import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load historical data if exists
try:
    df = pd.read_csv('vote_results.csv')
except FileNotFoundError:
    df = pd.DataFrame(columns=["时间", "杭州", "广州", "票差"])

# Remove duplicates, keeping the latest entry for each minute
df = df.drop_duplicates(subset="时间", keep="last")

# Convert the time column to only display hour and minute
df["时间"] = pd.to_datetime(df["时间"], format="%H:%M").dt.strftime("%H:%M")

# Streamlit app
# Remove the default title and display content directly
st.write("每分钟更新一次")

# Style the DataFrame for better visibility
def style_dataframe(df):
    styled_df = df.style.hide(axis="index").set_properties(**{'text-align': 'center'}).set_table_styles([{
        'selector': 'th',
        'props': [('text-align', 'center')]
    }])
    return styled_df

# Display the table and chart separately
st.subheader("投票数据表")
st.dataframe(style_dataframe(df), width=600, height=400)

st.subheader("投票数据走势")
fig, ax = plt.subplots(figsize=(10, 6))  # Increase the figure size for better readability
ax.plot(df["时间"], df["票差"], label="Difference", marker='o')
ax.set_xlabel("Time")
ax.set_ylabel("Difference in Votes")
ax.legend()
ax.grid(True)
plt.xticks(rotation=45)
plt.gca().invert_xaxis()  # Reverse the X-axis

# Format Y-axis to show numbers without scientific notation
ax.get_yaxis().get_major_formatter().set_scientific(False)

# Limit the number of X-axis labels to avoid clutter
max_xticks = 10
if len(df) > max_xticks:
    plt.xticks(df["时间"][::len(df) // max_xticks])

st.pyplot(fig)