getObject = {
    'accountId': 1234,
    'billingItem': {
        'id': 449,
        'categoryCode': 'storage_service_enterprise',
        'activeChildren': [{
            'categoryCode': 'storage_snapshot_space',
            'id': 123
        }]
    },
    'capacityGb': 20,
    'createDate': '2015:50:15-04:00',
    'guestId': '',
    'hardwareId': '',
    'hostId': '',
    'id': 100,
    'nasType': 'ISCSI',
    'notes': """{'status': 'available'}""",
    'password': '',
    'serviceProviderId': 1,
    'iops': 1000,
    'storageTierLevel': {'description': '2 IOPS per GB'},
    'snapshotCapacityGb': 10,
    'parentVolume': {'snapshotSizeBytes': 1024},
    'serviceResource': {'datacenter': {'id': 449500, 'name': 'dal05'}},
    'serviceResourceBackendIpAddress': '10.1.2.3',
    'serviceResourceName': 'Storage Type 01 Aggregate staaspar0101_pc01',
    'username': 'username',
    'storageType': {'keyName': 'ENDURANCE_STORAGE'},
    'bytesUsed': 0,
    'activeTransactions': None,
    'activeTransactionCount': 0,
    'allowedVirtualGuests': [{
        'id': 1234,
        'hostname': 'test-server',
        'domain': 'example.com',
        'primaryBackendIpAddress': '10.0.0.1',
        'allowedHost': {
            'name': 'test-server',
            'credential': {'username': 'joe', 'password': '12345'},
        },
    }],
    'lunId': 2,
    'allowedHardware': [{
        'id': 1234,
        'hostname': 'test-server',
        'domain': 'example.com',
        'primaryBackendIpAddress': '10.0.0.2',
        'allowedHost': {
            'name': 'test-server',
            'credential': {'username': 'joe', 'password': '12345'},
        },
    }],
    'allowedSubnets': [{
        'id': 1234,
        'networkIdentifier': '10.0.0.1',
        'cidr': '24',
        'note': 'backend subnet',
        'allowedHost': {
            'name': 'test-server',
            'credential': {'username': 'joe', 'password': '12345'},
        },
    }],
    'allowedIpAddresses': [{
        'id': 1234,
        'ipAddress': '10.0.0.1',
        'note': 'backend ip',
        'allowedHost': {
            'name': 'test-server',
            'credential': {'username': 'joe', 'password': '12345'},
        },
    }],
}

getSnapshots = [{
    'id': 470,
    'notes': 'unit_testing_note',
    'snapshotCreationTimestamp': '2016-07-06T07:41:19-05:00',
    'snapshotSizeBytes': '42',
}]

deleteObject = True
allowAccessFromHostList = True
removeAccessFromHostList = True

restoreFromSnapshot = True

createSnapshot = {
    'id': 449
}

enableSnapshots = True
disableSnapshots = True
