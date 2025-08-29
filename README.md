# Flood Prediction Demo Project

A comprehensive machine learning-based flood prediction system that forecasts precipitation patterns and maximum surface runoff across multiple communities in Nigeria. This project provides real-time flood risk assessment and early warning capabilities for disaster preparedness and management.

## 🌟 Features

- **Multi-location Predictions**: Covers 9 communities across Nigeria
- **Dual Model System**: 
  - Total Precipitation forecasting
  - Maximum Surface Runoff (MSR) prediction
- **REST API**: Flask-based backend with versioned endpoints
- **Multiple Time Horizons**: Predictions for today, tomorrow, week, month, and year
- **Flood Risk Assessment**: Automated flood status classification based on precipitation and runoff thresholds
- **Pre-computed Predictions**: Optimized performance with cached prediction data

## 🏘️ Supported Communities

- Amaechi Idodo
- Fangan
- Sokori
- Ibiade
- Okpanku
- Ogwuagor
- Isheri
- Lafiagi
- Pategi

## 🛠️ Technology Stack

- **Backend**: Flask with CORS support
- **Machine Learning**: 
  - LightGBM for gradient boosting
  - Scikit-learn for model training and evaluation
  - Joblib for model serialization
- **Data Processing**: Pandas, NumPy
- **Time Series**: NeuralProphet for forecasting
- **Visualization**: Matplotlib
- **API**: RESTful endpoints with JSON responses

## 📁 Project Structure

```
flood-prediction-demo-project/
├── backend/                    # Flask API backend
│   ├── app.py                 # Main Flask application
│   ├── predict.py             # Prediction logic and utilities
│   ├── maximum_surface_runoff.py  # MSR prediction models
│   ├── precipitation_pred.py   # Precipitation prediction models
│   ├── dummy.py               # Dummy data generation
│   └── predictions/           # Cached prediction files
│       ├── msr_prediction/    # Maximum surface runoff predictions
│       └── total_precipitation/  # Precipitation predictions
├── datasets/                   # Training datasets for each community
├── models/                     # Trained ML models (Gradient Boosting)
├── maximum_surface_runoff/     # MSR-specific models
│   └── models/                # Stacked surface runoff models
├── total_precipitation/        # Precipitation-specific models
│   └── models/                # Stacked precipitation models
├── implementation_script.py    # Model training and forecasting script
├── lagos_model.py             # Lagos-specific model implementation
└── new.json                   # Sample prediction data structure
```

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/chisomdaniel/flood-prediction-demo-project.git
   cd flood-prediction-demo-project
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirement.txt
   ```

## 🏃‍♂️ Running the Application

### Start the Flask API Server

```bash
cd backend
python app.py
```

The API will be available at `http://localhost:5000`

### API Endpoints

#### Get Forecast (Current Version - v2)
```
GET /api/v2/forecast/<community>/<period>
```

**Parameters**:
- `community`: One of the supported communities (case-insensitive)
- `period`: Time horizon (`today`, `tomorrow`, `week`, `month`, `year`)

**Example**:
```bash
curl http://localhost:5000/api/v2/forecast/sokori/week
```

**Response**:
```json
{
  "community": "sokori",
  "total_precipitation": {...},
  "averg_total_precipitation": 45.2,
  "tp_highest_risk_day": "2025-09-02",
  "maximum_surface_runoff": {...},
  "averg_maximum_surface_runoff": 18.7,
  "msr_highest_risk_day": "2025-09-03",
  "daily_flood_status": {...}
}
```

#### Get Available Values
```
GET /api/v2/forecast/values
```

Returns the list of supported communities and time periods.

### Running Predictions Manually

For custom forecasting and model training:

```bash
python implementation_script.py
```

This script allows you to:
- Select forecast duration (1 day to 1 year or custom)
- Generate predictions for Lagos and Ilorin
- Save results as CSV files
- Visualize forecasts with matplotlib

## 📊 Model Information

### Gradient Boosting Models
- Located in `models/` directory
- Individual models for each community
- Format: `{Community} Model (GB).joblib`

### Stacked Models
- **Precipitation Models**: `total_precipitation/models/`
- **Surface Runoff Models**: `maximum_surface_runoff/models/`
- Enhanced accuracy through ensemble methods

### Training Data
- Historical weather and hydrological data for each community
- Stored in `datasets/` as CSV files
- Format: `{Community}_Final.csv`

## 🔧 Model Training

To retrain models with new data:

1. Update the corresponding CSV file in `datasets/`
2. Run the model training scripts:
   ```bash
   python backend/precipitation_pred.py
   python backend/maximum_surface_runoff.py
   ```

## 📈 Prediction Output

The system provides:

- **Total Precipitation**: Expected rainfall amounts
- **Maximum Surface Runoff**: Water flow and drainage capacity
- **Flood Risk Status**: Automated classification based on thresholds
- **Risk Assessment**: Daily flood probability and severity
- **Highest Risk Days**: Peak danger periods identification

## 🚨 Flood Risk Classification

The system automatically classifies flood risk based on:
- Precipitation intensity and duration
- Surface runoff capacity
- Historical flood patterns
- Community-specific thresholds

Risk levels: `Low`, `Moderate`, `High`, `Critical`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For questions, issues, or contributions, please:
- Open an issue on GitHub
- Contact the development team
- Check the API documentation at `/api/v2/forecast/values`

## 🔮 Future Enhancements

- Real-time weather data integration
- Mobile application development
- Enhanced visualization dashboard
- SMS/Email alert system
- Integration with emergency response systems
- Machine learning model improvements
- Additional community coverage

---

**Built with ❤️ for disaster preparedness and community safety in Nigeria**