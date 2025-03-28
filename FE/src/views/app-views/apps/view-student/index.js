import React from 'react'
import StudentForm from '../StudentForm';

const ViewStudent = props => {
	return (
		<StudentForm mode="VIEW" param={props.match.params}/>
	)
}

export default ViewStudent
