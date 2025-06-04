import fs from 'fs';
import csv from 'csv-parser';
import { Pool } from 'pg';
import path from 'path';

interface PopulationRow {
  administrative_code: string;
  reference_date: string;
  province: string;
  city: string;
  district: string;
  age_0_9_male: number;
  age_0_9_female: number;
  age_10_19_male: number;
  age_10_19_female: number;
  age_20_29_male: number;
  age_20_29_female: number;
  age_30_39_male: number;
  age_30_39_female: number;
  age_40_49_male: number;
  age_40_49_female: number;
  age_50_59_male: number;
  age_50_59_female: number;
  age_60_69_male: number;
  age_60_69_female: number;
  age_70_79_male: number;
  age_70_79_female: number;
  age_80_89_male: number;
  age_80_89_female: number;
  age_90_99_male: number;
  age_90_99_female: number;
  age_100_plus_male: number;
  age_100_plus_female: number;
  total_population: number;
  total_male: number;
  total_female: number;
}

class DataImporter {
  private pool: Pool;

  constructor() {
    this.pool = new Pool({
      user: process.env.DB_USER || 'marketing_user',
      host: process.env.DB_HOST || 'localhost',
      database: process.env.DB_NAME || 'marketing_platform',
      password: process.env.DB_PASSWORD || 'marketing_password',
      port: parseInt(process.env.DB_PORT || '5432'),
    });
  }

  async importPopulationData(csvFilePath: string) {
    const results: any[] = [];
    
    return new Promise((resolve, reject) => {
      fs.createReadStream(csvFilePath)
        .pipe(csv())
        .on('data', (data) => results.push(data))
        .on('end', async () => {
          try {
            console.log(`Processing ${results.length} rows from ${csvFilePath}`);
            
            for (const row of results) {
              // CSV 컬럼명을 DB 컬럼명으로 매핑
              const populationData: PopulationRow = {
                administrative_code: row['행정기관코드'] || '0000000000',
                reference_date: this.parseDate(row['기준연월']),
                province: row['시도명'] || '',
                city: row['시군구명'] || '',
                district: row['읍면동명'] || '',
                age_0_9_male: parseInt(row['0~9세_남자']) || 0,
                age_0_9_female: parseInt(row['0~9세_여자']) || 0,
                age_10_19_male: parseInt(row['10~19세_남자']) || 0,
                age_10_19_female: parseInt(row['10~19세_여자']) || 0,
                age_20_29_male: parseInt(row['20~29세_남자']) || 0,
                age_20_29_female: parseInt(row['20~29세_여자']) || 0,
                age_30_39_male: parseInt(row['30~39세_남자']) || 0,
                age_30_39_female: parseInt(row['30~39세_여자']) || 0,
                age_40_49_male: parseInt(row['40~49세_남자']) || 0,
                age_40_49_female: parseInt(row['40~49세_여자']) || 0,
                age_50_59_male: parseInt(row['50~59세_남자']) || 0,
                age_50_59_female: parseInt(row['50~59세_여자']) || 0,
                age_60_69_male: parseInt(row['60~69세_남자']) || 0,
                age_60_69_female: parseInt(row['60~69세_여자']) || 0,
                age_70_79_male: parseInt(row['70~79세_남자']) || 0,
                age_70_79_female: parseInt(row['70~79세_여자']) || 0,
                age_80_89_male: parseInt(row['80~89세_남자']) || 0,
                age_80_89_female: parseInt(row['80~89세_여자']) || 0,
                age_90_99_male: parseInt(row['90~99세_남자']) || 0,
                age_90_99_female: parseInt(row['90~99세_여자']) || 0,
                age_100_plus_male: parseInt(row['100세 이상_남자']) || 0,
                age_100_plus_female: parseInt(row['100세 이상_여자']) || 0,
                total_population: parseInt(row['총인구수']) || 0,
                total_male: parseInt(row['남자총합']) || 0,
                total_female: parseInt(row['여자총합']) || 0,
              };

              await this.insertPopulationData(populationData);
            }
            
            console.log(`Successfully imported ${results.length} rows`);
            resolve(results.length);
          } catch (error) {
            reject(error);
          }
        });
    });
  }

  private parseDate(dateString: string): string {
    // 2025-04-30 형태를 Date로 변환
    if (dateString && dateString.includes('-')) {
      return dateString;
    }
    // 기본값 설정
    return '2025-01-01';
  }

  private async insertPopulationData(data: PopulationRow) {
    const query = `
      INSERT INTO population_statistics (
        administrative_code, reference_date, province, city, district,
        age_0_9_male, age_0_9_female, age_10_19_male, age_10_19_female,
        age_20_29_male, age_20_29_female, age_30_39_male, age_30_39_female,
        age_40_49_male, age_40_49_female, age_50_59_male, age_50_59_female,
        age_60_69_male, age_60_69_female, age_70_79_male, age_70_79_female,
        age_80_89_male, age_80_89_female, age_90_99_male, age_90_99_female,
        age_100_plus_male, age_100_plus_female,
        total_population, total_male, total_female
      ) VALUES (
        $1, $2, $3, $4, $5, $6, $7, $8, $9, $10,
        $11, $12, $13, $14, $15, $16, $17, $18, $19, $20,
        $21, $22, $23, $24, $25, $26, $27, $28, $29, $30
      ) ON CONFLICT (administrative_code, reference_date) DO UPDATE SET
        province = EXCLUDED.province,
        city = EXCLUDED.city,
        district = EXCLUDED.district,
        total_population = EXCLUDED.total_population,
        total_male = EXCLUDED.total_male,
        total_female = EXCLUDED.total_female
    `;

    const values = [
      data.administrative_code, data.reference_date, data.province, data.city, data.district,
      data.age_0_9_male, data.age_0_9_female, data.age_10_19_male, data.age_10_19_female,
      data.age_20_29_male, data.age_20_29_female, data.age_30_39_male, data.age_30_39_female,
      data.age_40_49_male, data.age_40_49_female, data.age_50_59_male, data.age_50_59_female,
      data.age_60_69_male, data.age_60_69_female, data.age_70_79_male, data.age_70_79_female,
      data.age_80_89_male, data.age_80_89_female, data.age_90_99_male, data.age_90_99_female,
      data.age_100_plus_male, data.age_100_plus_female,
      data.total_population, data.total_male, data.total_female
    ];

    await this.pool.query(query, values);
  }

  async createIncomeDistributionTable() {
    const query = `
      CREATE TABLE IF NOT EXISTS income_distribution (
        id SERIAL PRIMARY KEY,
        year INTEGER NOT NULL,
        region VARCHAR(50) NOT NULL,
        total_households INTEGER NOT NULL,
        under_50 INTEGER DEFAULT 0,
        from_50_to_100 INTEGER DEFAULT 0,
        from_100_to_200 INTEGER DEFAULT 0,
        from_200_to_300 INTEGER DEFAULT 0,
        from_300_to_400 INTEGER DEFAULT 0,
        from_400_to_500 INTEGER DEFAULT 0,
        from_500_to_600 INTEGER DEFAULT 0,
        from_600_to_700 INTEGER DEFAULT 0,
        from_700_to_800 INTEGER DEFAULT 0,
        over_800 INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(year, region)
      );
    `;
    
    await this.pool.query(query);
    console.log('Income distribution table created');
  }

  async importIncomeData(csvFilePath: string) {
    const results: any[] = [];
    
    return new Promise((resolve, reject) => {
      fs.createReadStream(csvFilePath)
        .pipe(csv())
        .on('data', (data) => results.push(data))
        .on('end', async () => {
          try {
            console.log(`Processing ${results.length} income rows from ${csvFilePath}`);
            
            // 테이블 생성
            await this.createIncomeDistributionTable();
            
            for (const row of results) {
              const incomeData = {
                year: parseInt(row['시점']) || 2020,
                region: row['군구별'] || '',
                total_households: parseInt(row['소계']) || 0,
                under_50: parseInt(row['50만원 미만']) || 0,
                from_50_to_100: parseInt(row['50~100만원 미만']) || 0,
                from_100_to_200: parseInt(row['100~200만원 미만']) || 0,
                from_200_to_300: parseInt(row['200~300만원 미만']) || 0,
                from_300_to_400: parseInt(row['300~400만원 미만']) || 0,
                from_400_to_500: parseInt(row['400~500만원 미만']) || 0,
                from_500_to_600: parseInt(row['500~600만원 미만']) || 0,
                from_600_to_700: parseInt(row['600~700만원 미만']) || 0,
                from_700_to_800: parseInt(row['700~800만원 미만']) || 0,
                over_800: parseInt(row['800만원 이상']) || 0,
              };

              await this.insertIncomeData(incomeData);
            }
            
            console.log(`Successfully imported ${results.length} income rows`);
            resolve(results.length);
          } catch (error) {
            reject(error);
          }
        });
    });
  }

  private async insertIncomeData(data: any) {
    const query = `
      INSERT INTO income_distribution (
        year, region, total_households, under_50, from_50_to_100,
        from_100_to_200, from_200_to_300, from_300_to_400, from_400_to_500,
        from_500_to_600, from_600_to_700, from_700_to_800, over_800
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
      ON CONFLICT (year, region) DO UPDATE SET
        total_households = EXCLUDED.total_households,
        under_50 = EXCLUDED.under_50,
        from_50_to_100 = EXCLUDED.from_50_to_100,
        from_100_to_200 = EXCLUDED.from_100_to_200,
        from_200_to_300 = EXCLUDED.from_200_to_300,
        from_300_to_400 = EXCLUDED.from_300_to_400,
        from_400_to_500 = EXCLUDED.from_400_to_500,
        from_500_to_600 = EXCLUDED.from_500_to_600,
        from_600_to_700 = EXCLUDED.from_600_to_700,
        from_700_to_800 = EXCLUDED.from_700_to_800,
        over_800 = EXCLUDED.over_800
    `;

    const values = [
      data.year, data.region, data.total_households, data.under_50, data.from_50_to_100,
      data.from_100_to_200, data.from_200_to_300, data.from_300_to_400, data.from_400_to_500,
      data.from_500_to_600, data.from_600_to_700, data.from_700_to_800, data.over_800
    ];

    await this.pool.query(query, values);
  }

  async close() {
    await this.pool.end();
  }
}

// 실행 스크립트
async function main() {
  const importer = new DataImporter();
  
  try {
    // 인구 데이터 가져오기
    const populationFile = path.join(__dirname, '../../docs/population_with_total_columns.csv');
    if (fs.existsSync(populationFile)) {
      await importer.importPopulationData(populationFile);
    }

    // 소득 데이터 가져오기
    const incomeFiles = [
      path.join(__dirname, '../../docs/incheon_gun_gu_pop_incheon2020.csv'),
      path.join(__dirname, '../../docs/incheon_gun_gu_pop_incheon2021.csv'),
      path.join(__dirname, '../../docs/incheon_gun_gu_pop_incheon2022.csv'),
    ];

    for (const file of incomeFiles) {
      if (fs.existsSync(file)) {
        await importer.importIncomeData(file);
      }
    }

    console.log('Data import completed successfully!');
  } catch (error) {
    console.error('Error importing data:', error);
  } finally {
    await importer.close();
  }
}

if (require.main === module) {
  main();
}

export { DataImporter };
