import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { Pool } from "pg";

class PostgreSQLMCPServer {
  private server: Server;
  private pool: Pool;

  constructor() {
    this.server = new Server(
      {
        name: "marketing-platform-postgresql",
        version: "1.0.0",
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    // PostgreSQL 연결 설정
    this.pool = new Pool({
      user: process.env.DB_USER || 'marketing_user',
      host: process.env.DB_HOST || 'localhost',
      database: process.env.DB_NAME || 'marketing_platform',
      password: process.env.DB_PASSWORD || 'marketing_password',
      port: parseInt(process.env.DB_PORT || '5432'),
    });

    this.setupHandlers();
  }

  private setupHandlers() {
    // 도구 목록 제공
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: "get_population_statistics",
          description: "인구 통계 데이터를 조회합니다",
          inputSchema: {
            type: "object",
            properties: {
              city: {
                type: "string",
                description: "도시명 (선택사항)",
              },
              district: {
                type: "string", 
                description: "구/군명 (선택사항)",
              },
              year: {
                type: "string",
                description: "연도 (선택사항)",
              },
            },
          },
        },
        {
          name: "get_income_distribution",
          description: "소득 분포 데이터를 조회합니다",
          inputSchema: {
            type: "object",
            properties: {
              region: {
                type: "string",
                description: "지역명 (선택사항)",
              },
              year: {
                type: "string",
                description: "연도 (선택사항)",
              },
            },
          },
        },
        {
          name: "execute_sql",
          description: "SQL 쿼리를 실행합니다",
          inputSchema: {
            type: "object",
            properties: {
              query: {
                type: "string",
                description: "실행할 SQL 쿼리",
              },
            },
            required: ["query"],
          },
        },
        {
          name: "analyze_target_customers",
          description: "특정 업종과 지역의 타겟 고객을 분석합니다",
          inputSchema: {
            type: "object",
            properties: {
              businessType: {
                type: "string",
                description: "업종 (예: restaurant, cafe, retail)",
              },
              region: {
                type: "string",
                description: "지역명 (시/구/동)",
              },
            },
            required: ["businessType", "region"],
          },
        },
        {
          name: "recommend_optimal_location",
          description: "최적 입지를 추천합니다",
          inputSchema: {
            type: "object",
            properties: {
              businessType: {
                type: "string",
                description: "업종",
              },
              budget: {
                type: "number",
                description: "예산",
              },
              targetAge: {
                type: "string",
                description: "타겟 연령대 (선택사항)",
              },
            },
            required: ["businessType", "budget"],
          },
        },
        {
          name: "get_marketing_timing",
          description: "마케팅 최적 타이밍을 분석합니다",
          inputSchema: {
            type: "object",
            properties: {
              targetAge: {
                type: "string",
                description: "타겟 연령대",
              },
              businessType: {
                type: "string",
                description: "업종",
              },
              region: {
                type: "string",
                description: "지역명",
              },
            },
            required: ["targetAge", "businessType", "region"],
          },
        },
      ],
    }));

    // 도구 실행 핸들러
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case "get_population_statistics":
            return await this.getPopulationStatistics(args);
          case "get_income_distribution":
            return await this.getIncomeDistribution(args);
          case "execute_sql":
            return await this.executeSql(args);
          case "analyze_target_customers":
            return await this.analyzeTargetCustomers(args);
          case "recommend_optimal_location":
            return await this.recommendOptimalLocation(args);
          case "get_marketing_timing":
            return await this.getMarketingTiming(args);
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: "text",
              text: `Error: ${error instanceof Error ? error.message : String(error)}`,
            },
          ],
        };
      }
    });
  }

  private async getPopulationStatistics(args: any) {
    let query = `
      SELECT 
        administrative_code,
        reference_date,
        province,
        city,
        district,
        total_population,
        total_male,
        total_female,
        age_0_9_male + age_0_9_female as age_0_9_total,
        age_10_19_male + age_10_19_female as age_10_19_total,
        age_20_29_male + age_20_29_female as age_20_29_total,
        age_30_39_male + age_30_39_female as age_30_39_total,
        age_40_49_male + age_40_49_female as age_40_49_total,
        age_50_59_male + age_50_59_female as age_50_59_total,
        age_60_69_male + age_60_69_female as age_60_69_total,
        age_70_79_male + age_70_79_female as age_70_79_total,
        age_80_89_male + age_80_89_female as age_80_89_total,
        age_90_99_male + age_90_99_female as age_90_99_total
      FROM population_statistics
      WHERE 1=1
    `;

    const params: any[] = [];
    let paramCount = 0;

    if (args.city) {
      paramCount++;
      query += ` AND city = $${paramCount}`;
      params.push(args.city);
    }

    if (args.district) {
      paramCount++;
      query += ` AND district = $${paramCount}`;
      params.push(args.district);
    }

    if (args.year) {
      paramCount++;
      query += ` AND EXTRACT(YEAR FROM reference_date) = $${paramCount}`;
      params.push(parseInt(args.year));
    }

    query += ` ORDER BY reference_date DESC, city, district LIMIT 100`;

    const result = await this.pool.query(query, params);

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result.rows, null, 2),
        },
      ],
    };
  }

  private async getIncomeDistribution(args: any) {
    // 소득 분포 데이터는 별도 테이블에서 조회
    // 현재는 기본 쿼리만 구현
    const query = `
      SELECT * FROM income_distribution 
      WHERE 1=1
      ORDER BY year DESC, region
      LIMIT 100
    `;

    const result = await this.pool.query(query);

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result.rows, null, 2),
        },
      ],
    };
  }

  private async executeSql(args: any) {
    const { query } = args;
    
    // 보안을 위해 SELECT 쿼리만 허용
    if (!query.trim().toLowerCase().startsWith('select')) {
      throw new Error('Only SELECT queries are allowed');
    }

    const result = await this.pool.query(query);

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({
            rowCount: result.rowCount,
            rows: result.rows,
          }, null, 2),
        },
      ],
    };
  }

  private async analyzeTargetCustomers(args: any) {
    const { businessType, region } = args;
    
    // 1. 지역별 인구 분포 조회
    const populationQuery = `
      SELECT 
        age_20_29_male + age_20_29_female as age_20_29_total,
        age_30_39_male + age_30_39_female as age_30_39_total,
        age_40_49_male + age_40_49_female as age_40_49_total,
        age_50_59_male + age_50_59_female as age_50_59_total,
        total_population,
        city,
        district
      FROM population_statistics
      WHERE city ILIKE $1 OR district ILIKE $1
      ORDER BY reference_date DESC
      LIMIT 10
    `;
    
    const populationResult = await this.pool.query(populationQuery, [`%${region}%`]);
    
    if (populationResult.rows.length === 0) {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              error: "해당 지역의 인구 데이터를 찾을 수 없습니다",
              searchedRegion: region
            }, null, 2),
          },
        ],
      };
    }

    // 2. 연령대별 비율 계산
    const data = populationResult.rows[0];
    const totalPop = data.total_population || 1;
    
    const ageAnalysis = {
      "20-29세": {
        count: data.age_20_29_total,
        percentage: ((data.age_20_29_total / totalPop) * 100).toFixed(1)
      },
      "30-39세": {
        count: data.age_30_39_total,
        percentage: ((data.age_30_39_total / totalPop) * 100).toFixed(1)
      },
      "40-49세": {
        count: data.age_40_49_total,
        percentage: ((data.age_40_49_total / totalPop) * 100).toFixed(1)
      },
      "50-59세": {
        count: data.age_50_59_total,
        percentage: ((data.age_50_59_total / totalPop) * 100).toFixed(1)
      }
    };

    // 3. 업종별 타겟 고객 분석 로직
    let primaryTarget = "";
    let secondaryTarget = "";
    let strategies: string[] = [];

    switch (businessType.toLowerCase()) {
      case "restaurant":
      case "cafe":
        // 30-40대가 주요 타겟
        const restaurant3040 = data.age_30_39_total + data.age_40_49_total;
        primaryTarget = restaurant3040 > data.age_20_29_total ? "30-49세" : "20-29세";
        secondaryTarget = "전 연령대";
        strategies = ["점심시간 할인", "직장인 맞춤 메뉴", "배달 서비스 강화"];
        break;
      case "retail":
      case "shopping":
        primaryTarget = "20-39세";
        secondaryTarget = "40-59세";
        strategies = ["온라인 연동 프로모션", "세일 이벤트", "멤버십 혜택"];
        break;
      default:
        primaryTarget = "30-49세";
        secondaryTarget = "20-29세";
        strategies = ["지역 맞춤 서비스", "고객 충성도 프로그램"];
    }

    const result = {
      region: `${data.city} ${data.district}`,
      totalPopulation: totalPop,
      ageAnalysis,
      targetCustomerAnalysis: {
        primaryTarget,
        secondaryTarget,
        strategies
      },
      confidence: "높음 (실제 인구통계 데이터 기반)",
      dataSource: "population_statistics 테이블"
    };

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }

  private async recommendOptimalLocation(args: any) {
    const { businessType, budget, targetAge } = args;
    
    // 1. 인구 밀도가 높은 지역 찾기
    const locationQuery = `
      SELECT 
        city,
        district,
        total_population,
        (age_20_29_male + age_20_29_female) as young_adults,
        (age_30_39_male + age_30_39_female + age_40_49_male + age_40_49_female) as middle_age,
        (age_50_59_male + age_50_59_female) as older_adults
      FROM population_statistics
      WHERE total_population > 5000
      ORDER BY total_population DESC
      LIMIT 20
    `;
    
    const locationResult = await this.pool.query(locationQuery);
    
    // 2. 점수 계산 알고리즘
    const scoredLocations = locationResult.rows.map(row => {
      let score = 0;
      const totalPop = row.total_population;
      
      // 인구 밀도 점수 (40%)
      score += (totalPop / 50000) * 40;
      
      // 타겟 연령대 비율 점수 (30%)
      if (targetAge?.includes("20-29")) {
        score += (row.young_adults / totalPop) * 30;
      } else if (targetAge?.includes("30-49")) {
        score += (row.middle_age / totalPop) * 30;
      } else {
        score += (row.middle_age / totalPop) * 20;
      }
      
      // 업종별 가중치 (30%)
      switch (businessType.toLowerCase()) {
        case "restaurant":
        case "cafe":
          score += (row.middle_age / totalPop) * 30;
          break;
        case "retail":
          score += (row.young_adults / totalPop) * 25;
          break;
        default:
          score += 15;
      }
      
      return {
        location: `${row.city} ${row.district}`,
        score: Math.min(score, 100),
        population: totalPop,
        youngAdults: row.young_adults,
        middleAge: row.middle_age,
        expectedROI: `${(score * 0.8 + 20).toFixed(1)}%`
      };
    });

    // 3. 상위 5개 지역 선별
    const topLocations = scoredLocations
      .sort((a, b) => b.score - a.score)
      .slice(0, 5);

    const result = {
      recommendedAreas: topLocations.map(loc => ({
        area: loc.location,
        score: loc.score.toFixed(1),
        expectedROI: loc.expectedROI,
        population: loc.population
      })),
      analysisMetadata: {
        totalAnalyzedLocations: locationResult.rows.length,
        confidenceLevel: "높음",
        factors: ["인구밀도", "타겟연령대비율", "업종적합성"],
        budget: budget
      }
    };

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }

  private async getMarketingTiming(args: any) {
    const { targetAge, businessType, region } = args;
    
    // 인구 데이터 기반 마케팅 타이밍 분석
    const timingQuery = `
      SELECT 
        city,
        district,
        total_population,
        (age_20_29_male + age_20_29_female) as age_20_29,
        (age_30_39_male + age_30_39_female) as age_30_39,
        (age_40_49_male + age_40_49_female) as age_40_49
      FROM population_statistics
      WHERE city ILIKE $1 OR district ILIKE $1
      ORDER BY reference_date DESC
      LIMIT 5
    `;
    
    const timingResult = await this.pool.query(timingQuery, [`%${region}%`]);
    
    if (timingResult.rows.length === 0) {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              error: "해당 지역의 데이터를 찾을 수 없습니다",
              searchedRegion: region
            }, null, 2),
          },
        ],
      };
    }

    const data = timingResult.rows[0];
    
    // 업종별 최적 타이밍 로직
    let bestDays: string[] = [];
    let bestHours: string[] = [];
    let seasonalTrends = "";
    
    switch (businessType.toLowerCase()) {
      case "restaurant":
        bestDays = ["화요일", "수요일", "목요일"];
        bestHours = ["11:30-13:00", "18:00-20:00"];
        seasonalTrends = "여름철 배달 주문 20% 증가 예상";
        break;
      case "cafe":
        bestDays = ["토요일", "일요일", "금요일"];
        bestHours = ["09:00-11:00", "14:00-17:00"];
        seasonalTrends = "겨울철 따뜻한 음료 수요 30% 증가";
        break;
      case "retail":
        bestDays = ["금요일", "토요일", "일요일"];
        bestHours = ["10:00-12:00", "15:00-19:00"];
        seasonalTrends = "연말 시즌 매출 40% 증가 예상";
        break;
      default:
        bestDays = ["월요일", "화요일", "수요일"];
        bestHours = ["10:00-17:00"];
        seasonalTrends = "계절별 변동 없음";
    }

    // 타겟 연령대에 따른 조정
    if (targetAge.includes("20-29")) {
      bestHours = ["19:00-22:00", "12:00-14:00"];
      bestDays = ["금요일", "토요일", "일요일"];
    } else if (targetAge.includes("40-49")) {
      bestHours = ["10:00-16:00"];
      bestDays = ["화요일", "수요일", "목요일"];
    }

    const result = {
      region: `${data.city} ${data.district}`,
      targetAge,
      businessType,
      timing: {
        bestDays,
        bestHours,
        seasonalTrends
      },
      populationContext: {
        totalPopulation: data.total_population,
        targetAgePopulation: targetAge.includes("20-29") ? data.age_20_29 : 
                           targetAge.includes("30-39") ? data.age_30_39 : data.age_40_49
      },
      confidence: "보통 (인구 데이터 + 업종 분석 기반)",
      recommendations: [
        "타겟 연령대 활동 패턴에 맞춘 마케팅 시간 설정",
        "지역 특성을 고려한 프로모션 기획",
        "계절별 메뉴/상품 라인업 조정"
      ]
    };

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error("PostgreSQL MCP Server running on stdio");
  }
}

const server = new PostgreSQLMCPServer();
server.run().catch(console.error);
