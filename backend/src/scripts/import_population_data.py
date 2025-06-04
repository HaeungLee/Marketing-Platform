import csv
from datetime import datetime
import sys
import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add backend/src to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, src_dir)

# Now we can import from src
from config.settings import settings

def import_population_data(csv_path):
    logger.info("Starting data import process...")
    logger.info(f"CSV file path: {csv_path}")
    
    try:
        # Create database engine
        engine = create_engine(settings.sync_database_url)
        Session = sessionmaker(bind=engine)
        session = Session()

        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            csv_reader = csv.DictReader(file)
            
            # Debug: Print first row and its keys
            first_row = next(csv_reader)
            logger.info("CSV columns: %s", list(first_row.keys()))
            file.seek(0)
            next(csv_reader)
            
            # Prepare batch insert
            values = []
            row_count = 0
            
            insert_stmt = text(
                '''INSERT INTO population_statistics (administrative_code, reference_date, province, city, district, 
                age_0_9_male, age_10_19_male, age_20_29_male, age_30_39_male, age_40_49_male, 
                age_50_59_male, age_60_69_male, age_70_79_male, age_80_89_male, age_90_99_male, 
                age_100_plus_male, age_0_9_female, age_10_19_female, age_20_29_female, age_30_39_female, 
                age_40_49_female, age_50_59_female, age_60_69_female, age_70_79_female, age_80_89_female, 
                age_90_99_female, age_100_plus_female, total_population, total_male, total_female) 
                VALUES (:administrative_code, :reference_date, :province, :city, :district, 
                :age_0_9_male, :age_10_19_male, :age_20_29_male, :age_30_39_male, :age_40_49_male, 
                :age_50_59_male, :age_60_69_male, :age_70_79_male, :age_80_89_male, :age_90_99_male, 
                :age_100_plus_male, :age_0_9_female, :age_10_19_female, :age_20_29_female, :age_30_39_female, 
                :age_40_49_female, :age_50_59_female, :age_60_69_female, :age_70_79_female, :age_80_89_female, 
                :age_90_99_female, :age_100_plus_female, :total_population, :total_male, :total_female)'''
            )
            
            for row in csv_reader:
                row_count += 1
                if row_count == 1:
                    logger.info("First row data: %s", row)
                
                # Convert date string to date object
                reference_date = datetime.strptime(row['기준연월'], '%Y-%m-%d').date()
                
                # Prepare row data
                value = {
                    'administrative_code': row['행정기관코드'],
                    'reference_date': reference_date,
                    'province': row['시도명'],
                    'city': row['시군구명'],
                    'district': row['읍면동명'],
                    # Male age groups
                    'age_0_9_male': int(row['0~9세_남자']),
                    'age_10_19_male': int(row['10~19세_남자']),
                    'age_20_29_male': int(row['20~29세_남자']),
                    'age_30_39_male': int(row['30~39세_남자']),
                    'age_40_49_male': int(row['40~49세_남자']),
                    'age_50_59_male': int(row['50~59세_남자']),
                    'age_60_69_male': int(row['60~69세_남자']),
                    'age_70_79_male': int(row['70~79세_남자']),
                    'age_80_89_male': int(row['80~89세_남자']),
                    'age_90_99_male': int(row['90~99세_남자']),
                    'age_100_plus_male': int(row['100세 이상_남자']),
                    # Female age groups
                    'age_0_9_female': int(row['0~9세_여자']),
                    'age_10_19_female': int(row['10~19세_여자']),
                    'age_20_29_female': int(row['20~29세_여자']),
                    'age_30_39_female': int(row['30~39세_여자']),
                    'age_40_49_female': int(row['40~49세_여자']),
                    'age_50_59_female': int(row['50~59세_여자']),
                    'age_60_69_female': int(row['60~69세_여자']),
                    'age_70_79_female': int(row['70~79세_여자']),
                    'age_80_89_female': int(row['80~89세_여자']),
                    'age_90_99_female': int(row['90~99세_여자']),
                    'age_100_plus_female': int(row['100세 이상_여자']),
                    # Totals
                    'total_population': int(row['총인구수']),
                    'total_male': int(row['남자총합']),
                    'total_female': int(row['여자총합']),
                }
                values.append(value)
                
                # Insert in batches of 1000
                if len(values) >= 1000:
                    logger.info(f"Inserting batch of {len(values)} records...")
                    session.execute(insert_stmt, values)
                    session.commit()
                    values = []
            
            # Insert remaining rows
            if values:
                logger.info(f"Inserting final batch of {len(values)} records...")
                session.execute(insert_stmt, values)
                session.commit()
            
            logger.info(f"Data import completed successfully! Total rows processed: {row_count}")
            
    except Exception as e:
        logger.error(f"Error during import: {str(e)}")
        logger.error("Error occurred while processing row: %s", row if 'row' in locals() else 'No row available')
        raise

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python import_population_data.py <csv_file_path>")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    import_population_data(csv_file_path)
