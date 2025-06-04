#!/usr/bin/env python3

import asyncio
import asyncpg
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Test the fixed database connection
async def test_db_connection():
    """Test database connection with the fixed code"""
    
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'marketing_platform',
        'user': 'postgres',
        'password': 'postgres'
    }
    
    try:
        print("Testing database connection...")
        conn = await asyncpg.connect(**db_config)
        try:
            # Test a simple query
            result = await conn.fetch("SELECT 1 as test")
            print(f"✅ Database connection successful: {result}")
            
            # Test our population query
            population_query = """
                SELECT 
                    province, city, district,
                    age_20_29_male + age_20_29_female as age_20s,
                    age_30_39_male + age_30_39_female as age_30s,
                    age_40_49_male + age_40_49_female as age_40s,
                    age_50_59_male + age_50_59_female as age_50s,
                    total_population
                FROM population_statistics 
                WHERE city ILIKE $1 OR district ILIKE $1
                LIMIT 3
            """
            
            population_data = await conn.fetch(population_query, "%강남%")
            print(f"✅ Population query successful: {len(population_data)} rows")
            
            for row in population_data:
                print(f"  - {row['city']} {row['district']}: {row['total_population']} people")
                
        finally:
            await conn.close()
            print("✅ Database connection closed properly")
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
        
    return True

if __name__ == "__main__":
    result = asyncio.run(test_db_connection())
    if result:
        print("\n🎉 Database connection test PASSED!")
    else:
        print("\n❌ Database connection test FAILED!")
