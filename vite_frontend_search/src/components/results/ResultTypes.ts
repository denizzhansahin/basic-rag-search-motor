export interface ClassicResult {
  title: string;
  url: string;
  content: string;
  score?: number;
}

export interface AiSuggestion {
  title: string;
  url: string;
}

export interface AiData {
  summary: string;
  //top_results?: ClassicResult[];
  suggestions?: AiSuggestion[];
}


