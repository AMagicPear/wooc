const baseApiUrl = 'http://localhost:5000'

export const getFile = (filePath?: string) => {
    return `${baseApiUrl}/get_file/${filePath}`
}

export default baseApiUrl