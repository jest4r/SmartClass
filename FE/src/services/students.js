import service from 'auth/FetchInterceptor'

const studentsService = {}

studentsService.getByID = function (id) {
  return service.get(`/students/${id}`)
}

studentsService.getAll = function (params) {
  return service.get('/students', { params })
}

studentsService.delete = function (id) {
  return service.delete(`/students/${id}`)
}

studentsService.update = function (id, data) {
  return service.post(`/students/${id}`, data)
}

studentsService.create = function (data) {
  return service.post('/students', data)
}

studentsService.copy = function (id) {
  return service.post(`/students/${id}/copy`)
}

studentsService.import = function (file) {
  const formData = new FormData();
  formData.append('attachment', file);
  return service.post('/students/import', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

studentsService.exportAll = function (type) {
  if (type !== 'xlsx' && type !== 'csv') {
    throw new Error('File type must be either xlsx or csv');
  }

  return service.get(`/students/export?type=${type}`, {
    responseType: 'blob' // Ensure response is treated as a binary file
  });
};


studentsService.export = function (ids, type) {
  if (type !== 'xlsx' && type !== 'csv') {
    throw new Error('File type must be either xlsx or csv');
  }
  return service.post(`/students/export/${type}`, { ids });
}

export default studentsService
