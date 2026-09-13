import {useEffect, useState} from 'react'

import './App.css'

const API_URL = 'http://127.0.0.1:8000/api/discrepancies/'

function App() {
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [reason, setReason] = useState('')
  const [locationId, setLocationId] = useState('')
  const [orgId, setOrgId] = useState('')
  const [sortBy, setSortBy] = useState('')

  useEffect(() => {
    setLoading(true)
    setError('')

    const params = new URLSearchParams()

    if (orgId) {
      params.append('org_id', orgId)
    }

    if (reason) {
      params.append('reason', reason)
    }

    if (locationId) {
      params.append('location_id', locationId)
    }

    if (sortBy) {
      params.append('sort', sortBy)
    }

    const queryString = params.toString()

    const url = queryString
      ? `${API_URL}?${queryString}`
      : API_URL

    fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch discrepancies')
        }

        return response.json()
      })
      .then(data => {
        setResults(data.results)
        setLoading(false)
      })
      .catch(() => {
        setError('Unable to load discrepancy data')
        setLoading(false)
      })
  }, [reason, locationId, sortBy, orgId])

  return (
    <div className="app">
      <h1>Reconciliation Dashboard</h1>

      <p className="subtitle">
        Compare System A and System B records across organizations and
        locations.
      </p>

      <p className="count">
        Total discrepancies: {results.length}
      </p>

      <div className="filters">
        <div>
          <label htmlFor="org-filter">Organization:</label>

          <select
            id="org-filter"
            value={orgId}
            onChange={event => setOrgId(event.target.value)}
          >
            <option value="">All organizations</option>
            <option value="ORG-A">ORG-A</option>
            <option value="ORG-B">ORG-B</option>
          </select>
        </div>

        <div>
          <label htmlFor="reason-filter">Reason:</label>

          <select
            id="reason-filter"
            value={reason}
            onChange={event => setReason(event.target.value)}
          >
            <option value="">All reasons</option>
            <option value="MISSING_IN_B">Missing in B</option>
            <option value="ORPHAN_IN_B">Orphan in B</option>
            <option value="DUPLICATE_IN_B">Duplicate in B</option>
            <option value="VALUE_MISMATCH">Value mismatch</option>
          </select>
        </div>

        <div>
          <label htmlFor="location-filter">Location:</label>

          <select
            id="location-filter"
            value={locationId}
            onChange={event => setLocationId(event.target.value)}
          >
            <option value="">All locations</option>
            <option value="LOC-101">LOC-101</option>
            <option value="LOC-102">LOC-102</option>
            <option value="LOC-103">LOC-103</option>
            <option value="LOC-201">LOC-201</option>
            <option value="LOC-202">LOC-202</option>
          </select>
        </div>

        <div>
          <label htmlFor="sort-filter">Sort by:</label>

          <select
            id="sort-filter"
            value={sortBy}
            onChange={event => setSortBy(event.target.value)}
          >
            <option value="">Record ID</option>
            <option value="system_a_value">System A value</option>
            <option value="system_b_value">System B value</option>
          </select>
        </div>
      </div>

      {loading && <p className="status">Loading discrepancies...</p>}

      {error && <p className="error">{error}</p>}

      {!loading && !error && (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Record ID</th>
                <th>Location</th>
                <th>Reason</th>
                <th>System A Value</th>
                <th>System B Value</th>
              </tr>
            </thead>

            <tbody>
              {results.length === 0 ? (
                <tr>
                  <td colSpan="5" className="empty">
                    No discrepancies found.
                  </td>
                </tr>
              ) : (
                results.map((result, index) => (
                  <tr
                    key={`${result.record_id}-${result.reason}-${index}`}
                  >
                    <td>{result.record_id}</td>
                    <td>{result.location_id}</td>
                    <td>
                      <span className={`reason ${result.reason}`}>
                        {result.reason}
                      </span>
                    </td>
                    <td>{result.system_a_value || '-'}</td>
                    <td>
                      {Array.isArray(result.system_b_value)
                        ? result.system_b_value.join(', ')
                        : result.system_b_value || '-'}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default App