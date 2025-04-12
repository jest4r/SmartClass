import React, { useState, useEffect } from 'react'
import PageHeaderAlt from 'components/layout-components/PageHeaderAlt'
import { Tabs, Form, Button, message } from 'antd';
import Flex from 'components/shared-components/Flex'
import GeneralField from './GeneralField'
// import classListData from "assets/data/class-data.json"
import { useHistory } from 'react-router-dom'
import classesServicce from 'services/classes'
const { TabPane } = Tabs;

const getBase64 = (img, callback) => {
  const reader = new FileReader();
  reader.addEventListener('load', () => callback(reader.result));
  reader.readAsDataURL(img);
}

const ADD = 'ADD'
const EDIT = 'EDIT'
const VIEW = 'VIEW'
const COPY = 'COPY'

const ClassForm = props => {
	let history = useHistory();
	const { mode = ADD, param } = props

	const [form] = Form.useForm();
	const [uploadedImg, setImage] = useState('')
	const [uploadLoading, setUploadLoading] = useState(false)
	const [submitLoading, setSubmitLoading] = useState(false)

	useEffect(() => {
		const fetchClassById = async (id) => {
			try {
				const response = await classesServicce.getByID(id);
				return response.data;
			} catch (error) {
				console.error('Error fetching class by ID:', error);
				return null;
			}
		};

		if (mode === EDIT || mode === VIEW || mode === COPY) {
			const { id } = param;
			const classId = parseInt(id);
			fetchClassById(classId).then((classData) => {
				console.log('classData:', classData);
				if (classData) {
					form.setFieldsValue({
						description: classData.description,
						category: classData.category,
						name: classData.name,
						code: classData.code,
					});
					setImage(classData.image);

					if (mode === VIEW) {
						// Disable all form fields in view mode
						Object.keys(form.getFieldsValue()).forEach((key) => {
							const field = form.getFieldInstance(key);
							if (field) {
								field.disabled = true;
							}
						});
					}
				}
			});
		}
	}, [form, mode, param, props]);

	const handleUploadChange = info => {
		if (info.file.status === 'uploading') {
			setUploadLoading(true)
			return;
		}
		if (info.file.status === 'done') {
			getBase64(info.file.originFileObj, imageUrl =>{
				setImage(imageUrl)
				setUploadLoading(true)
			});
		}
	};
	
	const onDiscard = () => {
		history.push('/app/apps/class-list')
	}

	const onFinish = () => {
		setSubmitLoading(true)
		form.validateFields().then(values => {
			setTimeout(async () => {
				setSubmitLoading(false)
				if (mode === ADD) {
					try {
						props.onSubmit(values);
						message.success(`Created ${values.name} to class list`);
						history.push('/app/apps/class-list');
					} catch (error) {
						message.error('Error creating class');
					}
				}
				if (mode === EDIT) {
					try {
						props.onSubmit(param, values);
						message.success(`Class saved`);
						history.push('/app/apps/class-list');
					} catch (error) {
						message.error('Error updating class');
					}
				}
				if (mode === COPY) {
					try {
						props.onSubmit(param, values);
						message.success(`Created ${values.name} to class list`);
						history.push('/app/apps/class-list');
					} catch (error) {
						message.error('Error copying class');
					}
				}
			}, 1500);
		}).catch(info => {
			setSubmitLoading(false)
			console.log('info', info)
			message.error('Please enter all required field ');
		});
	};

	return (
		<>
			<Form
				layout="vertical"
				form={form}
				name="advanced_search"
				className="ant-advanced-search-form"
				initialValues={{
					heightUnit: 'cm',
					widthUnit: 'cm',
					weightUnit: 'kg'
				}}
			>
				<PageHeaderAlt className="border-bottom" overlap>
					<div className="container">
						<Flex className="py-2" mobileFlex={false} justifyContent="between" alignItems="center">
							<h2 className="mb-3">
								{mode === 'ADD' ? 'Add New class' : mode === 'VIEW' ? 'View class' : mode === 'COPY' ? 'Copy new class': 'Edit class'}
							</h2>
							<div className="mb-3">
								<Button className="mr-2" onClick={() => onDiscard()}>
									{mode === 'VIEW' ? 'Back' : 'Discard'}
								</Button>
								{mode !== 'VIEW' && (
									<Button type="primary" onClick={() => onFinish()} htmlType="submit" loading={submitLoading}>
										{mode === 'ADD' || mode === 'COPY' ? 'Add' : 'Save'}
									</Button> 
								)}
							</div>
						</Flex>
					</div>
				</PageHeaderAlt>
				<div className="container">
					<Tabs defaultActiveKey="1" style={{marginTop: 30}}>
						<TabPane tab="Class Information" key="1">
							<GeneralField 
								uploadedImg={uploadedImg} 
								uploadLoading={uploadLoading} 
								handleUploadChange={handleUploadChange}
								viewMode={mode === 'VIEW'}
							/>
						</TabPane>
						{/* <TabPane tab="Variation" key="2">
							<VariationField />
						</TabPane>
						<TabPane tab="Shipping" key="3">
							<ShippingField />
						</TabPane> */}
					</Tabs>
				</div>
			</Form>
		</>
	)
}

export default ClassForm
