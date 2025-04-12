import React, {useState} from 'react'
import { Card, Table, message, Select, Upload, Button } from 'antd';
import classesService from 'services/classes'  // Fixed typo in import name
import AvatarStatus from 'components/shared-components/AvatarStatus';
import Flex from 'components/shared-components/Flex'
import utils from 'utils'
const { Option } = Select

const ImportClass = () => {
    const [classesData, setClassesData] = useState([]);
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

        const importClasses = async () => {
            try {
                const result = await classesService.import(file);
                if (result && result.data) {
                    console.log('Imported classes:', result.data);
                    setClassesData(result.data.created);
                    message.success(`Classes imported successfully`);
                    console.log(classesData);
                }
            } catch (error) {
                console.error('Error importing classes:', error);
                message.error('Failed to import classes. Please check the file format.');
            } finally {
                setLoading(false);
            }
        };
        
        importClasses();
    };

    const [list, setList] = useState([]);

    React.useEffect(() => {
        setList(classesData);
    }, [classesData]);

    const tableColumns = [
        {
            title: 'ID',
            dataIndex: 'id'
        },
        {
            title: 'Class Name',
            dataIndex: 'name',
            render: (_, record) => (
                <div className="d-flex">
                    <AvatarStatus size={60} type="square" src={'/img/thumbs/book.webp'} name={record.name}/>
                </div>
            ),
            sorter: (a, b) => utils.antdTableSorter(a, b, 'name')
        },
        {
            title: 'Code',
            dataIndex: 'code',
            sorter: (a, b) => utils.antdTableSorter(a, b, 'code')
        },
        {
            title: 'Description',
            dataIndex: 'description',
            sorter: (a, b) => utils.antdTableSorter(a, b, 'description')
        },
    ];


    const [fileType, setFileType] = useState('xlsx');
    const [fileList, setFileList] = useState([]);

    return (
        <>
            <div className="mb-3">
                <Card>
                    <Flex alignItems="center" justifyContent="space-between">
                        <h3 className="mb-0 mr-5">Import Classes</h3>
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
export default ImportClass;