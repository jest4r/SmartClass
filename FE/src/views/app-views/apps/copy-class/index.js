import React from 'react';
import Form from '../Form';
import classesService from 'services/classes';

const CopyClass = props => {
    const handleSubmit = async (param, data) => {
            try {
                const { id } = param;
                console.log(id);
                const response = await classesService.create(data);
                console.log('Class created successfully:', response);
            } catch (error) {
                console.error('Error copying class:', error);
            }
        }
    return (
        <Form mode="COPY" param={props.match.params} onSubmit={handleSubmit}/>
    )
}

export default CopyClass