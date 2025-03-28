import React from 'react';
import StudentForm from '../StudentForm';
import studentsService from 'services/students';

const AddStudent = () => {
	const handleSubmit = async (data) => {
		try {
			const response = await studentsService.create(data);
			console.log('Student created successfully:', response);
		} catch (error) {
			console.error('Error creating student:', error);
		}
	};

	return (
		<StudentForm mode="ADD" onSubmit={handleSubmit} />
	);
};

export default AddStudent;