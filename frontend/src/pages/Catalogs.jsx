import { useState, useEffect } from 'react'
import { Plus, Pencil, Trash2, X, ChevronRight } from 'lucide-react'
import { getCatalogs, createCatalog, updateCatalog, deleteCatalog, getCatalogValues } from '../services/api'

export default function Catalogs() {
  const [catalogs, setCatalogs] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [editingCatalog, setEditingCatalog] = useState(null)
  const [selectedCatalog, setSelectedCatalog] = useState(null)
  const [catalogValues, setCatalogValues] = useState([])
  const [formData, setFormData] = useState({
    catalog_code: '',
    catalog_name: '',
    catalog_type: 'SIMPLE',
    allow_user_values: false,
    cache_enabled: true
  })

  useEffect(() => {
    fetchCatalogs()
  }, [])

  const fetchCatalogs = async () => {
    try {
      const response = await getCatalogs()
      setCatalogs(response.data || [])
    } catch (error) {
      console.error('Error fetching catalogs:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchCatalogValues = async (catalogId) => {
    try {
      const response = await getCatalogValues(catalogId)
      setCatalogValues(response.data || [])
    } catch (error) {
      console.error('Error fetching catalog values:', error)
      setCatalogValues([])
    }
  }

  const handleSelectCatalog = (catalog) => {
    setSelectedCatalog(catalog)
    fetchCatalogValues(catalog.id)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editingCatalog) {
        await updateCatalog(editingCatalog.id, formData)
      } else {
        await createCatalog(formData)
      }
      fetchCatalogs()
      closeModal()
    } catch (error) {
      console.error('Error saving catalog:', error)
      alert('Error saving catalog: ' + (error.response?.data?.detail || error.message))
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this catalog?')) return
    try {
      await deleteCatalog(id)
      if (selectedCatalog?.id === id) {
        setSelectedCatalog(null)
        setCatalogValues([])
      }
      fetchCatalogs()
    } catch (error) {
      console.error('Error deleting catalog:', error)
    }
  }

  const openModal = (catalog = null) => {
    if (catalog) {
      setEditingCatalog(catalog)
      setFormData({
        catalog_code: catalog.catalog_code,
        catalog_name: catalog.catalog_name,
        catalog_type: catalog.catalog_type,
        allow_user_values: catalog.allow_user_values,
        cache_enabled: catalog.cache_enabled
      })
    } else {
      setEditingCatalog(null)
      setFormData({
        catalog_code: '',
        catalog_name: '',
        catalog_type: 'SIMPLE',
        allow_user_values: false,
        cache_enabled: true
      })
    }
    setShowModal(true)
  }

  const closeModal = () => {
    setShowModal(false)
    setEditingCatalog(null)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Catalogs</h1>
        <button
          onClick={() => openModal()}
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="h-5 w-5" />
          New Catalog
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Catalogs List */}
        <div className="bg-white rounded-xl shadow-sm overflow-hidden">
          <div className="px-4 py-3 border-b border-gray-200 bg-gray-50">
            <h3 className="font-semibold text-gray-700">Catalog List</h3>
          </div>
          <div className="divide-y divide-gray-200">
            {catalogs.length === 0 ? (
              <div className="px-4 py-8 text-center text-gray-500">
                No catalogs found
              </div>
            ) : (
              catalogs.map((catalog) => (
                <div
                  key={catalog.id}
                  onClick={() => handleSelectCatalog(catalog)}
                  className={`px-4 py-3 cursor-pointer hover:bg-gray-50 flex items-center justify-between ${
                    selectedCatalog?.id === catalog.id ? 'bg-blue-50 border-l-4 border-blue-600' : ''
                  }`}
                >
                  <div>
                    <p className="font-medium text-gray-900">{catalog.catalog_name}</p>
                    <p className="text-sm text-gray-500 font-mono">{catalog.catalog_code}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      catalog.catalog_type === 'SIMPLE' ? 'bg-blue-100 text-blue-700' :
                      catalog.catalog_type === 'HIERARCHICAL' ? 'bg-purple-100 text-purple-700' :
                      'bg-orange-100 text-orange-700'
                    }`}>
                      {catalog.catalog_type}
                    </span>
                    <ChevronRight className="h-4 w-4 text-gray-400" />
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Catalog Details & Values */}
        <div className="lg:col-span-2 bg-white rounded-xl shadow-sm overflow-hidden">
          {selectedCatalog ? (
            <>
              <div className="px-6 py-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
                <div>
                  <h3 className="font-semibold text-gray-900">{selectedCatalog.catalog_name}</h3>
                  <p className="text-sm text-gray-500">{selectedCatalog.catalog_code}</p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => openModal(selectedCatalog)}
                    className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg"
                  >
                    <Pencil className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => handleDelete(selectedCatalog.id)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
              <div className="p-6">
                <h4 className="font-medium text-gray-700 mb-3">Values</h4>
                {catalogValues.length === 0 ? (
                  <p className="text-gray-500 text-center py-8">No values in this catalog</p>
                ) : (
                  <table className="min-w-full">
                    <thead>
                      <tr className="text-left text-xs font-medium text-gray-500 uppercase">
                        <th className="pb-2">Code</th>
                        <th className="pb-2">Name</th>
                        <th className="pb-2">Order</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {catalogValues.map((value) => (
                        <tr key={value.id}>
                          <td className="py-2 font-mono text-sm">{value.value_code}</td>
                          <td className="py-2">{value.value_name}</td>
                          <td className="py-2 text-gray-500">{value.sort_order}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            </>
          ) : (
            <div className="flex items-center justify-center h-64 text-gray-500">
              Select a catalog to view details
            </div>
          )}
        </div>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-md p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-900">
                {editingCatalog ? 'Edit Catalog' : 'New Catalog'}
              </h2>
              <button onClick={closeModal} className="text-gray-500 hover:text-gray-700">
                <X className="h-5 w-5" />
              </button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Catalog Code</label>
                  <input
                    type="text"
                    value={formData.catalog_code}
                    onChange={(e) => setFormData({ ...formData, catalog_code: e.target.value.toUpperCase() })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="e.g., COUNTRY"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Catalog Name</label>
                  <input
                    type="text"
                    value={formData.catalog_name}
                    onChange={(e) => setFormData({ ...formData, catalog_name: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="e.g., Countries"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
                  <select
                    value={formData.catalog_type}
                    onChange={(e) => setFormData({ ...formData, catalog_type: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="SIMPLE">Simple</option>
                    <option value="HIERARCHICAL">Hierarchical</option>
                    <option value="DEPENDENT">Dependent</option>
                  </select>
                </div>
                <div className="flex items-center gap-4">
                  <label className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      checked={formData.allow_user_values}
                      onChange={(e) => setFormData({ ...formData, allow_user_values: e.target.checked })}
                      className="rounded border-gray-300"
                    />
                    <span className="text-sm text-gray-700">Allow user values</span>
                  </label>
                  <label className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      checked={formData.cache_enabled}
                      onChange={(e) => setFormData({ ...formData, cache_enabled: e.target.checked })}
                      className="rounded border-gray-300"
                    />
                    <span className="text-sm text-gray-700">Enable cache</span>
                  </label>
                </div>
              </div>
              <div className="mt-6 flex gap-3 justify-end">
                <button
                  type="button"
                  onClick={closeModal}
                  className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {editingCatalog ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
