import React, {useState} from 'react'
import { Card, Table, Select, Input, Button, Menu, message } from 'antd';
import studentsService from 'services/students'
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

const Students = () => {
	let history = useHistory();
	const [StudentsData, setStudentsData] = useState([]);

	React.useEffect(() => {
		const fetchStudents = async () => {
			try {
				const response = await studentsService.getAll();
				setStudentsData(response.data || []);
			} catch (error) {
				console.error('Error fetching students:', error);
				setStudentsData([]);
			}
		};
		fetchStudents();
	}, []);
	// console.log('ClassesData:', ClassesData);
	const [list, setList] = useState([]);

	React.useEffect(() => {
		setList(StudentsData);
	}, [StudentsData]);
	
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
			<Menu.Item onClick={() => editStudent(row)}>
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
	
	const addStudent = () => {
		history.push(`/app/apps/add-student`)
	}
	
	const editStudent = row => {
		history.push(`/app/apps/edit-student/${row.id}`)
	}

	const viewDetails = row => {
		history.push(`/app/apps/view-student/${row.id}`)
	}
	
	const deleteRow = async (row) => {
		try {
			const objKey = 'id';
			let data = [...list];
			
			if (selectedRows.length > 1) {
				for (const elm of selectedRows) {
					await studentsService.delete(elm.id);
					data = utils.deleteArrayRow(data, objKey, elm.id);
				}
				message.success('Student deleted successfully');
			} else if (row) {
				await studentsService.delete(row.id);
				data = utils.deleteArrayRow(data, objKey, row.id);
				message.success('Student deleted successfully');
			}
			
			setList(data);
			setSelectedRows([]);
			setSelectedRowKeys([]);
			history.push('/app/apps/students');
		} catch (error) {
			message.error('Error deleting student(s)');
			console.error("Error deleting student(es):", error);
		}
	}

	const handleCopy = row => {
		history.push(`/app/apps/copy-student/${row.id}`);
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
			title: 'Full Name',
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
			width: '100px',
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
			sorter: (a, b) => utils.antdTableSorter(a, b, 'class_id')
		},
		{
			title: 'Username',
			dataIndex: 'username',
			sorter: (a, b) => utils.antdTableSorter(a, b, 'username')
		},
		{
			title: '',
			dataIndex: 'actions',
			width: '80px',
			render: (_, elm) => (
				<div className="text-right">
					<EllipsisDropdown className="flex-start" menu={dropdownMenu(elm)}/>
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
		const searchArray = e.currentTarget.value? list : StudentsData
		const data = utils.wildCardSearch(searchArray, value)
		setList(data)
		setSelectedRowKeys([])
	}
	const handleExport = () => {
		console.log('exporting')
		history.push('/app/apps/export-student');
	}
	const handleImport = () => {
		console.log('importing')

		// Display file import dialog or redirect to import page
		// You don't need additional code here since you're already
		// navigating to the import page with history.push
		history.push('/app/apps/import-student');
	}
	const handleDelete = () => {
		console.log('deleting')
		deleteRow()
	}

	const handleMultipleCopy = async (row) => { 
		try {
			if (selectedRows.length > 1) {
				for (const elm of selectedRows) {
					await studentsService.copy(elm.id);
				}
				message.success('Students copied successfully');
				history.push('/app/apps/students');
			} else if (row) {
				await studentsService.copy(row.id);
				message.success('Students copied successfully');
			}
			setSelectedRows([]);
			setSelectedRowKeys([]);
		} catch (error) {
			message.error('Error copying student(s)');
			console.error("Error copying student(s):", error);
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
					<Button onClick={addStudent} type="primary" icon={<PlusCircleOutlined />} block>Add Student</Button>
				</div>
			</Flex>
			<div className="table-responsive">
				<Table 
					columns={tableColumns} 
					dataSource={list} 
					rowKey='id'
					size='middle'
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

export default Students;
