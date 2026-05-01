# Heart Disease MCP Server

A Model Context Protocol (MCP) server that provides heart disease prediction capabilities through a REST API interface. Built with TypeScript, Node.js, and machine learning models trained on heart disease datasets.

## Features

- **Heart Disease Prediction**: ML-powered tool to predict heart disease risk based on patient health metrics
- **MCP Protocol**: Implements the Model Context Protocol for seamless AI assistant integration
- **HTTP SSE Transport**: Server-sent events for real-time communication
- **Docker Support**: Pre-configured Docker setup for easy deployment
- **Python ML Pipeline**: Robust machine learning pipeline for data preprocessing and model inference

## Tech Stack

- **Backend**: Node.js 20, TypeScript
- **ML Framework**: Python 3 with scikit-learn, pandas, joblib
- **Server**: MCP Server with HTTP SSE transport
- **Containerization**: Docker Compose
- **Development**: ESLint, ts-node

## Project Structure

```
.
├── src/                           # TypeScript source code
│   ├── http-server.ts             # Main MCP server with HTTP SSE transport
│   ├── tools/                     # MCP tool implementations
│   │   ├── index.ts              # Tool registry
│   │   ├── predict.ts            # Heart disease prediction tool
│   │   └── hello.ts              # Example hello tool
│   └── types/                    # TypeScript type definitions
│
├── ai_models/heart_model/        # ML model and training pipeline
│   ├── predict_pipeline.py       # Prediction pipeline
│   ├── train_model.py            # Model training script
│   ├── split_data.py             # Data splitting utilities
│   ├── check_data.py             # Data validation
│   ├── test_prediction.py        # Prediction testing
│   ├── requirements.txt          # Python dependencies
│   ├── data/                     # Datasets
│   │   ├── heart.csv             # Full dataset
│   │   ├── train_heart.csv       # Training set
│   │   └── test_heart.csv        # Test set
│   ├── saved_models/             # Serialized models and feature columns
│   └── results/                  # Training results and summaries
│
├── docker-compose.yml            # Docker Compose configuration
├── Dockerfile                    # Multi-stage Docker build
├── package.json                  # Node.js dependencies
├── tsconfig.json                 # TypeScript configuration
└── eslint.config.mjs            # ESLint configuration
```

## Getting Started

### Prerequisites

- Node.js 20+
- Python 3.11+
- Docker & Docker Compose (for containerized deployment)
- npm or yarn

### Installation

1. **Clone and install dependencies:**

   ```bash
   npm install
   ```

2. **Set up Python environment (for local development):**

   ```bash
   cd ai_models/heart_model
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Build the TypeScript code:**
   ```bash
   npm run build
   ```

### Running Locally

**Development mode:**

```bash
npm run dev
```

The server will start on `http://localhost:3000`

**Production mode:**

```bash
npm run build
npm start
```

### Running with Docker

**Build and start containers:**

```bash
npm run docker:up:prod
```

**View logs:**

```bash
npm run docker:logs:prod
```

**Stop containers:**

```bash
npm run docker:down:prod
```

## Available Tools

### Predict

Predicts heart disease risk based on patient health metrics.

**Parameters:**

- `Age`: Patient age (numeric)
- `Sex`: Gender (0 or 1)
- `RestingBP`: Resting blood pressure (numeric)
- `Cholesterol`: Cholesterol level (numeric)
- `FastingBS`: Fasting blood sugar (0 or 1)
- `MaxHR`: Maximum heart rate achieved (numeric)
- `ExerciseAngina`: Exercise induced angina (0 or 1)
- `Oldpeak`: ST depression (numeric)
- `ChestPainType`: Type of chest pain (numeric)
- `RestingECG`: Resting electrocardiogram result (numeric)
- `ST_Slope`: Slope of ST segment (numeric)

**Returns:** Prediction result with confidence score

### Hello

## Development

### Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build TypeScript to JavaScript
npm start            # Start production server
npm run lint         # Run ESLint
npm run lint:fix     # Fix linting issues
npm run types        # Type-check without building
npm test             # Run tests (not yet configured)
```

### Key Notes

- The prediction tool auto-detects Python with required ML dependencies
- If needed, it bootstraps a virtual environment from `requirements.txt`
- The Docker setup includes all Python dependencies for seamless ML inference

## ML Model Details

The prediction model is built using a machine learning pipeline that:

- Preprocesses input features including one-hot encoding for categorical variables
- Applies feature scaling and normalization
- Uses a trained scikit-learn classifier for predictions
- Maintains consistent feature ordering via saved column mappings

### Training the Model

To retrain the model with new data:

```bash
cd ai_models/heart_model
python3 train_model.py
```

### Testing Predictions

```bash
cd ai_models/heart_model
python3 test_prediction.py
```

## Environment Variables

Create a `.env` file in the root directory:

```env
PORT=3000
```

## API Endpoints

The server exposes the following HTTP endpoints:

- `GET /sse/:sessionId` - Open SSE connection for a session
- `POST /call-tool/:sessionId` - Call a tool within a session

## Troubleshooting

**Python dependencies not found:**

- Ensure Python 3.11+ is installed
- Check that `ai_models/heart_model/requirements.txt` is up to date
- The tool will automatically create a virtual environment if needed

**Port already in use:**

- Change the PORT in `.env` or environment variables
- Default is 3000

**Docker build fails:**
sionId` - Call a tool within a session

## Troubleshooting

**Python dependencies not found:**

- Ensure Python 3.11+ is installed
- Check that `ai_models/heart_model/requirements.txt` is up to date
- The tool will automatically create a virtual environment if needed

**Port already in use:**

- Change the PORT in `.env` or environment variables
- Default is 3000

**Docker build fails:**

- Ensure Docker and Docker Compose are installed
- Check that Docker daemon is running
- Review logs with `npm run docker:logs:prod`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes and run linting: `npm run lint:fix`
4. Type-check your code: `npm run types`
5. Submit a pull request

## License

ISC

## Support

For issues, questions, or contributions, please open an issue in the repository.
