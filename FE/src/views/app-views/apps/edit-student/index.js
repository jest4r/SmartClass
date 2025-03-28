import React from 'react'
import StudentForm from '../StudentForm';
import studentsService from 'services/students';

const EditStudent = props => {
	const handleSubmit = async (param, data) => {
		try {
			const response = await studentsService.update(param.id, data);
			console.log('Student updated successfully:', response);
		} catch (error) {
			console.error('Error updating student:', error);
		}
	}
	return (
		<StudentForm mode="EDIT" param={props.match.params} onSubmit={handleSubmit} />
	)
}

export default EditStudent
