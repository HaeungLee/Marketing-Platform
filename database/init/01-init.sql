-- PostgreSQL 초기화 스크립트
-- Marketing Platform 데이터베이스 초기 설정

-- 확장 프로그램 활성화
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 한국어 지원을 위한 설정
SET default_text_search_config = 'korean';

-- 시간대 설정
SET timezone = 'Asia/Seoul';

-- 초기 관리자 계정 생성 (선택사항)
-- INSERT INTO users (id, email, username, is_active, is_superuser, created_at)
-- VALUES (
--     uuid_generate_v4(),
--     'admin@marketing-platform.com',
--     'admin',
--     true,
--     true,
--     NOW()
-- );

-- 기본 비즈니스 카테고리 데이터 삽입
INSERT INTO business_categories (name, description, created_at) VALUES
('음식점', '한식, 중식, 일식, 양식, 분식 등 음식점업', NOW()),
('카페/디저트', '커피전문점, 베이커리, 디저트 전문점', NOW()),
('뷰티/헤어', '미용실, 네일샵, 피부관리실, 마사지샵', NOW()),
('쇼핑/패션', '의류, 신발, 액세서리, 생활용품', NOW()),
('학원/교육', '어학원, 예체능학원, 과외, 온라인교육', NOW()),
('의료/건강', '병원, 한의원, 약국, 헬스장, 요가', NOW()),
('서비스', '세탁소, 수리점, 펜션, 부동산', NOW()),
('기타', '기타 업종', NOW())
ON CONFLICT (name) DO NOTHING;

-- 기본 콘텐츠 타입 데이터
INSERT INTO content_types (type, description, template, created_at) VALUES
('blog', '블로그 포스팅', '{"title": "", "content": "", "tags": []}', NOW()),
('instagram', '인스타그램 게시물', '{"caption": "", "hashtags": []}', NOW()),
('youtube', '유튜브 스크립트', '{"title": "", "description": "", "script": ""}', NOW()),
('flyer', '전단지/포스터', '{"headline": "", "body": "", "cta": ""}', NOW())
ON CONFLICT (type) DO NOTHING;

-- 인덱스 생성 (성능 최적화)
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_businesses_owner_id ON businesses(owner_id);
CREATE INDEX IF NOT EXISTS idx_businesses_category ON businesses(category);
CREATE INDEX IF NOT EXISTS idx_content_business_id ON generated_content(business_id);
CREATE INDEX IF NOT EXISTS idx_content_created_at ON generated_content(created_at);

-- 통계 정보 업데이트
ANALYZE;
