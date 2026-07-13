import plotly.express as px


def create_timeline_chart(df):
    """
    Creates the Netflix Content Added Over Time chart.
    """

    timeline_df = (
        df.groupby("year_added")
        .size()
        .reset_index(name="Titles")
    )

    fig = px.line(
        timeline_df,
        x="year_added",
        y="Titles",
        markers=True
    )

    fig.update_traces(
        line_color="#E50914",
        line_width=4,
        marker=dict(
            size=8,
            color="white",
            line=dict(color="#E50914", width=2)
        )
    )

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#0F1116",
        plot_bgcolor="#0F1116",

        font=dict(
            color="white",
            size=14
        ),

        title="📈 Netflix Content Added by Year",

        title_x=0.25,

        xaxis_title="Year",

        yaxis_title="Titles",

        height=450,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    return fig