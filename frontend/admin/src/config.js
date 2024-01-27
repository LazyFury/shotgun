
export const baseURL = import.meta.env.VITE_BASE_URL || 'http://localhost:3000'
export const apiURL = import.meta.env.VITE_API_URL || 'http://localhost:3000/api'

export const config = {
    baseURL: baseURL,
    apiURL: apiURL
}
export default config