"""
이메일 발송 유틸리티
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config.settings import settings
import logging

logger = logging.getLogger(__name__)

def send_verification_email(email: str, verification_code: str) -> None:
    """이메일 인증 메일 발송"""
    try:
        # 이메일 메시지 생성
        msg = MIMEMultipart()
        msg['From'] = settings.smtp_user
        msg['To'] = email
        msg['Subject'] = "이메일 인증 코드"
        
        body = f"""
        안녕하세요,
        
        회원가입을 위한 이메일 인증 코드입니다:
        
        {verification_code}
        
        이 코드는 24시간 동안 유효합니다.
        
        감사합니다.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # SMTP 서버 연결 및 이메일 발송
        server = smtplib.SMTP(settings.smtp_host, settings.smtp_port)
        server.starttls()  # TLS 보안 연결
        server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"이메일 발송 성공: {email}")
        
    except Exception as e:
        logger.error(f"이메일 발송 실패: {str(e)}")
        raise

def send_password_reset_email(email: str, reset_token: str) -> None:
    """비밀번호 재설정 이메일 발송"""
    try:
        # 이메일 메시지 생성
        msg = MIMEMultipart()
        msg['From'] = settings.smtp_user
        msg['To'] = email
        msg['Subject'] = "비밀번호 재설정"
        
        body = f"""
        안녕하세요,
        
        비밀번호 재설정을 위한 링크입니다:
        
        {settings.frontend_url}/reset-password?token={reset_token}
        
        이 링크는 1시간 동안 유효합니다.
        
        감사합니다.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # SMTP 서버 연결 및 이메일 발송
        server = smtplib.SMTP(settings.smtp_host, settings.smtp_port)
        server.starttls()  # TLS 보안 연결
        server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"이메일 발송 성공: {email}")
        
    except Exception as e:
        logger.error(f"이메일 발송 실패: {str(e)}")
        raise 