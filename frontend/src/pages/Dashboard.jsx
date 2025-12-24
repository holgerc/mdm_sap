import { useState, useEffect } from 'react'
import { Database, Box, List, CheckCircle, XCircle } from 'lucide-react'
import { getEntities, getCatalogs, getHealth } from '../services/api'

export default function Dashboard() {
  const [stats, setStats] = useState({
    entities: 0,
    catalogs: 0,
    healthy: false
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [entitiesRes, catalogsRes, healthRes] = await Promise.all([
          getEntities().catch(() => ({ data: { items: [], total: 0 } })),
          getCatalogs().catch(() => ({ data: [] })),
          getHealth().catch(() => ({ data: { status: 'unhealthy' } }))
        ])

        setStats({
          entities: entitiesRes.data?.total || entitiesRes.data?.items?.length || 0,
          catalogs: Array.isArray(catalogsRes.data) ? catalogsRes.data.length : 0,
          healthy: healthRes.data?.status === 'healthy'
        })
      } catch (error) {
        console.error('Error fetching stats:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
  }, [])

  const statCards = [
    { name: 'Entities', value: stats.entities, icon: Database, color: 'bg-blue-500' },
    { name: 'Catalogs', value: stats.catalogs, icon: List, color: 'bg-green-500' },
    {
      name: 'API Status',
      value: stats.healthy ? 'Healthy' : 'Unhealthy',
      icon: stats.healthy ? CheckCircle : XCircle,
      color: stats.healthy ? 'bg-emerald-500' : 'bg-red-500'
    },
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {statCards.map((stat) => (
          <div key={stat.name} className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center">
              <div className={`${stat.color} p-3 rounded-lg`}>
                <stat.icon className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">{stat.name}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-white rounded-xl shadow-sm p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Start</h2>
        <div className="space-y-3 text-gray-600">
          <p>1. Create <strong>Entities</strong> to define your master data structures (e.g., Customers, Products, Vendors)</p>
          <p>2. Add <strong>Attributes</strong> to entities to define their properties</p>
          <p>3. Set up <strong>Catalogs</strong> for dropdown/lookup values</p>
        </div>
      </div>
    </div>
  )
}
