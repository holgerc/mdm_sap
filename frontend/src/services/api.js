import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Entities
export const getEntities = () => api.get('/entities')
export const getEntity = (id) => api.get(`/entities/${id}`)
export const createEntity = (data) => api.post('/entities', data)
export const updateEntity = (id, data) => api.put(`/entities/${id}`, data)
export const deleteEntity = (id) => api.delete(`/entities/${id}`)

// Attributes
export const getAttributes = (params) => api.get('/attributes', { params })
export const getAttribute = (id) => api.get(`/attributes/${id}`)
export const createAttribute = (data) => api.post('/attributes', data)
export const updateAttribute = (id, data) => api.put(`/attributes/${id}`, data)
export const deleteAttribute = (id) => api.delete(`/attributes/${id}`)

// Catalogs
export const getCatalogs = () => api.get('/catalogs')
export const getCatalog = (id) => api.get(`/catalogs/${id}`)
export const createCatalog = (data) => api.post('/catalogs', data)
export const updateCatalog = (id, data) => api.put(`/catalogs/${id}`, data)
export const deleteCatalog = (id) => api.delete(`/catalogs/${id}`)

// Catalog Values
export const getCatalogValues = (catalogId) => api.get(`/catalogs/${catalogId}/values`)
export const createCatalogValue = (data) => api.post('/catalogs/values', data)

// Health
export const getHealth = () => api.get('/health')

export default api
