from preswald import text, plotly, connect, get_df, table, query, separator, selectbox, topbar, sidebar
import pandas as pd
import plotly.express as px

text("# Global AI Impact Analysis ")
text("### *This application provides interactive visualizations and analysis of AI's impact across the world!*")
text("*Select an option from below to explore how AI is impacting the world...*")

topbar()


def connect_to_dataset():
    try:
        connect()
        df = get_df('ai_impact_csv')
        return df
    except ValueError as e:
        print(f"Error in the configuration: {e}")
    except Exception as e:
        print(f"Error retrieving data: {e}")

    text("This is how the first 5 rows of the dataset look like...")
    table(df.head())
    separator()
    text(f"There are {df.shape[0]} rows and {df.shape[1]} columns in the dataset.")
    separator()


def plot_max_global_ai_usage(df):
    try:
        text(f"Maximum AI Usage Of Each Country")
        max_usage_df = df.loc[df.groupby("Country")["AI Adoption Rate (%)"].idxmax()].reset_index(drop=True)
        max_usage_df = max_usage_df[["Country","AI Adoption Rate (%)","Industry"]]
        max_chart = px.bar(
            max_usage_df,
            x="Country",
            y="AI Adoption Rate (%)",
            color="Industry",
            title="Maximum AI Adoption Rate by Country"
        )    
        max_chart.update_layout(
        xaxis_title="Country",
        yaxis_title="AI Adoption Rate (%)",
        legend_title="Industry",
        )
        # fig.show()
        plotly(max_chart)
        separator()
    except ValueError as e:
        print(f"Error in the configuration: {e}")
    except Exception as e:
        print(f"Error retrieving data: {e}")


def plot_min_global_ai_usage(df):
    try:
        text(f"Minimum AI Usage In Each Country")
        min_usage_df = df.loc[df.groupby("Country")["AI Adoption Rate (%)"].idxmin()].reset_index(drop=True)
        min_usage_df = min_usage_df[["Country","AI Adoption Rate (%)","Industry"]]
        min_chart = px.bar(
            min_usage_df,
            x="Country",
            y="AI Adoption Rate (%)",
            color="Industry",
            title="Minimum AI Adoption Rate by Country"
        )    
        min_chart.update_layout(
        xaxis_title="Country",
        yaxis_title="AI Adoption Rate (%)",
        legend_title="Industry",
        )
        plotly(min_chart)
        separator()
    except ValueError as e:
        print(f"Error in the configuration: {e}")
    except Exception as e:
        print(f"Error retrieving data: {e}")


def view_global_job_loss(df):
    try:
        text(f"Global job loss due to AI")
        job_loss_query = """
            SELECT 
                country,
                ROUND(AVG("Job Loss Due to AI (%)"),2) as "Average Job Loss Due to AI"
            FROM ai_impact_csv
            GROUP BY country
        """
        job_loss_df = query(job_loss_query,'ai_impact_csv')
        table(job_loss_df)

    except ValueError as e:
        print("Error in the configuration")
    except Exception as e:
        print(f"Error retrieving data: {e}")

def view_user_choice_plot(df):
    try:
        choice = selectbox(
            label="Choose a plot",
            options = [
                "Maximum AI Adoption Rate In Different Countries",
                "Minimum AI Adoption Rate In Different Countries",
                "Global Job Loss Due to AI"
            ]
        )

        print(f"Here is the analysis for {choice}:")
        if choice == "Minimum AI Adoption Rate In Different Countries":
            plot_min_global_ai_usage(df)
        elif choice == "Maximum AI Adoption Rate In Different Countries":
            plot_max_global_ai_usage(df)
        elif choice == "Global Job Loss Due to AI":
            view_global_job_loss(df)
    except Exception as e:
        print(f"Error in selection: {e}")


df = connect_to_dataset()
choice = view_user_choice_plot(df)




