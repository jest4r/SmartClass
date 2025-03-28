import React from 'react';
import StudentForm from '../StudentForm';
import studentsService from 'services/students';

const CopyStudent = props => {
    const handleSubmit = async (param, data) => {
            try {
                const { id } = param;
                console.log(id);
                const response = await studentsService.create(data);
                console.log('Student created successfully:', response);
            } catch (error) {
                console.error('Error copying student:', error);
            }
        }
    return (
        <StudentForm mode="COPY" param={props.match.params} onSubmit={handleSubmit}/>
    )
}

export default CopyStudent