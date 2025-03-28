import service from 'auth/FetchInterceptor'

const classesService = {}

classesService.getByID = function (id) {
  return service.get(`/classes/${id}`)
}

classesService.getAll = function (params) {
  return service.get('/classes', { params })
}

classesService.delete = function (id) {
  return service.delete(`/classes/${id}`)
}

classesService.update = function (id, data) {
  return service.post(`/classes/${id}`, data)
}

classesService.create = function (data) {
  return service.post('/classes', data)
}

classesService.copy = function (id) {
  return service.post(`/classes/${id}/copy`)
}

classesService.import = function (file) {
  const formData = new FormData();
  formData.append('attachment', file);
  return service.post('/classes/import', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

classesService.exportAll = function (type) {
  if (type !== 'xlsx' && type !== 'csv') {
    throw new Error('File type must be either xlsx or csv');
  }

  return service.get(`/classes/export?type=${type}`, {
    responseType: 'blob' // Ensure response is treated as a binary file
  });
};


classesService.export = function (ids, type) {
  if (type !== 'xlsx' && type !== 'csv') {
    throw new Error('File type must be either xlsx or csv');
  }
  return service.post(`/classes/export/${type}`, { ids });
}

export default classesService
