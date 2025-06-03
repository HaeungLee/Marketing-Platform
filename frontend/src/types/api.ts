// API 응답 타입 정의
export interface Business {
  id: string
  name: string
  category: string
  description: string
  latitude: number
  longitude: number
  address?: string
  phone?: string
  website?: string
  target_radius_km: number
  created_at: string
}

export interface ContentGenerationRequest {
  business_id: string
  business_name: string
  business_category: string
  business_description: string
  product_name: string
  product_description: string
  content_type: 'blog' | 'instagram' | 'youtube' | 'flyer'
  target_audience?: Record<string, any>
  tone?: string
  keywords?: string[]
}

export interface ContentGenerationResponse {
  content_id: string
  content_type: string
  title?: string
  content: string
  hashtags: string[]
  keywords: string[]
  estimated_engagement?: Record<string, number>
  performance_metrics: Record<string, any>
  created_at: string
}

export interface ImageGenerationRequest {
  prompt: string
  business_name?: string
  business_category?: string
  style?: string
}

export interface ImageGenerationResponse {
  success: boolean
  image_url?: string
  filename?: string
  prompt: string
  error?: string
  created_at: string
}

export interface TargetAudienceResponse {
  business_id: string
  analysis_date: string
  total_population: number
  demographics: Array<{
    age_group: string
    gender: string
    percentage: number
    income_level: string
    lifestyle: string[]
  }>
  peak_hours: Array<{
    hour: number
    traffic: number
    description: string
  }>
  seasonal_trends: Record<string, number>
  recommendations: string[]
}

export interface DashboardData {
  business_id: string
  last_updated: string
  key_metrics: Record<string, any>
  recent_insights: Array<{
    title: string
    description: string
    impact: string
    confidence: number
    source: string
  }>
  recommended_actions: string[]
  performance_score: number
}

export interface ApiError {
  detail: string
  type?: string
}
