import React, {useState} from 'react'
import { Card, Table, message, Select, Upload, Button } from 'antd';
import studentsService from 'services/students'  // Fixed typo in import name
import AvatarStatus from 'components/shared-components/AvatarStatus';
import Flex from 'components/shared-components/Flex'
import utils from 'utils'
const { Option } = Select

const ImportStudent = () => {
    const [studentsData, setStudentsData] = useState([]);
    const [loading, setLoading] = useState(false);

    // Fixed handleImport function - it was being called immediately
    const handleImport = () => {
        if (fileList.length === 0) {
            message.error('Please select a file first');
            return;
        }

        if (!fileType) {
            message.error('Please select a file type');
            return;
        }

        setLoading(true);
        const file = fileList[0]?.originFileObj;
        
        if (!file) {
            message.error('Invalid file');
            setLoading(false);
            return;
        }

        const importStudents = async () => {
            try {
                const result = await studentsService.import(file);
                if (result && result.data) {
                    console.log('Imported students:', result.data);
                    setStudentsData(result.data.created);
                    message.success(`Students imported successfully`);
                    console.log(studentsData);
                }
            } catch (error) {
                console.error('Error importing Students:', error);
                message.error('Failed to import students. Please check the file format.');
            } finally {
                setLoading(false);
            }
        };
        
        importStudents();
    };

    const [list, setList] = useState([]);

    React.useEffect(() => {
        setList(studentsData);
    }, [studentsData]);

    const tableColumns = [
		{
			title: 'ID',
			dataIndex: 'id',
			render: (_, record, index) => {
				return index + 1;
			},
			sorter: (a, b) => a.id - b.id
		},
		{
			title: 'Student Name',
			dataIndex: 'fullname',
			render: (_, record) => (
				<div className="d-flex">
					<AvatarStatus size={60} type="square" src={record.attachment} name={record.fullname}/>
				</div>
			),
			sorter: (a, b) => utils.antdTableSorter(a, b, 'name')
		},
		{
			title: 'Student Code',
			dataIndex: 'code',
			sorter: (a, b) => utils.antdTableSorter(a, b, 'code')
		},
		{
			title: 'Gender',
			dataIndex: 'sex',
			sorter: (a, b) => utils.antdTableSorter(a, b, 'sex'	)
		},
		{
			title: 'Date of Birth',
			dataIndex: 'dob',
			sorter: (a, b) => utils.antdTableSorter(a, b, 'dob')
		},
		{
			title: 'Home City',
			dataIndex: 'homecity',
			sorter: (a, b) => utils.antdTableSorter(a, b, 'homecity')	
		},
		{
			title: 'Address',
			dataIndex: 'address',
			sorter: (a, b) => utils.antdTableSorter(a, b, 'address')
		},
		{
			title: 'Phone',
			dataIndex: 'phone',
			sorter: (a, b) => utils.antdTableSorter(a, b, 'phone')
		},
		{
			title: 'Email',
			dataIndex: 'email',
			sorter: (a, b) => utils.antdTableSorter(a, b, 'email')
		},
		{
			title: 'Class',
			dataIndex: 'class_id',
			sorter: (a, b) => utils.antdTableSorter(a, b, 'classid')
		},
		{
			title: 'Username',
			dataIndex: 'username',
			sorter: (a, b) => utils.antdTableSorter(a, b, 'username')
		}
	];


    const [fileType, setFileType] = useState('xlsx');
    const [fileList, setFileList] = useState([]);

    return (
        <>
            <div className="mb-3">
                <Card>
                    <Flex alignItems="center" justifyContent="space-between">
                        <h3 className="mb-0 mr-5">Import Students</h3>
                        <Flex justifyContent='flex-start'>
                            <Upload
                                accept=".xlsx,.csv,.json"
                                showUploadList={true}
                                beforeUpload={(file) => {
                                    message.info(`File selected. Please click Import to proceed.`);
                                    return false;
                                }}
                                fileList={fileList}
                                onChange={({ file, fileList }) => {
                                    setFileList(fileList);
                                }}
                            >
                                <Button type="primary" style={{ marginRight: 16 }}>Select File</Button>
                            </Upload>   
                            <Select 
                                defaultValue="xlsx"
                                style={{ width: 200, marginLeft: 16 }}
                                onChange={(value) => {
                                    setFileType(value);
                                }}
                                placeholder="Select file type"
                            >
                                <Option value="xlsx">Excel (.xlsx)</Option>
                                <Option value="csv">CSV (.csv)</Option>
                                <Option value="json">JSON (.json)</Option>
                            </Select>
                            <Button 
                                onClick={handleImport} 
                                type="primary" 
                                loading={loading}
                                style={{ marginLeft: 500 }}
                            >
                                Import
                            </Button>
                        </Flex>
                    </Flex>
                </Card>
            </div>
            <Card>	
                <div className="table-responsive">
                    <Table 
                        columns={tableColumns} 
                        dataSource={list} 
                        rowKey='id' 
                        loading={loading}
                    />
                </div>
            </Card>
        </>
    )
}
export default ImportStudent;