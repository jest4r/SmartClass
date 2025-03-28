import React, { useState, useEffect } from 'react'
import PageHeaderAlt from 'components/layout-components/PageHeaderAlt'
import { Tabs, Form, Button, message } from 'antd';
import Flex from 'components/shared-components/Flex'
import GeneralField from './GeneralField'
// import classListData from "assets/data/class-data.json"
import { useHistory } from 'react-router-dom'
import studentsService from 'services/students'
import classesService from 'services/classes';

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

const StudentForm = props => {
	let history = useHistory();
	const { mode = ADD, param } = props

	const [form] = Form.useForm();
	const [uploadedImg, setImage] = useState('')
	const [uploadLoading, setUploadLoading] = useState(false)
	const [submitLoading, setSubmitLoading] = useState(false)
	const [allClasses, setAllClasses] = useState([])

	useEffect(() => {
		const fetchStudentById = async (id) => {
			try {
				const response = await studentsService.getByID(id);
				return response.data;
			} catch (error) {
				console.error('Error fetching student by ID:', error);
				return null;
			}
		};


		if (mode === EDIT || mode === VIEW || mode === COPY) {
			const { id } = param;
			const studentId = parseInt(id);
			fetchStudentById(studentId).then((studentData) => {
				console.log('studentData:', studentData);
				if (studentData) {
					form.setFieldsValue({
						fullname: studentData.fullname,
						code: studentData.code,
						sex: studentData.sex,
						dob: studentData.dob,
						homecity: studentData.homecity,
						address: studentData.address,
						phone: studentData.phone,
						email: studentData.email,
						class_id: studentData.class_id,
						username: studentData.username,
						password: studentData.password,
						attachment: studentData.attachment
					});
					setImage(studentData.attachment);

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

	useEffect(() => {
        const fetchClasses = async () => {
            try {
                const response = await classesService.getAll();
                if (response && response.data) {
                    setAllClasses(response.data);
                }
            } catch (error) {
                console.error('Error fetching classes:', error);
            }
        };
        
        fetchClasses();
    }, []);

	const handleUploadChange = info => {
		if (info.file.status === 'uploading') {
			setUploadLoading(true)
			return;
		}
		if (info.file.originFileObj) {
            setUploadLoading(true);
            
            getBase64(info.file.originFileObj, imageUrl => {
                setImage(imageUrl);
				form.setFieldsValue({
                    attachment: imageUrl
                });
                
                setUploadLoading(false);
                
                // Manually update file status to done
                info.file.status = 'done';
                
                // Optionally notify success
                message.success(`${info.file.name} uploaded successfully`);
            });
        }
	};
	
	const onDiscard = () => {
		history.push('/app/apps/students')
	}

	const onFinish = () => {
		setSubmitLoading(true)
		form.validateFields().then(values => {
            if (values.class_id) {
                console.log('Original class_id value:', values.class_id);
                
                if (!isNaN(parseInt(values.class_id, 10))) {
                    values.class_id = parseInt(values.class_id, 10);
                }
                else {
                    const classObj = allClasses.find(c => c.code === values.class_id);
                    if (classObj) {
                        console.log(`Mapped class code ${values.class_id} to ID ${classObj.id}`);
                        values.class_id = classObj.id;
                    } else {
                        console.warn(`Could not find class with code ${values.class_id}`);
                    }
                }
            }
			if (!values.attachment && uploadedImg) {
                values.attachment = uploadedImg;
            }
			setTimeout(async () => {
				setSubmitLoading(false)
				if (mode === ADD) {
					try {
						props.onSubmit(values);
						message.success(`Created ${values.name} to student list`);
						history.push('/app/apps/students');
					} catch (error) {
						message.error('Error creating student');
					}
				}
				if (mode === EDIT) {
					try {
						props.onSubmit(param, values);
						message.success(`Student saved`);
						history.push('/app/apps/students');
					} catch (error) {
						message.error('Error updating student');
					}
				}
				if (mode === COPY) {
					try {
						props.onSubmit(param, values);
						message.success(`Created ${values.name} to student list`);
						history.push('/app/apps/students');
					} catch (error) {
						message.error('Error copying student');
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
								{mode === 'ADD' ? 'Add New Student' : mode === 'VIEW' ? 'View student info' : mode === 'COPY' ? 'Copy new student': 'Edit student'}
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
						<TabPane tab="Student Information" key="1">
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

export default StudentForm
