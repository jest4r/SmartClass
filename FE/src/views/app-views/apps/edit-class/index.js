import React from 'react'
import Form from '../Form';

const EditClass = props => {
	return (
		<Form mode="EDIT" param={props.match.params}/>
	)
}

export default EditClass
