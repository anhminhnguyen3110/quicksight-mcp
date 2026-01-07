"""Unit tests for Template and Theme services"""

import pytest
from unittest.mock import Mock
from quicksight_mcp.services.template import TemplateService
from quicksight_mcp.services.theme import ThemeService
from quicksight_mcp.models.template import CreateTemplateRequest, TemplateSourceEntity
from quicksight_mcp.models.theme import CreateThemeRequest, ThemeConfiguration


@pytest.fixture
def mock_client():
    return Mock()


class TestTemplateService:
    """Tests for TemplateService"""
    
    @pytest.fixture
    def template_service(self, mock_client):
        return TemplateService(mock_client, "123456789012")
    
    def test_list_templates(self, template_service, mock_client):
        """Test listing templates"""
        mock_client.list_templates.return_value = {
            'TemplateSummaryList': [
                {'TemplateId': 'tpl1', 'Name': 'Template 1'},
                {'TemplateId': 'tpl2', 'Name': 'Template 2'}
            ]
        }
        
        result = template_service.list_templates()
        
        assert len(result) == 2
        assert result[0]['TemplateId'] == 'tpl1'
    
    def test_create_template(self, template_service, mock_client):
        """Test creating a template"""
        mock_client.create_template.return_value = {
            'Status': 200,
            'TemplateId': 'tpl1',
            'Arn': 'arn:aws:quicksight:us-east-1:123456789012:template/tpl1'
        }
        
        source_entity = TemplateSourceEntity(
            source_analysis={'Arn': 'arn:aws:quicksight:us-east-1:123456789012:analysis/analysis1'}
        )
        
        request = CreateTemplateRequest(
            template_id='tpl1',
            name='Test Template',
            source_entity=source_entity
        )
        
        result = template_service.create_template(request)
        
        assert result['Status'] == 200
        assert result['TemplateId'] == 'tpl1'


class TestThemeService:
    """Tests for ThemeService"""
    
    @pytest.fixture
    def theme_service(self, mock_client):
        return ThemeService(mock_client, "123456789012")
    
    def test_list_themes(self, theme_service, mock_client):
        """Test listing themes"""
        mock_client.list_themes.return_value = {
            'ThemeSummaryList': [
                {'ThemeId': 'theme1', 'Name': 'Theme 1'},
                {'ThemeId': 'theme2', 'Name': 'Theme 2'}
            ]
        }
        
        result = theme_service.list_themes()
        
        assert len(result) == 2
        assert result[0]['ThemeId'] == 'theme1'
    
    def test_create_theme(self, theme_service, mock_client):
        """Test creating a theme"""
        mock_client.create_theme.return_value = {
            'Status': 200,
            'ThemeId': 'theme1',
            'Arn': 'arn:aws:quicksight:us-east-1:123456789012:theme/theme1'
        }
        
        configuration = ThemeConfiguration(
            data_color_palette={'Colors': ['#FF0000', '#00FF00']},
            ui_color_palette={'PrimaryForeground': '#000000'}
        )
        
        request = CreateThemeRequest(
            theme_id='theme1',
            name='Test Theme',
            base_theme_id='MIDNIGHT',
            configuration=configuration
        )
        
        result = theme_service.create_theme(request)
        
        assert result['Status'] == 200
        assert result['ThemeId'] == 'theme1'
