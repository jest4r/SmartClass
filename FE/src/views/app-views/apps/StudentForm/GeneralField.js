import React from 'react'
import { Input, Row, Col, Card, Form, Upload, message, Select } from 'antd';
import { ImageSvg } from 'assets/svg/icon';
import CustomIcon from 'components/util-components/CustomIcon'
import { LoadingOutlined } from '@ant-design/icons';
import Password from 'antd/lib/input/Password';
import classesService from 'services/classes';

const { Dragger } = Upload;
const { Option } = Select;

const rules = {
	fullname: [
		{
			required: true,
			message: 'Please enter studen name',
		}
	],
	code: [
		{
			required: true,
			message: 'Please enter student code',
		}
	],
	sex: [		
		{
			required: true,
			message: 'Please enter gender',
		}
	],
	dob: [		
		{
			required: true,
			message: 'Please enter date of birth',
		}
	],
	homecity: [
		{
			required: false,
			message: 'Please enter home city',	
		}
	],
	address: [
		{
			required: false,
			message: 'Please enter address',
		}
	],
	phone: [
		{
			required: false,
			message: 'Please enter phone number',
		}
	],
	email: [
		{
			required: false,
			message: 'Please enter email',
		}
	],

	class_id: [
		{
			required: true,
			message: 'Please enter the class',
		}
	],
	username: [
		{
			required: true,
			message: 'Please enter the username',
		}
	],
	password: [
		{
			required: true,
			message: 'Please enter the password',
		}
	]
}

const imageUploadProps = {
  name: 'attachment',
	listType: "picture-card",
	showUploadList: false,
  action: 'https://www.mocky.io/v2/5cc8019d300000980a055e76'
}

const beforeUpload = file => {
  const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
  if (!isJpgOrPng) {
    message.error('You can only upload JPG/PNG file!');
  }
  const isLt2M = file.size / 1024 / 1024 < 2;
  if (!isLt2M) {
    message.error('Image must smaller than 2MB!');
  }
  return isJpgOrPng && isLt2M;
}


const GeneralField = props => {
	const [classes, setClasses] = React.useState([]);
	React.useEffect(() => {
		classesService.getAll().then(res => {
			setClasses(res.data.map(elm => elm.code))
		})
	}, [])
	return (
	<Row gutter={16}>
		<Col xs={24} sm={24} md={17}>
			<Card title="Basic Info">
				<Form.Item name="fullname" label="Student name" rules={rules.fullname}>
					<Input placeholder="Student Name" disabled={props.viewMode}/>
				</Form.Item>
				<Form.Item name="code" label="Student code" rules={rules.code}>
					<Input placeholder="Student Code" disabled={props.viewMode}/>	
				</Form.Item>
				<Form.Item name="sex" label="Gender" rules={rules.sex}>
					<Select placeholder="Select Gender" disabled={props.viewMode}> 
						<Option value="Male">Male</Option>
						<Option value="Female">Female</Option>
						<Option value="Other">Other</Option>
					</Select>
				</Form.Item>
				<Form.Item name="dob" label="Date of Birth" rules={rules.dob}>
					<Input type="date" placeholder="Date of Birth" disabled={props.viewMode}/>
				</Form.Item>
				<Form.Item name="homecity" label="Home City" rules={rules.homecity}>
					<Input placeholder="Home City" disabled={props.viewMode}/>
				</Form.Item>
			</Card>
			<Card title="Contact Info">
				<Row gutter={16}>
					<Col xs={24} sm={24} md={12}>
						<Form.Item name="address" label="Address" rules={rules.address}>
							<Input placeholder="Address" disabled={props.viewMode}/>
						</Form.Item>
					</Col>
					<Col xs={24} sm={24} md={12}>
						<Form.Item name="phone" label="Phone" rules={rules.phone}>
							<Input placeholder="Phone" disabled={props.viewMode}/>
						</Form.Item>
					</Col>
					<Col xs={24} sm={24} md={12}>
						<Form.Item name="email" label="Email" rules={rules.email}>
							<Input type='email' placeholder="Email" disabled={props.viewMode}/>
						</Form.Item>
					</Col>
					<Col xs={24} sm={24} md={12}>
						<Form.Item name="username" label="Username" rules={rules.username}>
							<Input placeholder="Username" disabled={props.viewMode}/>
						</Form.Item>
					</Col>
					<Col xs={24} sm={24} md={12}>
						<Form.Item name="password" label="Password" rules={rules.password}>
							<Password placeholder="Password" disabled={props.viewMode}/>
						</Form.Item>
					</Col>
				</Row>
			</Card>
		</Col>
		<Col xs={24} sm={24} md={7}>
			<Card title="Profile Picture">
				<Form.Item 
					name="attachment" 
					style={{ display: 'none' }}
				>
					<Input />
				</Form.Item>
				<Dragger {...imageUploadProps} beforeUpload={beforeUpload} onChange={e=> props.handleUploadChange(e)} disabled={props.viewMode}>
					{
						props.uploadedImg ? 
						<img src={props.uploadedImg} alt="avatar" className="img-fluid" /> 
						: 
						<div>
							{
								props.uploadLoading ? 
								<div>
									<LoadingOutlined className="font-size-xxl text-primary"/>
									<div className="mt-3">Uploading</div>
								</div> 
								: 
								<div>
									<CustomIcon className="display-3" svg={ImageSvg}/>
									<p>Click or drag file to upload</p>
								</div>
							}
						</div>
						
					}
				</Dragger>
			</Card>
			<Card title="Class">
				<Form.Item name="class_id" label="Class of this student" rules={rules.class_id}>
					<Select className="w-100" placeholder="Class code" disabled={props.viewMode}>
						{
							classes.map(elm => (
								<Option key={elm} value={elm}>{elm}</Option>
							))
						}
					</Select>
				</Form.Item>
			</Card>
		</Col>
	</Row>
)}

export default GeneralField
