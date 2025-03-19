import React from 'react'
import { Input, Row, Col, Card, Form, Upload, message, Select } from 'antd';
import { ImageSvg } from 'assets/svg/icon';
import CustomIcon from 'components/util-components/CustomIcon'
import { LoadingOutlined } from '@ant-design/icons';

const { Dragger } = Upload;
const { Option } = Select;

const rules = {
	name: [
		{
			required: true,
			message: 'Please enter class name',
		}
	],
	description: [
		{
			required: true,
			message: 'Please enter class description',
		}
	],
	code: [
		{
			required: true,
			message: 'Please enter class code',
		}
	],
}

const imageUploadProps = {
  name: 'file',
	multiple: true,
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

const categories = ['Information Technology', 'Electronics Telecommunications', 'Mechanics Engineering', 'Physics Engineering', 'Civil Engineering']
const tags = ['FIT', 'FET', 'FEMA', 'FCE', 'FAE', 'FPE', 'IAI' ]

const GeneralField = props => (
			<Card title="Basic Info" width="100%">
				<Form.Item name="name" label="Class name" rules={rules.name}>
					<Input placeholder="Class Name" disabled={props.viewMode} />
				</Form.Item>
				<Form.Item name="code" label="Class code" rules={rules.code}>
					<Input placeholder="Class Code" disabled={props.viewMode} />
				</Form.Item>
				<Form.Item name="description" label="Description" rules={rules.description}>
					<Input.TextArea rows={4} disabled={props.viewMode} />
				</Form.Item>
			</Card>
)

export default GeneralField
