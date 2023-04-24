import matplotlib.pyplot as plt
import numpy as np

# Create some sample data
data = np.random.rand(4)

# Create a bar plot with the coolwarm colormap
fig, ax = plt.subplots()
ax.bar(range(len(data)), data, color=plt.cm.coolwarm(data))

# Set the axis labels and title
ax.set_xlabel("X Label")
ax.set_ylabel("Y Label")
ax.set_title("Bar Plot with Colormap")

""" 
chart = (
    alt.Chart(average_alltime_mean)
    .mark_bar()
    .encode(
        x=alt.X(
            "Bundesland",
            axis=alt.Axis(labelFontSize=16, title=""),
            sort=alt.EncodingSortField(field="value", op="count", order="ascending"),
        ),
        y=alt.Y(
            "value",
            axis=alt.Axis(
                labelFontSize=16, title="Mean yearly air temperature since 1881"
            )
        ),
        #color=alt.Color("value", scale=alt.Scale(scheme="coolwarm"))
    )
    # .properties(width=500, height=300)
)

chart
# Set the chart background to white
#chart = chart.configure_view(fill="white")

# Display chart in Streamlit
#st.altair_chart(chart, use_container_width=True)
 """
 
 merged_df_short = merged_df[["Bundesland", "Bundesland"]]

my_order = merged_df_short.groupby("Bundesland")["value"].median().sort_values()

pivoted_data = merged_df_short.pivot(index=None, columns="Bundesland", values="value")

 

    
    fig4, ax = plt.subplots(figsize=(10, 3))
    ax = sns.boxplot(data=pivoted_data, orient="v", palette="coolwarm", linewidth=0.5)

    ax.set_ylabel("Air temperature in C")

    # Rotate x-axis labels by 90 degrees
    ax.set_xticklabels(ax.get_xticklabels(), rotation=75)

    # Remove x-axis label
    ax.set_xlabel("")
    ax.set(title="Boxplot of air temperature distribution from 1881 to 2022")

    st.pyplot(fig4)