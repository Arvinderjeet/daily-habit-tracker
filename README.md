# Daily Habit Tracker

A comprehensive web application built with Streamlit for tracking daily habits and monitoring progress over time.

## Features

### 🎯 Daily Habit Management
- Add multiple habits through an intuitive sidebar interface
- Daily check-in with status updates (Done/Skipped/Not Checked)
- Real-time completion rate tracking
- Date selection for retroactive updates

### 📊 Monthly Preview
- Calendar view showing habit completion by date
- Summary statistics with completion rates
- Interactive month selection
- Exportable data tables

### 📈 Analytics Dashboard
- Multiple time frame options (Week/Month/Year)
- Various chart types (Bar Chart, Line Chart, Heatmap)
- Overall statistics with key metrics
- Visual progress tracking

### 🎨 Design Features
- Professional, modern interface with custom styling
- Responsive design for desktop and mobile
- Intuitive navigation and user experience
- Color-coded status indicators

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Add Habits**: Use the sidebar to add new habits you want to track
2. **Daily Check-in**: Select a date and update the status of your habits
3. **View Progress**: Check the monthly preview and analytics dashboard
4. **Track Trends**: Use different chart types to visualize your progress

## Data Storage

The application uses CSV-based data storage for simplicity and portability. All habit data is stored in `habits.csv` in the same directory as the application.

## Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive charts and visualizations
- **Python**: Core programming language

## License

This project is open source and available under the MIT License.

