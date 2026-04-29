export interface PredictHeartDiseaseArgs {
  age: number;
  sex: number; // 0 for Female, 1 for Male
  resting_bp: number;
  cholesterol: number;
  fasting_bs: number; // 0 or 1
  max_hr: number;
  exercise_angina: number; // 0 or 1
  oldpeak: number;
  chest_pain_type: "ASY" | "NAP" | "ATA" | "TA";
  resting_ecg: "Normal" | "ST" | "LVH";
  st_slope: "Flat" | "Up" | "Down";
}

export interface PredictHeartDiseaseResponse {
  prediction: number;
  probability_of_disease: number | null;
  result_text: string;
}
