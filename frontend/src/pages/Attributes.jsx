import { useState, useEffect } from 'react'
import { Plus, Pencil, Trash2, X } from 'lucide-react'
import { getAttributes, createAttribute, updateAttribute, deleteAttribute, getEntities } from '../services/api'

const DATA_TYPES = ['STRING', 'INTEGER', 'DECIMAL', 'BOOLEAN', 'DATE', 'DATETIME', 'UUID', 'JSON', 'TEXT']

export default function Attributes() {
  const [attributes, setAttributes] = useState([])
  const [entities, setEntities] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [editingAttribute, setEditingAttribute] = useState(null)
  const [filterEntity, setFilterEntity] = useState('')
  const [formData, setFormData] = useState({
    entity_id: '',
    attribute_code: '',
    attribute_name: '',
    data_type: 'STRING',
    is_required: false,
    is_unique: false,
    default_value: ''
  })

  useEffect(() => {
    fetchData()
  }, [])

  useEffect(() => {
    fetchAttributes()
  }, [filterEntity])

  const fetchData = async () => {
    try {
      const [attrRes, entRes] = await Promise.all([
        getAttributes(),
        getEntities()
      ])
      setAttributes(attrRes.data || [])
      setEntities(entRes.data?.items || [])
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchAttributes = async () => {
    try {
      const params = filterEntity ? { entity_id: filterEntity } : {}
      const response = await getAttributes(params)
      setAttributes(response.data || [])
    } catch (error) {
      console.error('Error fetching attributes:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const payload = {
        entity_id: formData.entity_id,
        attribute_code: formData.attribute_code,
        attribute_name: formData.attribute_name,
        data_type: formData.data_type,
        is_required: formData.is_required,
        is_unique: formData.is_unique,
        default_value: formData.default_value || null
      }
      if (editingAttribute) {
        await updateAttribute(editingAttribute.id, payload)
      } else {
        await createAttribute(payload)
      }
      fetchAttributes()
      closeModal()
    } catch (error) {
      console.error('Error saving attribute:', error)
      alert('Error saving attribute: ' + (error.response?.data?.detail || error.message))
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this attribute?')) return
    try {
      await deleteAttribute(id)
      fetchAttributes()
    } catch (error) {
      console.error('Error deleting attribute:', error)
    }
  }

  const openModal = (attribute = null) => {
    if (attribute) {
      setEditingAttribute(attribute)
      setFormData({
        entity_id: attribute.entity_id,
        attribute_code: attribute.attribute_code,
        attribute_name: attribute.attribute_name,
        data_type: attribute.data_type,
        is_required: attribute.is_required,
        is_unique: attribute.is_unique,
        default_value: attribute.default_value || ''
      })
    } else {
      setEditingAttribute(null)
      setFormData({
        entity_id: filterEntity || '',
        attribute_code: '',
        attribute_name: '',
        data_type: 'STRING',
        is_required: false,
        is_unique: false,
        default_value: ''
      })
    }
    setShowModal(true)
  }

  const closeModal = () => {
    setShowModal(false)
    setEditingAttribute(null)
  }

  const getEntityName = (entityId) => {
    const entity = entities.find(e => e.id === entityId)
    return entity?.entity_name || entityId
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
        <h1 className="text-2xl font-bold text-gray-900">Attributes</h1>
        <div className="flex gap-3">
          <select
            value={filterEntity}
            onChange={(e) => setFilterEntity(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Entities</option>
            {entities.map((entity) => (
              <option key={entity.id} value={entity.id}>{entity.entity_name}</option>
            ))}
          </select>
          <button
            onClick={() => openModal()}
            className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            disabled={entities.length === 0}
          >
            <Plus className="h-5 w-5" />
            New Attribute
          </button>
        </div>
      </div>

      {entities.length === 0 ? (
        <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-6 text-center">
          <p className="text-yellow-800">Create an Entity first before adding attributes.</p>
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-sm overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Entity</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Code</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Constraints</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {attributes.length === 0 ? (
                <tr>
                  <td colSpan="6" className="px-6 py-12 text-center text-gray-500">
                    No attributes found
                  </td>
                </tr>
              ) : (
                attributes.map((attr) => (
                  <tr key={attr.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {getEntityName(attr.entity_id)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="font-mono text-sm bg-gray-100 px-2 py-1 rounded">{attr.attribute_code}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">{attr.attribute_name}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-xs px-2 py-1 rounded-full bg-purple-100 text-purple-700">
                        {attr.data_type}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex gap-1">
                        {attr.is_required && (
                          <span className="text-xs px-2 py-1 rounded-full bg-red-100 text-red-700">Required</span>
                        )}
                        {attr.is_unique && (
                          <span className="text-xs px-2 py-1 rounded-full bg-blue-100 text-blue-700">Unique</span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right">
                      <button
                        onClick={() => openModal(attr)}
                        className="text-blue-600 hover:text-blue-800 mr-3"
                      >
                        <Pencil className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(attr.id)}
                        className="text-red-600 hover:text-red-800"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-lg p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-900">
                {editingAttribute ? 'Edit Attribute' : 'New Attribute'}
              </h2>
              <button onClick={closeModal} className="text-gray-500 hover:text-gray-700">
                <X className="h-5 w-5" />
              </button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Entity</label>
                  <select
                    value={formData.entity_id}
                    onChange={(e) => setFormData({ ...formData, entity_id: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    required
                    disabled={editingAttribute}
                  >
                    <option value="">Select Entity</option>
                    {entities.map((entity) => (
                      <option key={entity.id} value={entity.id}>{entity.entity_name}</option>
                    ))}
                  </select>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Attribute Code</label>
                    <input
                      type="text"
                      value={formData.attribute_code}
                      onChange={(e) => setFormData({ ...formData, attribute_code: e.target.value.toLowerCase() })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                      placeholder="e.g., first_name"
                      required
                      disabled={editingAttribute}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Attribute Name</label>
                    <input
                      type="text"
                      value={formData.attribute_name}
                      onChange={(e) => setFormData({ ...formData, attribute_name: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                      placeholder="e.g., First Name"
                      required
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Data Type</label>
                  <select
                    value={formData.data_type}
                    onChange={(e) => setFormData({ ...formData, data_type: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    disabled={editingAttribute}
                  >
                    {DATA_TYPES.map((type) => (
                      <option key={type} value={type}>{type}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Default Value</label>
                  <input
                    type="text"
                    value={formData.default_value}
                    onChange={(e) => setFormData({ ...formData, default_value: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="Optional"
                  />
                </div>
                <div className="flex items-center gap-6">
                  <label className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      checked={formData.is_required}
                      onChange={(e) => setFormData({ ...formData, is_required: e.target.checked })}
                      className="rounded border-gray-300"
                    />
                    <span className="text-sm text-gray-700">Required</span>
                  </label>
                  <label className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      checked={formData.is_unique}
                      onChange={(e) => setFormData({ ...formData, is_unique: e.target.checked })}
                      className="rounded border-gray-300"
                    />
                    <span className="text-sm text-gray-700">Unique</span>
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
                  {editingAttribute ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
