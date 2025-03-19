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

classesService.copy = function (id, data) {
  return service.post(`/classes/${id}/copy`, data)
}

export default classesService
