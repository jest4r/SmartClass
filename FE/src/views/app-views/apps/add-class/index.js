import React from 'react';
import ClassForm from '../Form';
import classesService from 'services/classes';

const AddClass = () => {
	const handleSubmit = async (data) => {
		try {
			const response = await classesService.create(data);
			console.log('Class created successfully:', response);
		} catch (error) {
			console.error('Error creating class:', error);
		}
	};

	return (
		<ClassForm mode="ADD" onSubmit={handleSubmit} />
	);
};

export default AddClass;