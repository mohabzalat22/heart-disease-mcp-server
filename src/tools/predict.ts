import { exec } from "child_process";
import path from "path";
import { Tool } from "./index";
import { PredictHeartDiseaseArgs } from "../types/predict";

export const predictHeartDiseaseTool: Tool<PredictHeartDiseaseArgs> = {
  definition: {
    name: "predict_heart_disease",
    description: "Predict the risk of heart disease based on patient clinical data.",
    inputSchema: {
      type: "object",
      properties: {
        age: { type: "number", description: "Age of the patient" },
        sex: { type: "number", description: "Sex (1: Male, 0: Female)" },
        resting_bp: { type: "number", description: "Resting blood pressure (mm Hg)" },
        cholesterol: { type: "number", description: "Serum cholesterol (mm/dl)" },
        fasting_bs: { type: "number", description: "Fasting blood sugar > 120 mg/dl (1: True, 0: False)" },
        max_hr: { type: "number", description: "Maximum heart rate achieved" },
        exercise_angina: { type: "number", description: "Exercise induced angina (1: Yes, 0: No)" },
        oldpeak: { type: "number", description: "ST depression induced by exercise relative to rest" },
        chest_pain_type: { 
          type: "string", 
          enum: ["ASY", "NAP", "ATA", "TA"],
          description: "Chest pain type (ASY: Asymptomatic, NAP: Non-Anginal Pain, ATA: Atypical Angina, TA: Typical Angina)"
        },
        resting_ecg: { 
          type: "string", 
          enum: ["Normal", "ST", "LVH"],
          description: "Resting electrocardiogram results"
        },
        st_slope: { 
          type: "string", 
          enum: ["Flat", "Up", "Down"],
          description: "Slope of the peak exercise ST segment"
        },
      },
      required: [
        "age", "sex", "resting_bp", "cholesterol", "fasting_bs", 
        "max_hr", "exercise_angina", "oldpeak", "chest_pain_type", 
        "resting_ecg", "st_slope"
      ],
    },
  },
  handler: async (args: PredictHeartDiseaseArgs) => {
    const modelDir = path.join(process.cwd(), "ai_models", "heart_model_new");
    const scriptPath = path.join(modelDir, "predict_pipeline.py");
    const pythonPath = path.join(modelDir, "venv", "bin", "python3");
    
    const command = `"${pythonPath}" "${scriptPath}" ` +
      `--age ${args.age} ` +
      `--sex ${args.sex} ` +
      `--resting_bp ${args.resting_bp} ` +
      `--cholesterol ${args.cholesterol} ` +
      `--fasting_bs ${args.fasting_bs} ` +
      `--max_hr ${args.max_hr} ` +
      `--exercise_angina ${args.exercise_angina} ` +
      `--oldpeak ${args.oldpeak} ` +
      `--chest_pain_type "${args.chest_pain_type}" ` +
      `--resting_ecg "${args.resting_ecg}" ` +
      `--st_slope "${args.st_slope}"`;

    return new Promise((resolve) => {
      exec(command, { cwd: modelDir }, (error, stdout, stderr) => {
        if (error) {
          return resolve({
            content: [
              {
                type: "text",
                text: `Error executing prediction: ${stderr || error.message}`,
              },
            ],
            isError: true,
          });
        }

        try {
          const result = JSON.parse(stdout.trim());
          return resolve({
            content: [
              {
                type: "text",
                text: `Prediction Result:\n${result.result_text}\nProbability: ${(result.probability_of_disease * 100).toFixed(2)}%`,
              },
              {
                type: "text",
                text: JSON.stringify(result, null, 2),
              }
            ],
          });
        } catch {
          return resolve({
            content: [
              {
                type: "text",
                text: `Error parsing model output: ${stdout}`,
              },
            ],
            isError: true,
          });
        }
      });
    });
  },
};
