import React from 'react'
import Form from '../Form';

const ViewClass = props => {
	return (
		<Form mode="VIEW" param={props.match.params}/>
	)
}

export default ViewClass
