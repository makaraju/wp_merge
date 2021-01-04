import pytest
from unittest.mock import patch, mock_open, call
from src.wp_merge.core import MergeCsvRecords
import requests

class TestWpEngine(object):

    # Below is test data for happy path
    happy_path_input_1 = """Account ID,Account Name,First Name,Created On
12345,lexcorp,Lex,2011-01-12
8172,latveriaembassy,Victor,2014-11-19
"""

    happy_path_api_response_1 = [
        {'account_id': 12345, 'status': 'good', 'created_on': '2011-01-12'},
        {'account_id': 8172, 'status': 'closed', 'created_on': '2015-09-01'}
    ]
    happy_path_api_funcation_input_1 = [call('12345'), call('8172')]
    happy_path_expected_output_1 = [
        call('Account ID,First Name,Created On,Status,Status Set On\r\n'),
        call('12345,Lex,2011-01-12,good,2011-01-12\r\n'),
        call('8172,Victor,2014-11-19,closed,2015-09-01\r\n')
    ]

    # Below is test data for invalid account id
    invalid_acct_id_input_1 = """Account ID,Account Name,First Name,Created On
1111,lexcorp,Lex,2011-01-12
8172,latveriaembassy,Victor,2014-11-19
"""
    invalid_acct_id_response_1 = [
        None,
        {'account_id': 8172, 'status': 'closed', 'created_on': '2015-09-01'}
    ]
    invalid_acct_id_api_funcation_input_1 = [call('1111'), call('8172')]
    invalid_acct_id_expected_output_1 = [
        call('Account ID,First Name,Created On,Status,Status Set On\r\n'),
        call('8172,Victor,2014-11-19,closed,2015-09-01\r\n')
    ]

    def test_api_check_status_code_equals_200(self):
        response = requests.get("http://interview.wpengine.io/v1/accounts")
        assert response.status_code == 200

    @patch('os.path.exists')
    @patch("builtins.open", new_callable=mock_open, read_data=happy_path_input_1)
    @patch('src.wp_merge.core.MergeCsvRecords.fetchaccountinfo')
    def test_happy_path_with_mock_file(self, mock_wp_engine_api, mock_input_file, mock_os_path):

        mock_wp_engine_api.side_effect = self.happy_path_api_response_1
        mock_os_path.return_value = True
        test_merge_csv = MergeCsvRecords()
        test_merge_csv.generateoutput(inputfile='/path/to/your/file', outputfile='/path/to/your/output')
        mock_wp_engine_api.assert_has_calls(self.happy_path_api_funcation_input_1)
        mock_input_file.assert_has_calls([call('/path/to/your/output','w', newline=''), call('/path/to/your/file','r')],
                                         any_order=True)
        handle = mock_input_file()
        handle.write.assert_has_calls(self.happy_path_expected_output_1)

    @patch('os.path.exists')
    @patch("builtins.open", new_callable=mock_open, read_data=invalid_acct_id_input_1)
    @patch('src.wp_merge.core.MergeCsvRecords.fetchaccountinfo')
    def test_for_invalid_acct_id(self, mock_wp_engine_api, mock_input_file, mock_os_path):
        mock_wp_engine_api.side_effect = self.invalid_acct_id_response_1
        mock_os_path.return_value = True
        test_merge_csv = MergeCsvRecords()
        test_merge_csv.generateoutput(inputfile='/path/to/your/file', outputfile='/path/to/your/output')
        mock_input_file.assert_has_calls([call('/path/to/your/output','w', newline=''), call('/path/to/your/file','r')],
                                         any_order=True)
        mock_wp_engine_api.assert_has_calls(self.invalid_acct_id_api_funcation_input_1)

        handle = mock_input_file()
        handle.write.assert_has_calls(self.invalid_acct_id_expected_output_1)