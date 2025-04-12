import React, {useState} from 'react'
import { Card, Table, Select, Input, Button, Menu, message } from 'antd';
import classesService from 'services/classes'
import { EyeOutlined, DeleteOutlined, SearchOutlined, PlusCircleOutlined, EditOutlined, CopyOutlined } from '@ant-design/icons';
import AvatarStatus from 'components/shared-components/AvatarStatus';
import EllipsisDropdown from 'components/shared-components/EllipsisDropdown';
import Flex from 'components/shared-components/Flex'
import { useHistory } from "react-router-dom";
import utils from 'utils'
const { Option } = Select

// const getStockStatus = stockCount => {
// 	if(stockCount >= 10) {
// 		return <><Badge status="success" /><span>Active</span></>
// 	}
// 	if(stockCount < 10 && stockCount > 0) {
// 		return <><Badge status="warning" /><span>Warning</span></>
// 	}
// 	if(stockCount === 0) {
// 		return <><Badge status="error" /><span>Inactive</span></>
// 	}
// 	return null
// }

//const categories = ['Information Technology', 'Electronics Telecommunications', 'Mechanics Engineering', 'Physics Engineering', 'Civil Engineering']

const Classes = () => {
	let history = useHistory();
	const [ClassesData, setClassesData] = useState([]);

	React.useEffect(() => {
		const fetchClasses = async () => {
			try {
				const response = await classesService.getAll();
				setClassesData(response.data || []);
			} catch (error) {
				console.error('Error fetching classes:', error);
				setClassesData([]);
			}
		};
		fetchClasses();
	}, []);
	// console.log('ClassesData:', ClassesData);
	const [list, setList] = useState([]);

	React.useEffect(() => {
		setList(ClassesData);
	}, [ClassesData]);
	
	const [selectedRows, setSelectedRows] = useState([])
	const [selectedRowKeys, setSelectedRowKeys] = useState([])

	const dropdownMenu = row => (
		<Menu>
			<Menu.Item onClick={() => viewDetails(row)}>
				<Flex alignItems="center">
					<EyeOutlined />
					<span className="ml-2">View Details</span>
				</Flex>
			</Menu.Item>
			<Menu.Item onClick={() => editClass(row)}>
				<Flex alignItems="center">
					<EditOutlined />
					<span className="ml-2">Edit</span>
				</Flex>
			</Menu.Item>
			<Menu.Item onClick={() => deleteRow(row)}>
				<Flex alignItems="center">
					<DeleteOutlined />
					<span className="ml-2">{selectedRows.length > 0 ? `Delete (${selectedRows.length})` : 'Delete'}</span>
				</Flex>
			</Menu.Item>
			<Menu.Item onClick={() => handleCopy(row)}>
				<Flex alignItems="center">
					<CopyOutlined />
					<span className="ml-2">Copy</span>
				</Flex>
			</Menu.Item>
		</Menu>
	);
	
	const addClass = () => {
		history.push(`/app/apps/add-class`)
	}
	
	const editClass = row => {
		history.push(`/app/apps/edit-class/${row.id}`)
	}

	const viewDetails = row => {
		history.push(`/app/apps/view-class/${row.id}`)
	}
	
	
	const deleteRow = async (row) => {
		try {
			const objKey = 'id';
			let data = [...list];
			
			if (selectedRows.length > 1) {
				for (const elm of selectedRows) {
					await classesService.delete(elm.id);
					data = utils.deleteArrayRow(data, objKey, elm.id);
				}
				message.success('Classes deleted successfully');
			} else if (row) {
				await classesService.delete(row.id);
				data = utils.deleteArrayRow(data, objKey, row.id);
				message.success('Class deleted successfully');
			}
			
			setList(data);
			setSelectedRows([]);
			setSelectedRowKeys([]);
			history.push('/app/apps/classes');
		} catch (error) {
			message.error('Error deleting class(es)');
			console.error("Error deleting class(es):", error);
		}
	}

	const handleCopy = row => {
		history.push(`/app/apps/copy-class/${row.id}`);
	}

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
		{
			title: '',
			dataIndex: 'actions',
			render: (_, elm) => (
				<div className="text-right">
					<EllipsisDropdown menu={dropdownMenu(elm)}/>
				</div>
			)
		}
	];
	
	const rowSelection = {
		onChange: (key, rows) => {
			setSelectedRows(rows)
			setSelectedRowKeys(key)
		}
	};

	const onSearch = e => {
		const value = e.currentTarget.value
		const searchArray = e.currentTarget.value? list : ClassesData
		const data = utils.wildCardSearch(searchArray, value)
		setList(data)
		setSelectedRowKeys([])
	}
	const handleExport = () => {
		console.log('exporting')
		history.push('/app/apps/export-class');
	}
	const handleImport = () => {
		console.log('importing')

		// Display file import dialog or redirect to import page
		// You don't need additional code here since you're already
		// navigating to the import page with history.push
		history.push('/app/apps/import-class');
	}
	const handleDelete = () => {
		console.log('deleting')
		deleteRow()
	}

	const handleMultipleCopy = async (row) => { 
		try {
			if (selectedRows.length > 1) {
				for (const elm of selectedRows) {
					await classesService.copy(elm.id);
				}
				message.success('Classes copied successfully');
				history.push('/app/apps/classes');
			} else if (row) {
				await classesService.copy(row.id);
				message.success('Class copied successfully');
			}
			setSelectedRows([]);
			setSelectedRowKeys([]);
		} catch (error) {
			message.error('Error copying class(es)');
			console.error("Error copying class(es):", error);
		}
	}
	

	return (
		<Card>	
			<Flex alignItems="center" justifyContent="between" mobileFlex={false}>
				<Flex className="mb-1" mobileFlex={false}>
					<div className="mr-md-3 mb-3">
						<Input placeholder="Search" prefix={<SearchOutlined />} onChange={e => onSearch(e)}/>
					</div>
					<div className="mb-3">
						<Select
							defaultValue="Action" 
							className="w-100" 
							style={{ minWidth: 180 }} 
							placeholder="Action"
							onChange={(value) => {
								if (value === 'Export') handleExport();
								if (value === 'Import') handleImport();
								if (value === 'Delete') handleDelete();
								if (value === 'Copy') handleMultipleCopy();
							}}
						>
							<Option value="Export">Export data</Option>
							<Option value="Import">Import data</Option>
							<Option value="Delete">Delete data</Option>
							<Option value="Copy">Copy data</Option>
							
						</Select>
					</div>
				</Flex>
				<div>
					<Button onClick={addClass} type="primary" icon={<PlusCircleOutlined />} block>Add Class</Button>
				</div>
			</Flex>
			<div className="table-responsive">
				<Table 
					columns={tableColumns} 
					dataSource={list} 
					rowKey='id'
					pagination={{
						showSizeChanger: true,
						showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} items`
					}}
					rowSelection={{
						selectedRowKeys: selectedRowKeys,
						type: 'checkbox',
						preserveSelectedRowKeys: false,
						...rowSelection,
					}}
				/>
			</div>
		</Card>
	)
}

export default Classes;
