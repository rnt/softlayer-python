"""
    SoftLayer.tests.CLI.modules.file_tests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :license: MIT, see LICENSE for more details.
"""
from SoftLayer import testing

import json
import mock


class FileTests(testing.TestCase):

    def test_access_list(self):
        result = self.run_command(['file', 'access-list', '1234'])

        self.assert_no_fail(result)
        self.assertEqual([
            {
                'username': 'joe',
                'name': 'test-server.example.com',
                'type': 'VIRTUAL',
                'host_iqn': 'test-server',
                'password': '12345',
                'private_ip_address': '10.0.0.1',
                'id': 1234,
            },
            {
                'username': 'joe',
                'name': 'test-server.example.com',
                'type': 'HARDWARE',
                'host_iqn': 'test-server',
                'password': '12345',
                'private_ip_address': '10.0.0.2',
                'id': 1234,
            },
            {
                'username': 'joe',
                'name': '10.0.0.1/24 (backend subnet)',
                'type': 'SUBNET',
                'host_iqn': 'test-server',
                'password': '12345',
                'private_ip_address': None,
                'id': 1234,
            },
            {
                'username': 'joe',
                'name': '10.0.0.1 (backend ip)',
                'type': 'IP',
                'host_iqn': 'test-server',
                'password': '12345',
                'private_ip_address': None,
                'id': 1234,
            }],
            json.loads(result.output),)

    def test_authorize_host_to_volume(self):
        result = self.run_command(['file', 'access-authorize', '12345678',
                                   '--hardware-id=100', '--virtual-id=10',
                                   '--ip-address-id=192',
                                   '--ip-address=192.3.2.1',
                                   '--subnet-id=200'])

        self.assert_no_fail(result)

    def test_deauthorize_host_to_volume(self):
        result = self.run_command(['file', 'access-revoke', '12345678',
                                   '--hardware-id=100', '--virtual-id=10',
                                   '--ip-address-id=192',
                                   '--ip-address=192.3.2.1',
                                   '--subnet-id=200'])

        self.assert_no_fail(result)

    def test_volume_list(self):
        result = self.run_command(['file', 'volume-list'])

        self.assert_no_fail(result)
        self.assertEqual([
            {
                'bytes_used': None,
                'capacity_gb': 10,
                'datacenter': 'Dallas',
                'id': 1,
                'ip_addr': '127.0.0.1',
                'storage_type': 'ENDURANCE',
                'username': 'user',
                'active_transactions': None
            }],
            json.loads(result.output))

    def test_snapshot_list(self):
        result = self.run_command(['file', 'snapshot-list', '1234'])

        self.assert_no_fail(result)
        self.assertEqual([
            {
                'id': 470,
                'name': 'unit_testing_note',
                'created': '2016-07-06T07:41:19-05:00',
                'size_bytes': '42',
            }],
            json.loads(result.output))

    def test_volume_cancel(self):
        result = self.run_command([
            '--really', 'file', 'volume-cancel', '1234'])

        self.assert_no_fail(result)
        self.assertEqual('File volume with id 1234 has been marked'
                         ' for cancellation\n', result.output)
        self.assert_called_with('SoftLayer_Billing_Item', 'cancelItem',
                                args=(False, True, None))

    def test_volume_detail(self):
        result = self.run_command(['file', 'volume-detail', '1234'])

        self.assert_no_fail(result)
        self.assertEqual({'Username': 'username',
                          'Used Space': '0B',
                          'Endurance Tier': '2 IOPS per GB',
                          'IOPs': 1000,
                          'Snapshot Capacity (GB)': 10,
                          'Snapshot Used (Bytes)': 1024,
                          'Capacity (GB)': '20GB',
                          'Target IP': '10.1.2.3',
                          'Data Center': 'dal05',
                          'Type': 'ENDURANCE',
                          'ID': 100,
                          '# of Active Transactions': '0'
                          }, json.loads(result.output))

    @mock.patch('SoftLayer.FileStorageManager.order_file_volume')
    def test_volume_order(self, order_mock):
        order_mock.return_value = {
            'placedOrder': {
                'id': 478,
                'items': [{'description': 'Endurance Storage'},
                          {'description': 'File Storage'},
                          {'description': '0.25 IOPS per GB'},
                          {'description': '20 GB Storage Space'},
                          ]
                }
        }

        result = self.run_command(['file', 'volume-order',
                                   '--storage-type=endurance', '--size=20',
                                   '--tier=0.25', '--os-type=linux',
                                   '--location=dal05'])

        self.assert_no_fail(result)
        self.assertEqual(result.output,
                         'Order #478 placed successfully!\n'
                         ' > Endurance Storage\n > File Storage\n'
                         ' > 0.25 IOPS per GB\n > 20 GB Storage Space\n')

    def test_enable_snapshots(self):
        result = self.run_command(['file', 'snapshot-enable', '12345678',
                                   '--schedule-type=HOURLY', '--minute=10',
                                   '--retention-count=5'])

        self.assert_no_fail(result)

    def test_disable_snapshots(self):
        result = self.run_command(['file', 'snapshot-disable', '12345678',
                                   '--schedule-type=HOURLY'])
        self.assert_no_fail(result)

    def test_create_snapshot(self):
        result = self.run_command(['file', 'snapshot-create', '12345678'])

        self.assert_no_fail(result)
        self.assertEqual('New snapshot created with id: 449\n', result.output)

    def test_snapshot_restore(self):
        result = self.run_command(['file', 'snapshot-restore', '12345678',
                                   '--snapshot-id=87654321'])

        self.assert_no_fail(result)
        self.assertEqual(result.output, 'File volume 12345678 is being'
                         ' restored using snapshot 87654321\n')

    def test_delete_snapshot(self):
        result = self.run_command(['file', 'snapshot-delete', '12345678'])

        self.assert_no_fail(result)

    @mock.patch('SoftLayer.FileStorageManager.order_snapshot_space')
    def test_snapshot_order(self, order_mock):
        order_mock.return_value = {
            'placedOrder': {
                'id': 8702,
                'items': [{'description':
                           '10 GB Storage Space (Snapshot Space)'}],
                'status': 'PENDING_APPROVAL',
                }
        }

        result = self.run_command(['file', 'snapshot-order', '1234',
                                   '--capacity=10', '--tier=0.25'])

        self.assert_no_fail(result)
        self.assertEqual(result.output,
                         'Order #8702 placed successfully!\n'
                         ' > 10 GB Storage Space (Snapshot Space)\n'
                         ' > Order status: PENDING_APPROVAL\n')

    def test_snapshot_cancel(self):
        result = self.run_command(['--really',
                                   'file', 'snapshot-cancel', '1234'])

        self.assert_no_fail(result)
        self.assertEqual('File volume with id 1234 has been marked'
                         ' for snapshot cancellation\n', result.output)
        self.assert_called_with('SoftLayer_Billing_Item', 'cancelItem',
                                args=(False, True, None))
