import React from 'react'
import Form from '../Form';
import classesService from 'services/classes';

const EditClass = props => {
	const handleSubmit = async (param, data) => {
		try {
			const response = await classesService.update(param.id, data);
			console.log('Class updated successfully:', response);
		} catch (error) {
			console.error('Error updating class:', error);
		}
	}
	return (
		<Form mode="EDIT" param={props.match.params} onSubmit={handleSubmit} />
	)
}

export default EditClass
