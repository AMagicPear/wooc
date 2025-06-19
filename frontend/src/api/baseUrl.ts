const baseApiUrl = 'http://localhost:2025'

export const getFile = (filePath?: string) => {
    return `${baseApiUrl}/get_file/${filePath}`
}

export default baseApiUrl