import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface PopulationStatistics {
  administrative_code: string;
  reference_date: string;
  province: string;
  city: string;
  district: string;
  total_population: number;
  total_male: number;
  total_female: number;
  age_groups: {
    age_0_9: number;
    age_10_19: number;
    age_20_29: number;
    age_30_39: number;
    age_40_49: number;
    age_50_59: number;
    age_60_69: number;
    age_70_79: number;
    age_80_89: number;
    age_90_99: number;
  };
  gender_breakdown: {
    age_0_9_male: number;
    age_0_9_female: number;
    age_20_29_male: number;
    age_20_29_female: number;
    age_30_39_male: number;
    age_30_39_female: number;
    age_40_49_male: number;
    age_40_49_female: number;
  };
}

export interface AgeDistribution {
  city: string;
  district: string;
  total_population: number;
  age_distribution: {
    '0-9세': number;
    '10-19세': number;
    '20-29세': number;
    '30-39세': number;
    '40-49세': number;
    '50-59세': number;
    '60-69세': number;
    '70-79세': number;
  };
}

export interface IncomeDistribution {
  year: number;
  region: string;
  total_households: number;
  income_brackets: {
    '50만원미만': number;
    '50-100만원': number;
    '100-200만원': number;
    '200-300만원': number;
    '300-400만원': number;
    '400-500만원': number;
    '500-600만원': number;
    '600-700만원': number;
    '700-800만원': number;
    '800만원이상': number;
  };
}

export interface PopulationSummary {
  summary: {
    total_records: number;
    total_population: number;
    avg_population_per_district: number;
    total_cities: number;
    total_districts: number;
  };
  top_regions: Array<{
    city: string;
    district: string;
    population: number;
  }>;
}

export interface PopulationApiResponse<T> {
  data: T[];
  total_count: number;
  filters?: {
    city?: string;
    district?: string;
    year?: number;
  };
}

class PopulationService {
  private api = axios.create({
    baseURL: `${API_BASE_URL}/api`,
    timeout: 10000,
  });

  /**
   * 인구 통계 데이터를 조회합니다
   */
  async getPopulationStatistics(params?: {
    city?: string;
    district?: string;
    year?: number;
    limit?: number;
  }): Promise<PopulationApiResponse<PopulationStatistics>> {
    try {
      const response = await this.api.get('/population/statistics', {
        params,
      });
      return response.data;
    } catch (error) {
      console.error('인구 통계 데이터 조회 실패:', error);
      throw error;
    }
  }

  /**
   * 연령대별 인구 분포를 조회합니다
   */
  async getAgeDistribution(params?: {
    city?: string;
    top_districts?: number;
  }): Promise<PopulationApiResponse<AgeDistribution>> {
    try {
      const response = await this.api.get('/population/age-distribution', {
        params,
      });
      return response.data;
    } catch (error) {
      console.error('연령대별 인구 분포 조회 실패:', error);
      throw error;
    }
  }

  /**
   * 소득 분포 데이터를 조회합니다
   */
  async getIncomeDistribution(params?: {
    year?: number;
    region?: string;
  }): Promise<PopulationApiResponse<IncomeDistribution>> {
    try {
      const response = await this.api.get('/population/income-distribution', {
        params,
      });
      return response.data;
    } catch (error) {
      console.error('소득 분포 데이터 조회 실패:', error);
      throw error;
    }
  }

  /**
   * 인구 통계 요약 정보를 조회합니다
   */
  async getPopulationSummary(): Promise<PopulationSummary> {
    try {
      const response = await this.api.get('/population/summary');
      return response.data;
    } catch (error) {
      console.error('인구 통계 요약 조회 실패:', error);
      throw error;
    }
  }

  /**
   * 특정 지역의 인구 트렌드를 분석합니다
   */
  async analyzePopulationTrend(city: string, district?: string) {
    try {
      const data = await this.getPopulationStatistics({ city, district });
      
      if (data.data.length === 0) {
        return {
          status: 'no_data',
          message: '해당 지역의 데이터가 없습니다.',
        };
      }

      const regionData = data.data[0];
      
      // 연령대별 비율 계산
      const ageGroups = regionData.age_groups;
      const total = regionData.total_population;
      
      const ageRatios = Object.entries(ageGroups).map(([age, count]) => ({
        age_group: age.replace('age_', '').replace('_', '-') + '세',
        count,
        percentage: ((count / total) * 100).toFixed(1),
      }));

      // 성별 비율
      const genderRatio = {
        male_percentage: ((regionData.total_male / total) * 100).toFixed(1),
        female_percentage: ((regionData.total_female / total) * 100).toFixed(1),
      };

      // 주요 연령층 분석
      const workingAge = ageGroups.age_20_29 + ageGroups.age_30_39 + ageGroups.age_40_49 + ageGroups.age_50_59;
      const elderyAge = ageGroups.age_60_69 + ageGroups.age_70_79 + ageGroups.age_80_89 + ageGroups.age_90_99;
      const youthAge = ageGroups.age_0_9 + ageGroups.age_10_19;

      const demographics = {
        working_age_ratio: ((workingAge / total) * 100).toFixed(1),
        elderly_ratio: ((elderyAge / total) * 100).toFixed(1),
        youth_ratio: ((youthAge / total) * 100).toFixed(1),
      };

      return {
        status: 'success',
        region_info: {
          city: regionData.city,
          district: regionData.district,
          total_population: total,
        },
        age_distribution: ageRatios,
        gender_ratio: genderRatio,
        demographics,
        insights: this.generateInsights(demographics, genderRatio),
      };
    } catch (error) {
      console.error('인구 트렌드 분석 실패:', error);
      throw error;
    }
  }

  private generateInsights(demographics: any, genderRatio: any): string[] {
    const insights: string[] = [];
    
    const workingAgeRatio = parseFloat(demographics.working_age_ratio);
    const elderlyRatio = parseFloat(demographics.elderly_ratio);
    const youthRatio = parseFloat(demographics.youth_ratio);
    
    if (workingAgeRatio > 60) {
      insights.push('경제활동 인구 비율이 높아 상업시설 및 서비스업에 유리한 지역입니다.');
    }
    
    if (elderlyRatio > 20) {
      insights.push('고령 인구 비율이 높아 의료·복지 서비스 수요가 클 것으로 예상됩니다.');
    }
    
    if (youthRatio > 20) {
      insights.push('젊은 인구 비율이 높아 교육·문화 서비스에 대한 수요가 높습니다.');
    }
    
    const maleRatio = parseFloat(genderRatio.male_percentage);
    if (Math.abs(maleRatio - 50) > 5) {
      insights.push(
        maleRatio > 50
          ? '남성 인구 비율이 높아 남성 타겟 비즈니스에 유리합니다.'
          : '여성 인구 비율이 높아 여성 타겟 비즈니스에 유리합니다.'
      );
    }
    
    return insights;
  }
}

export const populationService = new PopulationService();
