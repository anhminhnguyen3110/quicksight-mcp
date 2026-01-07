"""Embed service for QuickSight embed URL operations"""

import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class EmbedService:
    """Service for managing QuickSight embed URLs"""
    
    def __init__(self, quicksight_client, aws_account_id: str):
        """
        Initialize embed service
        
        Args:
            quicksight_client: Boto3 QuickSight client
            aws_account_id: AWS Account ID
        """
        self.client = quicksight_client
        self.account_id = aws_account_id
    
    def generate_embed_url_for_anonymous_user(
        self,
        namespace: str,
        authorized_resource_arns: List[str],
        experience_configuration: Dict[str, Any],
        session_lifetime_in_minutes: Optional[int] = None,
        allowed_domains: Optional[List[str]] = None,
        session_tags: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Generate embed URL for anonymous users"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'Namespace': namespace,
                'AuthorizedResourceArns': authorized_resource_arns,
                'ExperienceConfiguration': experience_configuration
            }
            
            if session_lifetime_in_minutes:
                params['SessionLifetimeInMinutes'] = session_lifetime_in_minutes
            if allowed_domains:
                params['AllowedDomains'] = allowed_domains
            if session_tags:
                params['SessionTags'] = session_tags
            
            response = self.client.generate_embed_url_for_anonymous_user(**params)
            logger.info("Generated anonymous embed URL")
            return response
            
        except Exception as e:
            logger.error(f"Error generating anonymous embed URL: {str(e)}")
            raise
    
    def generate_embed_url_for_registered_user(
        self,
        user_arn: str,
        experience_configuration: Dict[str, Any],
        session_lifetime_in_minutes: Optional[int] = None,
        allowed_domains: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Generate embed URL for registered QuickSight users"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'UserArn': user_arn,
                'ExperienceConfiguration': experience_configuration
            }
            
            if session_lifetime_in_minutes:
                params['SessionLifetimeInMinutes'] = session_lifetime_in_minutes
            if allowed_domains:
                params['AllowedDomains'] = allowed_domains
            
            response = self.client.generate_embed_url_for_registered_user(**params)
            logger.info("Generated registered user embed URL")
            return response
            
        except Exception as e:
            logger.error(f"Error generating registered embed URL: {str(e)}")
            raise
