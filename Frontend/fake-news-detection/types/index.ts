export interface AnalysisResult {
    result: string;
    confidence: number;
  }
  
  export interface NewsFormProps {
    onSubmit: (formData: FormData) => void;
    loading: boolean;
  }  