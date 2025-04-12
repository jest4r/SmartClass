import React, { lazy, Suspense } from "react";
import { Redirect, Route, Switch } from 'react-router-dom';
import Loading from 'components/shared-components/Loading';

const Apps = ({ match }) => (
  <Suspense fallback={<Loading cover="content"/>}>
    <Switch>
      <Route path={`${match.url}/classes`} component={lazy(() => import(`./classes`))} />
      <Route path={`${match.url}/students`} component={lazy(() => import(`./students`))} />
      <Route path={`${match.url}/add-class`} component={lazy(() => import(`./add-class`))} />
			<Route path={`${match.url}/edit-class/:id`} component={lazy(() => import(`./edit-class`))} />
      <Route path={`${match.url}/view-class/:id`} component={lazy(() => import(`./view-class`))} />
      <Route path={`${match.url}/copy-class/:id`} component={lazy(() => import(`./copy-class`))} />
      <Route path={`${match.url}/import-class`} component={lazy(() => import(`./import-class`))} />
      <Route path={`${match.url}/export-class`} component={lazy(() => import(`./export-class`))} />
      <Route path={`${match.url}/add-student`} component={lazy(() => import(`./add-student`))} />
      <Route path={`${match.url}/edit-student/:id`} component={lazy(() => import(`./edit-student`))} />
      <Route path={`${match.url}/view-student/:id`} component={lazy(() => import(`./view-student`))} />
      <Route path={`${match.url}/copy-student/:id`} component={lazy(() => import(`./copy-student`))} />
      <Route path={`${match.url}/import-student`} component={lazy(() => import(`./import-student`))} />
      <Route path={`${match.url}/export-student`} component={lazy(() => import(`./export-student`))}    />
      <Redirect from={`${match.url}`} to={`${match.url}/classes`} />
    </Switch>
  </Suspense>
);

export default Apps;