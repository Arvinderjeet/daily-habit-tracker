
import streamlit as st
import pandas as pd
from data_manager import load_data, save_data, add_habit, update_habit_status, get_habits
import plotly.express as px
from datetime import datetime, timedelta

# Page configuration for responsive design
st.set_page_config(
    page_title="Daily Habit Tracker",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    load_css()
except FileNotFoundError:
    pass  # CSS file not found, continue without custom styling

def app():
    # Main title with emoji and styling
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h1 style='color: #2E8B57; font-size: 3rem; margin-bottom: 0.5rem;'>
            🎯 Daily Habit Tracker
        </h1>
        <p style='color: #666; font-size: 1.2rem; margin-top: 0;'>
            Build better habits, track your progress, achieve your goals
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar for habit management with enhanced styling
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 1rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 10px; margin-bottom: 1rem; color: white;'>
        <h2 style='margin: 0; color: white;'>🛠️ Manage Habits</h2>
    </div>
    """, unsafe_allow_html=True)
    new_habit_name = st.sidebar.text_input("Add New Habit")
    if st.sidebar.button("Add Habit"):
        if new_habit_name:
            if add_habit(new_habit_name):
                st.sidebar.success(f"Habit '{new_habit_name}' added!")
            else:
                st.sidebar.warning(f"Habit '{new_habit_name}' already exists.")
        else:
            st.sidebar.error("Please enter a habit name.")

    # Daily Check-in
    st.header("📅 Daily Check-in")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        selected_date = st.date_input("Select Date", datetime.today())
    with col2:
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    habits = get_habits()
    df = load_data()

    if habits:
        st.subheader(f"Habits for {selected_date.strftime('%A, %B %d, %Y')}")
        
        # Create a container for better layout
        with st.container():
            for i, habit in enumerate(habits):
                current_status = df[(df["habit"] == habit) & (df["date"] == pd.to_datetime(selected_date))]["status"].iloc[0] if not df[(df["habit"] == habit) & (df["date"] == pd.to_datetime(selected_date))].empty else "Not Checked"
                
                # Create an expander for each habit
                with st.expander(f"🎯 {habit}", expanded=True):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.write(f"**Current Status:** {current_status}")
                        
                    with col2:
                        status_options = ["Done", "Skipped", "Not Checked"]
                        selected_status = st.selectbox(
                            "Update Status", 
                            status_options, 
                            index=status_options.index(current_status), 
                            key=f"status_{habit}_{selected_date}"
                        )
                        
                    with col3:
                        if st.button("✅ Update", key=f"update_btn_{habit}_{selected_date}"):
                            update_habit_status(habit, pd.to_datetime(selected_date), selected_status)
                            st.success(f"Updated!")
                            st.rerun()
                            
        # Quick stats for today
        today_df = df[df["date"] == pd.to_datetime(selected_date)]
        if not today_df.empty:
            done_count = len(today_df[today_df["status"] == "Done"])
            total_count = len(habits)
            completion_rate = (done_count / total_count) * 100 if total_count > 0 else 0
            
            st.metric(
                label="Today's Completion Rate", 
                value=f"{completion_rate:.1f}%", 
                delta=f"{done_count}/{total_count} habits completed"
            )
    else:
        st.info("🚀 No habits added yet. Add some habits from the sidebar to get started!")

    # Monthly Habit Preview
    st.header("📊 Monthly Habit Preview")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        selected_month = st.date_input("Select Month for Preview", datetime.today())
    with col2:
        view_type = st.selectbox("View Type", ["Calendar View", "Summary Stats"])
    
    if not df.empty:
        # Filter data for selected month
        df_month = df[df["date"].dt.month == selected_month.month]
        df_month = df_month[df_month["date"].dt.year == selected_month.year]

        if not df_month.empty:
            if view_type == "Calendar View":
                # Pivot table for monthly view
                monthly_pivot = df_month.pivot_table(index="habit", columns="date", values="status", aggfunc=lambda x: x.iloc[0])
                st.subheader(f"Calendar View - {selected_month.strftime('%B %Y')}")
                st.dataframe(monthly_pivot, use_container_width=True)
                
            else:  # Summary Stats
                st.subheader(f"Monthly Summary - {selected_month.strftime('%B %Y')}")
                
                # Calculate monthly stats
                monthly_stats = []
                for habit in habits:
                    habit_data = df_month[df_month["habit"] == habit]
                    total_days = len(habit_data)
                    done_days = len(habit_data[habit_data["status"] == "Done"])
                    skipped_days = len(habit_data[habit_data["status"] == "Skipped"])
                    completion_rate = (done_days / total_days * 100) if total_days > 0 else 0
                    
                    monthly_stats.append({
                        "Habit": habit,
                        "Total Days": total_days,
                        "Completed": done_days,
                        "Skipped": skipped_days,
                        "Completion Rate": f"{completion_rate:.1f}%"
                    })
                
                if monthly_stats:
                    stats_df = pd.DataFrame(monthly_stats)
                    st.dataframe(stats_df, use_container_width=True)
                    
                    # Monthly completion chart
                    fig_monthly = px.bar(
                        stats_df, 
                        x="Habit", 
                        y="Completed", 
                        title=f"Habit Completion for {selected_month.strftime('%B %Y')}",
                        color="Completed",
                        color_continuous_scale="Greens"
                    )
                    st.plotly_chart(fig_monthly, use_container_width=True)
        else:
            st.info("No habit data for this month.")
    else:
        st.info("No habit data available for preview.")

    # Habit Analytics
    st.header("📈 Habit Analytics")
    
    if not df.empty:
        # Time frame selection
        col1, col2 = st.columns([1, 1])
        with col1:
            time_frame = st.selectbox("Select Time Frame", ["Week", "Month", "Year"])
        with col2:
            chart_type = st.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Heatmap"])

        # Calculate date range
        if time_frame == "Week":
            end_date = datetime.today()
            start_date = end_date - timedelta(days=7)
        elif time_frame == "Month":
            end_date = datetime.today()
            start_date = end_date - timedelta(days=30)
        else:  # Year
            end_date = datetime.today()
            start_date = end_date - timedelta(days=365)
        
        # Filter data for the selected time frame
        filtered_df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
        
        if not filtered_df.empty:
            # Prepare data for visualization
            completed_df = filtered_df[filtered_df["status"] == "Done"]
            
            if not completed_df.empty:
                if chart_type == "Bar Chart":
                    # Daily completion counts
                    daily_counts = completed_df.groupby(["date", "habit"]).size().reset_index(name="count")
                    fig = px.bar(
                        daily_counts, 
                        x="date", 
                        y="count", 
                        color="habit",
                        title=f"Habit Completion Over Last {time_frame}",
                        labels={"count": "Habits Completed", "date": "Date"}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                elif chart_type == "Line Chart":
                    # Cumulative completion over time
                    daily_totals = completed_df.groupby("date").size().reset_index(name="total_completed")
                    daily_totals["cumulative"] = daily_totals["total_completed"].cumsum()
                    
                    fig = px.line(
                        daily_totals, 
                        x="date", 
                        y="cumulative",
                        title=f"Cumulative Habit Completion Over Last {time_frame}",
                        labels={"cumulative": "Total Habits Completed", "date": "Date"}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                else:  # Heatmap
                    # Create a heatmap of habit completion
                    heatmap_data = filtered_df.pivot_table(
                        index="habit", 
                        columns="date", 
                        values="status", 
                        aggfunc=lambda x: 1 if x.iloc[0] == "Done" else 0
                    ).fillna(0)
                    
                    fig = px.imshow(
                        heatmap_data,
                        title=f"Habit Completion Heatmap - Last {time_frame}",
                        color_continuous_scale="Greens",
                        aspect="auto"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Overall statistics
                st.subheader("📋 Overall Statistics")
                col1, col2, col3, col4 = st.columns(4)
                
                total_completions = len(completed_df)
                total_possible = len(filtered_df)
                overall_rate = (total_completions / total_possible * 100) if total_possible > 0 else 0
                best_habit = completed_df["habit"].value_counts().index[0] if not completed_df.empty else "None"
                
                with col1:
                    st.metric("Total Completions", total_completions)
                with col2:
                    st.metric("Overall Rate", f"{overall_rate:.1f}%")
                with col3:
                    st.metric("Best Habit", best_habit)
                with col4:
                    st.metric("Active Days", len(filtered_df["date"].unique()))
                    
            else:
                st.info(f"No completed habits in the last {time_frame}.")
        else:
            st.info(f"No habit data available for the last {time_frame}.")
    else:
        st.info("No habit data available for analytics.")

if __name__ == "__main__":
    app()


