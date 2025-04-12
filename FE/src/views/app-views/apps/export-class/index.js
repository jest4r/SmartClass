import React, {useState, useEffect} from 'react'
import { Card, Table, message, Select, Button } from 'antd';
import classesService from 'services/classes'
import AvatarStatus from 'components/shared-components/AvatarStatus';
import Flex from 'components/shared-components/Flex'
import utils from 'utils'
const { Option } = Select

const ExportClass = () => {
    // State variables remain unchanged
    const [classesData, setClassesData] = useState([]);
    const [list, setList] = useState([]);
    const [loading, setLoading] = useState(false);
    const [fileType, setFileType] = useState('xlsx');
    const [selectedRows, setSelectedRows] = useState([]);
    const [selectedRowKeys, setSelectedRowKeys] = useState([]);

    // Initial data loading
    useEffect(() => {
        const fetchClasses = async () => {
            try {
                setLoading(true);
                const response = await classesService.getAll();
                setClassesData(response.data || []);
            } catch (error) {
                console.error('Error fetching classes:', error);
                message.error('Failed to load classes');
                setClassesData([]);
            } finally {
                setLoading(false);
            }
        };
        fetchClasses();
    }, []);
    
    useEffect(() => {
        setList(classesData);
    }, [classesData]);

    // Updated handleExport function with correct parameter order
    const handleExport = () => {
        if (!fileType) {
            message.error('Please select a file type');
            return;
        }

        // Determine what data to export (selected rows or all)
        const dataToExport = selectedRows.length > 0 ? selectedRows : list;
        
        if (dataToExport.length === 0) {
            message.warning('No data to export');
            return;
        } 

        // Check if we're exporting selected rows or all data
        if (selectedRows.length === 0) {
            // Use exportAll service when exporting all data
            const exportAllClasses = async () => {
                try {
                    setLoading(true);
                    const result = await classesService.exportAll(fileType);
                    console.log('Exported all classes:', result);
                    if (result) {
                        message.success(`All classes exported successfully as ${fileType.toUpperCase()}`);
                        
                        // Handle download the same way as in the regular export
                        if (result.url) {
                            window.open(result.url, '_blank');
                        } else {
                            const mimeType = fileType === 'xlsx' 
                                ? 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
                                : 'text/csv';
                            
                            let blob;
                            
                            if (result instanceof Blob) {
                                blob = result;
                            } else if (result.data) {
                                blob = new Blob([result.data], { type: mimeType });
                            } else {
                                blob = new Blob([result], { type: mimeType });
                            }
                            
                            const url = window.URL.createObjectURL(blob);
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = `all_classes_export_${new Date().toISOString().split('T')[0]}.${fileType}`;
                            document.body.appendChild(a);
                            a.click();
                            window.URL.revokeObjectURL(url);
                            a.remove();
                        }
                    }
                } catch (error) {
                    console.error('Error exporting all classes:', error);
                    message.error(`Failed to export all classes: ${error.message || 'Unknown error'}`);
                } finally {
                    setLoading(false);
                }
            };
            
            exportAllClasses();
            return; // Exit the function early after starting the exportAll process
        }

        setLoading(true);
        
        const exportClasses = async () => {
            try {
            // Build params object with IDs to export
            const params = {
                ids: dataToExport.map(item => item.id)
            };
            
            console.log(`Exporting with file type: ${fileType}, params:`, params);
            
            // Call the export service with proper URL encoding
            const ids = params.ids.join(',');
            
            // Create a properly encoded URL using URLSearchParams
            const queryParams = new URLSearchParams();
            queryParams.append('ids', ids);
            queryParams.append('type', fileType);
            
            const downloadUrl = `${process.env.REACT_APP_API_BASE_URL || ''}/api/classes/export?${queryParams.toString()}`;
            
            // Open the URL in a new tab to initiate download
            window.open(downloadUrl, '_blank');
            message.success(`Classes exported successfully as ${fileType.toUpperCase()}`);
            
            // Skip the rest of the function since we're handling the download directly
            setLoading(false);
            return;
            } catch (error) {
            console.error('Error exporting classes:', error);
            message.error(`Failed to export classes: ${error.message || 'Unknown error'}`);
            } finally {
            setLoading(false);
            }
        };
        
        // Execute the export function
        exportClasses();
    };

    // Table columns definition - unchanged
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

    // Row selection configuration - unchanged
    const rowSelection = {
        onChange: (keys, rows) => {
            setSelectedRowKeys(keys);
            setSelectedRows(rows);
        }
    };

    // Render component - unchanged except for button margin fix
    return (
        <>
            <div className="mb-3">
                <Card>
                    <Flex alignItems="center" justifyContent="space-between">
                        <h3 className="mb-0 mr-5">Export Classes</h3>
                        <Flex justifyContent='flex-start'>   
                            <Select 
                                defaultValue="xlsx"
                                style={{ width: 200 }}
                                value={fileType}
                                onChange={(value) => {
                                    setFileType(value);
                                }}
                                placeholder="Select file type"
                            >
                                <Option value="xlsx">Excel (.xlsx)</Option>
                                <Option value="csv">CSV (.csv)</Option>
                            </Select>
                            <Button 
                                onClick={handleExport}
                                type="primary" 
                                loading={loading}
                                style={{ marginLeft: 16 }}
                                disabled={list.length === 0}
                            >
                                {selectedRows.length > 0 
                                    ? `Export Selected (${selectedRows.length})` 
                                    : 'Export All'}
                            </Button>
                        </Flex>
                    </Flex>
                </Card>
            </div>
            <Card>	
                <div className="table-responsive">
                    <Table 
                        columns={tableColumns} 
                        dataSource={Array.isArray(list) ? list : []} 
                        rowKey='id' 
                        loading={loading}
                        rowSelection={{
                            selectedRowKeys,
                            type: 'checkbox',
                            ...rowSelection
                        }}
                    />
                </div>
            </Card>
        </>
    )
}

export default ExportClass;