
export const baseURL = import.meta.env.VITE_BASE_URL || 'http://localhost:3000'
export const apiURL = import.meta.env.VITE_API_URL || 'http://localhost:3000/api'
export const imgURL = import.meta.env.VITE_IMG_URL || 'http://localhost:3000'
export const config = {
    baseURL: baseURL,
    apiURL: apiURL,
    imgURL: imgURL,
}
export default config